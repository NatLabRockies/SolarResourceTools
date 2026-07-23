#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 10/23/19 12:03 PM

@author : rahul gupta (rgupta2)

"""
# Imports
import statistics
import tkinter as tk
import subprocess
import time
import os, sys
import platform
import tkinter.filedialog
from tkinter import messagebox
import tkinter.scrolledtext as tkst
import pandas as pd
import numpy as np
import utills
import utills as ut
import seriqc_script as script
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib import style
from PIL import Image, ImageTk, ImageGrab  # package name is PILLOW
import curveArea as cAr
from functools import partial
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector


def getFilePath():
    global data
    root = tk.Tk()
    root.withdraw()

    # Make sure the root window is centered
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    dialog_width = 600
    dialog_height = 400
    center_x = int((screen_width - dialog_width) / 2)
    center_y = int((screen_height - dialog_height) / 2)
    root.geometry(f"{dialog_width}x{dialog_height}+{center_x}+{center_y}")

    path = tkinter.filedialog.askopenfilename(parent=root, initialdir=os.getcwd(), title='Upload csv file',
                                              filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
    return path


def getQC0FilePath():
    root = tk.Tk()
    root.withdraw()

    # Make sure the root window is centered
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    dialog_width = 600
    dialog_height = 400
    center_x = int((screen_width - dialog_width) / 2)
    center_y = int((screen_height - dialog_height) / 2)
    root.geometry(f"{dialog_width}x{dialog_height}+{center_x}+{center_y}")

    path = tkinter.filedialog.askopenfilename(parent=root, initialdir=os.getcwd(), title='Upload QC0 file',
                                              filetypes=(("QC0 files", "*.QC0"), ("all files", "*.*")))
    return path


def getKspace(ip):
    miss = 9900.0
    ip['XT'] = -999.0
    ip['XN'] = -999.0
    ip['XD'] = -999.0
    ip['KT'] = -999.0
    ip['KN'] = -999.0
    ip['KT1'] = -999.0
    ip['KN1'] = -999.0
    ip['KD'] = -999.0

    ip['goAhead'] = 1.0
    ip.loc[(ip['ETR'] == 0.0), 'goAhead'] = 0.0
    Global = ip[ip.columns[2]]
    Direct = ip[ip.columns[3]]
    Diffuse = ip[ip.columns[4]]

    ip.loc[(ip['goAhead'] == 1.0) & (Diffuse < miss), 'XD'] = Diffuse / ip['ETR']

    ip.loc[(ip['goAhead'] == 1.0) & (Diffuse < miss) & (Direct < miss), 'XN'] = Direct / ip['ETRN']
    ip.loc[(ip['goAhead'] == 1.0) & (Diffuse < miss) & (Direct < miss), 'KT1'] = ip['XN'] + ip['XD']

    ip.loc[(ip['goAhead'] == 1.0) & (Diffuse < miss) & (Direct >= miss), 'KN'] = miss
    ip.loc[(ip['goAhead'] == 1.0) & (Diffuse < miss) & (Direct >= miss), 'KT1'] = miss

    ip.loc[(ip['goAhead'] == 1.0) & (Diffuse < miss) & (Global < miss), 'XT'] = Global / ip['ETR']
    ip.loc[(ip['goAhead'] == 1.0) & (Diffuse < miss) & (Global < miss), 'KN1'] = ip['XT'] - ip['XD']
    ip.loc[(ip['goAhead'] == 1.0) & (Diffuse < miss) & (Global >= miss), 'XT'] = miss
    ip.loc[(ip['goAhead'] == 1.0) & (Diffuse < miss) & (Global >= miss), 'KN1'] = miss

    ip.loc[(ip['goAhead'] == 1.0) & (Diffuse >= miss), 'XD'] = miss
    ip.loc[(ip['goAhead'] == 1.0) & (Diffuse >= miss), 'KT1'] = miss
    ip.loc[(ip['goAhead'] == 1.0) & (Diffuse >= miss), 'KN1'] = miss

    ip.loc[(ip['goAhead'] == 1.0) & (Diffuse >= miss) & (Direct < miss), 'XN'] = Direct / ip['ETRN']
    ip.loc[(ip['goAhead'] == 1.0) & (Diffuse >= miss) & (Direct >= miss), 'XN'] = miss

    ip.loc[(ip['goAhead'] == 1.0) & (Diffuse >= miss) & (Global < miss), 'XT'] = Global / ip['ETR']
    ip.loc[(ip['goAhead'] == 1.0) & (Diffuse >= miss) & (Global >= miss), 'XT'] = miss

    ip.loc[(ip['goAhead'] == 1.0) & (ip['XT'] < miss), 'KT'] = (ip['XT'] * 100)
    ip.loc[(ip['goAhead'] == 1.0) & (ip['XD'] < miss), 'KD'] = (ip['XD'] * 100)
    ip.loc[(ip['goAhead'] == 1.0) & (ip['XN'] < miss), 'KN'] = (ip['XN'] * 100)
    ip.loc[(ip['goAhead'] == 1.0) & (ip['KT1'] < miss), 'KT1'] = (ip['KT1'] * 100)
    ip.loc[(ip['goAhead'] == 1.0) & (ip['KN1'] < miss), 'KN1'] = (ip['KN1'] * 100)

    ip.loc[(ip['goAhead'] == 1.0) & (ip['XT'] < -10000.0), 'KT'] = -10000.0
    ip.loc[(ip['goAhead'] == 1.0) & (ip['XD'] < -10000.0), 'KD'] = -10000.0
    ip.loc[(ip['goAhead'] == 1.0) & (ip['XN'] < -10000.0), 'KN'] = -10000.0
    ip.loc[(ip['goAhead'] == 1.0) & (ip['KT1'] < -10000.0), 'KT1'] = -10000.0
    ip.loc[(ip['goAhead'] == 1.0) & (ip['KN1'] < -10000.0), 'KN1'] = -10000.0

    ip.loc[(ip['goAhead'] == 1.0) & (ip['XT'] < miss), 'KT'] = (ip['KT']).map(int)
    ip.loc[(ip['goAhead'] == 1.0) & (ip['XD'] < miss), 'KD'] = (ip['KD']).map(int)
    ip.loc[(ip['goAhead'] == 1.0) & (ip['XN'] < miss), 'KN'] = (ip['KN']).map(int)
    ip.loc[(ip['goAhead'] == 1.0) & (ip['KT1'] < miss), 'KT1'] = (ip['KT1']).map(int)
    ip.loc[(ip['goAhead'] == 1.0) & (ip['KN1'] < miss), 'KN1'] = (ip['KN1']).map(int)


def hitOpen():
    def newSite():

        def nsQC0Browse():
            global data, siteInfo
            nsPath = tkinter.filedialog.askdirectory(parent=newSiteRoot)
            data["qc0Path"] = nsPath + "/" + nssiteIDEntry.get() + ".qc0"
            qc0PathLabel = tk.Label(newSiteRoot, text=nsPath, font=(None, 12), anchor="w")
            qc0PathLabel.place(relx=0.15, rely=0.47, relwidth=0.84, relheight=0.04)

        def nsDatafolBrowse():
            # global data
            dfPath = tkinter.filedialog.askdirectory(parent=newSiteRoot)
            dfPathLabel = tk.Label(definFrame, text=dfPath, font=(None, 12), anchor="w")
            dfPathLabel.place(relx=0.14, rely=0.82, relwidth=0.85, relheight=0.12)
            data["defaultDataFolder"] = dfPath

        def nsOK():
            # global data, siteInfo
            try:
                if nssiteIDEntry.get() == "" or nssiteDescEntry.get() == "" or nsLatEntry.get() == "" or nsLongEntry.get() == "" or nsTZEntry.get() == "" or \
                        data["qc0Path"] == "":
                    messagebox.showerror("Error", "Bad input! Please provide all the values.")
                else:
                    data["siteCode"] = nssiteIDEntry.get()
                    data["siteDesc"] = nssiteDescEntry.get()
                    data["siteIdentifier"] = data["siteCode"] + "," + " " + data["siteDesc"]
                    data["latitude"] = float(nsLatEntry.get())
                    data["longitude"] = float(nsLongEntry.get())
                    data["timeZone"] = nsTZEntry.get()
                    data["comments"] = comments.get("1.0", tk.END)
                    data["integration"] = int(nsIntegVar.get())
                    data["plane"] = nsplaneVar.get()
                    # data["3compFilter"] = enableVar.get()
                    data["threshold"] = float(nsThreshVar.get())
                    data["elevation"] = float(nsElevVar.get())

                    if nsplaneVar.get() == 1:
                        data["plane"] = 1
                        # r1.select()
                    else:
                        if nsplaneVar == 2:
                            data["plane"] = 2
                            # r2.select()
                        else:
                            if nsplaneVar == 3:
                                data["plane"] = 3
                                # r3.select()
                    # creating blank Qc0 file
                    f = open('dataFiles/blankQC0', 'r')
                    rawData = f.read()
                    f.close()
                    f.flush
                    rawData = rawData.replace("Site Identifier:", "Site Identifier: " + data["siteIdentifier"])
                    rawData = rawData.replace(" --- Latitude:", " --- Latitude: " + str(nsLatEntry.get()))
                    rawData = rawData.replace(" -- Longitude:", " -- Longitude: " + str(nsLongEntry.get()))
                    rawData = rawData.replace(" -- Time Zone:", " -- Time Zone: " + str(nsTZEntry.get()))
                    rawData = rawData.replace("Integration (minutes):",
                                              "Integration (minutes): " + str(data["integration"]))
                    rawData = rawData.replace("Data Folder:", "Data Folder: " + data["defaultDataFolder"])
                    rawData = rawData.replace("Elevation:", "Elevation: " + str(data["elevation"]))
                    if data["plane"] == 1:
                        plane = "0 Kt-Kn"
                    else:
                        if data["plane"] == 2:
                            plane = "1 Kt-Kd"
                        else:
                            if data["plane"] == 3:
                                plane = "2 Kn-Kd"
                    rawData = rawData.replace("Plane:", "Plane: " + plane)
                    # if data["3compFilter"] == 1:
                    rawData = rawData.replace("3-Component Filter:", "3-Component Filter: " + str(data["threshold"]))
                    rawData = rawData.replace("comments:", "comments: " + data["comments"])

                    f = open(data["qc0Path"], 'w+')
                    f.write(rawData)

                    f.close
                    f.flush()

                    # updating siteinfo Dict
                    siteInfo[data["siteIdentifier"]] = data["qc0Path"]
                    siteOptList.append(data["siteIdentifier"])
                    menu = siteOption.children["menu"]
                    menu.delete(0, "end")
                    for i in siteOptList:
                        menu.add_command(label=i,
                                         command=lambda value=i: optVar.set(value))
                    optVar.set(siteOptList[len(siteOptList) - 1])
                    integVar.set(nsIntegVar.get())
                    # planeVar.set(nsplaneVar.get())
                    # compfiltVar.set(data["3compFilter"])

                    menu = threshOption.children["menu"]
                    menu.delete(0, "end")
                    for i in threshList:
                        menu.add_command(label=i,
                                         command=lambda value=i: threshVar.set(value))
                    threshVar.set(nsThreshVar.get())
                    openRoot.deiconify()
                    newSiteRoot.withdraw()
            except ValueError:
                messagebox.showerror("Error",
                                     "Bad input" + nssiteIDEntry.get() + nssiteDescEntry.get() + nsLatEntry.get() + nsLongEntry.get() + nsTZEntry.get() + nsElevVar.get() +
                                     data["qc0Path"])

        def nsCancel():
            openRoot.deiconify()
            newSiteRoot.withdraw()

        # mainRoot.deiconify()
        # openRoot.configure(state=tk.DISABLED)
        openRoot.withdraw()
        newSiteRoot = tk.Tk()
        newSiteRoot.wm_geometry("500x600+500+250")
        newSiteRoot.title("New Site")

        nsFrame = tk.Frame(newSiteRoot)
        nsFrame.place(relx=0, rely=0, relwidth=1, relheight=1)

        nssiteIDLabel = tk.Label(nsFrame, text="SiteID", font=(None, 12), anchor="w")
        nssiteIDLabel.place(relx=0.05, rely=0.02, relwidth=0.2, relheight=0.03)
        nssiteIDEntry = tk.Entry(nsFrame)
        nssiteIDEntry.place(relx=0.05, rely=0.055, relwidth=0.2, relheight=0.04)

        nssiteDescLabel = tk.Label(nsFrame, text="Site Description", font=(None, 12), anchor="w")
        nssiteDescLabel.place(relx=0.30, rely=0.02, relwidth=0.6, relheight=0.03)
        nssiteDescEntry = tk.Entry(nsFrame)
        nssiteDescEntry.place(relx=0.30, rely=0.055, relwidth=0.6, relheight=0.04)

        nsLatLabel = tk.Label(nsFrame, text="Latitude", font=(None, 12), anchor="w")
        nsLatLabel.place(relx=0.05, rely=0.105, relwidth=0.15, relheight=0.03)
        nsLatEntry = tk.Entry(nsFrame)
        nsLatEntry.place(relx=0.05, rely=0.14, relwidth=0.15, relheight=0.04)

        nsLongLabel = tk.Label(nsFrame, text="Longitude", font=(None, 12), anchor="w")
        nsLongLabel.place(relx=0.05, rely=0.19, relwidth=0.15, relheight=0.03)
        nsLongEntry = tk.Entry(nsFrame)
        nsLongEntry.place(relx=0.05, rely=0.225, relwidth=0.15, relheight=0.04)

        nsTZLabel = tk.Label(nsFrame, text="Time Zone", font=(None, 12), anchor="w")
        nsTZLabel.place(relx=0.05, rely=0.275, relwidth=0.15, relheight=0.03)
        nsTZEntry = tk.Entry(nsFrame)
        nsTZEntry.place(relx=0.05, rely=0.31, relwidth=0.15, relheight=0.04)

        commentLabel = tk.Label(nsFrame, text="Comments", font=(None, 12), anchor="w")
        commentLabel.place(relx=0.30, rely=0.105, relwidth=0.15, relheight=0.03)

        commentFrame = tk.Frame(nsFrame, bd=1, bg="Black")
        commentFrame.place(relx=0.30, rely=0.14, relwidth=0.6, relheight=0.21)
        comments = tkst.ScrolledText(commentFrame)
        comments.place(relx=0, rely=0, relwidth=1, relheight=1)

        nsqcPathLabel = tk.Label(nsFrame, text="QC0 Path", font=(None, 12), anchor="w")
        nsqcPathLabel.place(relx=0.05, rely=0.40, relwidth=0.25, relheight=0.03)
        qcBrowseButton = tk.Button(nsFrame, text="Browse", command=nsQC0Browse)
        qcBrowseButton.place(relx=0.35, rely=0.40, relwidth=0.15, relheight=0.04)

        # Creating defaults frame
        defaultFrame = tk.Frame(nsFrame, bd=2, bg="Black")
        defaultFrame.place(relx=0.05, rely=0.55, relwidth=0.9, relheight=0.30)
        definFrame = tk.Frame(defaultFrame)
        definFrame.place(relx=0, rely=0, relwidth=1, relheight=1)

        defLabel = tk.Label(definFrame, text="Defaults", font=(None, 16), anchor="w")
        defLabel.place(relx=0.03, rely=0.05, relwidth=0.18, relheight=0.15)

        nsIntegVar = tk.StringVar(nsFrame)
        nsIntegVar.set(60)
        nsIntegLabel = tk.Label(definFrame, text="Integration", font=(None, 12), anchor="w")
        nsIntegLabel.place(relx=0.30, rely=0.05, relwidth=0.18, relheight=0.1)
        nsintegOpt = tk.OptionMenu(definFrame, nsIntegVar, *integList)
        nsintegOpt.place(relx=0.295, rely=0.21, relwidth=0.15, relheight=0.15)

        nsPlaneLabel = tk.Label(definFrame, text="Plane", font=(None, 12))
        nsPlaneLabel.place(relx=0.50, rely=0.05, relwidth=0.18, relheight=0.1)

        nsplaneVar = tk.IntVar(nsFrame)
        rb1 = tk.Radiobutton(definFrame, text="Kt-Kn", font=(None, 12), variable=nsplaneVar, value=1)
        rb1.place(relx=0.5, rely=0.21, relwidth=0.18, relheight=0.12)
        rb2 = tk.Radiobutton(definFrame, text="Kt-Kd", font=(None, 12), variable=nsplaneVar, value=2)
        rb2.place(relx=0.5, rely=0.34, relwidth=0.18, relheight=0.12)
        rb3 = tk.Radiobutton(definFrame, text="Kn-Kd", font=(None, 12), variable=nsplaneVar, value=3)
        rb3.place(relx=0.5, rely=0.47, relwidth=0.18, relheight=0.12)
        rb1.select()

        ns3compLabel = tk.Label(definFrame, text="3-component Filter", font=(None, 12))
        ns3compLabel.place(relx=0.70, rely=0.05, relwidth=0.28, relheight=0.1)

        nsThreshVar = tk.StringVar(nsFrame)
        nsThreshVar.set('1')
        nsThreshOption = tk.OptionMenu(definFrame, nsThreshVar, *threshList)
        nsThreshOption.place(relx=0.685, rely=0.21, relwidth=0.14, relheight=0.16)
        nsThreshLabel = tk.Label(definFrame, text="Threshhold", font=(None, 12))
        nsThreshLabel.place(relx=0.84, rely=0.21, relwidth=0.136, relheight=0.14)

        dataFolderLabel = tk.Label(definFrame, text="Data Folder", anchor="w")
        dataFolderLabel.place(relx=0.03, rely=0.655, relwidth=0.25, relheight=0.12)
        qcBrowseButton = tk.Button(definFrame, text="Browse", command=nsDatafolBrowse)
        qcBrowseButton.place(relx=0.295, rely=0.655, relwidth=0.18, relheight=0.12)

        nsElevLabel = tk.Label(definFrame, text="Elevation", anchor="w")
        nsElevLabel.place(relx=0.5, rely=0.655, relwidth=0.18, relheight=0.12)
        nsElevVar = tk.StringVar(nsFrame)
        nsElevEntry = tk.Entry(definFrame, font=(None, 12), textvariable=nsElevVar)
        nsElevEntry.place(relx=0.70, rely=0.665, relwidth=0.15, relheight=0.15)
        nsElevVar.set("0")

        nsOKButton = tk.Button(nsFrame, text="OK", command=nsOK)
        nsOKButton.place(relx=0.50, rely=0.90, relwidth=0.20, relheight=0.05)
        nsCancelButton = tk.Button(nsFrame, text="Cancel", command=nsCancel)
        nsCancelButton.place(relx=0.75, rely=0.90, relwidth=0.20, relheight=0.05)
        newSiteRoot.iconbitmap('dataFiles/qcfit-icon.ico')
        newSiteRoot.protocol("WM_DELETE_WINDOW", nsCancel)

        newSiteRoot.mainloop()

    def browseQC0():
        global data, boundary, siteInfo
        qc0Path = getQC0FilePath()
        if len(qc0Path) > 1:
            data["qc0Path"] = qc0Path
            existQC0Data = utills.readFile(qc0Path)
            index = existQC0Data.find("Site Identifier:")
            string = existQC0Data[index + len("Site Identifier:"):]
            siteID = string.split("\n")
            data["siteIdentifier"] = siteID[0].strip()
            siteOptList.append(siteID[0].strip())
            index = existQC0Data.find('Data Folder: ')
            string = existQC0Data[index + len('Data Folder: '):]
            string = string.split("\n")
            data["defaultDataFolder"] = string[0]

            # updating siteinfo Dict
            siteInfo[data["siteIdentifier"]] = data["qc0Path"]

            menu = siteOption.children["menu"]
            menu.delete(0, "end")
            for i in siteOptList:
                menu.add_command(label=i,
                                 command=lambda value=i: optVar.set(value))
            optVar.set(siteOptList[len(siteOptList) - 1])

    def browseQCF():
        global ip, data
        path = getFilePath()
        qcfInputLabel = tk.Label(mainFrame, text=path, font=(None, 12), anchor="w")
        qcfInputLabel.place(relx=0.20, rely=0.53, relwidth=0.7, relheight=0.1)
        data['QCFDataFilepath'] = path
        if len(path) > 1:
            ip = pd.read_csv(data['QCFDataFilepath'])
            monthOption.configure(state=tk.NORMAL)
        # setting temp flags for zenith and kspace Calculation
        ip['IQCGlobal'] = 1
        ip['IQCDirect'] = 1
        ip['IQCDiffuse'] = 1
        ip['lowExclude'] = 0
        ip['medExclude'] = 0
        ip['highExclude'] = 0
        ip['NAM'] = 0

        ip["monthName"] = (pd.to_datetime(ip[ip.columns[0]])).dt.month_name()
        ip["year"] = (pd.to_datetime(ip[ip.columns[0]])).dt.year

        monList = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        months = set(ip["monthName"])
        toRemove = list(set(monList) - months)

        for i in toRemove:
            monList.remove(i)

        menu = monthOption.children["menu"]
        menu.delete(0, "end")
        data["monthList"] = monList

        for i in monList:
            menu.add_command(label=i,
                             command=lambda value=i: monthVar.set(value))
        monthVar.set(monList[0])

        # ipData['month'] = ipData['date'].dt.month_name().str.upper().str[0:3]

        data["yearList"] = list(set(ip["year"]))
        yearList = data["yearList"]
        yearList = ["All", *yearList]
        menu = yearOption.children["menu"]
        menu.delete(0, "end")
        for i in yearList:
            menu.add_command(label=i,
                             command=lambda value=i: yearVar.set(value))
        yearVar.set(yearList[0])
        data["year"] = yearList[0]

    def okOS():
        global ip, data, plotData, pdLow, pdMed, pdHigh, boundary, iterCount

        if iterCount > 0:
            iterCount = 0
            answer = messagebox.askyesno("Save Changes", "Do you want to save changes?")
            if answer == True:
                monthToSave = data["month"]
                save(monthToSave)
            resetStats()
        # read QC0 file
        qc0dat = utills.readFile(data["qc0Path"])
        boundary = utills.getBoundariesTable(qc0dat)
        temp = boundary
        data["integration"] = int(integVar.get())

        # calculate zenith, K-space vars and airmasses

        measFreq = 1  # assuming measuring frequency is 1 minute due the Averaging method of Solar Zenith calculation
        repFreq = int(data["integration"])
        avg = "No"  # as its not being utilised due the Averaging method of Solar Zenith calculation

        pressure = [item for item in ip.columns if 'Pressure' in item]
        if len(pressure) == 0:
            pressure = (101325 * (1 - (2.25577 * 10 ** (-5)) * data["elevation"]) ** 5.25588) / 100
        else:
            pressure = statistics.mean(ip[pressure])

        temperature = 12
        script.splitDate(ip)
        script.utcCoversion(ip, int((data["timeZone"])), repFreq, measFreq)
        script.calculateZenith(ip, repFreq, measFreq, avg, data["latitude"], data["longitude"],
                               data["elevation"], pressure, temperature)

        getKspace(ip)

        script.calculateAirmass(ip)
        # Add columns for density:
        ip['density1'] = 0
        ip['density2'] = 0
        ip['density3'] = 0
        ip['ldID'] = ""  # (ip["KT"].map(int)).map(str)+(ip["KN"].map(int)).map(str)
        ip['mdID'] = ""  # (ip["KT"].map(int)).map(str)+(ip["KN1"].map(int)).map(str)
        ip['hdID'] = ""  # (ip["KT1"].map(int)).map(str)+(ip["KN"].map(int)).map(str)

        # update Data dictionary
        data["siteIdentifier"] = optVar.get()
        data["month"] = monthVar.get()

        if (data[
            'QCFDataFilepath'] == "" or optVar.get == "select" or monthVar.get == "-select-" or integVar.get == ""):
            messagebox.showerror("Error", "File not provided. Please Try Again.")

        else:
            menu = monOption.children["menu"]
            menu.delete(0, "end")
            monList = data["monthList"]
            for i in monList:
                menu.add_command(label=i,
                                 command=lambda value=i: monVar.set(value))
            monVar.set(data["month"])
            enable(planeCanvas.winfo_children())
            enable(monYearCanvas.winfo_children())
            enable(compFilterCanvas.winfo_children())
            enable(densityCanvas.winfo_children())
            enable(lowKspaceCanvas.winfo_children())
            enable(lowStatsCanvas.winfo_children())
            enable(lowErrorCanvas.winfo_children())
            enable(medKspaceCanvas.winfo_children())
            enable(medStatsCanvas.winfo_children())
            enable(medErrorCanvas.winfo_children())
            enable(highKspaceCanvas.winfo_children())
            enable(highStatsCanvas.winfo_children())
            enable(highErrorCanvas.winfo_children())
            enable(integrationFrame.winfo_children())

            openRoot.withdraw()

            mainRoot.deiconify()
            # update mainRoot frame
            if data["plane"] != planeVar.get():
                planeVar.set(data["plane"])
        return

    def cancelOS():
        mainRoot.deiconify()
        openRoot.withdraw()

    mainRoot.withdraw()
    global openRoot, iterCount

    if iterCount > 0:
        iterCount = 0
        answer = messagebox.askyesno("Save Changes", "Do you want to save changes?")
        if answer == True:
            monthToSave = data["month"]
            save(monthToSave)
    openRoot.deiconify()
    openRoot.wm_geometry("500x300+500+250")
    openRoot.title("Open Site")
    mainFrame = tk.Frame(openRoot)
    mainFrame.place(relx=0, rely=0, relwidth=1, relheight=1)

    siteLabel = tk.Label(mainFrame, text="Site (code, description)", font=(None, 12), anchor="w")
    siteLabel.place(relx=0.05, rely=0.07, relwidth=0.4, relheight=0.1)
    global optVar
    optVar.set("select a site")
    siteOptList = ["select a site"]
    siteOption = tk.OptionMenu(mainFrame, optVar, *siteOptList, )
    siteOption.place(relx=0.15, rely=0.2, relwidth=0.35, relheight=0.1)
    data["siteIdentifier"] = optVar.get()
    optVar.trace_add("write", callback=updateSiteInfo)

    newSiteButton = tk.Button(mainFrame, text="New Site", command=newSite)
    newSiteButton.place(relx=0.54, rely=0.2, relwidth=0.20, relheight=0.1)

    newSiteBrowseButton = tk.Button(mainFrame, text="Browse", command=browseQC0)
    newSiteBrowseButton.place(relx=0.77, rely=0.2, relwidth=0.20, relheight=0.1)

    qcfLabel = tk.Label(mainFrame, text="QCF Data File", font=(None, 12), anchor="w")
    qcfLabel.place(relx=0.05, rely=0.4, relwidth=0.4, relheight=0.1)

    browseButton = tk.Button(mainFrame, text="Browse", command=browseQCF)
    browseButton.place(relx=0.6, rely=0.4, relwidth=0.20, relheight=0.1)

    monLabel = tk.Label(mainFrame, text="Month", font=(None, 12), anchor="w")
    monLabel.place(relx=0.06, rely=0.66, relwidth=0.20, relheight=0.1)
    monthVar = tk.StringVar(mainFrame)
    monthVar.set("-select-")
    monthOption = tk.OptionMenu(mainFrame, monthVar, *monList)
    monthOption.place(relx=0.05, rely=0.79, relwidth=0.25, relheight=0.1)
    monthOption.configure(state=tk.DISABLED)

    integList = [1, 5, 15, 60]

    global integVar
    integLabel = tk.Label(mainFrame, text="Integration Time", font=(None, 12), anchor="w")
    integLabel.place(relx=0.30, rely=0.66, relwidth=0.30, relheight=0.1)
    timeOpt = tk.OptionMenu(mainFrame, integVar, *integList)
    timeOpt.place(relx=0.30, rely=0.79, relwidth=0.20, relheight=0.1)
    integVar.set('60')

    okButton = tk.Button(mainFrame, text="OK", command=okOS)
    okButton.place(relx=0.54, rely=0.79, relwidth=0.20, relheight=0.1)

    cancelOSButton = tk.Button(mainFrame, text="Cancel", command=cancelOS)
    cancelOSButton.place(relx=0.77, rely=0.79, relwidth=0.20, relheight=0.1)

    openRoot.protocol("WM_DELETE_WINDOW", mainRoot.deiconify)
    openRoot.iconbitmap('dataFiles/qcfit-icon.ico')
    openRoot.mainloop()


def updateSiteInfo(*args):
    global data, integVar, siteInfo
    if optVar.get() == "select a site":
        return
    else:
        existQC0Data = utills.readFile(siteInfo[optVar.get()])
        latitude = utills.pickValue(existQC0Data, 'Latitude:')
        longitude = utills.pickValue(existQC0Data, 'Longitude:')
        timeZone = int(float(utills.pickValue(existQC0Data, 'Time Zone:')))
        elevation = float(utills.pickValue(existQC0Data, 'Elevation:'))
        threshold = utills.pickValue(existQC0Data, '3-Component Filter:')
        if threshold == '':
            threshold = 1
        else:
            threshold = float(threshold)
        data["latitude"] = latitude
        data["longitude"] = longitude
        data["timeZone"] = int(timeZone)
        data["elevation"] = elevation
        data["integration"] = int(utills.pickValue(existQC0Data, 'Integration (minutes):'))

        _plane = (utills.pickValue(existQC0Data, 'Plane:'))
        if _plane == "":
            data["plane"] = 1
        else:
            data["plane"] = int(_plane) + 1

        data["threshold"] = threshold
        integVar.set(data["integration"])


def hitEdit():
    global iterCount, data
    if iterCount > 0:
        answer = messagebox.askyesno("Save Changes", "Do you want to save changes?")
        if answer == True:
            monthToSave = data["month"]
            save(monthToSave)

    qc0Path = getQC0FilePath()
    if len(qc0Path) > 1:
        QC0Data = utills.readFile(qc0Path)

    index = QC0Data.find("Site Identifier:")
    string = QC0Data[index + len("Site Identifier:"):]
    siteinf = string.split("\n")
    siteinf = siteinf[0].split(",")

    siteid = siteinf[0]
    siteDesc = siteinf[1]
    latitude = utills.pickValue(QC0Data, 'Latitude:')
    longitude = utills.pickValue(QC0Data, 'Longitude:')
    timeZone = int(utills.pickValue(QC0Data, 'Time Zone:'))
    elevation = float(utills.pickValue(QC0Data, 'Elevation:'))
    threshold = utills.pickValue(QC0Data, '3-Component Filter:')
    if threshold == 0:
        threshold = 1
    integration = utills.pickValue(QC0Data, 'Integration (minutes):')
    plane = utills.pickValue(QC0Data, 'Plane:')
    index = QC0Data.find("Data Folder: ")
    string = QC0Data[index + len("Data Folder: "):]
    defFolder = string.split("\n")[0]
    index = QC0Data.find("comments:")
    if index > 1:
        comments = QC0Data[index + len("comments:"):]
    else:
        comments = ""

    def editQC0Browse():

        editQC0Path = tkinter.filedialog.askdirectory(parent=editQC0Root)
        qc0PathLabel.config(text=editQC0Path)

    def editQC0DatafolBrowse():
        # global data
        dfPath = tkinter.filedialog.askdirectory(parent=editQC0Root)
        dfPathLabel.config(text=dfPath)

    def editQC0OK(plane):
        # global data, siteInfo
        try:
            if editQC0siteIDEntry.get() == "" or editQC0siteDescEntry.get() == "" or editQC0LatEntry.get() == "" or editQC0LongEntry.get() == "" or editQC0TZEntry.get() == "":
                messagebox.showerror("Error", "Bad input! Please provide all the values.")
            else:
                # creating blank Qc0 file
                f = open('dataFiles/blankQC0', 'r')
                rawData = f.read()
                f.close()
                f.flush
                rawData = rawData.replace("Site Identifier:", "Site Identifier: " + str(edit_siteid.get()) + ", " + str(
                    edit_siteDesc.get()))
                rawData = rawData.replace(" --- Latitude:", " --- Latitude: " + str(editQC0LatEntry.get()))
                rawData = rawData.replace(" -- Longitude:", " -- Longitude: " + str(editQC0LongEntry.get()))
                rawData = rawData.replace(" -- Time Zone:", " -- Time Zone: " + str(editQC0TZEntry.get()))
                rawData = rawData.replace("Integration (minutes):",
                                          "Integration (minutes): " + str(editQC0IntegVar.get()))
                rawData = rawData.replace("Data Folder:", "Data Folder: " + defFolder)
                rawData = rawData.replace("Elevation:", "Elevation: " + str(editQC0ElevVar.get()))
                if (editQC0planeVar.get() == 1):
                    plane = "0 Kt-Kn"
                else:
                    if editQC0planeVar.get() == 2:
                        plane = "1 Kt-Kd"
                    else:
                        if editQC0planeVar.get() == 3:
                            plane = "2 Kn-Kd"
                rawData = rawData.replace("Plane:", "Plane: " + plane)
                # if data["3compFilter"] == 1:
                rawData = rawData.replace("3-Component Filter:", "3-Component Filter: " + str(threshold))
                rawData = rawData.replace("comments:", "comments: " + comments)

                f = open(qc0Path, 'w+')
                f.write(rawData)

                f.close
                f.flush()
                editQC0Root.withdraw()
        except ValueError:
            messagebox.showerror("Error",
                                 "Bad input" + editQC0siteIDEntry.get() + editQC0siteDescEntry.get() + editQC0LatEntry.get() + editQC0LongEntry.get() + editQC0TZEntry.get() + editQC0ElevVar.get() +
                                 data["qc0Path"])

    def editQC0Cancel():
        editQC0Root.withdraw()

    mainRoot.deiconify()
    # openRoot.configure(state=tk.DISABLED)
    editQC0Root = tk.Tk()
    editQC0Root.wm_geometry("500x600+500+250")
    editQC0Root.title("Edit QC0")

    editQC0Frame = tk.Frame(editQC0Root)
    editQC0Frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    editQC0siteIDLabel = tk.Label(editQC0Frame, text="SiteID", font=(None, 12), anchor="w")
    editQC0siteIDLabel.place(relx=0.05, rely=0.02, relwidth=0.2, relheight=0.03)

    edit_siteid = tk.StringVar(editQC0Frame)
    editQC0siteIDEntry = tk.Entry(editQC0Frame, font=(None, 12), textvariable=edit_siteid)
    editQC0siteIDEntry.place(relx=0.05, rely=0.055, relwidth=0.2, relheight=0.04)
    edit_siteid.set(siteid)

    editQC0siteDescLabel = tk.Label(editQC0Frame, text="Site Description", font=(None, 12), anchor="w")
    editQC0siteDescLabel.place(relx=0.30, rely=0.02, relwidth=0.6, relheight=0.03)

    edit_siteDesc = tk.StringVar(editQC0Frame)
    editQC0siteDescEntry = tk.Entry(editQC0Frame, font=(None, 12), textvariable=edit_siteDesc)
    editQC0siteDescEntry.place(relx=0.30, rely=0.055, relwidth=0.6, relheight=0.04)
    edit_siteDesc.set(siteDesc)

    editQC0LatLabel = tk.Label(editQC0Frame, text="Latitude", font=(None, 12), anchor="w")
    editQC0LatLabel.place(relx=0.05, rely=0.105, relwidth=0.15, relheight=0.03)

    edit_lat = tk.StringVar(editQC0Frame)
    editQC0LatEntry = tk.Entry(editQC0Frame, font=(None, 12), textvariable=edit_lat)
    editQC0LatEntry.place(relx=0.05, rely=0.14, relwidth=0.15, relheight=0.04)
    edit_lat.set(str(latitude))

    editQC0LongLabel = tk.Label(editQC0Frame, text="Longitude", font=(None, 12), anchor="w")
    editQC0LongLabel.place(relx=0.05, rely=0.19, relwidth=0.15, relheight=0.03)

    edit_long = tk.StringVar(editQC0Frame)
    editQC0LongEntry = tk.Entry(editQC0Frame, font=(None, 12), textvariable=edit_long)
    editQC0LongEntry.place(relx=0.05, rely=0.225, relwidth=0.15, relheight=0.04)
    edit_long.set(str(longitude))

    editQC0TZLabel = tk.Label(editQC0Frame, text="Time Zone", font=(None, 12), anchor="w")
    editQC0TZLabel.place(relx=0.05, rely=0.275, relwidth=0.15, relheight=0.03)

    edit_tzone = tk.StringVar(editQC0Frame)
    editQC0TZEntry = tk.Entry(editQC0Frame, font=(None, 12), textvariable=edit_tzone)
    editQC0TZEntry.place(relx=0.05, rely=0.31, relwidth=0.15, relheight=0.04)
    edit_tzone.set(str(timeZone))

    commentLabel = tk.Label(editQC0Frame, text="Comments", font=(None, 12), anchor="w")
    commentLabel.place(relx=0.30, rely=0.105, relwidth=0.15, relheight=0.03)

    commentFrame = tk.Frame(editQC0Frame, bd=1, bg="Black")
    commentFrame.place(relx=0.30, rely=0.14, relwidth=0.6, relheight=0.21)
    commArea = tkst.ScrolledText(commentFrame)
    commArea.place(relx=0, rely=0, relwidth=1, relheight=1)
    commArea.insert(tk.INSERT, comments)

    editQC0qcPathLabel = tk.Label(editQC0Frame, text="QC0 Path", font=(None, 12), anchor="w")
    editQC0qcPathLabel.place(relx=0.05, rely=0.40, relwidth=0.25, relheight=0.03)
    qc0PathLabel = tk.Label(editQC0Root, text=qc0Path, font=(None, 12), anchor="w")
    qc0PathLabel.place(relx=0.15, rely=0.47, relwidth=0.84, relheight=0.04)
    qcBrowseButton = tk.Button(editQC0Frame, text="Browse", command=editQC0Browse)
    qcBrowseButton.place(relx=0.35, rely=0.40, relwidth=0.15, relheight=0.04)

    # Creating defaults frame
    defaultFrame = tk.Frame(editQC0Frame, bd=2, bg="Black")
    defaultFrame.place(relx=0.05, rely=0.55, relwidth=0.9, relheight=0.30)
    definFrame = tk.Frame(defaultFrame)
    definFrame.place(relx=0, rely=0, relwidth=1, relheight=1)

    defLabel = tk.Label(definFrame, text="Defaults", font=(None, 16), anchor="w")
    defLabel.place(relx=0.03, rely=0.05, relwidth=0.18, relheight=0.15)

    editQC0IntegVar = tk.StringVar(editQC0Frame)
    editQC0IntegVar.set(integration)
    editQC0IntegLabel = tk.Label(definFrame, text="Integration", font=(None, 12), anchor="w")
    editQC0IntegLabel.place(relx=0.30, rely=0.05, relwidth=0.18, relheight=0.1)
    integList = [1, 5, 15, 60]
    editQC0integOpt = tk.OptionMenu(definFrame, editQC0IntegVar, *integList)
    editQC0integOpt.place(relx=0.295, rely=0.21, relwidth=0.15, relheight=0.15)

    editQC0PlaneLabel = tk.Label(definFrame, text="Plane", font=(None, 12))
    editQC0PlaneLabel.place(relx=0.50, rely=0.05, relwidth=0.18, relheight=0.1)

    editQC0planeVar = tk.IntVar(editQC0Frame)
    rb1 = tk.Radiobutton(definFrame, text="Kt-Kn", font=(None, 12), variable=editQC0planeVar, value=1)
    rb1.place(relx=0.5, rely=0.21, relwidth=0.18, relheight=0.12)
    rb2 = tk.Radiobutton(definFrame, text="Kt-Kd", font=(None, 12), variable=editQC0planeVar, value=2)
    rb2.place(relx=0.5, rely=0.34, relwidth=0.18, relheight=0.12)
    rb3 = tk.Radiobutton(definFrame, text="Kn-Kd", font=(None, 12), variable=editQC0planeVar, value=3)
    rb3.place(relx=0.5, rely=0.47, relwidth=0.18, relheight=0.12)
    if plane == "0 Kt-Kn":
        rb1.select()
    elif plane == "1 Kt-Kd":
        rb2.select()
    elif plane == "2 Kn-Kd":
        rb3.select()
    else:
        rb1.select()

    editQC03compLabel = tk.Label(definFrame, text="3-component Filter", font=(None, 12))
    editQC03compLabel.place(relx=0.70, rely=0.05, relwidth=0.28, relheight=0.1)

    editQC0ThreshVar = tk.StringVar(editQC0Frame)
    editQC0ThreshVar.set(str(threshold))
    editQC0ThreshOption = tk.OptionMenu(definFrame, editQC0ThreshVar, *threshList)
    editQC0ThreshOption.place(relx=0.685, rely=0.21, relwidth=0.14, relheight=0.16)
    # editQC0ThreshOption.configure(state=tk.DISABLED)
    editQC0ThreshLabel = tk.Label(definFrame, text="Threshhold", font=(None, 12))
    editQC0ThreshLabel.place(relx=0.84, rely=0.21, relwidth=0.136, relheight=0.14)

    dataFolderLabel = tk.Label(definFrame, text="Data Folder", anchor="w")
    dataFolderLabel.place(relx=0.03, rely=0.655, relwidth=0.25, relheight=0.12)
    dfPathLabel = tk.Label(definFrame, text=defFolder, font=(None, 12), anchor="w")
    dfPathLabel.place(relx=0.14, rely=0.82, relwidth=0.85, relheight=0.12)
    qcBrowseButton = tk.Button(definFrame, text="Browse", command=editQC0DatafolBrowse)
    qcBrowseButton.place(relx=0.295, rely=0.655, relwidth=0.18, relheight=0.12)

    editQC0ElevLabel = tk.Label(definFrame, text="Elevation", anchor="w")
    editQC0ElevLabel.place(relx=0.5, rely=0.655, relwidth=0.18, relheight=0.12)
    editQC0ElevVar = tk.StringVar(editQC0Frame)
    editQC0ElevEntry = tk.Entry(definFrame, font=(None, 12), textvariable=editQC0ElevVar)
    editQC0ElevEntry.place(relx=0.695, rely=0.67, relwidth=0.15, relheight=0.15)
    editQC0ElevVar.set(str(elevation))

    editQC0OKButton = tk.Button(editQC0Frame, text="OK", command=partial(editQC0OK, plane))
    editQC0OKButton.place(relx=0.50, rely=0.90, relwidth=0.20, relheight=0.05)
    editQC0CancelButton = tk.Button(editQC0Frame, text="Cancel", command=editQC0Cancel)
    editQC0CancelButton.place(relx=0.75, rely=0.90, relwidth=0.20, relheight=0.05)
    editQC0Root.iconbitmap('dataFiles/qcfit-icon.ico')
    editQC0Root.protocol("WM_DELETE_WINDOW", editQC0Cancel)
    editQC0Root.mainloop()


def plotUpdateThroughMonth(*args):
    global iterCount, dFlag, data
    monthToSave = data["month"]
    if iterCount > 0:
        dFlag = 2
        denseOnOff.select()

    plt.close('all')
    iterCount += 1
    if iterCount > 1:
        answer = messagebox.askyesno("Save Changes", "Do you want to save changes?")
        if answer == True:
            save(monthToSave)
        resetStats()
    data["plane"] = planeVar.get()
    data["month"] = monVar.get()
    data["year"] = yearVar.get()
    data["threshold"] = float(threshVar.get())
    curvefitting()
    getBoundaries()
    density()
    setStats()
    freqPlot()


def curvefitting():
    global ip, plotData, pdLow, pdMed, pdHigh, monVar, data
    data["plane"] = planeVar.get()
    data["month"] = monVar.get()
    data["year"] = yearVar.get()

    # calculate active flag for 3 spaces
    ip["activeKtKn"] = 0
    ip["activeKtKd"] = 0
    ip["activeKnKd"] = 0

    ip.loc[(ip["KT"] > ip["KN"]), "activeKtKn"] = 1
    ip.loc[(ip["KT"] > ip["KN1"]), "activeKtKd"] = 1
    ip.loc[(ip["KT1"] > ip["KN"]), "activeKnKd"] = 1

    # ignore negative and values more than 100
    ip.loc[(ip["KT"] > 100), "activeKtKn"] = 0
    ip.loc[(ip["KT"] > 100), "activeKtKd"] = 0
    ip.loc[(ip["KT"] > 100), "activeKnKd"] = 0
    ip.loc[(ip["KN"] > 100), "activeKtKn"] = 0
    ip.loc[(ip["KN"] > 100), "activeKtKd"] = 0
    ip.loc[(ip["KN"] > 100), "activeKnKd"] = 0
    ip.loc[(ip["KT"] < 0), "activeKtKn"] = 0
    ip.loc[(ip["KT"] < 0), "activeKtKd"] = 0
    ip.loc[(ip["KT"] < 0), "activeKnKd"] = 0
    ip.loc[(ip["KN"] < 0), "activeKtKn"] = 0
    ip.loc[(ip["KN"] < 0), "activeKtKd"] = 0
    ip.loc[(ip["KN"] < 0), "activeKnKd"] = 0

    # calculate error Kt-Kn-Kd
    ip["residual"] = 0
    ip["bin"] = ""
    ip["residual"] = ip["XT"] - ip["XN"] - ip["XD"]

    plotData = ip[ip["monthName"] == monVar.get()].copy()

    # seperate data based on airmasses

    pdLow = plotData[plotData["NAM"] == 1].copy()
    pdMed = plotData[plotData["NAM"] == 2].copy()
    pdHigh = plotData[plotData["NAM"] == 3].copy()

    # identify axes based on kspaces
    if data["plane"] == 1:
        flag = "activeKtKn"
        xAxis = data["xAxis"] = "KT"
        yAxis = data["yAxis"] = "KN"
    elif data["plane"] == 2:
        flag = "activeKtKd"
        xAxis = data["xAxis"] = "KT"
        yAxis = data["yAxis"] = "KN1"
    elif data["plane"] == 3:
        flag = "activeKnKd"
        xAxis = data["xAxis"] = "KT1"
        yAxis = data["yAxis"] = "KN"

    # by default 3-comp filtering with threshold
    for df in (pdLow, pdMed, pdHigh):
        df.loc[(df["residual"] > data["threshold"]), flag] = 0

    # calculate max values of K space - first read from QC0 if not present then find out

    knMax = boundary[boundary["month"] == data["month"][:3].upper()]
    knMax = int(list(knMax["MC_KN"])[0])
    ktMax = boundary[boundary["month"] == data["month"][:3].upper()]
    ktMax = int(list(ktMax["MC_KT_" + str(data["integration"])])[0])

    # global airmass throttles for kt and kn maximus
    am_thrott_kt = [0, 3, 10]
    am_thrott_kn = [0, 5, 15]
    amass = ["low", "med", "high"]
    for n, am in enumerate(amass):
        data[am + "AM"]["knMax"] = knMax - am_thrott_kn[n]
        data[am + "AM"]["ktMax"] = ktMax - am_thrott_kt[n]

    for i, df, amass in zip([0, 1, 2], [pdLow, pdMed, pdHigh], amass):
        # reduce maximus according to the airmass
        knMax = data[amass + "AM"]["knMax"]
        ktMax = data[amass + "AM"]["ktMax"]
        knMax = int(knMax)  # - int(am_thrott_kn[i])
        ktMax = int(ktMax)  # - int(am_thrott_kt[i])

        if (knMax < 1) or (ktMax < 1):
            for k in (["KT", "KN"]):
                df = df[df[flag] == 1]
                tempList = list(set(df[k]))

                if len(tempList) > 0:
                    tempList = [i for i in tempList if 0 < i < 100]
                    maxVal = int(max(tempList))
                else:
                    maxVal = "NA"
                if k == "KT":
                    ktMax = maxVal
                elif k == "KN":
                    knMax = maxVal

            # now update the data dictionary
            data[amass + "AM"]["ktMax"] = ktMax
            data[amass + "AM"]["knMax"] = knMax
            # data[amass + "AM"]["kdMax"] = kdMax

            # now update the data dictionary
            data[amass + "AM"]["ktMax"] = ktMax
            data[amass + "AM"]["knMax"] = knMax


def getBoundaries():
    global data, pdLow, pdMed, pdHigh, pcL, dcL, pcR, dcR
    # get area table for left and right curves
    areaLeft = cAr.getArea("left")
    areaRight = cAr.getArea("right")
    airmasses = ["low", "med", "high"]
    dataFrames = [pdLow, pdMed, pdHigh]
    location = [lowCanvas, medCanvas, highCanvas]

    for amass, dframe, location in zip(airmasses, dataFrames, location):
        # identifying column names in Boundary dataframe
        if amass == "low":
            boundShapeL = "LA_Left_S"
            boundPosL = "LA_Left_P"
            boundShapeR = "LA_Right_S"
            boundPosR = "LA_Right_"
            dim = 0
        elif amass == "med":
            boundShapeL = "MA_Left_S"
            boundPosL = "MA_Left_P"
            boundShapeR = "MA_Right_S"
            boundPosR = "MA_Right_"
            dim = 1
        elif amass == "high":
            boundShapeL = "HA_Left_S"
            boundPosL = "HA_Left_P"
            boundShapeR = "HA_Right_S"
            boundPosR = "HA_Right_"
            dim = 2

        shapeL = boundary[boundary["month"] == data["month"][:3].upper()]
        shapeL = list(shapeL[boundShapeL])[0]
        posL = boundary[boundary["month"] == data["month"][:3].upper()]
        posL = list(posL[boundPosL])[0]
        shapeR = boundary[boundary["month"] == data["month"][:3].upper()]
        shapeR = list(shapeR[boundShapeR])[0]
        posR = boundary[boundary["month"] == data["month"][:3].upper()]
        posR = list(posR[boundPosR + str(data["integration"])])[0]

        # updating the data dictionary

        shapeL = data[amass + "AM"]["shapeLeft"] = int(shapeL)
        positionL = data[amass + "AM"]["posLeft"] = int(posL)
        shapeR = data[amass + "AM"]["shapeRight"] = int(shapeR)
        positionR = data[amass + "AM"]["posRight"] = int(posR)

        # identify flag and axes based on kspaces
        if data["plane"] == 1:
            flag = "activeKtKn"
            xAxis = data["xAxis"] = "KT"
            yAxis = data["yAxis"] = "KN"
        elif data["plane"] == 2:
            flag = "activeKtKd"
            xAxis = data["xAxis"] = "KT"
            yAxis = data["yAxis"] = "KN1"
        elif data["plane"] == 3:
            flag = "activeKnKd"
            xAxis = data["xAxis"] = "KT1"
            yAxis = data["yAxis"] = "KN"

        # giving shortcuts
        ktMax = data[amass + "AM"]["ktMax"]
        knMax = data[amass + "AM"]["knMax"]

        # get/calculate  boundaries if ktMax or knMax are not NA. (i,e. data frame is not empty)

        if (len(dframe[dframe[flag] == 1]) > 0):

            # Let's find left boundary of active points
            actFrame = dframe[dframe[flag] == 1]
            activeLBound = []
            eCount = 1
            for y in range(0, int(knMax) + 1):
                x = list(actFrame[actFrame["KN"] == y]["KT"])
                if len(x) > 0:
                    activeLBound.append(min(x))
                else:
                    if y == 0:
                        activeLBound.append(0)
                    else:
                        activeLBound.append("fill")
                        eCount += 1
            indices = [i for i, v in enumerate(activeLBound) if v == "fill"]
            # Now filling empty values with average
            for i in indices:
                nexti = 0
                prev = 0
                prev = activeLBound[i - 1]
                for j in range(i + 1, int(knMax) + 1):
                    if activeLBound[j] != "fill":
                        nexti = activeLBound[j]
                        break
                activeLBound[i] = (int(prev) + int(nexti)) / 2

            # Now find right boundary of active points
            activeRBound = []
            eCount = 1
            for y in range(0, int(knMax) + 1):
                x = list(actFrame[actFrame["KN"] == y]["KT"])
                if len(x) > 0:
                    if max(x) <= ktMax:
                        activeRBound.append(max(x))
                    else:
                        while max(x) > ktMax:
                            x.remove(max(x))
                            if len(x) == 0:
                                activeRBound.append(ktMax)
                                break
                        if len(x) > 0:
                            activeRBound.append(max(x))
                else:
                    if y == 0:
                        activeRBound.append(0)
                    else:
                        activeRBound.append("fill")  # +str(eCount))
                        eCount += 1
            indices = [i for i, v in enumerate(activeRBound) if v == "fill"]
            # Now filling empty values with average
            activeRBound[-1] = ktMax

            for i in indices:
                nexti = 0
                prev = 0
                prev = activeRBound[i - 1]
                for j in range(i + 1, int(knMax) + 1):
                    if activeRBound[j] != "fill":
                        nexti = activeRBound[j]
                        break
                activeRBound[i] = (int(prev) + int(nexti)) / 2
                if activeRBound[i] > ktMax:
                    activeRBound[i] = ktMax

            # updating dictionary
            data[amass + "AM"]["activeLBound"] = activeLBound
            data[amass + "AM"]["activeRBound"] = activeRBound

            if (shapeL == 0):  # Assumption is we have both the boundaries (left and right) or none
                # count active points on the left of curve.
                df = dframe[dframe[flag] == 1]

                # setting default scores to 1000 as we want the lowest possible
                scoreL = 1000
                scoreR = 1000

                for curve in range(0, 6):
                    for position in range(1, 21):
                        shift = ((position - 1) * 2.5)
                        dataCountL = 0
                        dataCountR = 0
                        # Find the curve with shift and set negative values as 0
                        pointsL = ut.curveLeft[curve]
                        pointsL = [(point) + shift for point in pointsL]
                        zeroesL = [0 for point in pointsL if point < 0]
                        pointsL = zeroesL + pointsL[len(zeroesL):]

                        # Find the right curve with shift
                        if curve < 5:
                            pointsR = ut.curveRight[curve]
                            pointsR = [(point) + shift for point in pointsR]

                        for y in range(0, int(knMax) + 1):
                            activeCountL = list(df[df["KN"] == y]["KT"])
                            activeCountL = len([x for x in activeCountL if x < (pointsL[y])])
                            """# for debugging purpose
                            if curve == 3:
                                if position == 5:
                                    print("for curve:4-5 at y = ", y,"point on curve is ", (ut.curveLeft[curve][y])+shift, " left out = ", activeCountL, " and points are ",
                                          [x for x in (list(df[df["KN"] == y]["KT"])) if x < ((ut.curveLeft[curve][y]) + shift)])

                            # delete till here"""
                            dataCountL = dataCountL + activeCountL

                            """if curve == 1:
                                if position == 14:
                                    print("")"""
                            if curve < 5:
                                activeCountR = list(df[df["KN"] == y]["KT"])
                                activeCountR = len([x for x in activeCountR if x > (pointsR[y])])
                                """# for debugging purpose

                                if curve == 1:
                                    if position == 14:
                                        print("for curve:2-14 at y = ", y,"point on curve is ", (ut.curveRight[curve][y])+shift, " right out = ", activeCountL, " and points are ",
                                              [x for x in (list(df[df["KN"] == y]["KT"])) if x > ((ut.curveRight[curve][y]) + shift)])

                                # delete till here"""
                                dataCountR = dataCountR + activeCountR

                        pixCountL = np.sum(abs(np.array(pointsL[:knMax + 1]) - np.array(activeLBound)))
                        pcL[dim, curve, position - 1] = pixCountL
                        pixCountL = pixCountL / (areaLeft.iloc[int(knMax) - 1][(curve * 20) + position])

                        dcL[dim, curve, position - 1] = dataCountL
                        lcount = dataCountL
                        dataCountL = dataCountL / len(df)
                        scoreNowL = pixCountL + dataCountL

                        if curve < 5:
                            pixCountR = np.sum(abs(np.array(pointsR[:knMax + 1]) - np.array(activeRBound)))
                            pcR[dim, curve, position - 1] = pixCountR
                            pixCountR = pixCountR / (areaRight.iloc[int(knMax) - 1][(curve * 20) + position])
                            dcR[dim, curve, position - 1] = dataCountR
                            rcount = dataCountR
                            dataCountR = dataCountR / len(df)
                            scoreNowR = pixCountR + dataCountR

                        # print("curve : ", curve, " position : ", position, " score left ",scoreNowL, "score right ", scoreNowR, " out left ", lcount, " out right ", rcount )

                        if scoreNowL < scoreL:
                            scoreL = scoreNowL
                            shapeL = curve + 1
                            positionL = position
                            outL = lcount
                        if curve < 5:
                            if scoreNowR < scoreR:
                                scoreR = scoreNowR
                                shapeR = curve + 1
                                positionR = position
                                outR = rcount

                        # print("curve : ", shapeL, " position : ", positionL, " out left ", outL, "listL",
                        # list(df[df["KN"] == y]["KT"]), "curvePoint", (ut.curveLeft[shapeL][y] + shiftL),
                        #  " out right ", outR)

                """if (shapeR == 0): #if activating then align 4 spaces to the left
                            # count active points on the right of curve.
                            df = dframe[dframe[flag] == 1]

                            posCountlistRight = []  # a list to store active data points for all 120 curves.
                            scoreR = 1000
                            for curve in range(0, 5):
                                for position in range(1, 21):
                                    dataCountR = 0
                                    for y in range(0, int(knMax)):
                                        activeCountR = list(df[df["KN"] == y]["KT"])
                                        activeCountR = len([x for x in activeCountR if x > ut.curveRight[curve][y]])
                                        #activeCount = len([x for x in activeCount if x <= int(ktMax)])

                                        dataCountR = dataCountR + activeCountR
                                    posCountlistRight.append(dataCountR)
                                    scoreNowR = dataCountR / (areaRight.iloc[int(knMax) - 1][(curve * 20) + position])
                                    print("curve : ", curve, " at position : ", position, " has a score for right ", y, " is : ",
                                          scoreNowR)
                                    if scoreNowR < scoreR:
                                        scoreR = scoreNowR
                                        bestShapeR = curve + 1
                                        bestposR = position
                                        outR = dataCountR

                            shapeR = data[amass + "AM"]["shapeRight"] = bestShapeR


                            positionR = data[amass + "AM"]["posRight"] = bestposR"""
            else:
                # Calculating shifts
                shiftL = ((positionL - 1) * 2.5)
                shiftR = ((positionR - 1) * 2.5)
                outL = 0
                outR = 0

                # Find the left curve with shift and set negative values as 0
                pointsL = ut.curveLeft[shapeL - 1]
                pointsL = [point + shiftL for point in pointsL]
                zeroesL = [0 for point in pointsL if point < 0]
                pointsL = zeroesL + pointsL[len(zeroesL):]

                # Find the right curve with shift
                pointsR = ut.curveRight[shapeR - 1]
                pointsR = [point + shiftR for point in pointsR]

                for y in range(0, int(knMax) + 1):
                    df = dframe[dframe[flag] == 1]

                    activeCountL = list(df[df["KN"] == y]["KT"])
                    activeCountL = len([x for x in activeCountL if x < (pointsL[y])])
                    outL = outL + activeCountL

                    activeCountR = list(df[df["KN"] == y]["KT"])
                    activeCountR = len([x for x in activeCountR if x > (pointsR[y])])
                    # activeCountR = len([x for x in activeCountR if x <= int(ktMax)])
                    outR = outR + activeCountR
                    # print("curve : ", shapeL, " position : ", positionL," out left ", outL,"listL",list(df[df["KN"] == y]["KT"]), "curvePoint",(ut.curveLeft[shapeL][y]+shiftL), " out right ", outR)

            data[amass + "AM"]["shapeLeft"] = shapeL
            data[amass + "AM"]["posLeft"] = positionL
            data[amass + "AM"]["shapeRight"] = shapeR
            data[amass + "AM"]["posRight"] = positionR

            leftB = list(ut.curveLeft[shapeL - 1])
            leftB = leftB[0:int(knMax)]  # get all the points of curve upto Ymax
            leftB = [(i + (2.5 * positionL)) for i in leftB]

            if leftB[-1] != int(ktMax):
                leftB.append(int(ktMax))
            # leftB.append(ktMax)

            # copy first value at 0th index
            leftB = [leftB[0], *leftB]

            # set 0 for negative values
            for n, i in enumerate(leftB):
                if int(i) < 0:
                    leftB[n] = 0

            rightB = list(ut.curveRight[shapeR - 1])
            rightB = rightB[0:int(knMax)]  # get all the points of curve upto Ymax
            rightB = [(i + (2.5 * positionR)) for i in rightB]
            rightB = [i for i in rightB if i <= int(ktMax)]
            if rightB[-1] != int(ktMax):
                rightB.append(int(ktMax))
            # rightB.append(int(ktMax))

            # copy first value at 0th index
            rightB = [rightB[0], *rightB]

            # set 0 for negative values
            for n, i in enumerate(rightB):
                if int(i) < 0:
                    rightB[n] = 0

            # count if points are above configured kn max
            upCount = dframe[dframe[flag] == 1]
            upCount = upCount[upCount["KN"] > int(knMax)]
            outUp = upCount.__len__()
            data[amass + "AM"]["lBound"] = leftB
            data[amass + "AM"]["rBound"] = rightB
            data[amass + "AM"]["In"] = len(dframe[dframe[flag] == 1]) - (outL + outR + outUp)
            # data[amass + "AM"]["Out"] = outL + outR + outUp
            data[amass + "AM"]["Active"] = len(dframe[dframe[flag] == 1])
            if data[amass + "AM"]["Active"] > 1:
                data[amass + "AM"]["Out"] = str(outL + outR + outUp) + " (" + str(round(
                    ((outL + outR + outUp) / data[amass + "AM"]["Active"]) * 100, 2)) + " %)"
            else:
                data[amass + "AM"]["Out"] = outL + outR + outUp
            data[amass + "AM"]["Ignored"] = len(dframe[dframe[flag] == 0])
            data[amass + "AM"]["Total"] = len(dframe)
            data[amass + "AM"]["Err_L"] = round((((outL) / data[amass + "AM"]["Active"]) * 100), 2)
            data[amass + "AM"]["Err_R"] = round((((outR) / data[amass + "AM"]["Active"]) * 100), 2)

            ####################
            # now work on plot
            ####################
            plotGraph(dframe, amass, location, xAxis, yAxis, flag)
        else:
            outL = 0
            outR = 0
            matplotlib.use("TKAgg")
            style.use("ggplot")
            f = Figure(figsize=(3, 2.5), dpi=100)
            a = f.add_subplot(111)
            a.clear()
            line = np.linspace(0, 100, 101)
            a.set_xlim([0, 100])
            a.set_ylim([0, 100])
            a.plot(line, line, color="black")
            canvas = FigureCanvasTkAgg(f, master=location)
            canvas.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1)
            canvas.draw()

            """if location == lowCanvas:
                lowButton = tk.Button(location, text="Configure", font=(None, 10), command=lowConfig,
                                      state=tk.DISABLED)
                lowButton.place(relx=.75, rely=0.015, relwidth=0.22, relheight=0.1)
            elif location == medCanvas:
                medButton = tk.Button(location, text="Configure", font=(None, 10), command=medConfig,
                                      state=tk.DISABLED)
                medButton.place(relx=.75, rely=0.015, relwidth=0.22, relheight=0.1)
            elif location == highCanvas:
                highButton = tk.Button(location, text="Configure", font=(None, 10), command=highConfig,
                                       state=tk.DISABLED)
                highButton.place(relx=.75, rely=0.015, relwidth=0.22, relheight=0.1)"""


def plotGraph(dframe, amass, location, xAxis, yAxis, flag):
    if len(dframe) > 1:
        col = dframe.columns

        if len(dframe[dframe[flag] == 1]) > 0:  # Plot boundary only if data is there
            # Plotting left boundary
            xLB = data[amass + "AM"]["lBound"]
            # Making x count = 101 so it doesn't mess with existing graph
            fillCount = 101 - len(xLB)
            if fillCount > 0:
                fillList = [xLB[-1]] * fillCount
                xLB = xLB + fillList
            yLB = list(np.linspace(0, data[amass + "AM"]["knMax"], data[amass + "AM"]["knMax"] + 1))
            fillCount = 101 - len(yLB)
            fillList = [yLB[-1]] * fillCount
            yLB = yLB + fillList

            # plotting right boundary
            xRB = data[amass + "AM"]["rBound"]
            # Making x count = 101 so it doesn't mess with existing graph
            fillCount = 101 - len(xRB)
            if fillCount > 0:
                fillList = [xRB[-1]] * fillCount
                xRB = xRB + fillList

            yRB = yLB
            # yRB = [0,*yRB]
            # yRB[-1] = yLB[-1]
            # fillCount = 101 - len(yRB)
            # fillList = [yRB[-1]] * fillCount
            # yRB = yRB + fillList

            # Now update data dictionary

            # check if anypoint of left boundary is falling beyond right boundary if yes restrict at right boundary
            """for (x), i in enumerate(xLB):
                if int(x) > int(xRB[i]):
                    xLB[i]=xRB[i]"""
            xlimit = max(xRB)
            xLB = [x if (x < xlimit) else xlimit for x in xLB]

            # Now update data dictionary

            data[amass + "AM"]["xLB"] = xLB
            data[amass + "AM"]["yLB"] = yLB
            data[amass + "AM"]["xRB"] = xRB
            data[amass + "AM"]["yRB"] = yRB

        dframe = dframe.copy()
        dframe["outFlag"] = 0
        setOutFlag(dframe, xAxis, yAxis, amass, "left")
        setOutFlag(dframe, xAxis, yAxis, amass, "right")

        active_mask = dframe[flag] == 1
        out_mask = dframe["outFlag"] == 1
        inact_mask = dframe[flag] == 0

        xAct = dframe.loc[active_mask & (~out_mask), xAxis]
        yAct = dframe.loc[active_mask & (~out_mask), yAxis]
        xActOut = dframe.loc[active_mask & out_mask, xAxis]
        yActOut = dframe.loc[active_mask & out_mask, yAxis]
        xInact = dframe.loc[inact_mask, xAxis]
        yInact = dframe.loc[inact_mask, yAxis]

        matplotlib.use("TKAgg")
        style.use("ggplot")
        f = Figure(figsize=(3, 2.5), dpi=100)
        a = f.add_subplot(111)
        a.clear()
        line = np.linspace(0, 100, 101)
        '''x=dframe[xAxis]
        y=dframe[yAxis]
        xy=np.vstack([x,y])
        from scipy.stats import gaussian_kde
        z = gaussian_kde(xy)(xy)
        a.scatter(x,y,c=z,s=100,edgecolor='')'''
        a.scatter(xInact, yInact, color='gray', marker=".")
        a.scatter(xAct, yAct, color='orangered', marker=".")
        if len(xActOut) > 0:
            a.scatter(xActOut, yActOut, color='firebrick', marker=".")

        a.set_xlim([0, 100])
        a.set_ylim([0, 100])
        a.plot(line, line, color="black")
        a.tick_params(axis='x', colors='black')
        a.tick_params(axis='y', colors='black')

        if len(xAct) > 0:  # Plot boundary only if data is there

            # plot left boundary
            a.plot(xLB, yLB, color="green")

            # plot right boundary
            a.plot(xRB, yRB, color="green")

        canvas = FigureCanvasTkAgg(f, master=location)
        canvas.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1)
        canvas.draw()
        canvas.flush_events()

        # canvas.mpl_connect('button_press_event', graphConfig)
        if location == lowCanvas:
            lowButton = tk.Button(location, text="Configure", font=(None, 10), command=lowConfig)
            lowButton.place(relx=.75, rely=0.015, relwidth=0.22, relheight=0.1)
        elif location == medCanvas:
            medButton = tk.Button(location, text="Configure", font=(None, 10), command=medConfig)
            medButton.place(relx=.75, rely=0.015, relwidth=0.22, relheight=0.1)
        elif location == highCanvas:
            highButton = tk.Button(location, text="Configure", font=(None, 10), command=highConfig)
            highButton.place(relx=.75, rely=0.015, relwidth=0.22, relheight=0.1)


def lowConfig():
    global data, flag
    amass = "low"
    dframe = pdLow
    graphConfig(amass, dframe)


def medConfig():
    global data, flag
    amass = "med"
    dframe = pdMed
    graphConfig(amass, dframe)


def highConfig():
    global data, flag
    amass = "high"
    dframe = pdHigh
    graphConfig(amass, dframe)


def getCoordinates(eclick, erelease):
    data["x1"], data["y1"] = round(eclick.xdata), round(eclick.ydata)
    data["x2"], data["y2"] = round(erelease.xdata), round(erelease.ydata)


def toggle_selector(event):
    if event.key in ['Q', 'q'] and toggle_selector.RS.active:
        toggle_selector.RS.set_active(False)
    if event.key in ['A', 'a'] and not toggle_selector.RS.active:
        toggle_selector.RS.set_active(True)


def graphConfig(amass, dframe):
    global data, editGraph
    locationDict = {'low': lowCanvas, 'med': medCanvas, 'high': highCanvas}

    if data["plane"] == 1:
        flag = data["flag"] = "activeKtKn"
        x = data["xAxis"] = "KT"
        y = data["yAxis"] = "KN"
        titleString = "Global, Direct"
    elif data["plane"] == 2:
        flag = data["flag"] = "activeKtKd"
        x = data["xAxis"] = "KT"
        y = data["yAxis"] = "KN1"
        titleString = "Global, Diffuse"
    elif data["plane"] == 3:
        flag = data["flag"] = "activeKnKd"
        x = data["xAxis"] = "KT1"
        y = data["yAxis"] = "KN"
        titleString = "Direct, Diffuse"

    def plotForEdit(amass, dframe, flag, x, y, titleString):
        global data, editGraph
        dframe = dframe.copy()
        dframe["outFlag"] = 0
        setOutFlag(dframe, x, y, amass, "left")
        setOutFlag(dframe, x, y, amass, "right")

        active = dframe[flag] == 1
        inact = dframe[flag] == 0
        out = dframe["outFlag"] == 1

        xActb10 = dframe.loc[active & (dframe["densBin"] == 1) & (~out), x]
        yActb10 = dframe.loc[active & (dframe["densBin"] == 1) & (~out), y]
        xActb11 = dframe.loc[active & (dframe["densBin"] == 1) & out, x]
        yActb11 = dframe.loc[active & (dframe["densBin"] == 1) & out, y]

        xActb20 = dframe.loc[active & (dframe["densBin"] == 2) & (~out), x]
        yActb20 = dframe.loc[active & (dframe["densBin"] == 2) & (~out), y]
        xActb21 = dframe.loc[active & (dframe["densBin"] == 2) & out, x]
        yActb21 = dframe.loc[active & (dframe["densBin"] == 2) & out, y]

        xActb30 = dframe.loc[active & (dframe["densBin"] == 3) & (~out), x]
        yActb30 = dframe.loc[active & (dframe["densBin"] == 3) & (~out), y]
        xActb31 = dframe.loc[active & (dframe["densBin"] == 3) & out, x]
        yActb31 = dframe.loc[active & (dframe["densBin"] == 3) & out, y]

        xActb40 = dframe.loc[active & (dframe["densBin"] == 4) & (~out), x]
        yActb40 = dframe.loc[active & (dframe["densBin"] == 4) & (~out), y]
        xActb41 = dframe.loc[active & (dframe["densBin"] == 4) & out, x]
        yActb41 = dframe.loc[active & (dframe["densBin"] == 4) & out, y]

        xActb50 = dframe.loc[active & (dframe["densBin"] == 5) & (~out), x]
        yActb50 = dframe.loc[active & (dframe["densBin"] == 5) & (~out), y]
        xActb51 = dframe.loc[active & (dframe["densBin"] == 5) & out, x]
        yActb51 = dframe.loc[active & (dframe["densBin"] == 5) & out, y]

        xInact = dframe.loc[inact, x]
        yInact = dframe.loc[inact, y]

        f = plt.figure(figsize=(6, 5), dpi=100)
        ax = f.add_subplot(111)
        ax.clear()

        f.canvas.set_window_title(data["siteIdentifier"] + " " + "- " + amass.upper() + " - QCFIT")
        style.use("ggplot")
        line = np.linspace(0, 100, 101)

        titleFont = {'family': 'serif', 'color': 'black', 'weight': 'heavy', 'size': 25}
        labelFont = {'family': 'serif', 'color': 'darkred', 'weight': 'normal', 'size': 12}

        plt.suptitle(amass.upper() + " Air Mass - " + titleString, fontdict=titleFont)
        plt.xlabel("kt * 100", fontdict=labelFont)
        plt.ylabel("kn * 100", fontdict=labelFont)
        plt.tick_params(axis='x', colors='black')
        plt.tick_params(axis='y', colors='black')
        plt.yticks(rotation=90)
        plt.xlim(0, 100)
        plt.ylim(0, 100)
        ax.scatter(xInact, yInact, color='gray', marker=".")

        if len(xActb10) > 0:
            ax.scatter(xActb10, yActb10, color='orangered', marker=".")
        if len(xActb20) > 0:
            ax.scatter(xActb20, yActb20, color='darkorange', marker=".")
        if len(xActb30) > 0:
            ax.scatter(xActb30, yActb30, color='orange', marker=".")
        if len(xActb40) > 0:
            ax.scatter(xActb40, yActb40, color='gold', marker=".")
        if len(xActb50) > 0:
            ax.scatter(xActb50, yActb50, color='yellow', marker=".")
        if len(xActb11) > 0:
            ax.scatter(xActb11, yActb11, color='firebrick', marker=".")
        if len(xActb21) > 0:
            ax.scatter(xActb21, yActb21, color='chocolate', marker=".")
        if len(xActb31) > 0:
            ax.scatter(xActb31, yActb31, color='peru', marker=".")
        if len(xActb41) > 0:
            ax.scatter(xActb41, yActb41, color='goldenrod', marker=".")
        if len(xActb51) > 0:
            ax.scatter(xActb51, yActb51, color='khaki', marker=".")

        ax.plot(line, line, color="black")  # line no 0
        ax.plot(data[amass + "AM"]["xLB"], data[amass + "AM"]["yLB"], color="green")  # line no 1
        ax.plot(data[amass + "AM"]["xRB"], data[amass + "AM"]["yRB"], color="green")  # line no 2
        toggle_selector.RS = RectangleSelector(ax, getCoordinates, drawtype='box', useblit=False, button=[1],
                                               minspanx=5, minspany=5, spancoords='pixels',
                                               interactive=True)
        plt.connect('key_press_event', toggle_selector)

        mngr = plt.get_current_fig_manager()
        # to put it into the upper left corner:
        mngr.window.setGeometry = (50, 100, 640, 545)
        # mngr.window.setGeometry = (250, 120, 1280, 1024)
        # mngr.window.setGeometry
        mngr.window.wm_iconbitmap("dataFiles/qcfit-icon.ico")
        plt.show(block=False)

    if data["editWinFlag"] == 1:
        return
    else:
        data["editWinFlag"] = 1

        ktMaxSpinVal = 99
        minKt = data[amass + "AM"]["xLB"][int(data[amass + "AM"]["yLB"][-1])]
        knMaxSpinVal = 99

        if len(filterDict[amass]) > 0:
            dframe = filterDict[amass]

        # dframe = dframe[dframe[amass + "Exclude"] == 0]

        plotForEdit(amass, dframe, flag, x, y, titleString)

        # actvate the controller page
        editGraph.deiconify()
        header = amass.upper() + " Air Mass - " + titleString
        inPoints = data[amass + "AM"]["In"]
        outPoints = data[amass + "AM"]["Out"]
        activePoints = data[amass + "AM"]["Active"]
        ignoredPoints = data[amass + "AM"]["Ignored"]
        totalPoints = data[amass + "AM"]["Total"]
        errL = data[amass + "AM"]["Err_L"]
        errR = data[amass + "AM"]["Err_R"]

        def handleGraphCross():
            global data, editGraph
            plt.close('all')
            data["editWinFlag"] = 0
            editGraph.withdraw()

        def reset(dframe, amass, x, y):
            global data
            plt.close('all')
            outL = 0
            outR = 0

            ktMax = int(data[amass + "AM"]["knMax"])

            plotForEdit(amass, dframe, flag, x, y, titleString)
            # ax.scatter(xAct, yAct, color='blue')
            # ax.scatter(xInact, yInact, color='orange')
            # ax.plot(line, line, color="black")  # line no 0
            # ax.plot(data[amass + "AM"]["xLB"], data[amass + "AM"]["yLB"], color="green")  # line no 1
            # ax.plot(data[amass + "AM"]["xRB"], data[amass + "AM"]["yRB"], color="green")  # line no 2

            # update data dictionary
            for yp in range(0, ktMax):
                # activeCountL = list(df[df["KN"] == y][x])
                # activeCountL = len([x for x in activeCountL if x < (ut.curveLeft[shapeL][y] + shiftL)])
                # outL = outL + activeCountL

                countL = list(dframe[dframe[y] == yp][x])
                countL = [xp for xp in countL if xp < int(data[amass + "AM"]["xLB"][yp])]
                outL = outL + len(countL)
                countR = list(dframe[dframe[y] == yp][x])
                countR = [xp for xp in countR if x > int(data[amass + "AM"]["xRB"][yp])]
                outR = outR + len(countR)
                # print("at y = ", y, "  ", "out left ", outL, "listL",
                # list(filterData[filterData["KN"] == y][x]), "curvePoint", data[amass+"AM"]["xLB"][y], " out right ",
                # outR)

            # count if points are above configured kn max
            upCount = dframe[dframe[flag] == 1]
            upCount = upCount[upCount[y] > int(knVal.get())]
            outUp = upCount.__len__()

            # updating data dictionary
            data[amass + "AM"]["In"] = len(dframe[dframe[flag] == 1]) - (outL + outR + outUp)
            # data[amass + "AM"]["Out"] = outL + outR + outUp
            data[amass + "AM"]["Active"] = len(dframe[dframe[flag] == 1])
            if data[amass + "AM"]["Active"] > 1:
                data[amass + "AM"]["Out"] = str(outL + outR + outUp) + " (" + str(round(
                    ((outL + outR + outUp) / data[amass + "AM"]["Active"]) * 100, 2)) + " %)"
            else:
                data[amass + "AM"]["Out"] = outL + outR + outUp
            data[amass + "AM"]["Ignored"] = len(dframe[dframe[flag] == 0])
            data[amass + "AM"]["Total"] = len(dframe)
            if data[amass + "AM"]["Active"] > 1:
                data[amass + "AM"]["Err_L"] = round((((outL) / data[amass + "AM"]["Active"]) * 100), 2)
                data[amass + "AM"]["Err_R"] = round((((outR) / data[amass + "AM"]["Active"]) * 100), 2)
            setStats()

            # update main canvas plot
            plotGraph(dframe, amass, locationDict[amass], data["xAxis"], data["yAxis"], data["flag"])

        def listPoints(amass, df, x, y):
            """if data["listPageFlag"] == 1:
                return
            else:
                data["listPageFlag"] = 1"""
            df = df[df[amass + "Exclude"] == 0]
            df["toList"] = 0
            # selecting points inside rectangular selection
            df.loc[(df["toList"] == 0) & (df[x] < data["x2"]), "toList"] = 1  # left max bound
            df.loc[(df["toList"] == 1) & (df[x] < data["x1"]), "toList"] = 0  # left min bound
            df.loc[(df["toList"] == 1) & (df[y] > data["y2"]), "toList"] = 0  # top max bound
            df.loc[(df["toList"] == 1) & (df[y] < data["y1"]), "toList"] = 0  # lower min bound

            df = df[df["toList"] == 1]
            cols = list(df.columns[0:8])
            points = pd.DataFrame()
            for col in cols:
                points[col] = df[col]
            # now add KT KN and KD

            points["KT"] = df[x]
            points["KN"] = df[y]
            points["KD"] = df["KD"]
            points[points.columns[0]] = points[points.columns[0]]  # .dt.date

            # limit upto 4th dec places
            # decimals = pd.Series([2, 2, 2], index=[points.columns[2], points.columns[3], points.columns[4]])
            points[points.columns[2]] = points[points.columns[2]].astype('float').round(2)
            points[points.columns[3]] = points[points.columns[3]].astype('float').round(2)
            points[points.columns[4]] = points[points.columns[4]].astype('float').round(2)
            points[points.columns[8]] = points[points.columns[8]].map(int)
            points[points.columns[9]] = points[points.columns[9]].map(int)
            points[points.columns[10]] = points[points.columns[10]].map(int)

            points.to_csv("Data_Points.csv")
            np.savetxt(r'Data_Points.txt', points.values, fmt='%s')

            # add header in txt file

            f = open("Data_Points.txt", "r+")
            content = f.read()

            c1 = points.columns[2].replace(" ", "_")
            c2 = points.columns[3].replace(" ", "_")
            c3 = points.columns[4].replace(" ", "_")
            content = "date time " + c1 + " " + c2 + " " + c3 + " " + "IQCGlobal IQCDirect IQCDiffuse KT KN KD \n" + content
            content.replace(" ", "    ")
            f.seek(0, 0)
            f.write(content)
            f.close()

            if platform.system() == "Windows":
                os.system("Data_Points.txt")
                os.system("Data_Points.csv")
            else:
                subprocess.run(['open', "Data_Points.txt"], check=True)
                subprocess.run(['open', "Data_Points.csv"], check=True)

        def exclude(amass, dframe, x, y):
            plt.close('all')
            global data, filterDict
            # dframe[amass+"Exclude"] = 0
            # dframe.loc[]
            flaglevel = max(list(set(dframe[amass + "Exclude"]))) + 1
            # oldFilter = dframe[dframe[amass + "Exclude"] == 0]

            # selecting points inside rectangular selection
            dframe.loc[(dframe[amass + "Exclude"] == 0) & (dframe[x] < data["x2"]), (
                    amass + "Exclude")] = flaglevel  # left max bound
            dframe.loc[(dframe[amass + "Exclude"] == flaglevel) & (dframe[x] < data["x1"]), (
                    amass + "Exclude")] = 0  # left min bound
            dframe.loc[(dframe[amass + "Exclude"] == flaglevel) & (dframe[y] > data["y2"]), (
                    amass + "Exclude")] = 0  # top max bound
            dframe.loc[(dframe[amass + "Exclude"] == flaglevel) & (dframe[y] < data["y1"]), (
                    amass + "Exclude")] = 0  # lower min bound
            # del ax.collections[0]  # removes active
            # del ax.collections[0]  # removes inactive
            # plt.show
            newFilter = filterDict[amass] = dframe[dframe[amass + "Exclude"] == 0]

            plotForEdit(amass, newFilter, flag, x, y, titleString)

            # ax.scatter(xAct, yAct, color='blue')
            # ax.scatter(xInact, yInact, color='orange')
            # plt.show

            # calculating and updating stats
            # left
            outL = 0
            outR = 0
            ktMax = int(data[amass + "AM"]["ktMax"])
            knMax = int(data[amass + "AM"]["knMax"])
            filterData = newFilter[newFilter[flag] == 1]
            for yp in range(0, knMax):
                # activeCountL = list(df[df["KN"] == y]["KT"])
                # activeCountL = len([x for x in activeCountL if x < (ut.curveLeft[shapeL][y] + shiftL)])
                # outL = outL + activeCountL

                countL = list(filterData[filterData[y] == yp][x])
                countL = [xp for xp in countL if xp < data[amass + "AM"]["xLB"][yp]]
                outL = outL + len(countL)
                countR = list(filterData[filterData[y] == yp][x])
                countR = [xp for xp in countR if xp > data[amass + "AM"]["xRB"][yp]]
                outR = outR + len(countR)
                # print("at y = ", y, "  ", "out left ", outL, "listL",
                # list(filterData[filterData["KN"] == y]["KT"]), "curvePoint", data[amass+"AM"]["xLB"][y], " out right ",
                # outR)

            # count if points are above configured kn max
            upCount = newFilter[newFilter[flag] == 1]
            upCount = upCount[upCount[y] > int(knVal.get())]
            outUp = upCount.__len__()

            # updating data dictionary
            data[amass + "AM"]["In"] = len(newFilter[newFilter[flag] == 1]) - (outL + outR + outUp)
            # data[amass + "AM"]["Out"] = outL + outR + outUp
            data[amass + "AM"]["Active"] = len(newFilter[newFilter[flag] == 1])
            if data[amass + "AM"]["Active"] > 1:
                data[amass + "AM"]["Out"] = str(outL + outR + outUp) + " (" + str(round(
                    ((outL + outR + outUp) / data[amass + "AM"]["Active"]) * 100, 2)) + " %)"
            else:
                data[amass + "AM"]["Out"] = outL + outR + outUp
            data[amass + "AM"]["Ignored"] = len(newFilter[newFilter[flag] == 0])
            data[amass + "AM"]["Total"] = len(newFilter)
            if data[amass + "AM"]["Active"] > 1:
                data[amass + "AM"]["Err_L"] = round((((outL) / data[amass + "AM"]["Active"]) * 100), 2)
                data[amass + "AM"]["Err_R"] = round((((outR) / data[amass + "AM"]["Active"]) * 100), 2)

            InVal.configure(text=data[amass + "AM"]["In"])
            OutVal.configure(text=data[amass + "AM"]["Out"])
            ActiveVal.configure(text=data[amass + "AM"]["Active"])
            IgnoredVal.configure(text=data[amass + "AM"]["Ignored"])
            TotalVal.configure(text=data[amass + "AM"]["Total"])
            ErrLVal.configure(text=data[amass + "AM"]["Err_L"])
            ErrRVal.configure(text=data[amass + "AM"]["Err_R"])
            setStats()

            # update main canvas plot

            plotGraph(newFilter, amass, locationDict[amass], data["xAxis"], data["yAxis"], data["flag"])
            # update dashboard

            # tempData = dframe[dframe["KT"] < data["x2"]]
            # tempData = tempData[tempData["KT"] > data["x1"]]

        def spinCalculation(currAmass, x, y):
            global data, pdLow, pdMed, pdHigh
            line = list(np.linspace(0, 100, 101))

            knChange = int(knVal.get()) - int(data[currAmass + "AM"]["knMax"])
            ktChange = int(ktVal.get()) - int(data[currAmass + "AM"]["ktMax"])

            # if ktVal.get()==int(data[currAmass + "AM"]["xRB"][ktVal.get]):
            # return

            for amass, dframe in zip(["low", "med", "high"], [pdLow, pdMed, pdHigh]):
                if data[amass + "AM"]["knMax"] != 'NA':
                    if 1 <= (int(data[amass + "AM"]["knMax"]) + knChange) <= 99:
                        if 1 <= (int(data[amass + "AM"]["ktMax"]) + ktChange) <= 99:

                            data[amass + "AM"]["knMax"] = int(data[amass + "AM"]["knMax"]) + knChange
                            data[amass + "AM"]["ktMax"] = int(data[amass + "AM"]["ktMax"]) + ktChange

                            # renaming for ease
                            Kn = int(data[amass + "AM"]["knMax"])
                            Kt = int(data[amass + "AM"]["ktMax"])

                            # Prepare left boundary
                            yLB = line[0:Kn + 1] + [Kn for point in line if point > Kn]
                            shiftL = data[amass + 'AM']['posLeft'] * 2.5
                            xLB = utills.curveLeft[data[amass + 'AM']['shapeLeft'] - 1]
                            xLB = [point + shiftL for point in xLB]

                            # copy first value at 0th index
                            xLB = [xLB[0], *xLB]

                            # replace the values greater than knmax-th value in curve with knmax-th value
                            xLB = xLB[0:Kn + 1]
                            xLB += [Kt] * (len(line) - len(xLB))

                            # Replace negative values with 0
                            zeroesL = [0 for point in xLB if point < 0]
                            xLB = zeroesL + xLB[len(zeroesL):]

                            # Prepare right boundary
                            yRB = line[0:Kn + 1] + [Kn for point in line if point > Kn]
                            shiftR = data[amass + 'AM']['posRight'] * 2.5
                            xRB = utills.curveRight[data[amass + 'AM']['shapeRight'] - 1]
                            xRB = [point + shiftR for point in xRB]
                            # copy first value at 0th index
                            xRB = [xRB[0], *xRB]
                            # replace the values greater than knmax-th value in curve with knmax-th value
                            xRB = xRB[0:Kt + 1]
                            xRB = [i for i in xRB if i <= Kt]

                            xRB += [xRB[-1]] * (len(line) - len(xRB))

                            # update data dictionary with new boundaries and bounds(lBound and rBound)
                            data[amass + 'AM']['xLB'] = xLB
                            data[amass + 'AM']['yLB'] = yLB
                            data[amass + "AM"]["lBound"] = xLB

                            data[amass + 'AM']['xRB'] = xRB
                            data[amass + 'AM']['yRB'] = yRB
                            data[amass + "AM"]["rBound"] = xRB

                            filtFrame = dframe[dframe[amass + "Exclude"] == 0]

                            # now clear old boundaries and plot new one.
                            if amass == currAmass:
                                plt.close('all')
                                plotForEdit(amass, filtFrame, flag, x, y, titleString)

                            # update main canvas plot
                            plotGraph(filtFrame, amass, locationDict[amass], data["xAxis"], data["yAxis"], data["flag"])
                            outL = 0
                            outR = 0
                            for yp in range(0, Kn + 1):
                                # activeCountL = list(df[df["KN"] == y]["KT"])
                                # activeCountL = len([x for x in activeCountL if x < (ut.curveLeft[shapeL][y] + shiftL)])
                                # outL = outL + activeCountL

                                countL = list(filtFrame[filtFrame[y] == yp][x])
                                countL = [xp for xp in countL if xp < data[amass + "AM"]["xLB"][yp]]
                                outL = outL + len(countL)
                                countR = list(filtFrame[filtFrame[y] == yp][x])
                                countR = [xp for xp in countR if xp > data[amass + "AM"]["xRB"][yp]]
                                outR = outR + len(countR)
                                # print("at y = ", y, "  ", "out left ", outL, "listL",
                                # list(filterData[filterData["KN"] == y]["KT"]), "curvePoint", data[amass+"AM"]["xLB"][y], " out right ",
                                # outR)

                            # count if points are above configured kn max
                            upCount = filtFrame[filtFrame[flag] == 1]
                            upCount = upCount[upCount[y] > Kn]
                            outUp = upCount.__len__()

                            # updating data dictionary
                            data[amass + "AM"]["In"] = len(filtFrame[filtFrame[flag] == 1]) - (outL + outR + outUp)
                            # data[amass + "AM"]["Out"] = outL + outR + outUp
                            data[amass + "AM"]["Active"] = len(filtFrame[filtFrame[flag] == 1])
                            if data[amass + "AM"]["Active"] > 1:
                                data[amass + "AM"]["Out"] = str(outL + outR + outUp) + " (" + str(round(
                                    ((outL + outR + outUp) / data[amass + "AM"]["Active"]) * 100, 2)) + " %)"
                            else:
                                data[amass + "AM"]["Out"] = outL + outR + outUp
                            data[amass + "AM"]["Ignored"] = len(filtFrame[filtFrame[flag] == 0])
                            data[amass + "AM"]["Total"] = len(filtFrame)
                            if data[amass + "AM"]["Active"] > 1:
                                data[amass + "AM"]["Err_L"] = round((((outL) / data[amass + "AM"]["Active"]) * 100), 2)
                                data[amass + "AM"]["Err_R"] = round((((outR) / data[amass + "AM"]["Active"]) * 100), 2)

                            setStats()

            # Now update the current frame values
            InVal.configure(text=data[currAmass + "AM"]["In"])
            OutVal.configure(text=data[currAmass + "AM"]["Out"])
            ActiveVal.configure(text=data[currAmass + "AM"]["Active"])
            IgnoredVal.configure(text=data[currAmass + "AM"]["Ignored"])
            TotalVal.configure(text=data[currAmass + "AM"]["Total"])
            ErrLVal.configure(text=data[currAmass + "AM"]["Err_L"])
            ErrRVal.configure(text=data[currAmass + "AM"]["Err_R"])

            pass

        def reval(currAmass, x, y, *args):
            global data, pdLow, pdMed, pdHigh

            # update the data dictionary
            data[amass + 'AM']['shapeLeft'] = cLVar.get()
            data[amass + 'AM']['shapeRight'] = cRVar.get()
            data[amass + 'AM']['posLeft'] = pLVar.get()
            data[amass + 'AM']['posRight'] = pRVar.get()

            line = list(np.linspace(0, 100, 101))

            if data[amass + "AM"]["knMax"] != 'NA':

                # renaming for ease
                Kn = int(data[amass + "AM"]["knMax"])
                Kt = int(data[amass + "AM"]["ktMax"])

                # Prepare left boundary
                yLB = line[0:Kn + 1] + [Kn for point in line if point > Kn]
                shiftL = data[amass + 'AM']['posLeft'] * 2.5
                xLB = utills.curveLeft[data[amass + 'AM']['shapeLeft'] - 1]
                xLB = [point + shiftL for point in xLB]

                # copy first value at 0th index
                xLB = [xLB[0], *xLB]

                # replace the values greater than knmax-th value in curve with knmax-th value
                xLB = xLB[0:Kn + 1]
                xLB += [Kt] * (len(line) - len(xLB))

                # Replace negative values with 0
                zeroesL = [0 for point in xLB if point < 0]
                xLB = zeroesL + xLB[len(zeroesL):]

                # Prepare right boundary
                yRB = line[0:Kn + 1] + [Kn for point in line if point > Kn]
                shiftR = data[amass + 'AM']['posRight'] * 2.5
                xRB = utills.curveRight[data[amass + 'AM']['shapeRight'] - 1]
                xRB = [point + shiftR for point in xRB]
                # copy first value at 0th index
                xRB = [xRB[0], *xRB]
                # replace the values greater than knmax-th value in curve with knmax-th value
                xRB = xRB[0:Kt + 1]
                xRB = [i for i in xRB if i <= Kt]

                xRB += [xRB[-1]] * (len(line) - len(xRB))

                # update data dictionary with new boundaries and bounds(lBound and rBound)
                data[amass + 'AM']['xLB'] = xLB
                data[amass + 'AM']['yLB'] = yLB
                data[amass + "AM"]["lBound"] = xLB

                data[amass + 'AM']['xRB'] = xRB
                data[amass + 'AM']['yRB'] = yRB
                data[amass + "AM"]["rBound"] = xRB

                filtFrame = dframe[dframe[amass + "Exclude"] == 0]

                # now clear old boundaries and plot new one.
                if amass == currAmass:
                    plt.close('all')
                    plotForEdit(amass, filtFrame, flag, x, y, titleString)

                # update main canvas plot
                plotGraph(filtFrame, amass, locationDict[amass], data["xAxis"], data["yAxis"], data["flag"])
                outL = 0
                outR = 0
                for yp in range(0, Kn + 1):
                    # activeCountL = list(df[df["KN"] == y]["KT"])
                    # activeCountL = len([x for x in activeCountL if x < (ut.curveLeft[shapeL][y] + shiftL)])
                    # outL = outL + activeCountL

                    countL = list(filtFrame[filtFrame[y] == yp][x])
                    countL = [xp for xp in countL if xp < data[amass + "AM"]["xLB"][yp]]
                    outL = outL + len(countL)
                    countR = list(filtFrame[filtFrame[y] == yp][x])
                    countR = [xp for xp in countR if xp > data[amass + "AM"]["xRB"][yp]]
                    outR = outR + len(countR)
                    # print("at y = ", y, "  ", "out left ", outL, "listL",
                    # list(filterData[filterData["KN"] == y]["KT"]), "curvePoint", data[amass+"AM"]["xLB"][y], " out right ",
                    # outR)

                # count if points are above configured kn max
                upCount = filtFrame[filtFrame[flag] == 1]
                upCount = upCount[upCount[y] > Kn]
                outUp = upCount.__len__()

                # updating data dictionary
                data[amass + "AM"]["In"] = len(filtFrame[filtFrame[flag] == 1]) - (outL + outR + outUp)
                # data[amass + "AM"]["Out"] = outL + outR + outUp
                data[amass + "AM"]["Active"] = len(filtFrame[filtFrame[flag] == 1])
                if data[amass + "AM"]["Active"] > 1:
                    data[amass + "AM"]["Out"] = str(outL + outR + outUp) + " (" + str(round(
                        ((outL + outR + outUp) / data[amass + "AM"]["Active"]) * 100, 2)) + " %)"
                else:
                    data[amass + "AM"]["Out"] = outL + outR + outUp
                data[amass + "AM"]["Ignored"] = len(filtFrame[filtFrame[flag] == 0])
                data[amass + "AM"]["Total"] = len(filtFrame)
                if data[amass + "AM"]["Active"] > 1:
                    data[amass + "AM"]["Err_L"] = round((((outL) / data[amass + "AM"]["Active"]) * 100), 2)
                    data[amass + "AM"]["Err_R"] = round((((outR) / data[amass + "AM"]["Active"]) * 100), 2)

                setStats()

            # Now update the current frame values
            InVal.configure(text=data[currAmass + "AM"]["In"])
            OutVal.configure(text=data[currAmass + "AM"]["Out"])
            ActiveVal.configure(text=data[currAmass + "AM"]["Active"])
            IgnoredVal.configure(text=data[currAmass + "AM"]["Ignored"])
            TotalVal.configure(text=data[currAmass + "AM"]["Total"])
            ErrLVal.configure(text=data[currAmass + "AM"]["Err_L"])
            ErrRVal.configure(text=data[currAmass + "AM"]["Err_R"])

        def wideLeft(amass, x, y):
            if pLVar.get() >= 2:
                pLVar.set(pLVar.get() - 1)
                reval(amass, x, y)
            else:
                return

        def wideBoth(amass, x, y):
            if pLVar.get() >= 2:
                pLVar.set(pLVar.get() - 1)
            if pRVar.get() <= 19:
                pRVar.set(pRVar.get() + 1)
            reval(amass, x, y)

        def wideRight(amass, x, y):
            if pRVar.get() <= 19:
                pRVar.set(pRVar.get() + 1)
                reval(amass, x, y)
            else:
                return

        def narrowLeft(amass, x, y):
            if pLVar.get() <= 19:
                pLVar.set(pLVar.get() + 1)
                reval(amass, x, y)
            else:
                return

        def narrowBoth(amass, x, y):
            if pLVar.get() <= 19:
                pLVar.set(pLVar.get() + 1)
            if pRVar.get() >= 2:
                pRVar.set(pRVar.get() - 1)
            reval(amass, x, y)

        def narrowRight(amass, x, y):
            if pRVar.get() >= 2:
                pRVar.set(pRVar.get() - 1)
                reval(amass, x, y)
            else:
                return

        def lessErr(amass, x, y):
            global data
            level = errLevel.cget("text")
            level = int(level)
            errLevel.config(text=str(level - 1))

            scale = data[amass + "AM"]["scale"]
            scale = scale * 10
            data[amass + "AM"]["scale"] = scale
            errorCalculation(amass, scale, x, y)

        def moreErr(amass, x, y):
            global data
            level = errLevel.cget("text")
            level = int(level)
            errLevel.config(text=str(level + 1))

            scale = data[amass + "AM"]["scale"]
            scale = scale / 10
            data[amass + "AM"]["scale"] = scale
            errorCalculation(amass, scale, x, y)

        def errorCalculation(amass, scale, x, y):
            global pcl, pcR, dcL, dcR, data

            if amass == "low":
                _df = pdLow
                dim = 0
            elif amass == "med":
                _df = pdMed
                dim = 1
            elif amass == "high":
                _df = pdHigh
                dim = 2

            flag = data["flag"]
            areaLeft = cAr.getArea("left")
            areaRight = cAr.getArea("right")
            scoreL = 1000000
            scoreR = 1000000
            line = np.linspace(0, 100, 101)

            df = _df[_df[flag] == 1]
            knMax = int(knVal.get())
            ktMax = int(ktVal.get())

            # get/calculate  boundaries if ktMax or knMax are not NA. (i,e. data frame is not empty)
            # if (ktMax != "NA") or (knMax != "NA"):

            if (np.sum(data[amass + "AM"]["activeLBound"]) < 2):

                # Let's find left boundary of active points
                actFrame = dframe[dframe[flag] == 1]
                activeLBound = []
                eCount = 1
                for yp in range(0, int(knMax) + 1):
                    xpts = list(actFrame[actFrame[y] == yp][x])
                    if len(xpts) > 0:
                        activeLBound.append(min(xpts))
                    else:
                        if yp == 0:
                            activeLBound.append(0)
                        else:
                            activeLBound.append("fill")  # +str(eCount))
                            eCount += 1
                indices = [i for i, v in enumerate(activeLBound) if v == "fill"]
                # Now filling empty values with average
                for i in indices:
                    nexti = 0
                    prev = 0
                    prev = activeLBound[i - 1]
                    for j in range(i + 1, int(knMax) + 1):
                        if activeLBound[j] != "fill":
                            nexti = activeLBound[j]
                            break
                    activeLBound[i] = (int(prev) + int(nexti)) / 2

                # Now find right boundary of active points
                activeRBound = []
                eCount = 1
                for yp in range(0, int(knMax) + 1):
                    xpts = list(actFrame[actFrame[y] == yp][x])
                    if len(xpts) > 0:
                        if max(xpts) <= ktMax:
                            activeRBound.append(max(xpts))
                        else:
                            while max(xpts) > ktMax:
                                xpts.remove(max(xpts))
                                if len(xpts) == 0:
                                    activeRBound.append(ktMax)
                                    break
                            if len(xpts) > 0:
                                activeRBound.append(max(xpts))
                    else:
                        if yp == 0:
                            activeRBound.append(0)
                        else:
                            activeRBound.append("fill")  # +str(eCount))
                            eCount += 1
                indices = [i for i, v in enumerate(activeRBound) if v == "fill"]
                # Now filling empty values with average
                activeRBound[-1] = ktMax

                for i in indices:
                    nexti = 0
                    prev = 0
                    prev = activeRBound[i - 1]
                    for j in range(i + 1, int(knMax) + 1):
                        if activeRBound[j] != "fill":
                            nexti = activeRBound[j]
                            break
                    activeRBound[i] = (int(prev) + int(nexti)) / 2
                    if activeRBound[i] > ktMax:
                        activeRBound[i] = ktMax
            else:
                activeLBound = data[amass + "AM"]["activeLBound"]
                activeRBound = data[amass + "AM"]["activeRBound"]

            for curve in range(0, 6):
                for position in range(1, 21):
                    shift = ((position - 1) * 2.5)
                    dataCountL = 0
                    dataCountR = 0
                    # Find the curve with shift and set negative values as 0
                    pointsL = ut.curveLeft[curve]
                    pointsL = [(point) + shift for point in pointsL]
                    zeroesL = [0 for point in pointsL if point < 0]
                    pointsL = zeroesL + pointsL[len(zeroesL):]

                    # Find the right curve with shift
                    if curve < 5:
                        pointsR = ut.curveRight[curve]
                        pointsR = [(point) + shift for point in pointsR]

                    # check if dcl, pcl arrays have data or they are empty
                    if np.sum(dcL[dim, :, :]) < 1:
                        for yp in range(0, int(knMax) + 1):
                            activeCountL = list(df[df[y] == yp][x])
                            activeCountL = len([xp for xp in activeCountL if xp < (pointsL[yp])])
                            dataCountL = dataCountL + activeCountL

                            if curve < 5:
                                activeCountR = list(df[df[y] == yp][x])
                                activeCountR = len([xp for xp in activeCountR if xp > (pointsR[yp])])
                                dataCountR = dataCountR + activeCountR

                        pixCountL = np.sum(abs(np.array(pointsL[:knMax + 1]) - np.array(activeLBound)))
                        pcL[dim, curve, position - 1] = pixCountL  # / scale
                        dcL[dim, curve, position - 1] = dataCountL  # * scale

                        if curve < 5:
                            pixCountR = np.sum(abs(np.array(pointsR[:knMax + 1]) - np.array(activeRBound)))
                            pcR[dim, curve, position - 1] = pixCountR  # / scale
                            dcR[dim, curve, position - 1] = dataCountR  # * scale

                    pixCountL = pcL[dim, curve, position - 1] / scale
                    pixCountL = pixCountL / (areaLeft.iloc[int(knMax) - 1][(curve * 20) + position])

                    dataCountL = dcL[dim, curve, position - 1] * scale
                    lcount = dcL[dim, curve, position - 1]
                    dataCountL = dataCountL / len(df)

                    scoreNowL = pixCountL + dataCountL
                    # print("LEFT - previous score was:",scoreL, "and new is:", scoreNowL, "and out points are: ", lcount)

                    if scoreNowL < scoreL:
                        scoreL = scoreNowL
                        shapeL = curve + 1
                        positionL = position
                        outL = lcount

                    if curve < 5:
                        pixCountR = pcR[dim, curve, position - 1] / scale
                        pixCountR = pixCountR / (areaRight.iloc[int(knMax) - 1][(curve * 20) + position])
                        dataCountR = dcR[dim, curve, position - 1] * scale
                        rcount = dcR[dim, curve, position - 1]
                        dataCountR = dataCountR / len(df)
                        scoreNowR = pixCountR + dataCountR
                        if scoreNowR < scoreR:
                            scoreR = scoreNowR
                            shapeR = curve + 1
                            positionR = position
                            outR = rcount
                    print("curve : ", curve, " position : ", position, " score left ", scoreNowL, "score right ",
                          scoreNowR, " out left ", lcount, " out right ", rcount)

            # now updating Data dictionary
            data[amass + "AM"]["shapeLeft"] = shapeL
            data[amass + "AM"]["posLeft"] = positionL
            data[amass + "AM"]["shapeRight"] = shapeR
            data[amass + "AM"]["posRight"] = positionR

            leftB = list(ut.curveLeft[shapeL - 1])
            leftB = leftB[0:int(knMax)]  # get all the points of curve upto Ymax
            leftB = [(i + (2.5 * positionL)) for i in leftB]

            if leftB[-1] != int(ktMax):
                leftB.append(int(ktMax))
            # leftB.append(ktMax)

            # copy first value at 0th index
            leftB = [leftB[0], *leftB]

            # set 0 for negative values
            for n, i in enumerate(leftB):
                if int(i) < 0:
                    leftB[n] = 0

            rightB = list(ut.curveRight[shapeR - 1])
            rightB = rightB[0:int(knMax)]  # get all the points of curve upto Ymax
            rightB = [(i + (2.5 * positionR)) for i in rightB]
            rightB = [i for i in rightB if i <= int(ktMax)]
            if rightB[-1] != int(ktMax):
                rightB.append(int(ktMax))

            # copy first value at 0th index
            rightB = [rightB[0], *rightB]

            # set 0 for negative values
            for n, i in enumerate(rightB):
                if int(i) < 0:
                    rightB[n] = 0

            # count if points are above configured kn max
            upCount = dframe[dframe[flag] == 1]
            upCount = upCount[upCount[y] > int(knMax)]
            outUp = upCount.__len__()
            data[amass + "AM"]["lBound"] = leftB
            data[amass + "AM"]["rBound"] = rightB
            data[amass + "AM"]["In"] = len(dframe[dframe[flag] == 1]) - (outL + outR + outUp)
            data[amass + "AM"]["Active"] = len(dframe[dframe[flag] == 1])
            if data[amass + "AM"]["Active"] > 1:
                data[amass + "AM"]["Out"] = str(outL + outR + outUp) + " (" + str(round(
                    ((outL + outR + outUp) / data[amass + "AM"]["Active"]) * 100, 2)) + " %)"
            else:
                data[amass + "AM"]["Out"] = outL + outR + outUp
            data[amass + "AM"]["Ignored"] = len(dframe[dframe[flag] == 0])
            data[amass + "AM"]["Total"] = len(dframe)
            data[amass + "AM"]["Err_L"] = round((((outL) / data[amass + "AM"]["Active"]) * 100), 2)
            data[amass + "AM"]["Err_R"] = round((((outR) / data[amass + "AM"]["Active"]) * 100), 2)

            # Prepare left boundary
            yLB = list(line[0:knMax + 1]) + [knMax for point in line if point > knMax]
            shiftL = data[amass + 'AM']['posLeft'] * 2.5
            xLB = utills.curveLeft[data[amass + 'AM']['shapeLeft'] - 1]
            xLB = [point + shiftL for point in xLB]

            # copy first value at 0th index
            xLB = [xLB[0], *xLB]

            # replace the values greater than knmax-th value in curve with knmax-th value
            xLB = xLB[0:knMax + 1]
            xLB += [ktMax] * (len(line) - len(xLB))

            # Replace negative values with 0
            zeroesL = [0 for point in xLB if point < 0]
            xLB = zeroesL + xLB[len(zeroesL):]

            # Prepare right boundary
            yRB = list(line[0:knMax + 1]) + [knMax for point in line if point > knMax]
            shiftR = data[amass + 'AM']['posRight'] * 2.5
            xRB = utills.curveRight[data[amass + 'AM']['shapeRight'] - 1]
            xRB = [point + shiftR for point in xRB]
            # copy first value at 0th index
            xRB = [xRB[0], *xRB]
            # replace the values greater than knmax-th value in curve with knmax-th value
            xRB = xRB[0:ktMax + 1]
            xRB = [i for i in xRB if i <= ktMax]

            xRB += [xRB[-1]] * (len(line) - len(xRB))

            # update data dictionary with new boundaries and bounds(lBound and rBound)
            data[amass + 'AM']['xLB'] = xLB
            data[amass + 'AM']['yLB'] = yLB
            data[amass + "AM"]["lBound"] = xLB

            data[amass + 'AM']['xRB'] = xRB
            data[amass + 'AM']['yRB'] = yRB
            data[amass + "AM"]["rBound"] = xRB

            filtFrame = _df[_df[amass + "Exclude"] == 0]

            # now clear old boundaries and plot new one.
            plt.close('all')
            plotForEdit(amass, filtFrame, flag, x, y, titleString)

            # update main canvas plot
            plotGraph(filtFrame, amass, locationDict[amass], data["xAxis"], data["yAxis"], data["flag"])
            setStats()

        def close():
            data["editWinFlag"] = 0
            plt.close("all")
            editGraph.withdraw()

        heading = tk.Label(editGraph, text=header, font=(None, 20))
        heading.place(relx=0.01, rely=0.03, relwidth=0.98, relheight=0.1)

        StatCanvas = tk.Canvas(editGraph)
        StatCanvas.place(relx=0.10, rely=0.15, relwidth=0.50, relheight=0.25)
        ErrCanvas = tk.Canvas(StatCanvas)
        ErrCanvas.place(relx=0.5, rely=0.5, relwidth=0.5, relheight=0.5)

        editGraph.wm_geometry("400x500+500+250")
        editGraph.title(data["siteIdentifier"] + " " + "- " + amass.upper() + " - QCFIT")

        InLabel = tk.Label(StatCanvas, text="In", font=(None, 12), anchor="w")
        InLabel.place(relx=0.02, rely=0.01, relwidth=0.23, relheight=0.188)
        InVal = tk.Label(StatCanvas, text=inPoints, font=(None, 12), anchor="w")
        InVal.place(relx=0.26, rely=0.01, relwidth=0.20, relheight=0.188)

        OutLabel = tk.Label(StatCanvas, text="Out", font=(None, 12), anchor="w")
        OutLabel.place(relx=0.02, rely=0.198, relwidth=0.23, relheight=0.188)
        OutVal = tk.Label(StatCanvas, text=outPoints, font=(None, 12), anchor="w")
        OutVal.place(relx=0.26, rely=0.198, relwidth=0.40, relheight=0.188)

        ActiveLabel = tk.Label(StatCanvas, text="Active", font=(None, 12), anchor="w")
        ActiveLabel.place(relx=0.02, rely=0.396, relwidth=0.23, relheight=0.188)
        ActiveVal = tk.Label(StatCanvas, text=activePoints, font=(None, 12), anchor="w")
        ActiveVal.place(relx=0.26, rely=0.396, relwidth=0.20, relheight=0.188)

        IgnoredLabel = tk.Label(StatCanvas, text="Ignored", font=(None, 12), anchor="w")
        IgnoredLabel.place(relx=0.02, rely=0.594, relwidth=0.23, relheight=0.188)
        IgnoredVal = tk.Label(StatCanvas, text=ignoredPoints, font=(None, 12), anchor="w")
        IgnoredVal.place(relx=0.26, rely=0.594, relwidth=0.20, relheight=0.188)

        TotalLabel = tk.Label(StatCanvas, text="Total", font=(None, 12), anchor="w")
        TotalLabel.place(relx=0.02, rely=0.792, relwidth=0.23, relheight=0.188)
        TotalVal = tk.Label(StatCanvas, text=totalPoints, font=(None, 12), anchor="w")
        TotalVal.place(relx=0.26, rely=0.792, relwidth=0.20, relheight=0.188)

        # entries in error frame

        ErrL = tk.Label(ErrCanvas, text="Err(L):", font=(None, 12), anchor="w")
        ErrL.place(relx=0.02, rely=0.10, relwidth=0.40, relheight=0.35)
        ErrLVal = tk.Label(ErrCanvas, text=errL, font=(None, 12), anchor="w")
        ErrLVal.place(relx=0.47, rely=0.10, relwidth=0.31, relheight=0.35)
        ErrLper = tk.Label(ErrCanvas, text="%", font=(None, 12), anchor="w")
        ErrLper.place(relx=0.82, rely=0.10, relwidth=0.15, relheight=0.35)

        ErrR = tk.Label(ErrCanvas, text="Err(R):", font=(None, 12), anchor="w")
        ErrR.place(relx=0.02, rely=0.55, relwidth=0.40, relheight=0.35)
        ErrRVal = tk.Label(ErrCanvas, text=errR, font=(None, 12), anchor="w")
        ErrRVal.place(relx=0.47, rely=0.55, relwidth=0.31, relheight=0.35)
        ErrRper = tk.Label(ErrCanvas, text="%", font=(None, 12), anchor="w")
        ErrRper.place(relx=0.82, rely=0.55, relwidth=0.15, relheight=0.35)

        excludeButton = tk.Button(editGraph, text="Exclude", command=partial(exclude, amass, dframe, x, y))
        excludeButton.place(relx=0.1, rely=0.40, relwidth=0.20, relheight=0.1)
        excludeButton.config(state=tk.NORMAL)
        listButton = tk.Button(editGraph, text="List", command=partial(listPoints, amass, dframe, x, y))
        listButton.place(relx=0.4, rely=0.40, relwidth=0.20, relheight=0.1)
        resetButton = tk.Button(editGraph, text="Reset", command=partial(reset, dframe, amass, x, y))
        resetButton.place(relx=0.7, rely=0.40, relwidth=0.20, relheight=0.1)

        # frame for kn max and kt max adjustment controls
        kFrame = tk.Frame(editGraph, bg='grey')
        kFrame.place(relx=0.1, rely=0.51, relwidth=0.8, relheight=0.08)
        kCanvas = tk.Canvas(kFrame)
        kCanvas.place(relx=0.004, rely=0.022, relwidth=0.9925, relheight=0.95)

        knSpinVar = tk.IntVar()
        knLabel = tk.Label(kCanvas, text="Kn Max * 100", font=(None, 12))
        knLabel.place(relx=0.01, rely=0.2, relwidth=0.30, relheight=0.6)
        knVal = tk.Spinbox(kCanvas, from_=1, to=knMaxSpinVal, textvariable=knSpinVar,
                           command=partial(spinCalculation, amass, x, y))
        knVal.place(relx=0.32, rely=0.1, relwidth=0.17, relheight=0.8)
        knVal.delete(0, 'end')
        knVal.insert(0, int(data[amass + "AM"]["knMax"]))
        knVal.bind("<Return>", lambda event, a=amass: spinCalculation(a, x, y))

        ktSpinVar = tk.IntVar()
        ktLabel = tk.Label(kCanvas, text="Kt Max * 100", font=(None, 12))
        ktLabel.place(relx=0.51, rely=0.2, relwidth=0.30, relheight=0.6)
        ktVal = tk.Spinbox(kCanvas, from_=minKt, to=ktMaxSpinVal, textvariable=ktSpinVar,
                           command=partial(spinCalculation, amass))
        ktVal.place(relx=0.82, rely=0.1, relwidth=0.17, relheight=0.8)
        ktVal.delete(0, 'end')
        ktVal.insert(0, int(data[amass + "AM"]["ktMax"]))
        ktVal.bind("<Return>", lambda event, a=amass: spinCalculation(a, x, y))

        # frame for curve and shape adjustment controls
        boundFrame = tk.Frame(editGraph, bg='grey')
        boundFrame.place(relx=0.1, rely=0.61, relwidth=0.395, relheight=0.24)
        boundCanvas = tk.Canvas(boundFrame)
        boundCanvas.place(relx=0.005, rely=0.01, relwidth=0.987, relheight=0.98)

        # list for option menus
        curveL = [1, 2, 3, 4, 5, 6]
        curveR = [1, 2, 3, 4, 5]
        posit = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

        cLabel = tk.Label(boundCanvas, text="Curve", font=(None, 12), anchor="w")
        cLabel.place(relx=0.01, rely=0.3566, relwidth=0.32, relheight=0.2866)
        pLabel = tk.Label(boundCanvas, text="Position", font=(None, 12), anchor="w")
        pLabel.place(relx=0.01, rely=0.6632, relwidth=0.32, relheight=0.2866)
        lLabel = tk.Label(boundCanvas, text="Left", font=(None, 12))
        lLabel.place(relx=0.34, rely=0.05, relwidth=0.32, relheight=0.2866)
        rLabel = tk.Label(boundCanvas, text="Right", font=(None, 12))
        rLabel.place(relx=0.67, rely=0.05, relwidth=0.32, relheight=0.2866)

        cLVar = tk.IntVar(editGraph)
        cRVar = tk.IntVar(editGraph)
        pLVar = tk.IntVar(editGraph)
        pRVar = tk.IntVar(editGraph)

        cLOpt = tk.OptionMenu(boundCanvas, cLVar, *curveL, command=partial(reval, amass, x, y))
        cLOpt.place(relx=0.34, rely=0.3566, relwidth=0.32, relheight=0.2866)
        cLOpt.config(font=('Helvetica', 10))
        cLVar.set(int(data[amass + "AM"]["shapeLeft"]))

        cROpt = tk.OptionMenu(boundCanvas, cRVar, *curveR, command=partial(reval, amass, x, y))
        cROpt.place(relx=0.67, rely=0.3566, relwidth=0.32, relheight=0.2866)
        cROpt.config(font=('Helvetica', 10))
        cRVar.set(int(data[amass + "AM"]["shapeRight"]))

        pLOpt = tk.OptionMenu(boundCanvas, pLVar, *posit, command=partial(reval, amass, x, y))
        pLOpt.place(relx=0.335, rely=0.6632, relwidth=0.325, relheight=0.2866)
        pLOpt.config(font=('Helvetica', 10))
        pLVar.set(int(data[amass + "AM"]["posLeft"]))

        pROpt = tk.OptionMenu(boundCanvas, pRVar, *posit, command=partial(reval, amass, x, y))
        pROpt.place(relx=0.6653, rely=0.6632, relwidth=0.325, relheight=0.2866)
        pROpt.config(font=('Helvetica', 10))

        pRVar.set(int(data[amass + "AM"]["posRight"]))

        # frame for curve and shape (wide and narrow) adjustment controls
        wnFrame = tk.Frame(editGraph, bg='grey')
        wnFrame.place(relx=0.505, rely=0.61, relwidth=0.395, relheight=0.24)
        wnCanvas = tk.Canvas(wnFrame)
        wnCanvas.place(relx=0.005, rely=0.01, relwidth=0.987, relheight=0.98)

        lLabel = tk.Label(wnCanvas, text="Left", font=(None, 12), anchor="w")
        lLabel.place(relx=0.01, rely=0.05, relwidth=0.29, relheight=0.2866)
        bLabel = tk.Label(wnCanvas, text="Both", font=(None, 12), anchor="w")
        bLabel.place(relx=0.01, rely=0.3566, relwidth=0.29, relheight=0.2866)
        rLabel = tk.Label(wnCanvas, text="Right", font=(None, 12), anchor="w")
        rLabel.place(relx=0.01, rely=0.6632, relwidth=0.29, relheight=0.2866)

        wideL = tk.Button(wnCanvas, text="Wide", font=(None, 10), command=partial(wideLeft, amass, x, y))
        wideL.place(relx=0.3066, rely=0.05, relwidth=0.3066, relheight=0.2866)
        wideB = tk.Button(wnCanvas, text="Wide", font=(None, 10), command=partial(wideBoth, amass, x, y))
        wideB.place(relx=0.3066, rely=0.3566, relwidth=0.3066, relheight=0.2866)
        wideR = tk.Button(wnCanvas, text="Wide", font=(None, 10), command=partial(wideRight, amass, x, y))
        wideR.place(relx=0.3066, rely=0.6632, relwidth=0.3066, relheight=0.2866)

        narrowL = tk.Button(wnCanvas, text="Narrow", font=(None, 10), command=partial(narrowLeft, amass, x, y))
        narrowL.place(relx=0.6332, rely=0.05, relwidth=0.35, relheight=0.2866)
        narrowB = tk.Button(wnCanvas, text="Narrow", font=(None, 10), command=partial(narrowBoth, amass, x, y))
        narrowB.place(relx=0.6332, rely=0.3566, relwidth=0.35, relheight=0.2866)
        narrowR = tk.Button(wnCanvas, text="Narrow", font=(None, 10), command=partial(narrowRight, amass, x, y))
        narrowR.place(relx=0.6332, rely=0.6632, relwidth=0.35, relheight=0.2866)

        # frame for low Err and more Err adjustment controls
        errFrame = tk.Frame(editGraph, bg='grey')
        errFrame.place(relx=0.1, rely=0.87, relwidth=0.6, relheight=0.08)
        errCanvas = tk.Canvas(errFrame)
        errCanvas.place(relx=0.005, rely=0.022, relwidth=0.99, relheight=0.95)
        lessErr = tk.Button(errCanvas, text="Less Error", font=(None, 12), command=partial(lessErr, amass, x, y))
        lessErr.place(relx=0.04, rely=0.05, relwidth=0.42, relheight=0.9)

        errLevel = tk.Label(errCanvas, text="0")
        errLevel.place(relx=0.47, rely=0.05, relwidth=0.06, relheight=0.9)

        moreErr = tk.Button(errCanvas, text="More Error", font=(None, 12), command=partial(moreErr, amass, x, y))
        moreErr.place(relx=0.54, rely=0.05, relwidth=0.42, relheight=0.9)

        close = tk.Button(editGraph, text="Close", font=(None, 12), command=close)
        close.place(relx=0.72, rely=0.88, relwidth=0.18, relheight=0.07)

        editGraph.protocol("WM_DELETE_WINDOW", handleGraphCross)
        editGraph.iconbitmap('dataFiles/qcfit-icon.ico')
        editGraph.mainloop()


def setStats():
    # lowX.config(text=(data["xAxis"] + " Max"))
    lowXVal.config(text=(data["lowAM"]["ktMax"]))

    # lowY.config(text=(data["yAxis"] + " Max"))
    lowYVal.config(text=(data["lowAM"]["knMax"]))

    if lowXVal.cget("text") != 'NA':
        lowLeftVal.config(text=(str(data["lowAM"]["shapeLeft"]) + "," + str(data["lowAM"]["posLeft"])))
        lowRightVal.config(text=(str(data["lowAM"]["shapeRight"]) + "," + str(data["lowAM"]["posRight"])))

    lowInVal.config(text=(data["lowAM"]["In"]))
    lowOutVal.config(text=(data["lowAM"]["Out"]))
    lowActiveVal.config(text=(data["lowAM"]["Active"]))
    lowIgnoredVal.config(text=(data["lowAM"]["Ignored"]))
    lowTotalVal.config(text=(data["lowAM"]["Total"]))

    lowErrLVal.config(text=(round(data["lowAM"]["Err_L"], 2)))
    lowErrRVal.config(text=(round(data["lowAM"]["Err_R"], 2)))

    # medX.config(text=(data["xAxis"] + " Max"))
    medXVal.config(text=(data["medAM"]["ktMax"]))

    # medY.config(text=(data["yAxis"] + " Max"))
    medYVal.config(text=(data["medAM"]["knMax"]))

    if medXVal.cget("text") != 'NA':
        medLeftVal.config(text=(str(data["medAM"]["shapeLeft"]) + "," + str(data["medAM"]["posLeft"])))
        medRightVal.config(text=(str(data["medAM"]["shapeRight"]) + "," + str(data["medAM"]["posRight"])))

    medInVal.config(text=(data["medAM"]["In"]))
    medOutVal.config(text=(data["medAM"]["Out"]))
    medActiveVal.config(text=(data["medAM"]["Active"]))
    medIgnoredVal.config(text=(data["medAM"]["Ignored"]))
    medTotalVal.config(text=(data["medAM"]["Total"]))

    medErrLVal.config(text=(round(data["medAM"]["Err_L"], 2)))
    medErrRVal.config(text=(round(data["medAM"]["Err_R"], 2)))

    # highX.config(text=(data["xAxis"] + " Max"))
    highXVal.config(text=(data["highAM"]["ktMax"]))

    # highY.config(text=(data["yAxis"] + " Max"))
    highYVal.config(text=(data["highAM"]["knMax"]))

    if highXVal.cget("text") != 'NA':
        highLeftVal.config(text=(str(data["highAM"]["shapeLeft"]) + "," + str(data["highAM"]["posLeft"])))
        highRightVal.config(text=(str(data["highAM"]["shapeRight"]) + "," + str(data["highAM"]["posRight"])))

    highInVal.config(text=(data["highAM"]["In"]))
    highOutVal.config(text=(data["highAM"]["Out"]))
    highActiveVal.config(text=(data["highAM"]["Active"]))
    highIgnoredVal.config(text=(data["highAM"]["Ignored"]))
    highTotalVal.config(text=(data["highAM"]["Total"]))

    highErrLVal.config(text=(round(data["highAM"]["Err_L"], 2)))
    highErrRVal.config(text=(round(data["highAM"]["Err_R"], 2)))

    integTimeLabel.config(text="Integration Time (min): " + str(data["integration"]))


def resetStats():
    for am in ["low", "med", "high"]:
        data[am + "AM"]['shapeLeft'] = 0
        data[am + "AM"]['shapeRight'] = 0
        data[am + "AM"]['posLeft'] = 0
        data[am + "AM"]['posRight'] = 0
        data[am + "AM"]['In'] = 0
        data[am + "AM"]['Out'] = 0
        data[am + "AM"]['Active'] = 0
        data[am + "AM"]['Ignored'] = 0
        data[am + "AM"]['Total'] = 0
        data[am + "AM"]['Err_L'] = 0
        data[am + "AM"]['Err_R'] = 0
    setStats()


def plotUpdateThroughkspace(*args):
    global pdLow, pdMed, pdHigh, dFlag
    if iterCount > 0:
        dFlag = 2
        denseOnOff.select()

    data["plane"] = planeVar.get()
    data["month"] = monVar.get()
    data["year"] = yearVar.get()

    # identify axes based on kspaces
    if data["plane"] == 1:
        flag = data["flag"] = "activeKtKn"
        xAxis = data["xAxis"] = "KT"
        yAxis = data["yAxis"] = "KN"
    elif data["plane"] == 2:
        flag = data["flag"] = "activeKtKd"
        xAxis = data["xAxis"] = "KT"
        yAxis = data["yAxis"] = "KN1"
    elif data["plane"] == 3:
        flag = data["flag"] = "activeKnKd"
        xAxis = data["xAxis"] = "KT1"
        yAxis = data["yAxis"] = "KN"

    airmasses = ["low", "med", "high"]
    dataFrames = [pdLow, pdMed, pdHigh]
    location = [lowCanvas, medCanvas, highCanvas]

    for amass, dframe, location in zip(airmasses, dataFrames, location):
        plotGraph(dframe, amass, location, xAxis, yAxis, flag)
        Kn = data[amass + "AM"]["knMax"]
        outL = 0
        outR = 0
        if Kn != "NA":
            for y in range(0, Kn + 1):
                countL = list(dframe[dframe[yAxis] == y][xAxis])
                countL = [x for x in countL if x < data[amass + "AM"]["xLB"][y]]
                outL = outL + len(countL)
                countR = list(dframe[dframe[yAxis] == y][xAxis])
                countR = [x for x in countR if x > data[amass + "AM"]["xRB"][y]]
                outR = outR + len(countR)
                # print("at y = ", y, "  ", "out left ", outL, "listL",
                # list(filterData[filterData["KN"] == y]["KT"]), "curvePoint", data[amass+"AM"]["xLB"][y], " out right ",
                # outR)

            # count if points are above configured kn max
            upCount = dframe[dframe[flag] == 1]
            upCount = upCount[upCount[yAxis] > Kn]
            outUp = upCount.__len__()

            # updating data dictionary
            data[amass + "AM"]["In"] = len(dframe[dframe[flag] == 1]) - (outL + outR + outUp)
            data[amass + "AM"]["Active"] = len(dframe[dframe[flag] == 1])
            if data[amass + "AM"]["Active"] > 1:
                data[amass + "AM"]["Out"] = str(outL + outR + outUp) + " (" + str(round(
                    ((outL + outR + outUp) / data[amass + "AM"]["Active"]) * 100, 2)) + " %)"
            else:
                data[amass + "AM"]["Out"] = outL + outR + outUp
            data[amass + "AM"]["Ignored"] = len(dframe[dframe[flag] == 0])
            data[amass + "AM"]["Total"] = len(dframe)

            if outL + outR + outUp > len(dframe):
                data[amass + "AM"]["Out"] = str(len(dframe)) + " (" + str(round(
                    ((len(dframe)) / data[amass + "AM"]["Active"]) * 100, 2)) + " %)"

            if data[amass + "AM"]["In"] < 0:
                data[amass + "AM"]["In"] = 0

            if data[amass + "AM"]["Active"] > 1:
                data[amass + "AM"]["Err_L"] = round((((outL) / data[amass + "AM"]["Active"]) * 100), 2)
                data[amass + "AM"]["Err_R"] = round((((outR) / data[amass + "AM"]["Active"]) * 100), 2)

    setStats()


def plotByYear(*args):
    global pdLow, pdMed, pdHigh, iterCount, dFlag
    if iterCount > 0:
        dFlag = 2
        denseOnOff.select()
    if iterCount > 0:
        data["plane"] = planeVar.get()
        data["month"] = monVar.get()
        data["year"] = yearVar.get()

        if data["plane"] == 1:
            flag = "activeKtKn"
            xAxis = data["xAxis"] = "KT"
            yAxis = data["yAxis"] = "KN"
        elif data["plane"] == 2:
            flag = "activeKtKd"
            xAxis = data["xAxis"] = "KT"
            yAxis = data["yAxis"] = "KN1"
        elif data["plane"] == 3:
            flag = "activeKnKd"
            xAxis = data["xAxis"] = "KT1"
            yAxis = data["yAxis"] = "KN"

        airmasses = ["low", "med", "high"]
        dataFrames = [pdLow, pdMed, pdHigh]
        location = [lowCanvas, medCanvas, highCanvas]

        for amass, dframe, location in zip(airmasses, dataFrames, location):
            year = yearVar.get()
            if year == "All":
                thisYearData = dframe
            else:
                year = int(yearVar.get())
                thisYearData = dframe[dframe["year"] == year]

            if len(thisYearData) < 1:
                continue
            else:

                if len(dframe) > 0:

                    dframe = dframe.copy()
                    dframe["outFlag"] = 0
                    setOutFlag(dframe, xAxis, yAxis, amass, "left")
                    setOutFlag(dframe, xAxis, yAxis, amass, "right")

                    active_mask = dframe[flag] == 1
                    out_mask = dframe["outFlag"] == 1
                    inact_mask = dframe[flag] == 0

                    xAct = dframe.loc[active_mask & (~out_mask), xAxis]
                    yAct = dframe.loc[active_mask & (~out_mask), yAxis]
                    xActOut = dframe.loc[active_mask & out_mask, xAxis]
                    yActOut = dframe.loc[active_mask & out_mask, yAxis]
                    xInact = dframe.loc[inact_mask, xAxis]
                    yInact = dframe.loc[inact_mask, yAxis]

                    xLB = data[amass + "AM"]["xLB"]
                    xRB = data[amass + "AM"]["xRB"]
                    yLB = data[amass + "AM"]["yLB"]
                    yRB = data[amass + "AM"]["yRB"]

                    matplotlib.use("TKAgg")
                    style.use("ggplot")
                    f = Figure(figsize=(3, 2.5), dpi=100)
                    a = f.add_subplot(111)
                    a.clear()
                    line = np.linspace(0, 100, 101)
                    a.scatter(xInact, yInact, color='gray', marker=".")
                    a.scatter(xAct, yAct, color='orangered', marker=".")
                    if len(xActOut) > 0:
                        a.scatter(xActOut, yActOut, color='firebrick', marker=".")

                    if year != "All":
                        thisYearX = thisYearData[xAxis]
                        thisYearY = thisYearData[yAxis]
                        a.scatter(thisYearX, thisYearY, color='cyan', marker=".")
                    a.set_xlim([0, 100])
                    a.set_ylim([0, 100])
                    a.plot(line, line, color="black")
                    a.plot(xLB, yLB, color="green")
                    a.plot(xRB, yRB, color="green")

            canvas = FigureCanvasTkAgg(f, master=location)
            canvas.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1)
            canvas.draw()
            if location == lowCanvas:
                lowButton = tk.Button(location, text="Configure", font=(None, 10), command=lowConfig)
                lowButton.place(relx=.75, rely=0.015, relwidth=0.22, relheight=0.1)
            elif location == medCanvas:
                medButton = tk.Button(location, text="Configure", font=(None, 10), command=medConfig)
                medButton.place(relx=.75, rely=0.015, relwidth=0.22, relheight=0.1)
            elif location == highCanvas:
                highButton = tk.Button(location, text="Configure", font=(None, 10), command=highConfig)
                highButton.place(relx=.75, rely=0.015, relwidth=0.22, relheight=0.1)


def animatePlots():
    global data, pdLow, pdMed, pdHigh
    current = data["plane"]
    planeVar.set(1)

    time.sleep(0.5)
    planeVar.set(2)

    time.sleep(0.5)

    planeVar.set(3)

    time.sleep(0.5)
    planeVar.set(current)


def disable(childList):
    for child in childList:
        child.configure(state=tk.DISABLED)


def enable(childList):
    for child in childList:
        child.configure(state=tk.NORMAL)


def compFilter():
    global data
    # update threshhold value
    data["threshold"] = threshVar.get()

    plotUpdateThroughMonth()


def freqPlot():
    global data, ip

    loMed = pd.concat([pdLow, pdMed], ignore_index=True)
    dat = pd.concat([loMed, pdHigh], ignore_index=True)
    dat["bin"] = 0
    dat["freqStatus"] = dat["lowExclude"] + dat["medExclude"] + dat["highExclude"]

    fData = dat[dat["month"] == ((monVar.get()).upper())[:3]][dat["freqStatus"] == 0]
    if data["plane"] == 1:
        flag = data["flag"] = "activeKtKn"
    elif data["plane"] == 2:
        flag = data["flag"] = "activeKtKd"
    elif data["plane"] == 3:
        flag = data["flag"] = "activeKnKd"

    fData.loc[fData[flag] == 1, 'bin'] = [min(max(int(i * 100), -15), 15) for i in
                                          (fData[fData[flag] == 1]["residual"])]
    freq = list(fData[fData[flag] == 1]["bin"])

    matplotlib.use("TKAgg")
    style.use("ggplot")
    f = Figure(figsize=(3, 2.5), dpi=100)
    a = f.add_subplot(111)
    a.clear()
    # a.tick_params(axis='x', colors='black')
    # a.tick_params(axis='y', colors='black')
    a.hist(freq, bins=31, range=(-15, 15))
    canvas = FigureCanvasTkAgg(f, master=histoCanvas)
    canvas.get_tk_widget().place(relx=-0.12, rely=0.05, relwidth=1.2, relheight=0.9)
    canvas.draw()
    canvas.mpl_connect('button_press_event', freqZoomed)


def freqZoomed(event):
    if event.dblclick:
        global data, ip, pdLow, pdMed, pdHigh

        plt.close('all')

        loMed = pd.concat([pdLow, pdMed], ignore_index=True)
        dat = pd.concat([loMed, pdHigh], ignore_index=True)
        dat["bin"] = 0
        fData = dat[dat["month"] == ((monVar.get()).upper())[:3]]

        if data["plane"] == 1:
            flag = data["flag"] = "activeKtKn"
        elif data["plane"] == 2:
            flag = data["flag"] = "activeKtKd"
        elif data["plane"] == 3:
            flag = data["flag"] = "activeKnKd"
        freq = []

        fData.loc[fData[flag] == 1, 'bin'] = [min(max(int(i * 100), -15), 15) for i in
                                              (fData[fData[flag] == 1]["residual"])]
        freq = list(fData[fData[flag] == 1]["bin"])

        matplotlib.use("TKAgg")
        style.use("ggplot")
        f = plt.figure(figsize=(3, 2.5), dpi=100)
        ax = f.add_subplot(111)
        ax.clear()
        f.canvas.set_window_title("QCFIT")

        titleFont = {'family': 'serif', 'color': 'black', 'weight': 'heavy', 'size': 25}
        labelFont = {'family': 'serif', 'color': 'red', 'weight': 'normal', 'size': 12}

        plt.suptitle(" 3-Component Error Frequency Distribution", fontdict=titleFont)
        plt.xlabel("Kt-Kn-Kd", fontdict=labelFont)
        plt.tick_params(axis='x', colors='black')
        plt.ylabel("Frequency", fontdict=labelFont)
        plt.tick_params(axis='y', colors='black')
        plt.tick_params(axis='x', colors='black')

        plt.hist(freq, bins=31, range=(-15, 15), color="grey")
        plt.tick_params(axis='y', colors='black')
        plt.show(block=False)
        plt.xlim(-15, 15)

        pLow = fData[fData[flag] == 1][fData["NAM"] == 1]
        if len(pLow) > 0:
            lowMean = list(pLow["bin"])
            lowMean = [int(i) for i in lowMean]
            lowMean = [sum(lowMean) / len(lowMean)]
            lowMean = lowMean * 20
        else:
            lowMean = [0] * 20
        pMed = fData[fData[flag] == 1][fData["NAM"] == 2]
        if len(pMed) > 0:
            medMean = list(pMed["bin"])
            medMean = [int(i) for i in medMean]
            medMean = [sum(medMean) / len(medMean)]
            medMean = medMean * 30
        else:
            medMean = [0] * 30
        pHigh = fData[fData[flag] == 1][fData["NAM"] == 3]
        if len(pHigh) > 0:
            highMean = list(pHigh["bin"])
            highMean = [int(i) for i in highMean]
            highMean = [sum(highMean) / len(highMean)]
            highMean = highMean * 40
        else:
            highMean = [0] * 40

        plt.hist((lowMean), label="Low Airmass", rwidth=1, color='red')
        plt.hist((medMean), label="Medium Airmass", color='green')
        plt.hist((highMean), label="High Airmass", color='blue')
        plt.legend()
        mngr = plt.get_current_fig_manager()
        mngr.window.wm_iconbitmap("dataFiles/qcfit-icon.ico")


def density(*args):
    global ip, pdLow, pdMed, pdHigh, data, dFlag, iterCount

    if iterCount < 1:
        return
    if dFlag == 2:  # 2 means new plot is invoked through kspace, month chnage or year change.
        dFlag = 0
        return

    if data["plane"] == 1:
        flag = "activeKtKn"
        x = "KT"
        y = "KN"
    elif data["plane"] == 2:
        flag = "activeKtKd"
        x = "KT"
        y = "KN1"
    elif data["plane"] == 3:
        flag = "activeKnKd"
        x = "KT1"
        y = "KN"
    bin1Label.config(text="----")
    bin2Label.config(text="----")
    bin3Label.config(text="----")
    bin4Label.config(text="----")
    bin5Label.config(text="----")

    pdLow = pdLow.copy()
    pdMed = pdMed.copy()
    pdHigh = pdHigh.copy()

    # make sure merges dont make any definition change in data frame is yes revert

    lastIndex = list(pdLow.columns).index("bin")
    if (pdLow.shape[1] > lastIndex + 1):
        pdLow = pdLow.iloc[:, :lastIndex + 1].copy()

    lastIndex = list(pdMed.columns).index("bin")
    if (pdMed.shape[1] > lastIndex + 1):
        pdMed = pdMed.iloc[:, :lastIndex + 1].copy()

    lastIndex = list(pdHigh.columns).index("bin")
    if (pdHigh.shape[1] > lastIndex + 1):
        pdHigh = pdHigh.iloc[:, :lastIndex + 1].copy()

    pdLow.loc[(pdLow["NAM"] == 1), "ldID"] = "ldID" + (pdLow[x].map(int)).map(str) + (pdLow[y].map(int)).map(str) + \
                                             pdLow["month"] + pdLow[flag].map(str) + str(1)
    pdLow["density1"] = pdLow["ldID"].map(pdLow['ldID'].value_counts())

    pdMed.loc[(pdMed["NAM"] == 2), "mdID"] = "mdID" + (pdMed[x].map(int)).map(str) + (pdMed[y].map(int)).map(str) + \
                                             pdMed["month"] + pdMed[flag].map(str) + str(2)
    pdMed["density2"] = pdMed["mdID"].map(pdMed['mdID'].value_counts())
    pdHigh.loc[(pdHigh["NAM"] == 3), "hdID"] = "hdID" + (pdHigh[x].map(int)).map(str) + (pdHigh[y].map(int)).map(
        str) + pdHigh["month"] + pdHigh[flag].map(str) + str(3)
    pdHigh["density3"] = pdHigh["hdID"].map(pdHigh['hdID'].value_counts())

    month_key = ((monVar.get()).upper())[:3]
    lFilt = pdLow.loc[(pdLow["NAM"] == 1) & (pdLow["lowExclude"] == 0) & (pdLow["month"] == month_key) & (pdLow[flag] == 1)]
    mFilt = pdMed.loc[(pdMed["NAM"] == 2) & (pdMed["medExclude"] == 0) & (pdMed["month"] == month_key) & (pdMed[flag] == 1)]
    hFilt = pdHigh.loc[(pdHigh["NAM"] == 3) & (pdHigh["highExclude"] == 0) & (pdHigh["month"] == month_key) & (pdHigh[flag] == 1)]

    lDF = lFilt.filter(["ldID", "density1"], axis=1)
    lDF.columns = ["id", "density"]
    mDF = mFilt.filter(["mdID", "density2"], axis=1)
    mDF.columns = ["id", "density"]
    hDF = hFilt.filter(["hdID", "density3"], axis=1)
    hDF.columns = ["id", "density"]
    densDF = pd.concat([lDF, mDF, hDF])

    densityData = pd.DataFrame({"density": list(set(densDF["density"]))})
    densityData["frequency"] = 0
    densityData["densBin"] = 0
    # find frequency
    for d in densityData["density"]:
        densityData.loc[(densityData["density"] == d), "frequency"] = len(densDF[densDF["density"] == d])

    # create density and bin columns in pd frames:
    pdLow["outFlag"] = pd.Series(0, index=pdLow.index, dtype="int64")
    pdMed["outFlag"] = pd.Series(0, index=pdMed.index, dtype="int64")
    pdHigh["outFlag"] = pd.Series(0, index=pdHigh.index, dtype="int64")

    if densVar.get() == 1:
        expEntry.configure(state=tk.DISABLED)
        densityData["densBin"] = 1
        densDF = pd.merge(densDF, densityData)  # put bin data in densDF

        """for d in (list(densDF["id"])):
            if d[:2] == "ld":
                pdLow.loc[(pdLow["ldID"] == d), "density"] = list(densDF[densDF["id"] == d]["density"])[0]
                pdLow["densBin"] = 1
            elif d[:2] == "md":
                pdMed.loc[(pdMed["mdID"] == d), "density"] = list(densDF[densDF["id"] == d]["density"])[0]
                pdMed["densBin"] = 1
            elif d[:2] == "hd":
                pdHigh["densBin"] = 1
                pdHigh.loc[(pdHigh["hdID"] == d), "density"] = list(densDF[densDF["id"] == d]["density"])[0] """
        pdLow = pdLow.merge(densDF, left_on="ldID", right_on="id", how='left', indicator="ind")  # put bin data in df
        pdLow = pdLow.drop_duplicates()
        pdMed = pdMed.merge(densDF, left_on="mdID", right_on="id", how='left', indicator="ind")  # put bin data in df
        pdMed = pdMed.drop_duplicates()
        pdHigh = pdHigh.merge(densDF, left_on="hdID", right_on="id", how='left',
                              indicator="ind")  # put bin data in df"""
        pdHigh = pdHigh.drop_duplicates()

    if densVar.get() == 2:  # Equal frequency
        dFlag = 1
        expEntry.configure(state=tk.DISABLED)

        densityData["freq%"] = densityData["frequency"] / sum(densityData["frequency"])
        densityData = densityData.sort_values(by=['density'])
        densityData["cumulative"] = densityData['freq%'].cumsum()
        densityData.iloc[len(densityData) - 1, 4] = 1
        # Allocating bins
        densityData.loc[(densityData["cumulative"] <= 1), "densBin"] = 5
        densityData.loc[(densityData["cumulative"] < .8), "densBin"] = 4
        densityData.loc[(densityData["cumulative"] < .6), "densBin"] = 3
        densityData.loc[(densityData["cumulative"] < .4), "densBin"] = 2
        densityData.loc[(densityData["cumulative"] < .2), "densBin"] = 1

        # check if data is allocated to first bin if not then change the lowest bin to first bin

        if densityData["densBin"].min() != 1:
            minDens = densityData["density"].min()
            densityData.loc[(densityData["density"] == minDens), "densBin"] = 1

        densDF = pd.merge(densDF, densityData)  # put bin data in densDF

        """for d in (list(densDF["id"])):
            if d[:2]=="ld":
                pdLow.loc[(pdLow["ldID"]== d), "density"] = list(densDF[densDF["id"]==d]["density"])[0]
                pdLow.loc[(pdLow["ldID"] == d), "densBin"] = list(densDF[densDF["id"] == d]["densBin"])[0]
            elif d[:2] == "md":
                pdMed.loc[(pdMed["mdID"] == d), "densBin"] = list(densDF[densDF["id"] == d]["densBin"])[0]
                pdMed.loc[(pdMed["mdID"] == d), "density"] = list(densDF[densDF["id"] == d]["density"])[0]
            elif d[:2] == "hd":
                pdHigh.loc[(pdHigh["hdID"] == d), "densBin"] = list(densDF[densDF["id"] == d]["densBin"])[0]
                pdHigh.loc[(pdHigh["hdID"] == d), "density"] = list(densDF[densDF["id"] == d]["density"])[0]"""

        pdLow = pdLow.merge(densDF, left_on="ldID", right_on="id", how='left', indicator="ind")  # put bin data in df
        pdLow = pdLow.drop_duplicates()
        pdMed = pdMed.merge(densDF, left_on="mdID", right_on="id", how='left', indicator="ind")  # put bin data in df
        pdMed = pdMed.drop_duplicates()
        pdHigh = pdHigh.merge(densDF, left_on="hdID", right_on="id", how='left',
                              indicator="ind")  # put bin data in df"""
        pdHigh = pdHigh.drop_duplicates()

    if densVar.get() == 3:
        dFlag = 1
        expEntry.configure(state=tk.DISABLED)
        densityData["densBin"] = ((((densityData["density"] - densityData["density"].min()) / (
                densityData["density"].max() - densityData["density"].min())) * 5) + 1).map(int)
        densityData.loc[(densityData["densBin"] > 5), "densBin"] = 5

        densDF = pd.merge(densDF, densityData)  # put bin data in densDF
        """
        for d in (list(densDF["id"])):
            if d[:2] == "ld":
                pdLow.loc[(pdLow["ldID"] == d), "density"] = list(densDF[densDF["id"] == d]["density"])[0]
                pdLow.loc[(pdLow["ldID"] == d), "densBin"] = list(densDF[densDF["id"] == d]["densBin"])[0]
            elif d[:2] == "md":
                pdMed.loc[(pdMed["mdID"] == d), "densBin"] = list(densDF[densDF["id"] == d]["densBin"])[0]
                pdMed.loc[(pdMed["mdID"] == d), "density"] = list(densDF[densDF["id"] == d]["density"])[0]
            elif d[:2] == "hd":
                pdHigh.loc[(pdHigh["hdID"] == d), "densBin"] = list(densDF[densDF["id"] == d]["densBin"])[0]
                pdHigh.loc[(pdHigh["hdID"] == d), "density"] = list(densDF[densDF["id"] == d]["density"])[0]

        """

        pdLow = pdLow.merge(densDF, left_on="ldID", right_on="id", how='left', indicator="ind")  # put bin data in df
        pdLow = pdLow.drop_duplicates()
        pdMed = pdMed.merge(densDF, left_on="mdID", right_on="id", how='left', indicator="ind")  # put bin data in df
        pdMed = pdMed.drop_duplicates()
        pdHigh = pdHigh.merge(densDF, left_on="hdID", right_on="id", how='left',
                              indicator="ind")  # put bin data in df"""
        pdHigh = pdHigh.drop_duplicates()

    if densVar.get() == 4:
        dFlag = 1
        expEntry.configure(state=tk.NORMAL)
        factor = int(float(expEntry.get()))
        binRatios = []
        for i in range(0, 5):
            binRatios.append(1 / pow(factor, 4 - i))
        densityData["ratio"] = ((densityData["density"] - densityData["density"].min()) / (
                densityData["density"].max() - densityData["density"].min()))
        densityData.loc[(densityData["ratio"] <= binRatios[4]), "densBin"] = 5
        densityData.loc[(densityData["ratio"] < binRatios[3]), "densBin"] = 4
        densityData.loc[(densityData["ratio"] < binRatios[2]), "densBin"] = 3
        densityData.loc[(densityData["ratio"] < binRatios[1]), "densBin"] = 2
        densityData.loc[(densityData["ratio"] < binRatios[0]), "densBin"] = 1

        if densityData["densBin"].min() != 1:
            minDens = densityData["density"].min()
            densityData.loc[(densityData["density"] == minDens), "densBin"] = 1

        densDF = pd.merge(densDF, densityData)  # put bin data in densDF

        """for d in (list(densDF["id"])):
            if d[:2] == "ld":
                pdLow.loc[(pdLow["ldID"] == d), "density"] = list(densDF[densDF["id"] == d]["density"])[0]
                pdLow.loc[(pdLow["ldID"] == d), "densBin"] = list(densDF[densDF["id"] == d]["densBin"])[0]
            elif d[:2] == "md":
                pdMed.loc[(pdMed["mdID"] == d), "densBin"] = list(densDF[densDF["id"] == d]["densBin"])[0]
                pdMed.loc[(pdMed["mdID"] == d), "density"] = list(densDF[densDF["id"] == d]["density"])[0]
            elif d[:2] == "hd":
                pdHigh.loc[(pdHigh["hdID"] == d), "densBin"] = list(densDF[densDF["id"] == d]["densBin"])[0]
                pdHigh.loc[(pdHigh["hdID"] == d), "density"] = list(densDF[densDF["id"] == d]["density"])[0]"""

        pdLow = pdLow.merge(densDF, left_on="ldID", right_on="id", how='left', indicator="ind")  # put bin data in df
        pdLow = pdLow.drop_duplicates()
        pdMed = pdMed.merge(densDF, left_on="mdID", right_on="id", how='left', indicator="ind")  # put bin data in df
        pdMed = pdMed.drop_duplicates()
        pdHigh = pdHigh.merge(densDF, left_on="hdID", right_on="id", how='left',
                              indicator="ind")  # put bin data in df"""
        pdHigh = pdHigh.drop_duplicates()

    # let's identify whether the point is inside boundary or outside.
    # for left

    setOutFlag(pdLow, x, y, "low", "left")
    setOutFlag(pdLow, x, y, "low", "right")
    setOutFlag(pdMed, x, y, "med", "left")
    setOutFlag(pdMed, x, y, "med", "right")
    setOutFlag(pdHigh, x, y, "high", "left")
    setOutFlag(pdHigh, x, y, "high", "right")

    color3 = tk.Frame(densityColorCanvas, highlightbackground="black", highlightcolor="black", bg="darkorange1",
                      highlightthickness=1, width=100, height=100, bd=0)
    color3.place(relx=0.40, rely=0.15, relwidth=0.03, relheight=0.7)
    color4 = tk.Frame(densityColorCanvas, highlightbackground="black", highlightcolor="black", bg="darkorange3",
                      highlightthickness=1, width=100, height=100, bd=0)
    color4.place(relx=0.43, rely=0.15, relwidth=0.03, relheight=0.7)

    color5 = tk.Frame(densityColorCanvas, highlightbackground="black", highlightcolor="black", bg="orange",
                      highlightthickness=1, width=100, height=100, bd=0)
    color5.place(relx=0.55, rely=0.15, relwidth=0.03, relheight=0.7)
    color6 = tk.Frame(densityColorCanvas, highlightbackground="black", highlightcolor="black", bg="peru",
                      highlightthickness=1, width=100, height=100, bd=0)
    color6.place(relx=0.58, rely=0.15, relwidth=0.03, relheight=0.7)

    color7 = tk.Frame(densityColorCanvas, highlightbackground="black", highlightcolor="black", bg="gold",
                      highlightthickness=1, width=100, height=100, bd=0)
    color7.place(relx=0.70, rely=0.15, relwidth=0.03, relheight=0.7)
    color8 = tk.Frame(densityColorCanvas, highlightbackground="black", highlightcolor="black", bg="goldenrod",
                      highlightthickness=1, width=100, height=100, bd=0)
    color8.place(relx=0.73, rely=0.15, relwidth=0.03, relheight=0.7)

    color9 = tk.Frame(densityColorCanvas, highlightbackground="black", highlightcolor="black", bg="yellow",
                      highlightthickness=1, width=100, height=100, bd=0)
    color9.place(relx=0.85, rely=0.15, relwidth=0.03, relheight=0.7)
    color10 = tk.Frame(densityColorCanvas, highlightbackground="black", highlightcolor="black", bg="khaki",
                       highlightthickness=1, width=100, height=100, bd=0)
    color10.place(relx=0.88, rely=0.15, relwidth=0.03, relheight=0.7)

    # now start plotting
    if iterCount > 0:
        data["plane"] = planeVar.get()
        data["month"] = monVar.get()
        data["year"] = yearVar.get()
        airmasses = ["low", "med", "high"]
        dataFrames = [pdLow, pdMed, pdHigh]
        location = [lowCanvas, medCanvas, highCanvas]

        for amass, dframe, location in zip(airmasses, dataFrames, location):
            year = yearVar.get()
            if year == "All":
                thisYearData = dframe
            else:
                year = int(yearVar.get())
                thisYearData = dframe[dframe["year"] == year]

            if len(thisYearData) < 1:
                continue
            else:
                if (len(dframe[dframe[flag] == 1]) > 0):

                    active = dframe[flag] == 1
                    inact = dframe[flag] == 0
                    out = dframe["outFlag"] == 1

                    xActb10 = dframe.loc[active & (dframe["densBin"] == 1) & (~out), x]
                    yActb10 = dframe.loc[active & (dframe["densBin"] == 1) & (~out), y]
                    xActb11 = dframe.loc[active & (dframe["densBin"] == 1) & out, x]
                    yActb11 = dframe.loc[active & (dframe["densBin"] == 1) & out, y]

                    xActb20 = dframe.loc[active & (dframe["densBin"] == 2) & (~out), x]
                    yActb20 = dframe.loc[active & (dframe["densBin"] == 2) & (~out), y]
                    xActb21 = dframe.loc[active & (dframe["densBin"] == 2) & out, x]
                    yActb21 = dframe.loc[active & (dframe["densBin"] == 2) & out, y]

                    xActb30 = dframe.loc[active & (dframe["densBin"] == 3) & (~out), x]
                    yActb30 = dframe.loc[active & (dframe["densBin"] == 3) & (~out), y]
                    xActb31 = dframe.loc[active & (dframe["densBin"] == 3) & out, x]
                    yActb31 = dframe.loc[active & (dframe["densBin"] == 3) & out, y]

                    xActb40 = dframe.loc[active & (dframe["densBin"] == 4) & (~out), x]
                    yActb40 = dframe.loc[active & (dframe["densBin"] == 4) & (~out), y]
                    xActb41 = dframe.loc[active & (dframe["densBin"] == 4) & out, x]
                    yActb41 = dframe.loc[active & (dframe["densBin"] == 4) & out, y]

                    xActb50 = dframe.loc[active & (dframe["densBin"] == 5) & (~out), x]
                    yActb50 = dframe.loc[active & (dframe["densBin"] == 5) & (~out), y]
                    xActb51 = dframe.loc[active & (dframe["densBin"] == 5) & out, x]
                    yActb51 = dframe.loc[active & (dframe["densBin"] == 5) & out, y]

                    xInact = dframe.loc[inact, x]
                    yInact = dframe.loc[inact, y]

                    xLB = data[amass + "AM"]["xLB"]
                    xRB = data[amass + "AM"]["xRB"]
                    yLB = data[amass + "AM"]["yLB"]
                    yRB = data[amass + "AM"]["yRB"]

                    matplotlib.use("TKAgg")
                    style.use("ggplot")
                    f = Figure(figsize=(3, 2.5), dpi=100)
                    a = f.add_subplot(111)
                    a.clear()
                    line = np.linspace(0, 100, 101)
                    a.scatter(xInact, yInact, color='gray', marker=".")

                    if len(xActb10) > 0:
                        a.scatter(xActb10, yActb10, color='orangered', marker=".")
                        lower = int(dframe.loc[active & (dframe["densBin"] == 1), "density"].min())
                        upper = int(dframe.loc[active & (dframe["densBin"] == 1), "density"].max())
                        previous = bin1Label.cget("text")
                        string = findRange(previous, lower, upper)
                        bin1Label.config(text=string)
                    if len(xActb20) > 0:
                        a.scatter(xActb20, yActb20, color='darkorange', marker=".")
                        lower = int(dframe.loc[active & (dframe["densBin"] == 2), "density"].min())
                        upper = int(dframe.loc[active & (dframe["densBin"] == 2), "density"].max())
                        previous = bin2Label.cget("text")
                        string = findRange(previous, lower, upper)
                        bin2Label.config(text=string)
                    if len(xActb30) > 0:
                        a.scatter(xActb30, yActb30, color='orange', marker=".")
                        lower = int(dframe.loc[active & (dframe["densBin"] == 3), "density"].min())
                        upper = int(dframe.loc[active & (dframe["densBin"] == 3), "density"].max())
                        previous = bin3Label.cget("text")
                        string = findRange(previous, lower, upper)
                        bin3Label.config(text=string)
                    if len(xActb40) > 0:
                        a.scatter(xActb40, yActb40, color='gold', marker=".")
                        lower = int(dframe.loc[active & (dframe["densBin"] == 4), "density"].min())
                        upper = int(dframe.loc[active & (dframe["densBin"] == 4), "density"].max())
                        previous = bin4Label.cget("text")
                        string = findRange(previous, lower, upper)
                        bin4Label.config(text=string)
                    if len(xActb50) > 0:
                        a.scatter(xActb50, yActb50, color='yellow', marker=".")
                        lower = int(dframe.loc[active & (dframe["densBin"] == 5), "density"].min())
                        upper = int(dframe.loc[active & (dframe["densBin"] == 5), "density"].max())
                        previous = bin5Label.cget("text")
                        string = findRange(previous, lower, upper)
                        bin5Label.config(text=string)

                    if len(xActb11) > 0:
                        a.scatter(xActb11, yActb11, color='firebrick', marker=".")
                    if len(xActb21) > 0:
                        a.scatter(xActb21, yActb21, color='chocolate', marker=".")
                    if len(xActb31) > 0:
                        a.scatter(xActb31, yActb31, color='peru', marker=".")
                    if len(xActb41) > 0:
                        a.scatter(xActb41, yActb41, color='goldenrod', marker=".")
                    if len(xActb51) > 0:
                        a.scatter(xActb51, yActb51, color='khaki', marker=".")

                    a.set_xlim([0, 100])
                    a.set_ylim([0, 100])
                    a.plot(line, line, color="black")
                    a.plot(xLB, yLB, color="green")
                    a.plot(xRB, yRB, color="green")

                    canvas = FigureCanvasTkAgg(f, master=location)
                    canvas.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1)
                    canvas.draw()
                    if location == lowCanvas:
                        lowButton = tk.Button(location, text="Configure", font=(None, 10), command=lowConfig)
                        lowButton.place(relx=.75, rely=0.015, relwidth=0.22, relheight=0.1)
                    elif location == medCanvas:
                        medButton = tk.Button(location, text="Configure", font=(None, 10), command=medConfig)
                        medButton.place(relx=.75, rely=0.015, relwidth=0.22, relheight=0.1)
                    elif location == highCanvas:
                        highButton = tk.Button(location, text="Configure", font=(None, 10), command=highConfig)
                        highButton.place(relx=.75, rely=0.015, relwidth=0.22, relheight=0.1)


def findRange(previous, lower, upper):
    if "-" in previous:
        dashCount = previous.count("-")
        if dashCount == 1:
            case = 1
        else:
            case = 2
    else:
        case = 3

    if case == 1:
        tem = previous.split("-")
        # update if and only if new lower/upper values are less/greater than previous
        if lower < int(tem[0]):
            tem[0] = lower
        if upper > int(tem[1]):
            tem[1] = upper
        string = str(tem[0]) + "-" + str(tem[1])
    elif case == 2:
        if lower == upper:
            string = str(lower)
        else:
            string = str(lower) + "-" + str(upper)
    elif case == 3:
        if lower < int(previous):
            string = str(lower)
        else:
            string = previous
    print(case)
    return string


def setOutFlag(df, xAxis="KT", yAxis="KN", am="low", side="left"):
    global data
    if len(df) > 0:
        if data[am + "AM"]["knMax"] != "NA":
            for yp in range(int(data[am + "AM"]["knMax"])):
                if side == "left":
                    pointOnCurve = data[am + "AM"]["xLB"][yp]
                    xPoints = [point for point in list(df[df[yAxis] == yp][xAxis]) if point < pointOnCurve]
                    if len(xPoints) > 0:
                        for point in xPoints:
                            df.loc[(df[yAxis] == yp) & (df[xAxis] == point), "outFlag"] = 1
                elif side == "right":
                    pointOnCurve = data[am + "AM"]["xRB"][yp]
                    xPoints = [point for point in list(df[df[yAxis] == yp][xAxis]) if point > pointOnCurve]
                    if len(xPoints) > 0:
                        for point in xPoints:
                            df.loc[(df[yAxis] == yp) & (df[xAxis] == point), "outFlag"] = 1

            df.loc[(df[yAxis] > data[am + "AM"]["knMax"]), "outFlag"] = 1


def save(month):
    global monList, iterCount
    if iterCount == 0:
        messagebox.showerror("Error", "Sorry, No data available to save.")
        return
    fileQC = open(data["qc0Path"], "r")
    content = fileQC.read().splitlines()
    fileQC.close()
    # fileQC.flush()

    # update QC0 data
    position = monList.index(month) + 9  # locating month
    string = content[position]

    # find knMax and KtMax
    __kn = [data["lowAM"]["knMax"], data["medAM"]["knMax"], data["highAM"]["knMax"]]
    __kn = [i for i in __kn if i != "NA"]
    __kt = [data["lowAM"]["ktMax"], data["medAM"]["ktMax"], data["highAM"]["ktMax"]]
    __kt = [i for i in __kt if i != "NA"]

    # identify right position index
    if data["integration"] == 60:
        ind = 3
    elif data["integration"] == 15:
        ind = 2
    elif data["integration"] == 5:
        ind = 1
    elif data["integration"] == 1:
        ind = 0

    # first writing Knmax and left curve shape and positions
    string = string.split()
    _mon = string[0]
    _kmaxes = string[1]
    _lam_left = string[2]
    _lam_right = string[3]
    _mam_left = string[4]
    _mam_right = string[5]
    _ham_left = string[6]
    _ham_right = string[7]

    # break, update and join kspace maxes
    _kmaxes = _kmaxes.split("-")

    _kmaxes[0] = str(int(max(__kn)))
    _kt = _kmaxes[1].split(";")
    _kt = _kt[0].split("/")

    if ind == 3:
        _kt[ind] = str(int(float(max(__kt))))
    else:
        _kt[ind] = str(int(float(max(__kt))))
    _kt = "/".join(_kt)
    _kmaxes[1] = _kt + ";"
    _kmaxes = "-".join(_kmaxes)

    # update left shape and position for all airmasses

    i = [_lam_left, _mam_left, _ham_left]

    for j in (2, 4, 6):
        if j == 2:
            _am = "low"
            _lam_left = _lam_left.split("-")
            _lam_left[0] = str(data[_am + "AM"]["shapeLeft"])
            _lam_left[1] = str(data[_am + "AM"]["posLeft"])
            if len(_lam_left[1]) == 1:
                _lam_left[1] = "0" + _lam_left[1]
            _lam_left = "-".join(_lam_left)
        elif j == 4:
            _am = "med"
            _mam_left = _lam_left.split("-")
            _mam_left[0] = str(data[_am + "AM"]["shapeLeft"])
            _mam_left[1] = str(data[_am + "AM"]["posLeft"])
            if len(_mam_left[1]) == 1:
                _mam_left[1] = "0" + _mam_left[1]
            _mam_left = "-".join(_mam_left)
        elif j == 6:
            i = _ham_left
            _am = "high"
            _ham_left = _lam_left.split("-")
            _ham_left = _lam_left.split("-")
            _ham_left[0] = str(data[_am + "AM"]["shapeLeft"])
            _ham_left[1] = str(data[_am + "AM"]["posLeft"])
            if len(_ham_left[1]) == 1:
                _ham_left[1] = "0" + _ham_left[1]
            _ham_left = "-".join(_ham_left)

        # do the same for rest#

    for j in (3, 5, 7):
        if j == 3:
            _am = "low"
            _lam_right = _lam_right.split("-")
            _lam_right[0] = str(data[_am + "AM"]["shapeRight"])
            _pos = _lam_right[1].split("/")
            _pos[ind] = str(data[_am + "AM"]["posRight"])
            if len(_pos[ind]) == 1:
                _pos[ind] = "0" + _pos[ind]
            if ind == 3:
                _pos[ind] = _pos[ind] + ";"
            _pos = "/".join(_pos)
            _lam_right[1] = _pos
            _lam_right = "-".join(_lam_right)
        if j == 5:
            _am = "med"
            _mam_right = _mam_right.split("-")
            _mam_right[0] = str(data[_am + "AM"]["shapeRight"])
            _pos = _mam_right[1].split("/")
            _pos[ind] = str(data[_am + "AM"]["posRight"])
            if len(_pos[ind]) == 1:
                _pos[ind] = "0" + _pos[ind]
            if ind == 3:
                _pos[ind] = _pos[ind] + ";"
            _pos = "/".join(_pos)
            _mam_right[1] = _pos
            _mam_right = "-".join(_mam_right)
        if j == 7:
            _am = "high"
            _ham_right = _ham_right.split("-")
            _ham_right[0] = str(data[_am + "AM"]["shapeRight"])
            _pos = _ham_right[1].split("/")
            _pos[ind] = str(data[_am + "AM"]["posRight"])
            if len(_pos[ind]) == 1:
                _pos[ind] = "0" + _pos[ind]
            _pos = "/".join(_pos)
            _ham_right[1] = _pos
            _ham_right = "-".join(_ham_right)
    string = [_mon, _kmaxes, _lam_left, _lam_right, _mam_left, _mam_right, _ham_left, _ham_right]
    string = " ".join(string)
    content[position] = string
    content = "\n".join(content)
    fid = open(data["qc0Path"], 'w')

    if data["plane"] == 1:
        plane = "0 Kt-Kn"
    else:
        if data["plane"] == 2:
            plane = "1 Kt-Kd"
        else:
            if data["plane"] == 3:
                plane = "2 Kn-Kd"

    planeIndex = content.find("Plane")
    remain = content[planeIndex:]
    planeStr = remain[:remain.find("\n")]
    content = content.replace(planeStr, "Plane: " + plane)

    compIndex = content.find("3-Component")
    remain = content[compIndex:]
    compStr = remain[:remain.find("\n")]
    content = content.replace(compStr, "3-Component Filter: " + str(data["threshold"]))
    fid.write(content)
    fid.close()
    # fid.flush()


def savePng():
    global data, iterCount
    if iterCount == 0:
        messagebox.showerror("Error", "Sorry, No data available to save.")
        return
    if platform.system() == "Windows":
        x = mainRoot.winfo_x() + 10
        y = mainRoot.winfo_y() + 50
        height = y + mainRoot.winfo_height()
        width = x + mainRoot.winfo_width()
    else:
        x = mainRoot.winfo_x() * 2
        y = mainRoot.winfo_y() * 2
        height = y + 50 + mainRoot.winfo_height() * 2
        width = x + mainRoot.winfo_width() * 2
    time.sleep(0.5)
    image = ImageGrab.grab(bbox=(x, y, width, height))
    if not os.path.exists('images'):
        os.makedirs('images')
    image.save("images/" + data['siteIdentifier'] + str(int(time.time())) + '.png')


def saveBmp():
    global data, iterCount
    if iterCount == 0:
        messagebox.showerror("Error", "Sorry, No data available to save.")
        return
    if platform.system() == "Windows":
        x = mainRoot.winfo_x() + 10
        y = mainRoot.winfo_y() + 50
        height = y + mainRoot.winfo_height()
        width = x + mainRoot.winfo_width()
    else:
        x = mainRoot.winfo_x() * 2
        y = mainRoot.winfo_y() * 2
        height = y + 50 + mainRoot.winfo_height() * 2
        width = x + mainRoot.winfo_width() * 2
    time.sleep(0.5)
    image = ImageGrab.grab(bbox=(x, y, width, height))
    if not os.path.exists('images'):
        os.makedirs('images')
    image.save("images/" + data['siteIdentifier'] + str(int(time.time())) + '.bmp')


def exitProgram():
    global iterCount, data
    if iterCount > 0:
        answer = messagebox.askyesno("Save Changes", "Do you want to save changes?")
        if answer == True:
            monthToSave = data["month"]
            save(monthToSave)
            sys.exit()
        else:
            sys.exit()
    else:
        sys.exit()


def help():
    helpRoot = tk.Toplevel()

    helpRoot.wm_geometry("800x720+500+250")
    logo = ImageTk.PhotoImage(Image.open('dataFiles/disclaimer.png'))

    logoFrame = tk.Frame(helpRoot, bd=2)
    logoFrame.place(relx=0, rely=0, relwidth=0.5, relheight=1)
    labelImg = tk.Label(logoFrame, image=logo)
    labelImg.place(relx=0, rely=0, relwidth=1, relheight=1)
    text = "DISCLAIMER FOR \n SOFTWARE SUBMITTED TO OSTI\n\nThis  Software  is  provided by the  National  Renewable  Energy\n" \
           "Laboratory  (\"NREL\"),  which  is operated  by  the  Alliance for\n" \
           " Sustainable Energy, LLC (\"ALLIANCE\") for the " \
           "U.S. Department \nof Energy (\"DOE\"). \n\n" \
           "" \
           " Access to and use of this Software shall impose the following\n" \
           "obligations on the user, as set forth herein. The user is granted\n" \
           " the  right,  without  any  fee or  cost, to use, copy, modify, alter,\n" \
           " enhance   and   distribute   this   Software   for   any   purpose \n" \
           " whatsoever,  provided  that this  entire   notice   appears  in  all \n" \
           "copies of the Software.  Further, the user agrees to credit DOE\n" \
           "/NREL/ALLIANCE in any publication that results from the use of\n" \
           " this Software.  The names DOE/NREL/ALLIANCE, however, may\n" \
           "not be used in any advertising or publicity to endorse or promote\n" \
           " anyproducts  or  commercial  entities  unless  specific  written \n" \
           "permission  is  obtained  from  DOE/NREL/ALLIANCE.  The user\n" \
           " also  understands  that  DOE/NREL/Alliance  is not obligated  to \n" \
           "provide   the  user  with  any   support, consulting,  training  or \n" \
           "assistance of any kind  with regard  to the  use  of this Software\n" \
           "or  to  provide  the  user with  any  updates,  revisions  or  new \n" \
           "versions of this Software.\n\n" \
           "YOU  AGREE  TO  INDEMNIFY  DOE/NREL/ALLIANCE,  AND  ITS\n" \
           "SUBSIDIARIES,   AFFILIATES,   OFFICERS,   AGENTS,   AND\n" \
           "EMPLOYEES  AGAINST  ANY   CLAIM  OR  DEMAND,  INCLUDING\n" \
           "REASONABLE  ATTORNEYS' FEES,  RELATED  TO  YOUR  USE OF\n" \
           "THIS  SOFTWARE.  THIS  SOFTWARE  IS  PROVIDED  BY  DOE/\n" \
           "NREL/ALLIANCE\"AS  IS\"  AND  ANY  EXPRESS  OR  IMPLIED\n" \
           "WARRANTIES, INCLUDING  BUT NOT LIMITED TO, THE IMPLIED\n" \
           "WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A \n" \
           "PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL\n" \
           "DOE/NREL/ALLIANCE BE LIABLE FOR ANY SPECIAL, INDIRECT\n" \
           "OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES \n" \
           "WHATSOEVER, INCLUDING BUT NOT LIMITED TO CLAIMS \n" \
           "ASSOCIATED WITH THE LOSS OF DATA OR PROFITS, WHICH\n" \
           "MAY RESULT FROM AN ACTION IN CONTRACT, NEGLIGENCE On\n" \
           "OTHER TORTIOUS CLAIM THAT ARISES OUT OF OR IN \n" \
           "CONNECTION WITH THE ACCESS, USE OR PERFORMANCE OF\n" \
           "THIS SOFTWARE. "

    textLabel = tk.Label(helpRoot, text=text)
    textLabel.place(relx=0.5, rely=0.0, relwidth=0.50, relheight=1)

    helpRoot.iconbitmap('dataFiles/qcfit-icon.ico')
    helpRoot.mainloop()


def callSave():
    global data
    monthToSave = data["month"]
    save(monthToSave)


# Main GUI of form

mainRoot = tk.Tk()
mainRoot.wm_geometry("1000x550+500+250")
mainRoot.title("QCFIT")
menuBar = tk.Menu(mainRoot)
file = tk.Menu(menuBar, tearoff=0)
file.add_command(label="Open", command=hitOpen)
file.add_separator()
file.add_command(label="Edit QC0", command=hitEdit)
file.add_separator()
file.add_command(label="Save", command=callSave)
file.add_command(label="Save BMP Image", command=saveBmp)
file.add_command(label="Save PNG Image", command=savePng)
file.add_separator()
file.add_command(label="Exit", command=exitProgram)
menuBar.add_cascade(label="File", menu=file)

Help = tk.Menu(menuBar, tearoff=0)
Help.add_command(label="About", command=help)
menuBar.add_cascade(label="Help", menu=Help, command=help)
mainRoot.config(menu=menuBar)

####################################################
#
# Variables and lists
#
####################################################
data = {'qc0Path': '', 'defaultDataFolder': '', 'siteCode': '', 'siteDesc': '', 'siteIdentifier': '', 'latitude': 0.0,
        'longitude': 0.0, 'timeZone': 0, 'elevation': 0.0, 'comments': '', 'integration': 1, 'plane': '',
        '3compFilter': '', 'threshold': 0.05, 'QCFDataFilepath': '', 'month': '', 'year': '', 'editWinFlag': 0,
        'listPageFlag': 0, 'flag': 'activeKtKn', 'xAxis': 'KT', 'yAxis': 'KN', 'x1': 0, 'x2': 0, 'y1': 0, 'y2': 0,
        'density': {'low': {'lower': "", 'upper': ""}, 'med': {'lower': "", 'upper': ""},
                    'high': {'lower': "", 'upper': ""}},
        'lowAM': {'ktMax': 0, 'knMax': 0, 'kdMax': 0, 'shapeLeft': 0, 'shapeRight': 0, 'posLeft': 0, 'posRight': 0,
                  'lBound': [0], 'rBound': [0], 'In': 0, 'Out': 0, 'Active': 0, 'Ignored': 0, 'Total': 0, 'Err_L': 0,
                  'Err_R': 0, 'activeLBound': [0], 'activeRBound': [0], 'scale': 1},
        'medAM': {'ktMax': 0, 'knMax': 0, 'kdMax': 0, 'shapeLeft': 0, 'shapeRight': 0, 'posLeft': 0, 'posRight': 0,
                  'lBound': [0], 'rBound': [0], 'In': 0, 'Out': 0, 'Active': 0, 'Ignored': 0, 'Total': 0, 'Err_L': 0,
                  'Err_R': 0, 'activeLBound': [0], 'activeRBound': [0], 'scale': 1},
        'highAM': {'ktMax': 0, 'knMax': 0, 'kdMax': 0, 'shapeLeft': 0, 'shapeRight': 0, 'posLeft': 0, 'posRight': 0,
                   'lBound': [0], 'rBound': [0], 'In': 0, 'Out': 0, 'Active': 0, 'Ignored': 0, 'Total': 0, 'Err_L': 0,
                   'Err_R': 0, 'activeLBound': [0], 'activeRBound': [0], 'scale': 1}}

siteInfo = {}
ip = pd.DataFrame(columns=["year", "monthName", "NAM"])
boundary = pd.DataFrame()
plotData = pd.DataFrame()
pdLow = pd.DataFrame()
pdMed = pd.DataFrame()
pdHigh = pd.DataFrame()
lowFilter = pd.DataFrame()
medFilter = pd.DataFrame()
highFilter = pd.DataFrame()
dcL = np.zeros([3, 6, 20])
pcL = np.zeros([3, 6, 20])
dcR = np.zeros([3, 5, 20])
pcR = np.zeros([3, 5, 20])
scoreLeft = np.zeros([3, 5, 20])
scoreRight = np.zeros([3, 5, 20])
iterCount = 0
dFlag = 0
filterDict = {'low': lowFilter, 'med': medFilter, 'high': highFilter}

nsPath = ""
dfPath = ""
buttonList = []
flag = "activeKtKn"  # by default flag
monList = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November",
           "December"]
ipData = pd.DataFrame()
yearList = ["fetch", "All"]
planeVar = tk.IntVar()
monVar = tk.StringVar()
yearVar = tk.StringVar()
threshVar = tk.StringVar()
densVar = tk.IntVar()

openRoot = tk.Tk()
optVar = tk.StringVar(openRoot)
integVar = tk.StringVar(openRoot)
openRoot.withdraw()

editGraph = tk.Tk()
editGraph.withdraw()

####################################################
#
# planeFrame and controls
#
####################################################
planeFrame = tk.Frame(mainRoot, bd=2, bg="gray")
planeFrame.place(relx=0.01, rely=0.01, relwidth=0.14, relheight=0.13)
planeCanvas = tk.Canvas(planeFrame)
planeCanvas.place(relx=0, rely=0, relwidth=1, relheight=1)
planeLabel = tk.Label(planeCanvas, text="Plane")
planeLabel.place(relx=0.02, rely=0.11, relwidth=0.5, relheight=0.4)

r1 = tk.Radiobutton(planeCanvas, text="Kt-Kn", font=(None, 9), variable=planeVar, value=1)
r1.place(relx=0.6, rely=0.01, relwidth=0.4, relheight=0.3)
r2 = tk.Radiobutton(planeCanvas, text="Kt-Kd", font=(None, 9), variable=planeVar, value=2)
r2.place(relx=0.6, rely=0.34, relwidth=0.4, relheight=0.3)
r3 = tk.Radiobutton(planeCanvas, text="Kn-Kd", font=(None, 9), variable=planeVar, value=3)
r3.place(relx=0.6, rely=0.67, relwidth=0.4, relheight=0.3)
r1.select()
planeVar.trace_add("write", callback=plotUpdateThroughkspace)
animateButton = tk.Button(planeCanvas, text="Animate", font=(None, 10), command=animatePlots)
animateButton.place(relx=0.04, rely=0.52, relwidth=0.5, relheight=0.38)
disable(planeCanvas.winfo_children())
####################################################
#
# month year frame and controls
#
####################################################


monYearFrame = tk.Frame(mainRoot, bd=2, bg="gray", borderwidth=1)
monYearFrame.place(relx=0.16, rely=0.01, relwidth=0.17, relheight=0.13)

monYearCanvas = tk.Canvas(monYearFrame)
monYearCanvas.place(relx=0, rely=0, relwidth=1, relheight=1)

monthLabel = tk.Label(monYearCanvas, text="Month")
monthLabel.place(relx=0.05, rely=0.15, relwidth=0.25, relheight=0.2)

yearLabel = tk.Label(monYearCanvas, text="Year")
yearLabel.place(relx=0.05, rely=0.6, relwidth=0.25, relheight=0.2)

monOption = tk.OptionMenu(monYearCanvas, monVar, *monList)
monOption.place(relx=0.35, rely=0.03, relwidth=0.6, relheight=0.45)
monVar.trace_add("write", callback=plotUpdateThroughMonth)

yearOption = tk.OptionMenu(monYearCanvas, yearVar, *yearList)
yearOption.place(relx=0.35, rely=0.51, relwidth=0.6, relheight=0.45)
yearVar.trace_add('write', callback=plotByYear)

disable(monYearCanvas.winfo_children())

####################################################

# 3 component filter frame and controls
#
####################################################
compFilterFrame = tk.Frame(mainRoot, bd=2, bg="gray")
compFilterFrame.place(relx=0.34, rely=0.01, relwidth=0.32, relheight=0.13)

compFilterCanvas = tk.Canvas(compFilterFrame)
compFilterCanvas.place(relx=0, rely=0, relwidth=1, relheight=1)

compFiltLabel = tk.Label(compFilterCanvas, text="3 Component Filtering")
compFiltLabel.place(relx=0.03, rely=0.11, relwidth=0.5, relheight=0.32)

kSpaceLabel = tk.Label(compFilterCanvas, text="K-Space Threshold", font=(None, 10))
kSpaceLabel.place(relx=0.05, rely=0.60, relwidth=0.35, relheight=0.25)

applyButton = tk.Button(compFilterCanvas, text="Apply", font=(None, 10), command=compFilter)
applyButton.place(relx=0.55, rely=0.1, relwidth=0.15, relheight=0.4)

threshVar.set('1')
threshList = ['0', '0.05', '0.1', '0.15', '0.2', '0.25', '0.3', '0.35', '0.4', '0.45', '0.5', '0.55', '0.6', '0.65',
              '0.7', '0.75', '0.8', '0.85', '0.9', '0.95', '1']
threshOption = tk.OptionMenu(compFilterCanvas, threshVar, *threshList)
threshOption.place(relx=0.45, rely=0.55, relwidth=0.25, relheight=0.4)

freqLabel = tk.Label(compFilterCanvas, text="Freq Kt-Kn-Kd", font=(None, 8))
freqLabel.place(relx=0.72, rely=0.02, relwidth=0.28, relheight=0.2)

histoCanvas = tk.Canvas(compFilterCanvas, bg="#e0e0eb")
histoCanvas.place(relx=0.72, rely=0.24, relwidth=0.28, relheight=0.74)
disable(compFilterCanvas.winfo_children())
####################################################

# density frame and controls
#
####################################################
densityFrame = tk.Frame(mainRoot, bd=2, bg="gray")
densityFrame.place(relx=0.67, rely=0.01, relwidth=0.22, relheight=0.13)

densityCanvas = tk.Canvas(densityFrame)
densityCanvas.place(relx=0, rely=0, relwidth=1, relheight=1)

densLabel = tk.Label(densityCanvas, text="Density")
densLabel.place(relx=0.05, rely=0.11, relwidth=0.30, relheight=0.30)

denseOnOff = tk.Radiobutton(densityCanvas, text="Off", font=(None, 9), variable=densVar, value=1)  # , command=plot)
denseOnOff.place(relx=0.08, rely=0.55, relwidth=0.2, relheight=0.4)
denseOnOff.select()
equalFreq = tk.Radiobutton(densityCanvas, text="Equal Freq", font=(None, 9), variable=densVar,
                           value=2)  # , command=plot)
equalFreq.place(relx=0.4, rely=0.01, relwidth=0.5, relheight=0.3)
equalRange = tk.Radiobutton(densityCanvas, text="Equal Range", font=(None, 9), variable=densVar,
                            value=3)  # , command=plot)
equalRange.place(relx=0.4, rely=0.34, relwidth=0.4, relheight=0.3)
expFactor = tk.Radiobutton(densityCanvas, text="Exp(Factor):", font=(None, 9), variable=densVar,
                           value=4)  # , command=plot)
densVar.trace_add('write', callback=density)
expFactor.place(relx=0.4, rely=0.67, relwidth=0.4, relheight=0.3)
expVar = tk.StringVar(mainRoot, value='3.0')
expEntry = tk.Entry(densityCanvas, textvariable=expVar, state=tk.DISABLED)
expEntry.place(relx=0.82, rely=0.67, relwidth=0.16, relheight=0.3)
expEntry.configure(state=tk.DISABLED)

expVar.trace_add('write', callback=density)

disable(densityCanvas.winfo_children())
####################################################

# Logo frame
#
####################################################

logo = ImageTk.PhotoImage(Image.open('dataFiles/log.png'))

logoFrame = tk.Frame(mainRoot, bd=2)
logoFrame.place(relx=0.90, rely=0.01, relwidth=0.09, relheight=0.13)
labelImg = tk.Label(logoFrame, image=logo)
labelImg.place(relx=0, rely=0, relwidth=1, relheight=1)
####################################################

# Low air mass K-Space frame and controls
#
####################################################

lowKspaceFrame = tk.Frame(mainRoot, bd=2, bg="gray")
lowKspaceFrame.place(relx=0.01, rely=0.15, relwidth=0.08, relheight=0.19)
lowKspaceCanvas = tk.Canvas(lowKspaceFrame)
lowKspaceCanvas.place(relx=0, rely=0, relwidth=1, relheight=1)

lowStatsFrame = tk.Frame(mainRoot, bd=2, bg="gray")
lowStatsFrame.place(relx=0.12, rely=0.15, relwidth=0.21, relheight=0.19)
lowStatsCanvas = tk.Canvas(lowStatsFrame)
lowStatsCanvas.place(relx=0, rely=0, relwidth=1, relheight=1)

lowErrorFrame = tk.Frame(lowStatsFrame, bd=2, bg="#a8a7a2")
lowErrorFrame.place(relx=0.5, rely=0.5, relwidth=0.5, relheight=0.5)
lowErrorCanvas = tk.Canvas(lowErrorFrame)
lowErrorCanvas.place(relx=0, rely=0, relwidth=1, relheight=1)

lowY = tk.Label(lowKspaceCanvas, text="KnMax:", font=(None, 9), anchor="w")
lowY.place(relx=0.05, rely=0.02, relwidth=0.55, relheight=0.2)
lowYVal = tk.Label(lowKspaceCanvas, text="", font=(None, 9), anchor="w")
lowYVal.place(relx=0.65, rely=0.02, relwidth=0.20, relheight=0.2)

lowX = tk.Label(lowKspaceCanvas, text="KtMax:", font=(None, 9), anchor="w")
lowX.place(relx=0.05, rely=0.24, relwidth=0.5, relheight=0.2)
lowXVal = tk.Label(lowKspaceCanvas, text="", font=(None, 9), anchor="w")
lowXVal.place(relx=0.65, rely=0.24, relwidth=0.20, relheight=0.2)

lowLeft = tk.Label(lowKspaceCanvas, text="Left:", font=(None, 9), anchor="w")
lowLeft.place(relx=0.05, rely=0.50, relwidth=0.38, relheight=0.2)
lowLeftVal = tk.Label(lowKspaceCanvas, text="", font=(None, 9), anchor="w")
lowLeftVal.place(relx=0.65, rely=0.50, relwidth=0.35, relheight=0.2)

lowRight = tk.Label(lowKspaceCanvas, text="Right:", font=(None, 9), anchor="w")
lowRight.place(relx=0.05, rely=0.72, relwidth=0.43, relheight=0.2)
lowRightVal = tk.Label(lowKspaceCanvas, text="", font=(None, 9), anchor="w")
lowRightVal.place(relx=0.65, rely=0.72, relwidth=0.35, relheight=0.2)

# entries in stats frame
lowInLabel = tk.Label(lowStatsCanvas, text="In", font=(None, 9), anchor="w")
lowInLabel.place(relx=0.02, rely=0.01, relwidth=0.46, relheight=0.188)
lowInVal = tk.Label(lowStatsCanvas, text="0", font=(None, 9), anchor="w")
lowInVal.place(relx=0.26, rely=0.01, relwidth=0.40, relheight=0.188)

lowOutLabel = tk.Label(lowStatsCanvas, text="Out", font=(None, 9), anchor="w")
lowOutLabel.place(relx=0.02, rely=0.198, relwidth=0.46, relheight=0.188)
lowOutVal = tk.Label(lowStatsCanvas, text="0", font=(None, 9), anchor="w")
lowOutVal.place(relx=0.26, rely=0.198, relwidth=0.80, relheight=0.188)

lowActiveLabel = tk.Label(lowStatsCanvas, text="Active", font=(None, 9), anchor="w")
lowActiveLabel.place(relx=0.02, rely=0.396, relwidth=0.46, relheight=0.188)
lowActiveVal = tk.Label(lowStatsCanvas, text="0", font=(None, 9), anchor="w")
lowActiveVal.place(relx=0.26, rely=0.396, relwidth=0.40, relheight=0.188)

lowIgnoredLabel = tk.Label(lowStatsCanvas, text="Ignored", font=(None, 9), anchor="w")
lowIgnoredLabel.place(relx=0.02, rely=0.594, relwidth=0.46, relheight=0.188)
lowIgnoredVal = tk.Label(lowStatsCanvas, text="0", font=(None, 9), anchor="w")
lowIgnoredVal.place(relx=0.26, rely=0.594, relwidth=0.40, relheight=0.188)

lowTotalLabel = tk.Label(lowStatsCanvas, text="Total", font=(None, 9), anchor="w")
lowTotalLabel.place(relx=0.02, rely=0.792, relwidth=0.46, relheight=0.188)
lowTotalVal = tk.Label(lowStatsCanvas, text="0", font=(None, 9), anchor="w")
lowTotalVal.place(relx=0.26, rely=0.792, relwidth=0.40, relheight=0.188)

# entries in error frame

lowErrL = tk.Label(lowErrorCanvas, text="Err(L):", font=(None, 9), anchor="w")
lowErrL.place(relx=0.02, rely=0.10, relwidth=0.40, relheight=0.35)
lowErrLVal = tk.Label(lowErrorCanvas, text="0.00", font=(None, 9), anchor="w")
lowErrLVal.place(relx=0.47, rely=0.10, relwidth=0.31, relheight=0.35)
lowErrLper = tk.Label(lowErrorCanvas, text="%", font=(None, 9), anchor="w")
lowErrLper.place(relx=0.82, rely=0.10, relwidth=0.15, relheight=0.35)

lowErrR = tk.Label(lowErrorCanvas, text="Err(R):", font=(None, 9), anchor="w")
lowErrR.place(relx=0.02, rely=0.55, relwidth=0.40, relheight=0.35)
lowErrRVal = tk.Label(lowErrorCanvas, text="0.00", font=(None, 9), anchor="w")
lowErrRVal.place(relx=0.47, rely=0.55, relwidth=0.31, relheight=0.35)
lowErrRper = tk.Label(lowErrorCanvas, text="%", font=(None, 9), anchor="w")
lowErrRper.place(relx=0.82, rely=0.55, relwidth=0.15, relheight=0.35)

disable(lowKspaceCanvas.winfo_children())
disable(lowStatsCanvas.winfo_children())
disable(lowErrorCanvas.winfo_children())

####################################################

# Med air mass K-Space frame and controls
#
####################################################
medKspaceFrame = tk.Frame(mainRoot, bd=2, bg="gray")
medKspaceFrame.place(relx=0.34, rely=0.15, relwidth=0.08, relheight=0.19)
medKspaceCanvas = tk.Canvas(medKspaceFrame)
medKspaceCanvas.place(relx=0, rely=0, relwidth=1, relheight=1)

medStatsFrame = tk.Frame(mainRoot, bd=2, bg="gray")
medStatsFrame.place(relx=0.45, rely=0.15, relwidth=0.21, relheight=0.19)
medStatsCanvas = tk.Canvas(medStatsFrame)
medStatsCanvas.place(relx=0, rely=0, relwidth=1, relheight=1)

medErrorFrame = tk.Frame(medStatsFrame, bd=2, bg="#a8a7a2")
medErrorFrame.place(relx=0.5, rely=0.5, relwidth=0.5, relheight=0.5)
medErrorCanvas = tk.Canvas(medErrorFrame)
medErrorCanvas.place(relx=0, rely=0, relwidth=1, relheight=1)

medY = tk.Label(medKspaceCanvas, text="KnMax:", font=(None, 9), anchor="w")
medY.place(relx=0.05, rely=0.02, relwidth=0.55, relheight=0.2)
medYVal = tk.Label(medKspaceCanvas, text="", font=(None, 9), anchor="w")
medYVal.place(relx=0.65, rely=0.02, relwidth=0.20, relheight=0.2)

medX = tk.Label(medKspaceCanvas, text="KtMax:", font=(None, 9), anchor="w")
medX.place(relx=0.05, rely=0.24, relwidth=0.5, relheight=0.2)
medXVal = tk.Label(medKspaceCanvas, text="", font=(None, 9), anchor="w")
medXVal.place(relx=0.65, rely=0.24, relwidth=0.20, relheight=0.2)

medLeft = tk.Label(medKspaceCanvas, text="Left:", font=(None, 9), anchor="w")
medLeft.place(relx=0.05, rely=0.50, relwidth=0.38, relheight=0.2)
medLeftVal = tk.Label(medKspaceCanvas, text="", font=(None, 9), anchor="w")
medLeftVal.place(relx=0.65, rely=0.50, relwidth=0.35, relheight=0.2)

medRight = tk.Label(medKspaceCanvas, text="Right:", font=(None, 9), anchor="w")
medRight.place(relx=0.05, rely=0.72, relwidth=0.43, relheight=0.2)
medRightVal = tk.Label(medKspaceCanvas, text="", font=(None, 9), anchor="w")
medRightVal.place(relx=0.65, rely=0.72, relwidth=0.35, relheight=0.2)

# entries in stats frame

medInLabel = tk.Label(medStatsCanvas, text="In", font=(None, 9), anchor="w")
medInLabel.place(relx=0.02, rely=0.01, relwidth=0.23, relheight=0.188)
medInVal = tk.Label(medStatsCanvas, text="0", font=(None, 9), anchor="w")
medInVal.place(relx=0.26, rely=0.01, relwidth=0.20, relheight=0.188)

medOutLabel = tk.Label(medStatsCanvas, text="Out", font=(None, 9), anchor="w")
medOutLabel.place(relx=0.02, rely=0.198, relwidth=0.23, relheight=0.188)
medOutVal = tk.Label(medStatsCanvas, text="0", font=(None, 9), anchor="w")
medOutVal.place(relx=0.26, rely=0.198, relwidth=0.40, relheight=0.188)

medActiveLabel = tk.Label(medStatsCanvas, text="Active", font=(None, 9), anchor="w")
medActiveLabel.place(relx=0.02, rely=0.396, relwidth=0.23, relheight=0.188)
medActiveVal = tk.Label(medStatsCanvas, text="0", font=(None, 9), anchor="w")
medActiveVal.place(relx=0.26, rely=0.396, relwidth=0.20, relheight=0.188)

medIgnoredLabel = tk.Label(medStatsCanvas, text="Ignored", font=(None, 9), anchor="w")
medIgnoredLabel.place(relx=0.02, rely=0.594, relwidth=0.23, relheight=0.188)
medIgnoredVal = tk.Label(medStatsCanvas, text="0", font=(None, 9), anchor="w")
medIgnoredVal.place(relx=0.26, rely=0.594, relwidth=0.20, relheight=0.188)

medTotalLabel = tk.Label(medStatsCanvas, text="Total", font=(None, 9), anchor="w")
medTotalLabel.place(relx=0.02, rely=0.792, relwidth=0.23, relheight=0.188)
medTotalVal = tk.Label(medStatsCanvas, text="0", font=(None, 9), anchor="w")
medTotalVal.place(relx=0.26, rely=0.792, relwidth=0.20, relheight=0.188)

# entries in error frame

medErrL = tk.Label(medErrorCanvas, text="Err(L):", font=(None, 9), anchor="w")
medErrL.place(relx=0.02, rely=0.10, relwidth=0.40, relheight=0.35)
medErrLVal = tk.Label(medErrorCanvas, text="0.00", font=(None, 9), anchor="w")
medErrLVal.place(relx=0.47, rely=0.10, relwidth=0.31, relheight=0.35)
medErrLper = tk.Label(medErrorCanvas, text="%", font=(None, 9), anchor="w")
medErrLper.place(relx=0.82, rely=0.10, relwidth=0.15, relheight=0.35)

medErrR = tk.Label(medErrorCanvas, text="Err(R):", font=(None, 9), anchor="w")
medErrR.place(relx=0.02, rely=0.55, relwidth=0.40, relheight=0.35)
medErrRVal = tk.Label(medErrorCanvas, text="0.00", font=(None, 9), anchor="w")
medErrRVal.place(relx=0.47, rely=0.55, relwidth=0.31, relheight=0.35)
medErrRper = tk.Label(medErrorCanvas, text="%", font=(None, 9), anchor="w")
medErrRper.place(relx=0.82, rely=0.55, relwidth=0.15, relheight=0.35)

disable(medKspaceCanvas.winfo_children())
disable(medStatsCanvas.winfo_children())
disable(medErrorCanvas.winfo_children())

####################################################

# High air mass K-Space frame and controls
#
####################################################
highKspaceFrame = tk.Frame(mainRoot, bd=2, bg="gray")
highKspaceFrame.place(relx=0.67, rely=0.15, relwidth=0.08, relheight=0.19)
highKspaceCanvas = tk.Canvas(highKspaceFrame)
highKspaceCanvas.place(relx=0, rely=0, relwidth=1, relheight=1)

highStatsFrame = tk.Frame(mainRoot, bd=2, bg="gray")
highStatsFrame.place(relx=0.78, rely=0.15, relwidth=0.21, relheight=0.19)
highStatsCanvas = tk.Canvas(highStatsFrame)
highStatsCanvas.place(relx=0, rely=0, relwidth=1, relheight=1)

highErrorFrame = tk.Frame(highStatsFrame, bd=2, bg="#a8a7a2")
highErrorFrame.place(relx=0.5, rely=0.5, relwidth=0.5, relheight=0.5)
highErrorCanvas = tk.Canvas(highErrorFrame)
highErrorCanvas.place(relx=0, rely=0, relwidth=1, relheight=1)

highY = tk.Label(highKspaceCanvas, text="KnMax:", font=(None, 9), anchor="w")
highY.place(relx=0.05, rely=0.02, relwidth=0.55, relheight=0.2)
highYVal = tk.Label(highKspaceCanvas, text="", font=(None, 9), anchor="w")
highYVal.place(relx=0.65, rely=0.02, relwidth=0.20, relheight=0.2)

highX = tk.Label(highKspaceCanvas, text="KtMax:", font=(None, 9), anchor="w")
highX.place(relx=0.05, rely=0.24, relwidth=0.5, relheight=0.2)
highXVal = tk.Label(highKspaceCanvas, text="", font=(None, 9), anchor="w")
highXVal.place(relx=0.65, rely=0.24, relwidth=0.20, relheight=0.2)

highLeft = tk.Label(highKspaceCanvas, text="Left:", font=(None, 9), anchor="w")
highLeft.place(relx=0.05, rely=0.50, relwidth=0.38, relheight=0.2)
highLeftVal = tk.Label(highKspaceCanvas, text="", font=(None, 9), anchor="w")
highLeftVal.place(relx=0.65, rely=0.50, relwidth=0.35, relheight=0.2)

highRight = tk.Label(highKspaceCanvas, text="Right:", font=(None, 9), anchor="w")
highRight.place(relx=0.05, rely=0.72, relwidth=0.43, relheight=0.2)
highRightVal = tk.Label(highKspaceCanvas, text="", font=(None, 9), anchor="w")
highRightVal.place(relx=0.65, rely=0.72, relwidth=0.35, relheight=0.2)

# entries in stats frame

highInLabel = tk.Label(highStatsCanvas, text="In", font=(None, 9), anchor="w")
highInLabel.place(relx=0.02, rely=0.01, relwidth=0.23, relheight=0.188)
highInVal = tk.Label(highStatsCanvas, text="0", font=(None, 9), anchor="w")
highInVal.place(relx=0.26, rely=0.01, relwidth=0.20, relheight=0.188)

highOutLabel = tk.Label(highStatsCanvas, text="Out", font=(None, 9), anchor="w")
highOutLabel.place(relx=0.02, rely=0.198, relwidth=0.23, relheight=0.188)
highOutVal = tk.Label(highStatsCanvas, text="0", font=(None, 9), anchor="w")
highOutVal.place(relx=0.26, rely=0.198, relwidth=0.40, relheight=0.188)

highActiveLabel = tk.Label(highStatsCanvas, text="Active", font=(None, 9), anchor="w")
highActiveLabel.place(relx=0.02, rely=0.396, relwidth=0.23, relheight=0.188)
highActiveVal = tk.Label(highStatsCanvas, text="0", font=(None, 9), anchor="w")
highActiveVal.place(relx=0.26, rely=0.396, relwidth=0.20, relheight=0.188)

highIgnoredLabel = tk.Label(highStatsCanvas, text="Ignored", font=(None, 9), anchor="w")
highIgnoredLabel.place(relx=0.02, rely=0.594, relwidth=0.23, relheight=0.188)
highIgnoredVal = tk.Label(highStatsCanvas, text="0", font=(None, 9), anchor="w")
highIgnoredVal.place(relx=0.26, rely=0.594, relwidth=0.20, relheight=0.188)

highTotalLabel = tk.Label(highStatsCanvas, text="Total", font=(None, 9), anchor="w")
highTotalLabel.place(relx=0.02, rely=0.792, relwidth=0.23, relheight=0.188)
highTotalVal = tk.Label(highStatsCanvas, text="0", font=(None, 9), anchor="w")
highTotalVal.place(relx=0.26, rely=0.792, relwidth=0.20, relheight=0.188)

# entries in error frame

highErrL = tk.Label(highErrorCanvas, text="Err(L):", font=(None, 9), anchor="w")
highErrL.place(relx=0.02, rely=0.10, relwidth=0.40, relheight=0.35)
highErrLVal = tk.Label(highErrorCanvas, text="0.00", font=(None, 9), anchor="w")
highErrLVal.place(relx=0.47, rely=0.10, relwidth=0.31, relheight=0.35)
highErrLper = tk.Label(highErrorCanvas, text="%", font=(None, 9), anchor="w")
highErrLper.place(relx=0.82, rely=0.10, relwidth=0.15, relheight=0.35)

highErrR = tk.Label(highErrorCanvas, text="Err(R):", font=(None, 9), anchor="w")
highErrR.place(relx=0.02, rely=0.55, relwidth=0.40, relheight=0.35)
highErrRVal = tk.Label(highErrorCanvas, text="0.00", font=(None, 9), anchor="w")
highErrRVal.place(relx=0.47, rely=0.55, relwidth=0.31, relheight=0.35)
highErrRper = tk.Label(highErrorCanvas, text="%", font=(None, 9), anchor="w")
highErrRper.place(relx=0.82, rely=0.55, relwidth=0.15, relheight=0.35)

disable(highKspaceCanvas.winfo_children())
disable(highStatsCanvas.winfo_children())
disable(highErrorCanvas.winfo_children())

####################################################
#
# Graph labels
#
####################################################
labelFrame = tk.Frame(mainRoot, bd=2, bg="gray")
labelFrame.place(relx=0.01, rely=0.35, relwidth=0.98, relheight=0.05)

lowLabel = tk.Label(labelFrame, text="Low Air Mass", bg="gray", font=(None, 10))
lowLabel.place(relx=0, rely=0, relwidth=0.325, relheight=1)

medLabel = tk.Label(labelFrame, text="Medium Air Mass", bg="gray", font=(None, 10))
medLabel.place(relx=0.335, rely=0, relwidth=0.33, relheight=1)

highLabel = tk.Label(labelFrame, text="High Air Mass", bg="gray", font=(None, 10))
highLabel.place(relx=0.675, rely=0, relwidth=0.33, relheight=1)
####################################################
#
# Graph Canvas
#
####################################################
lowCanvasFrame = tk.Frame(mainRoot, bd=2, bg="gray")
lowCanvasFrame.place(relx=0.01, rely=0.41, relwidth=0.32, relheight=0.52)

lowCanvas = tk.Canvas(lowCanvasFrame)
lowCanvas.place(relx=0, rely=0, relwidth=1, relheight=1)

medCanvasFrame = tk.Frame(mainRoot, bd=2, bg="gray")
medCanvasFrame.place(relx=0.34, rely=0.41, relwidth=0.32, relheight=0.52)
medCanvas = tk.Canvas(medCanvasFrame)
medCanvas.place(relx=0, rely=0, relwidth=1, relheight=1)
medCanvas.create_line(20, 30, 20 + 1, 30)

highCanvasFrame = tk.Frame(mainRoot, bd=2, bg="gray")
highCanvasFrame.place(relx=0.67, rely=0.41, relwidth=0.32, relheight=0.52)
highCanvas = tk.Canvas(highCanvasFrame)
highCanvas.place(relx=0, rely=0, relwidth=1, relheight=1)
####################################################
#
# Density color frame
#
####################################################
densityColorFrame = tk.Frame(mainRoot, bd=2, bg="gray")
densityColorFrame.place(relx=0.01, rely=0.94, relwidth=0.72, relheight=0.05)
densityColorCanvas = tk.Canvas(densityColorFrame)
densityColorCanvas.place(relx=0, rely=0, relwidth=1, relheight=1)
desityLabel = tk.Label(densityColorCanvas, text="Density", font=(None, 10))
desityLabel.place(relx=0.01, rely=0, relwidth=0.1, relheight=1)

bin1Label = tk.Label(densityColorCanvas, text="----", font=(None, 9))
bin1Label.place(relx=0.17, rely=0, relwidth=0.075, relheight=1)
color1 = tk.Frame(densityColorCanvas, highlightbackground="black", highlightcolor="black", bg="orangered",
                  highlightthickness=1, width=100, height=100, bd=0)
color1.place(relx=0.25, rely=0.15, relwidth=0.03, relheight=0.7)
color2 = tk.Frame(densityColorCanvas, highlightbackground="black", highlightcolor="black", bg="firebrick",
                  highlightthickness=1, width=100, height=100, bd=0)
color2.place(relx=0.28, rely=0.15, relwidth=0.03, relheight=0.7)
bin2Label = tk.Label(densityColorCanvas, text="----", font=(None, 9))
bin2Label.place(relx=0.32, rely=0, relwidth=0.075, relheight=1)
bin3Label = tk.Label(densityColorCanvas, text="----", font=(None, 9))
bin3Label.place(relx=0.47, rely=0, relwidth=0.075, relheight=1)
bin4Label = tk.Label(densityColorCanvas, text="----", font=(None, 9))
bin4Label.place(relx=0.62, rely=0, relwidth=0.075, relheight=1)
bin5Label = tk.Label(densityColorCanvas, text="----", font=(None, 9))
bin5Label.place(relx=0.77, rely=0, relwidth=0.075, relheight=1)

####################################################
#
# Integration time frame
#
####################################################
integrationFrame = tk.Frame(mainRoot, bd=2, bg="gray")
integrationFrame.place(relx=0.74, rely=0.94, relwidth=0.25, relheight=0.05)
integrationCanvas = tk.Canvas(integrationFrame)
integrationCanvas.place(relx=0, rely=0, relwidth=1, relheight=1)

integTimeLabel = tk.Label(integrationFrame, text="Integration Time (min): " + str(data["integration"]))
integTimeLabel.place(relx=0.05, rely=0.1, relwidth=0.70, relheight=0.8)

disable(integrationFrame.winfo_children())
mainRoot.protocol("WM_DELETE_WINDOW", exitProgram)
mainRoot.iconbitmap('dataFiles/qcfit-icon.ico')
mainRoot.mainloop()
