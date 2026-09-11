#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2019-08-01 11:29

@author : rahul gupta (rgupta2)

"""
from typing import List, Union
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import webbrowser
import os
from matplotlib import ticker


def plot_graphs(data, flag='IQCGlobal', repfreq=1):
    # Data preparation / creating column for graph
    # Copy after filtering to avoid chained-assignment warnings.
    data = data.loc[data["ETR"] > 0].copy()
    Global = data[data.columns[2]].map(float)
    Direct = data[data.columns[3]].map(float)
    Diffuse = data[data.columns[4]].map(float)
    data['dateOnly'] = data.date.dt.date
    data['timeOnly'] = data.date.dt.strftime('%H:%M')
    data['qc_flag'] = data[flag]
    data['gKt'] = -1
    data['gKn'] = -1
    data['gKd'] = -1

    # Flag based operations
    data.loc[((data[flag] == 7) | (data[flag] == 8)), 'qc_flag'] = 99

    # Solzen based operations for Kt ,Kn and Kd.
    data.loc[(data['solzen'] < 89.9), 'gKt'] = Global / data['ETR']
    data.loc[(data['solzen'] < 89.9), 'gKn'] = Direct / data['ETRN']
    data.loc[(data['solzen'] < 89.9), 'gKd'] = Diffuse / data['ETR']
    data.loc[(data['gKt'] == np.inf) | (data['gKt'] < 0), 'gKt'] = 0
    data.loc[(data['gKn'] == np.inf) | (data['gKn'] < 0), 'gKn'] = 0
    data.loc[(data['gKd'] == np.inf) | (data['gKd'] < 0), 'gKd'] = 0
    data.loc[(data['ETR'] == 0), 'gKt'] = 0
    data.loc[(data['ETR'] == 0), 'gKn'] = 0
    data.loc[(data['ETR'] == 0), 'gKd'] = 0

    data.loc[(data[flag] == 99), 'gKt'] = 1
    data.loc[(data[flag] == 99), 'gKn'] = 1
    data.loc[(data[flag] == 99), 'gKd'] = 1

    # Creating matrix and sorting.
    matrix1 = data.pivot(index="dateOnly", columns="timeOnly", values="qc_flag")
    matrix1 = matrix1.reindex(sorted(matrix1.columns), axis=1)

    matrix2 = data.pivot(index="dateOnly", columns="timeOnly", values="gKt")
    matrix2 = matrix2.reindex(sorted(matrix2.columns), axis=1)

    matrix3 = data.pivot(index="dateOnly", columns="timeOnly", values="gKn")
    matrix3 = matrix3.reindex(sorted(matrix3.columns), axis=1)

    matrix4 = data.pivot(index="dateOnly", columns="timeOnly", values="gKd")
    matrix4 = matrix4.reindex(sorted(matrix4.columns), axis=1)

    # Time based operations for X axis customizations
    xAxis = []
    for index, time in enumerate(matrix1.columns):
        if index == 0 or index == len(matrix1.columns) - 1:
            xAxis.append(time)
        else:
            if str(time)[3:5] == "00":
                xAxis.append(int(str(time)[0:2]))
            else:
                xAxis.append("")
    # remove 2nd and second last ticker if overlapping
    ticks = [val for val in xAxis if val != ""]

    if str(ticks[0])[3:5] != "00":
        xAxis[xAxis.index(ticks[1])] = ""
    if str(ticks[-1])[3:5] != "00":
        xAxis[xAxis.index(ticks[-2])] = ""

    xAxis[xAxis.index(12)] = "Noon"
    temp = xAxis

    # Updating matrix column for time in X-axis
    matrix1.columns = temp
    matrix2.columns = temp
    matrix3.columns = temp
    matrix4.columns = temp

    # Operations for Y axis
    # yAxis = [""] * matrix1.index
    indexVals = [""] * len(matrix1.index)
    if len(matrix1.index) < 48:
        pass
    else:
        gap = int(len(matrix1.index) / 24)  # we will have only 24 ticks
        i = 0
        while i < len(matrix1.index):
            if (i == 0) or (i == len(matrix1.index)) or (i % (gap * 5) == 0):
                indexVals[i] = matrix1.index[i].strftime('%b %d %Y')
            else:
                indexVals[i] = matrix1.index[i].strftime('%b %d')
            i += gap

    if indexVals[-1] == "":
        backIndex = (len(indexVals) - 1) - (len(indexVals) - 1) % gap  # last index of data minus Remainder(modulus)
        indexVals[backIndex] = ""
        indexVals[-1] = matrix1.index[-1].strftime('%b %d %Y')

    # set Index
    matrix1.index = indexVals

    # ticklabels = [''] * len(matrix1.index)
    # ticklabels[::1] = [item.strftime('%b %d') for item in matrix1.index[::1]]
    """ticklabels[::1] = [item.strftime('%b %d') for item in matrix2.index[::1]]
    ticklabels[::1] = [item.strftime('%b %d') for item in matrix3.index[::1]]
    ticklabels[::1] = [item.strftime('%b %d') for item in matrix4.index[::1]]"""
    # Every 12th ticklabel includes the year
    # ticklabels[::12] = [item.strftime('%b %d\n%Y') for item in matrix.index[::12]]

    font_axis = {'family': 'arial',
                 'color': 'darkred',
                 'weight': 'bold',
                 'size': 12,
                 }

    font_title = {'family': 'arial',
                  'color': 'darkred',
                  'weight': 'bold',
                  'size': 16,
                  }

    f, (ax, ax1, ax2, ax3) = plt.subplots(1, 4,
                                          gridspec_kw={'width_ratios': [1.8, 1.8, 1.8, 1.8]}, figsize=(20, 10))
    ax.get_shared_y_axes().join(ax1, ax2, ax3)
    sns.set(style="ticks", color_codes=True)
    g = sns.heatmap(matrix1, cmap="jet", xticklabels=True, yticklabels=True, cbar=True, ax=ax, vmin=0, vmax=100)
    g.set_ylabel("Days", fontdict=font_axis)
    g.set_xlabel("Time in hours", fontdict=font_axis)
    g1 = sns.heatmap(matrix2, cmap="jet", xticklabels=True, cbar=True, yticklabels=False, ax=ax1, vmin=0, vmax=1)
    g1.set_ylabel('')
    g1.set_xlabel("Time in hours", fontdict=font_axis)
    g2 = sns.heatmap(matrix3, cmap="jet", xticklabels=True, yticklabels=False, cbar=True, ax=ax2, vmin=0, vmax=1)
    g2.set_ylabel('')
    g2.set_xlabel("Time in hours", fontdict=font_axis)
    g2.set_yticks([])
    g3 = sns.heatmap(matrix4, cmap="jet", xticklabels=True, yticklabels=False, ax=ax3, cbar=True, vmin=0, vmax=1)
    g3.set_ylabel('')
    g3.set_xlabel("Time in hours", fontdict=font_axis)

    # Setting titles of sub plots
    ax.set_title(flag[3:], fontdict=font_title)
    ax1.set_title("Kt", fontdict=font_title)
    ax2.set_title("Kn", fontdict=font_title)
    ax3.set_title("Kd", fontdict=font_title)
    ax.tick_params(length=0)
    ax1.tick_params(length=0)
    ax2.tick_params(length=0)
    ax3.tick_params(length=0)

    # Setting grids for sub plots

    # g.yaxis.set_major_formatter(ticker.FixedFormatter(ticklabels))
    plt.savefig('Graph.png', bbox_inches='tight', dpi=1000)
    # plt.show()
    return f


def get_flg_score(data):
    blank = [0, 0, 0, 0, 0, 0, 0]
    stats_d = pd.DataFrame({'Global': blank, 'Direct': blank, 'Diffuse': blank})
    stats_n = pd.DataFrame({'Global': blank, 'Direct': blank, 'Diffuse': blank})
    threshold1 = ((5 + 1) * 4 + 1)
    threshold2 = ((10 + 1) * 4. + 1)
    qc_flags = ['IQCGlobal', 'IQCDirect', 'IQCDiffuse']
    for i in range(3):
        j = 0
        stats_d.iloc[j, i] = len(data[(data[qc_flags[i]] == 99) & data['solzen'] != 0])  # missing

        stats_d.iloc[j + 1, i] = len(data[(data[qc_flags[i]] != 99) & data['solzen'] != 0])  # present

        stats_d.iloc[j + 2, i] = len(data[(data[qc_flags[i]] != 99) & (data[qc_flags[i]] != 7) & (
                data[qc_flags[i]] != 8) & (data[qc_flags[i]] != 9) & (data['solzen'] != 0) & (
                                                 data[qc_flags[i]] <= threshold1)])  # threshold 5%

        stats_d.iloc[j + 3, i] = len(data[(data[qc_flags[i]] != 99) & (data[qc_flags[i]] != 7) & (
                data[qc_flags[i]] != 8) & (data[qc_flags[i]] != 9) & (data['solzen'] != 0) & (
                                                 data[qc_flags[i]] > threshold2)])  # threshold 10%

        stats_d.iloc[j + 4, i] = len(data[(data[qc_flags[i]] == 7) & (data['solzen'] != 0)])  # below empirical

        stats_d.iloc[j + 5, i] = len(data[(data[qc_flags[i]] == 8) & (data['solzen'] != 0)])  # above empirical

        stats_d.iloc[j + 6, i] = len(data[(data[qc_flags[i]] == 9) & (data['solzen'] != 0)])  # strange

    for i in range(3):
        j = 0
        stats_n.iloc[j, i] = len(data[(data[qc_flags[i]] == 99) & (data['solzen'] == 0)])  # missing

        stats_n.iloc[j + 1, i] = len(data[(data[qc_flags[i]] != 99) & (data['solzen'] == 0)])  # present

        stats_n.iloc[j + 2, i] = len(data[(data[qc_flags[i]] != 99) & (data[qc_flags[i]] != 7) & (
                data[qc_flags[i]] != 8) & (data[qc_flags[i]] != 9) & (data['solzen'] == 0) & (
                                                 data[qc_flags[i]] <= threshold1)])  # threshold 5%

        stats_n.iloc[j + 3, i] = len(data[(data[qc_flags[i]] != 99) & (data[qc_flags[i]] != 7) & (
                data[qc_flags[i]] != 8) & (data[qc_flags[i]] != 9) & (data['solzen'] == 0) & (
                                                 data[qc_flags[i]] > threshold2)])  # threshold 10%

        stats_n.iloc[j + 4, i] = len(data[(data[qc_flags[i]] == 7) & (data['solzen'] == 0)])  # below empirical

        stats_n.iloc[j + 5, i] = len(data[(data[qc_flags[i]] == 8) & (data['solzen'] == 0)])  # above empirical

        stats_n.iloc[j + 6, i] = len(data[(data[qc_flags[i]] == 9) & (data['solzen'] == 0)])  # strange

    stats_d = stats_d
    stats_n = stats_n
    for i in range(3):
        stats_d.loc[(stats_d[stats_d.columns[i]] != 0), stats_d.columns[i]] = (stats_d[
                                                                                   stats_d.columns[i]] /
                                           stats_d.iloc[1, i]) * 100
        stats_n.loc[(stats_d[stats_n.columns[i]] != 0), stats_n.columns[i]] = (stats_n[
                                                                                   stats_n.columns[i]] /
                                           stats_n.iloc[1, i]) * 100
    stats_d = stats_d.round(2)
    stats_n = stats_n.round(2)

    return stats_d, stats_n


def write_report(data, lat, long, timezone, resolution, site_name="BMS, NREL's SRRL Baseline Measurement System"):
    f = open('Report.html', 'w')
    day_score, night_score = get_flg_score(data)
    message = """



    <!DOCTYPE html>
    <html>
    <body>
      <p>
          <h1> 
               <center>
                """ + site_name + """</center> </h1> </p> 
                <figure> <center> <img src="Graph.png" alt="The Pulpit 
                Rock" width="1550" height="600"> </center> </figure> <br/>
                
                <p> <h2><u><center> Summary Statistics </center></u></h2></p><br/>



                <style>
                    table, th, td {
                                    border: 1px solid black;
                                }
                    th {
                        text-align: left;
                        }
                </style>

                <center><div style="width:70%"><table style="float: left; width:50%" >

                    <tr style="text-align: right;">
                    <th width = "150" rowspan="2"></th>
                    <th colspan="3"> <center> Day Time </center> </th>
                    <th rowspan="8" width =30> <center>  </center> </th>
                    <th colspan="3"> <center> Night time </center> </th>
    </tr>

  <tr>
      <th width="70"><center> Global </center></th>
      <th width="70"><center> Direct </center></th>
      <th width="70"><center> Diffuse </center></th>
      <th width="70"><center> Global </center></th>
      <th width="70"><center> Direct </center></th>
      <th width="70"><center> Diffuse </center></th>

    </tr>
    <tr>
      <th> Present </th>
      <td><center>""" + str(day_score.loc[1][0]) + """</center></td>
      <td><center>""" + str(day_score.loc[1][1]) + """</center></td>
      <td><center>""" + str(day_score.loc[1][2]) + """</center></td>
      <td><center>""" + str(night_score.loc[1][0]) + """</center></td>
      <td><center>""" + str(night_score.loc[1][1]) + """</center></td>
      <td><center>""" + str(night_score.loc[1][2]) + """</center></td>

    </tr>
    <tr>
      <th> Threshold 5% </th>
      <td><center>""" + str(day_score.loc[2][0]) + """</center></td>
      <td><center>""" + str(day_score.loc[2][1]) + """</center></td>
      <td><center>""" + str(day_score.loc[2][2]) + """</center></td>
      <td><center>""" + str(night_score.loc[2][0]) + """</center></td>
      <td><center>""" + str(night_score.loc[2][1]) + """</center></td>
      <td><center>""" + str(night_score.loc[2][2]) + """</center></td>

    </tr>
    <tr>
      <th> Threshold 10% </th>
      <td><center>""" + str(day_score.loc[3][0]) + """</center></td>
      <td><center>""" + str(day_score.loc[3][1]) + """</center></td>
      <td><center>""" + str(day_score.loc[3][2]) + """</center></td>
      <td><center>""" + str(night_score.loc[3][0]) + """</center></td>
      <td><center>""" + str(night_score.loc[3][1]) + """</center></td>
      <td><center>""" + str(night_score.loc[3][2]) + """</center></td>

    </tr>
    <tr>
      <th> Below Empirical </th>
      <td><center>""" + str(day_score.loc[4][0]) + """</center></td>
      <td><center>""" + str(day_score.loc[4][1]) + """</center></td>
      <td><center>""" + str(day_score.loc[4][2]) + """</center></td>
      <td><center>""" + str(night_score.loc[4][0]) + """</center></td>
      <td><center>""" + str(night_score.loc[4][1]) + """</center></td>
      <td><center>""" + str(night_score.loc[4][2]) + """</center></td>

    </tr>
    <tr>
      <th> Above Empirical </th>
      <td><center>""" + str(day_score.loc[5][0]) + """</center></td>
      <td><center>""" + str(day_score.loc[5][1]) + """</center></td>
      <td><center>""" + str(day_score.loc[5][2]) + """</center></td>
      <td><center>""" + str(night_score.loc[5][0]) + """</center></td>
      <td><center>""" + str(night_score.loc[5][1]) + """</center></td>
      <td><center>""" + str(night_score.loc[5][2]) + """</center></td>

    </tr>
    <tr>
      <th> Strange but true </th>
      <td><center>""" + str(day_score.loc[6][0]) + """</center></td>
      <td><center>""" + str(day_score.loc[6][1]) + """</center></td>
      <td><center>""" + str(day_score.loc[6][2]) + """</center></td>
      <td><center>""" + str(night_score.loc[6][0]) + """</center></td>
      <td><center>""" + str(night_score.loc[6][1]) + """</center></td>
      <td><center>""" + str(night_score.loc[6][2]) + """</center></td>

    </tr>
</table> 

<table style="float: right; width:20%">
  <tr>
    <th colspan="2" ><center> Site Information</center></th>
  <tr>
    <th>Latitude</td>
    <td>""" + str(lat) + """</td>
  </tr>
  <tr>
    <th>Longitude</td>
    <td>""" + str(long) + """</td>
  </tr>
  <tr>
    <th>Time Zone</td>
    <td>""" + str(timezone) + """</td>
  </tr>
  <tr>
    <th>Data Resolution</td>
    <td>""" + str(resolution) + """</td>
  </tr>
</table></div></center>

<br/>
<br/>
<br/><br/><br/><br/><br/><br/><br/><br/><br/></br>


<div> *Flag statistics indicate percent or present data. 
                                <span style="float: right">*Developed by the National Renewable Energy Laboratory.</span>  </body> </div>

               </html>   """

    f.write(message)
    f.close()
    filename = os.getcwd() + 'Report.html'
    webbrowser.open_new_tab(filename)

# write_report(data, lat, long, timezone, site_name="BMS, NREL's SRRL Baseline Measurement System")
