#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 21 10:04:21 2019

@author: rahul gupta (rgupta2)
"""

import tkinter as tk
import os, sys
import tkinter.filedialog
from tkinter import messagebox


def thankYou():
    def close():
        root.after(1, root.withdraw())
        root.after(1, root.destroy())
        sys.exit()

    root = tkinter.Tk()
    root.title("Finish!!")
    root.wm_geometry("330x260+100+100")
    location = os.getcwd()
    tkinter.Label(root, text="Thank you! \n\n\n output file has been created at : \n\n " + location,
                  justify=tkinter.CENTER, padx=20, pady=40).pack()
    tkinter.Button(root, text="Close", command=close, pady=10).pack()
    root.iconbitmap('dataFiles/seriqc-icon.ico')
    root.mainloop()


def getPath(format):
    root = tk.Tk()
    root.withdraw()
    root.update()
    if format == "qa0":
        path = tkinter.filedialog.askopenfilename(parent=root, initialdir="/", title='Upload QA0 file',
                                                  filetypes=(("QA0 files", "*.QA0"), ("all files", "*.*")))
    if format == "csv":
        path = tkinter.filedialog.askopenfilename(parent=root, initialdir="/", title='Upload CSV file',
                                                  filetypes=(("csv files", "*.csv"), ("all files", "*.*")))

    if len(path) < 1:
        messagebox.showerror("Error", "File not provided. Please Try Again.")
        root.after(3, root.destroy())
        sys.exit()
    root.after(1, root.destroy())
    return path


def validateFile(path, ext1, ext2):
    root = tk.Tk()
    root.withdraw()
    if len(path) < 1:
        messagebox.showerror("Error", "File not provided. Please Try Again.")
        root.after(3, root.destroy())

        sys.exit()
    else:
        if path[len(path) - 4:] == ext1:
            root.after(3, root.destroy())
            return True
        else:
            if ext2 is not None:
                if path[len(path) - 4:] == ext2:
                    root.after(3, root.destroy())
                    return True
                else:
                    messagebox.showerror("Error", "File format not supported.")
                    root.after(3, root.destroy())
                    sys.exit()
            else:
                messagebox.showerror("Error", "File format not supported.")
                root.after(3, root.destroy())
                sys.exit()


def getData():
    root = tk.Tk()
    root.wm_geometry("500x375+450+250")
    root.title("Provide Data")

    def hitSubmit():
        f = open('temp', 'w+')
        f.write(measVar.get() + '\n')
        f.write(repVar.get() + '\n')
        f.write(avgVar.get() + '\n')
        f.close()
        root.after(1, root.destroy())

    Label = tk.Label(root, text='What is your measurement frequency?')
    Label.pack()
    Label.place(x=30, y=45)
    measVar = tk.StringVar(root)
    measList = ['1', '5', '15', '60']
    measVar.set(measList[0])  # set the default option
    measMenu = tk.OptionMenu(root, measVar, *measList)
    measMenu.pack()
    measMenu.config(width=6)
    measMenu.place(x=140, y=90)
    """text = tk.Entry(root)
    text.pack()
    text.config(width=8)
    text.place(x=140, y=90)
    text.delete(0, tk.END)
    text.insert(0, measFreq)"""

    Label2 = tk.Label(root, text='What is your reporting Interval?')
    Label2.pack()
    Label2.place(x=30, y=145)
    repVar = tk.StringVar(root)
    repVar.set(measList[0])  # set the default option
    repMenu = tk.OptionMenu(root, repVar, *measList)
    repMenu.pack()
    repMenu.config(width=6)
    repMenu.place(x=140, y=190)
    """text2 = tk.Entry(root)
    text2.pack()
    text2.config(width=8)
    text2.place(x=140, y=190)
    text2.delete(0, tk.END)
    text2.insert(0, repFreq)"""
    avgVar = tk.StringVar(root)
    avgList = ['Yes', 'No']
    avgVar.set(avgList[1])  # set the default option

    Label3 = tk.Label(root, text="Is your data averaged?")
    Label3.pack()
    Label3.place(x=30, y=245)
    avgMenu = tk.OptionMenu(root, avgVar, *avgList)
    avgMenu.pack()
    avgMenu.config(width=6)
    avgMenu.place(x=140, y=290)
    submitButton = tk.Button(root, text="Submit", command=hitSubmit)
    submitButton.pack()
    submitButton.place(x=365, y=295)
    submitButton.config(width=10)
    root.iconbitmap('dataFiles/seriqc-icon.ico')
    root.mainloop()


'''
"""
def getData(measFreq, repFreq, avg):
    root = tk.Tk()
    root.wm_geometry("500x375+450+250")
    root.title("Provide Data")

    def hitSubmit():
        f = open('temp', 'w+')
        f.write(measVar.get() + '\n')
        f.write(repVar.get() + '\n')
        f.write(avgVar.get() + '\n')
        f.close()
        root.after(1, root.destroy())

    Label = tk.Label(root, text='What is your measurement frequency?')
    Label.pack()
    Label.place(x=30, y=45)
    measVar = tk.StringVar(root)
    measList = ['1', '5', '15', '60']
    measVar.set(measFreq)  # set the default option
    measMenu = tk.OptionMenu(root, measVar, *measList)
    measMenu.pack()
    measMenu.config(width=6)
    measMenu.place(x=140, y=90)
    """text = tk.Entry(root)
    text.pack()
    text.config(width=8)
    text.place(x=140, y=90)
    text.delete(0, tk.END)
    text.insert(0, measFreq)"""

    Label2 = tk.Label(root, text='What is your reporting Interval?')
    Label2.pack()
    Label2.place(x=30, y=145)
    repVar = tk.StringVar(root)
    repVar.set(repFreq)  # set the default option
    repMenu = tk.OptionMenu(root, repVar, *measList)
    repMenu.pack()
    repMenu.config(width=6)
    repMenu.place(x=140, y=190)
    """text2 = tk.Entry(root)
    text2.pack()
    text2.config(width=8)
    text2.place(x=140, y=190)
    text2.delete(0, tk.END)
    text2.insert(0, repFreq)"""
    avgVar = tk.StringVar(root)
    avgList = ['Yes', 'No']
    avgVar.set(avg)  # set the default option

    Label3 = tk.Label(root, text="Is your data averaged?")
    Label3.pack()
    Label3.place(x=30, y=245)
    avgMenu = tk.OptionMenu(root, avgVar, *avgList)
    avgMenu.pack()
    avgMenu.config(width=6)
    avgMenu.place(x=140, y=290)
    submitButton = tk.Button(root, text="Submit", command=hitSubmit)
    submitButton.pack()
    submitButton.place(x=365, y=295)
    submitButton.config(width=10)
    submitButton.configure(background='blue')
    root.mainloop()
"""'''


def getEntry(caption, Note, defaultVal):
    root = tk.Tk()
    root.wm_geometry("500x150+350+250")
    root.title("Provide Data")

    def hitSubmit():
        f = open('temp', 'w+')
        f.write(text.get() + '\n')
        f.close()
        root.after(1, root.destroy())

    Label = tk.Label(root, text=caption)
    Label.pack()
    Label.place(x=30, y=45)
    text = tk.Entry(root)
    text.pack()
    text.place(x=270, y=45)
    text.delete(0, tk.END)
    text.insert(0, defaultVal)

    Label2 = tk.Label(root, text=Note)
    Label2.pack()
    Label2.place(x=30, y=80)

    submitButton = tk.Button(root, text="Submit", command=hitSubmit)
    submitButton.pack()
    submitButton.place(x=300, y=110)
    submitButton.config(width=10)
    submitButton.configure(background='blue')
    root.iconbitmap('dataFiles/seriqc-icon.ico')
    root.mainloop()


def getParams():
    root = tk.Tk()
    root.wm_geometry("500x400+150+150")
    root.title("SERI - QC")

    def hitSubmit():
        f = open('temp', 'w+')
        f.write(source.get() + '\n')
        f.write(frequency.get() + '\n')
        f.write(elev.get() + '\n')
        f.write(pres.get() + '\n')
        f.write(temp.get() + '\n')
        f.close()
        root.after(1, root.destroy())

    label = tk.Label(root, text="Please provide the parameters.")
    label.pack(side='left')
    label.config(font=("Bookman", 15))
    label.place(x=10, y=20)

    source = tk.StringVar(root)
    frequency = tk.StringVar(root)

    sourceList = ['MIDC', 'Other']
    source.set('-select-')  # set the default option
    frequencyList = ['Hourly', 'Minute']
    frequency.set('-select-')  # set the default option

    sourceLabel = tk.Label(root, text="Data Source")
    sourceLabel.pack()
    sourceLabel.place(x=100, y=55)
    sourceMenu = tk.OptionMenu(root, source, *sourceList)
    sourceMenu.pack()
    sourceMenu.config(width=18)
    sourceMenu.place(x=300, y=55)

    frequencyLabel = tk.Label(root, text="Data Frequency")
    frequencyLabel.pack()
    frequencyLabel.place(x=100, y=90)
    frequencyMenu = tk.OptionMenu(root, frequency, *frequencyList)
    frequencyMenu.pack()
    frequencyMenu.config(width=18)
    frequencyMenu.place(x=300, y=90)

    elevationLabel = tk.Label(root, text='Elevation')
    elevationLabel.pack()
    elevationLabel.place(x=100, y=125)
    elev = tk.Entry(root)
    elev.pack()
    elev.place(x=300, y=125)
    elev.delete(0, tk.END)
    # elev.insert(0, 1025)

    pressureLabel = tk.Label(root, text='Pressure')
    pressureLabel.pack()
    pressureLabel.place(x=100, y=160)
    pres = tk.Entry(root)
    pres.pack()
    pres.place(x=300, y=160)
    pres.delete(0, tk.END)
    # pres.insert(0, 1025)

    temperatureLabel = tk.Label(root, text='Temperature')
    temperatureLabel.pack()
    temperatureLabel.place(x=100, y=195)
    temp = tk.Entry(root)
    temp.pack()
    temp.place(x=300, y=195)
    temp.delete(0, tk.END)
    # temp.insert(0, 1025)

    submitButton = tk.Button(root, text="Submit", command=hitSubmit)
    submitButton.pack()
    submitButton.place(x=300, y=230)
    submitButton.config(width=10)
    submitButton.configure(background='blue')
    root.iconbitmap('dataFiles/seriqc-icon.ico')
    root.mainloop()
