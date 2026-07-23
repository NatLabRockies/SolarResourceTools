#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 21 09:27:41 2019

@author: rahul gupta (rgupta2)
"""
import sys
from tkinter import messagebox
import tkinter as tk

import forms as frm
import utills
import time
import pandas as pd
import math
from spa import SPA
import numpy as np
import datetime as datetime
import statistics
import dataPlots


def takeValues():
    meas_freq = 0
    rep_freq = 0
    avgd = '-select-'
    try:
        while ((meas_freq == 0) or (rep_freq == 0) or (avgd == '-select-') or (meas_freq < 1) or (meas_freq > 60) or (
                rep_freq < 1) or (rep_freq > 60)):
            meas_freq = 0
            rep_freq = 0
            avgd = '-select-'
            # frm.getData(meas_freq, rep_freq, avgd)
            frm.getData()
            dList = utills.readList('temp')
            meas_freq = int(dList[0])
            rep_freq = int(dList[1])
            avgd = dList[2]
        if ((meas_freq == 0) or (rep_freq == 0) or (avgd == '-select-') or (meas_freq < 1) or (meas_freq > 60) or (
                rep_freq < 1) or (rep_freq > 60)):
            takeValues()

    except ValueError:
        while (meas_freq == 0) or (rep_freq == 0) or (avgd == '-select-'):
            # frm.getData(meas_freq, rep_freq, avgd)
            frm.getData()
            dList = utills.readList('temp')
            meas_freq = int(dList[0])
            rep_freq = int(dList[1])
            avgd = dList[2]
        if ((meas_freq == 0) or (rep_freq == 0) or (avgd == '-select-') or (meas_freq < 1) or (meas_freq > 60) or (
                rep_freq < 1) or (rep_freq > 60)):
            takeValues()
    return meas_freq, rep_freq, avgd


def label4000(curveRight, data):
    data['flag3'] = 0  # reseting temporary flag.
    data['flag4'] = 0  # reseting temporary flag.
    data['flag5'] = 0  # reseting temporary flag.

    a = data[data['tempLabel'] == 'label4000']['Xn2']
    b = data[data['tempLabel'] == 'label4000']['Xn']
    c = data[data['tempLabel'] == 'label4000']['Xt2']
    d = data[data['tempLabel'] == 'label4000']['Xt']

    data.loc[(data['tempLabel'] == 'label4000'), 'Dist'] = [(pow(i - j, 2) + pow(k - l, 2)) for (i, j, k, l) in
                                                            zip(a, b, c, d)]

    data.loc[(data['tempLabel'] == 'label4000') & (data['Dist'] <= data['dPrev']), 'flag3'] = 1

    # flag3 Truth case

    data.loc[(data['tempLabel'] == 'label4000') & (data['flag3'] == 1), 'Xn'] = data['Xn'] + data['yDir']
    data.loc[(data['tempLabel'] == 'label4000') & (data['flag3'] == 1) & (data['Xn'] <= data['KNmax']) & (
            data['Xn'] >= 1), 'flag4'] = 1

    # flag3 and flag4 Truth case

    data.loc[(data['tempLabel'] == 'label4000') & (data['flag3'] == 1) & (data['flag4'] == 1), 'J'] = data['Xn']
    a = data[(data['tempLabel'] == 'label4000') & (data['flag3'] == 1) & (data['flag4'] == 1)]['Ir'].map(int)
    b = data[(data['tempLabel'] == 'label4000') & (data['flag3'] == 1) & (data['flag4'] == 1)]['J'].map(int)
    c = data[(data['tempLabel'] == 'label4000') & (data['flag3'] == 1) & (data['flag4'] == 1)]['off_R']
    data.loc[(data['tempLabel'] == 'label4000') & (data['flag3'] == 1) & (data['flag4'] == 1), 'Xt'] = [
        (curveRight[i - 1][j - 1] + k) for (i, j, k) in zip(a, b, c)]

    a = data[(data['tempLabel'] == 'label4000') & (data['flag3'] == 1) & (data['flag4'] == 1)]['Xt']
    b = data[(data['tempLabel'] == 'label4000') & (data['flag3'] == 1) & (data['flag4'] == 1)]['KTmax']
    data.loc[(data['tempLabel'] == 'label4000') & (data['flag3'] == 1) & (data['flag4'] == 1), 'Xt'] = [min(i, j) for
                                                                                                        (i, j) in
                                                                                                        zip(a, b)]
    data.loc[(data['tempLabel'] == 'label4000') & (data['flag3'] == 1) & (data['flag4'] == 1), 'Xt'] = [max(i, 1) for i
                                                                                                        in a]
    data.loc[(data['tempLabel'] == 'label4000') & (data['flag3'] == 1) & (data['flag4'] == 1), 'dPrev'] = data['Dist']

    # flag3 Truth and flag4 False case

    data.loc[
        (data['tempLabel'] == 'label4000') & (data['flag3'] == 1) & (data['flag4'] == 0) & (data['Xn'] < 1), 'Xt'] = 0
    data.loc[
        (data['tempLabel'] == 'label4000') & (data['flag3'] == 1) & (data['flag4'] == 0) & (data['Xn'] < 1), 'dPrev'] = \
        data['Dist']

    # Xn < 1 False case

    data.loc[(data['tempLabel'] == 'label4000') & (data['flag3'] == 1) & (data['flag4'] == 0) & (
            data['Xn'] >= 1), 'sqc2_flag'] = 0  # updating the flag
    data.loc[(data['tempLabel'] == 'label4000') & (data['flag3'] == 1) & (data['flag4'] == 0) & (
            data['Xn'] >= 1), 'tempLabel'] = 'none'  # reseting label for data points those are done.

    # flag3 False case

    data.loc[(data['tempLabel'] == 'label4000') & (data['flag3'] == 0) & (data['yDir'] > 0), 'flag5'] = 1

    # flag3 False and flag5 Truth case

    data.loc[(data['tempLabel'] == 'label4000') & (data['flag3'] == 0) & (data['flag5'] == 1), 'Xn'] = data['Xn'] - 1
    data.loc[(data['tempLabel'] == 'label4000') & (data['flag3'] == 0) & (data['flag5'] == 1), 'yDir'] = - 1

    # Xn >= 1 Truth case

    data.loc[
        (data['tempLabel'] == 'label4000') & (data['flag3'] == 0) & (data['flag5'] == 1) & (data['Xn'] >= 1), 'J'] = \
        data['Xn']
    a = data[(data['tempLabel'] == 'label4000') & (data['flag3'] == 0) & (data['flag5'] == 1) & (data['Xn'] >= 1)][
        'Ir'].map(int)
    b = data[(data['tempLabel'] == 'label4000') & (data['flag3'] == 0) & (data['flag5'] == 1) & (data['Xn'] >= 1)][
        'J'].map(int)
    c = data[(data['tempLabel'] == 'label4000') & (data['flag3'] == 0) & (data['flag5'] == 1) & (data['Xn'] >= 1)][
        'off_R']
    data.loc[
        (data['tempLabel'] == 'label4000') & (data['flag3'] == 0) & (data['flag5'] == 1) & (data['Xn'] >= 1), 'Xt'] = [
        (curveRight[i - 1][j - 1] + k) for (i, j, k) in zip(a, b, c)]

    a = data[(data['tempLabel'] == 'label4000') & (data['flag3'] == 0) & (data['flag5'] == 1) & (data['Xn'] >= 1)]['Xt']
    b = data[(data['tempLabel'] == 'label4000') & (data['flag3'] == 0) & (data['flag5'] == 1) & (data['Xn'] >= 1)][
        'KTmax']
    data.loc[
        (data['tempLabel'] == 'label4000') & (data['flag3'] == 0) & (data['flag5'] == 1) & (data['Xn'] >= 1), 'Xt'] = [
        min(i, j) for (i, j) in zip(a, b)]
    data.loc[
        (data['tempLabel'] == 'label4000') & (data['flag3'] == 0) & (data['flag5'] == 1) & (data['Xn'] >= 1), 'Xt'] = [
        max(i, 1) for i in a]
    data.loc[
        (data['tempLabel'] == 'label4000') & (data['flag3'] == 0) & (data['flag5'] == 1) & (data['Xn'] >= 1), 'dPrev'] = \
        data['Dist']

    # Xn >= 1 False case

    data.loc[(data['tempLabel'] == 'label4000') & (data['flag3'] == 0) & (data['flag5'] == 1) & (
            data['Xn'] < 1), 'sqc2_flag'] = 0  # updating the flag
    data.loc[(data['tempLabel'] == 'label4000') & (data['flag3'] == 0) & (data['flag5'] == 1) & (
            data['Xn'] < 1), 'tempLabel'] = 'none'  # reseting label for data points those are done.

    # flag3 and flag5 False case

    data.loc[(data['tempLabel'] == 'label4000') & (data['flag3'] == 0) & (
            data['flag5'] == 0), 'sqc2_flag'] = 0  # updating the flag
    data.loc[(data['tempLabel'] == 'label4000') & (data['flag3'] == 0) & (
            data['flag5'] == 0), 'tempLabel'] = 'none'  # reseting label for data points those are done.


def label2000(curveLeft, data):
    """The point is to the left of the left curve.
      * I seek the  distance (squared) (x^2 + y^2) to each point on
      * the curve and compare that to the minimum distance that I had
      * saved earlier.  I start with the point on the curve directly to
      * the right of my point and march up the curve.  As soon as the
      * distance increases (the curve moves away from my point, I reverse
      * my direction (yDir) and move down the curve.  The closest point
      * determines the flag value.
    """

    data['flag3'] = 0  # reseting temporary flag.
    data['flag4'] = 0  # reseting temporary flag.
    data['flag5'] = 0  # reseting temporary flag.

    # find minimum distance.

    a = data[data['tempLabel'] == 'label2000']['Xn2']
    b = data[data['tempLabel'] == 'label2000']['Xn']
    c = data[data['tempLabel'] == 'label2000']['Xt2']
    d = data[data['tempLabel'] == 'label2000']['Xt']

    data.loc[(data['templabel'] == 'label2000'), 'Dist'] = [(pow(i - j, 2) + pow(k - l, 2)) for (i, j, k, l) in
                                                            zip(a, b, c, d)]

    '''New distance is new minimum.  Increment the value of Kn*100 (J),
      * and, if we haven't run off the map, get another curve point
      * and try again.
    '''

    data.loc[(data['tempLabel'] == 'label2000') & (data['Dist'] <= data['dPrev']), 'flag3'] = 1

    # flag3 Truth case

    data.loc[(data['tempLabel'] == 'label2000') & (data['flag3'] == 1), 'Xn'] = data['Xn'] + data['yDir']
    data.loc[(data['tempLabel'] == 'label2000') & (data['flag3'] == 1) & (data['Xn'] <= data['KNmax']) & (
            data['Xn'] >= 1), 'flag4'] = 1

    # flag3 and flag4 Truth case

    data.loc[(data['tempLabel'] == 'label2000') & (data['flag3'] == 1) & (data['flag4'] == 1), 'J'] = data['Xn']
    a = data[(data['tempLabel'] == 'label2000') & (data['flag3'] == 1) & (data['flag4'] == 1)]['Il'].map(int)
    b = data[(data['tempLabel'] == 'label2000') & (data['flag3'] == 1) & (data['flag4'] == 1)]['J'].map(int)
    c = data[(data['tempLabel'] == 'label2000') & (data['flag3'] == 1) & (data['flag4'] == 1)]['off_L']
    data.loc[(data['tempLabel'] == 'label2000') & (data['flag3'] == 1) & (data['flag4'] == 1), 'Xt'] = [
        (curveLeft[i - 1][j - 1] + k) for (i, j, k) in zip(a, b, c)]

    a = data[(data['tempLabel'] == 'label2000') & (data['flag4'] == 1)]['Xt']
    b = data[(data['tempLabel'] == 'label2000') & (data['flag4'] == 1)]['KTmax']
    data.loc[(data['tempLabel'] == 'label2000') & (data['flag3'] == 1) & (data['flag4'] == 1), 'Xt'] = [min(i, j) for
                                                                                                        (i, j) in
                                                                                                        zip(a, b)]
    data.loc[(data['tempLabel'] == 'label2000') & (data['flag3'] == 1) & (data['flag4'] == 1), 'Xt'] = [max(i, 1) for i
                                                                                                        in a]
    data.loc[(data['tempLabel'] == 'label2000') & (data['flag3'] == 1) & (data['flag4'] == 1), 'dPrev'] = data['Dist']

    # flag3 Truth and flag4 False case

    data.loc[
        (data['tempLabel'] == 'label2000') & (data['flag3'] == 1) & (data['flag4'] == 0) & (data['Xn'] < 1), 'Xt'] = \
        data['KTmax']
    data.loc[
        (data['tempLabel'] == 'label2000') & (data['flag3'] == 1) & (data['flag4'] == 0) & (data['Xn'] < 1), 'dPrev'] = \
        data['Dist']

    # Xn < 1 False case

    data.loc[(data['tempLabel'] == 'label2000') & (data['flag3'] == 1) & (data['flag4'] == 0) & (
            data['Xn'] >= 1), 'sqc2_flag'] = 0  # updating the flag
    data.loc[(data['tempLabel'] == 'label2000') & (data['flag3'] == 1) & (data['flag4'] == 0) & (
            data['Xn'] >= 1), 'tempLabel'] = 'none'  # reseting label for data points those are done.

    ''' /*
      * The new distance is greater than the old one.  If we were going
      * up, reverse direction and go down.  If we are not off the map,
      * get another curve point and try again.
      */

    '''

    # flag3 False case

    data.loc[(data['tempLabel'] == 'label2000') & (data['flag3'] == 0) & (data['yDir'] > 0), 'flag5'] = 1

    # flag3 False and flag5 Truth case

    data.loc[(data['tempLabel'] == 'label2000') & (data['flag3'] == 0) & (data['flag5'] == 1), 'Xn'] = data['Xn'] - 1
    data.loc[(data['tempLabel'] == 'label2000') & (data['flag3'] == 0) & (data['flag5'] == 1), 'yDir'] = - 1

    # Xn >= 1 Truth case

    data.loc[
        (data['tempLabel'] == 'label2000') & (data['flag3'] == 0) & (data['flag5'] == 1) & (data['Xn'] >= 1), 'J'] = \
        data['Xn']
    a = data[(data['tempLabel'] == 'label2000') & (data['flag3'] == 0) & (data['flag5'] == 1) & (data['Xn'] >= 1)][
        'Il'].map(int)
    b = data[(data['tempLabel'] == 'label2000') & (data['flag3'] == 0) & (data['flag5'] == 1) & (data['Xn'] >= 1)][
        'J'].map(int)
    c = data[(data['tempLabel'] == 'label2000') & (data['flag3'] == 0) & (data['flag5'] == 1) & (data['Xn'] >= 1)][
        'off_l']
    data.loc[
        (data['tempLabel'] == 'label2000') & (data['flag3'] == 0) & (data['flag5'] == 1) & (data['Xn'] >= 1), 'Xt'] = [
        (curveLeft[i - 1][j - 1] + k) for (i, j, k) in zip(a, b, c)]

    a = data[(data['tempLabel'] == 'label2000') & (data['flag3'] == 0) & (data['flag5'] == 1) & (data['Xn'] >= 1)]['Xt']
    b = data[(data['tempLabel'] == 'label2000') & (data['flag3'] == 0) & (data['flag5'] == 1) & (data['Xn'] >= 1)][
        'KTmax']
    data.loc[
        (data['tempLabel'] == 'label2000') & (data['flag3'] == 0) & (data['flag5'] == 1) & (data['Xn'] >= 1), 'Xt'] = [
        min(i, j) for (i, j) in zip(a, b)]
    data.loc[
        (data['tempLabel'] == 'label2000') & (data['flag3'] == 0) & (data['flag5'] == 1) & (data['Xn'] >= 1), 'Xt'] = [
        max(i, 1) for i in a]
    data.loc[
        (data['tempLabel'] == 'label2000') & (data['flag3'] == 0) & (data['flag5'] == 1) & (data['Xn'] >= 1), 'dPrev'] = \
        data['Dist']

    # Xn >= 1 False case

    data.loc[(data['tempLabel'] == 'label2000') & (data['flag3'] == 0) & (data['flag5'] == 1) & (
            data['Xn'] < 1), 'sqc2_flag'] = 0  # updating the flag
    data.loc[(data['tempLabel'] == 'label2000') & (data['flag3'] == 0) & (data['flag5'] == 1) & (
            data['Xn'] < 1), 'tempLabel'] = 'none'  # reseting label for data points those are done.

    # flag3 and flag5 False case

    data.loc[(data['tempLabel'] == 'label2000') & (data['flag3'] == 0) & (
            data['flag5'] == 0), 'sqc2_flag'] = 0  # updating the flag
    data.loc[(data['tempLabel'] == 'label2000') & (data['flag3'] == 0) & (
            data['flag5'] == 0), 'tempLabel'] = 'none'  # reseting label for data points those are done.


def SQC_2C(KTvar, KNvar, qcFlag1, qcFlag2, data, curveLeft, curveRight):
    """The Gompertz boundaries are defined here.  The indices of Curve(I,J,K) are:

         I := 0 if the left boundary, 1 if the right. (in below discussion, subtract 1 from index)

         J := the curve type.  When I is 1, J spans 1 to 6; when I is 2, J spans 1 to 5.

         K := the value of 100 * Kn, rounded to the nearest integer.  If L < 1, L is reassigned to 1.  If K > 100,
         K is reassigned to 100.  This is because such values are both meaningless and troublesome for the Gompertz
         function. """

    # Assume success.

    data['IQC2'] = 0
    data['J'] = 0
    data['iFlag'] = 0
    data['IQCLow'] = 0
    data['IQCHigh'] = 0
    data['bot_R'] = 0
    data['top_R'] = 0
    data['off_R'] = 0
    data['bot_L'] = 0
    data['top_L'] = 0
    data['off_L'] = 0
    data['Xn2'] = 0
    data['Xt2'] = 0
    data['Xn'] = 0
    data['Dist'] = 0
    data['Xt'] = 0
    data['yDir'] = 0
    data['dPrev'] = 0
    data['flag3'] = 0  # initiating with 0.
    data['flag4'] = 0  # initiating with 0.
    data['flag5'] = 0  # initiating with 0.
    data['flag6'] = 0  # initiating with 0.
    data['label'] = 'none'  # labels for process flow.
    data['tempLabel'] = 'none'  # temp labels for process flow.

    data.loc[(data['sqc2_flag'] == 1), qcFlag1] = 2
    data.loc[(data['sqc2_flag'] == 1), qcFlag2] = 2

    # If KN is negative or greater than KNMAX, but KT lies within the Gompertz bounds, we should measure the vertical
    # distance only.

    data.loc[(data['sqc2_flag'] == 1), 'Xt2'] = data[KTvar]
    # data.loc[(data['sqc2_flag'] == 1 ),'XTmax2'] = data['KTmax']
    data.loc[(data['sqc2_flag'] == 1), 'Xn2'] = data[KNvar]
    # data.loc[(data['sqc2_flag'] == 1 ),'XNmax2'] = data['KNmax']

    data.loc[(data['sqc2_flag'] == 1), 'off_L'] = 2.5 * ((data[data['sqc2_flag'] == 1]['Jl']).map(int) - 1)
    data.loc[(data['sqc2_flag'] == 1), 'top_L'] = [curveLeft[i][j] for (i, j) in
                                                   zip((data[data['sqc2_flag'] == 1]['Il'].map(int) - 1),
                                                       (data[data['sqc2_flag'] == 1]['KNmax'].map(int) - 1))] + \
                                                  data[data['sqc2_flag'] == 1]['off_L']
    data.loc[(data['sqc2_flag'] == 1), 'top_L'] = [max(i, 0) for i in (data[data['sqc2_flag'] == 1]['top_L'])]
    data.loc[(data['sqc2_flag'] == 1), 'top_L'] = [min(i, j) for (i, j) in zip((data[data['sqc2_flag'] == 1]['top_L']),
                                                                               (data[data['sqc2_flag'] == 1]['KTmax']))]

    data.loc[(data['sqc2_flag'] == 1), 'bot_L'] = [curveLeft[i][1 - 1] for i in
                                                   (data[data['sqc2_flag'] == 1]['Il'].map(int) - 1)] + \
                                                  data[data['sqc2_flag'] == 1]['off_L']
    data.loc[(data['sqc2_flag'] == 1), 'bot_L'] = [max(i, 0) for i in (data[data['sqc2_flag'] == 1]['bot_L'])]
    data.loc[(data['sqc2_flag'] == 1), 'bot_L'] = [min(i, j) for (i, j) in zip((data[data['sqc2_flag'] == 1]['bot_L']),
                                                                               (data[data['sqc2_flag'] == 1]['KTmax']))]

    data.loc[(data['sqc2_flag'] == 1), 'off_R'] = 2.5 * ((data[data['sqc2_flag'] == 1]['Jr']).map(int) - 1)

    data.loc[(data['sqc2_flag'] == 1), 'top_R'] = [curveRight[i][j] for (i, j) in
                                                   zip((data[data['sqc2_flag'] == 1]['Ir'].map(int) - 1),
                                                       (data[data['sqc2_flag'] == 1]['KNmax'].map(int) - 1))] + \
                                                  data[data['sqc2_flag'] == 1]['off_R']
    data.loc[(data['sqc2_flag'] == 1), 'top_R'] = [max(i, 0) for i in (data[data['sqc2_flag'] == 1]['top_R'])]
    data.loc[(data['sqc2_flag'] == 1), 'top_R'] = [min(i, j) for (i, j) in zip((data[data['sqc2_flag'] == 1]['top_R']),
                                                                               (data[data['sqc2_flag'] == 1]['KTmax']))]

    data.loc[(data['sqc2_flag'] == 1), 'bot_R'] = [curveRight[i][1 - 1] for i in
                                                   (data[data['sqc2_flag'] == 1]['Ir'].map(int) - 1)] + \
                                                  data[data['sqc2_flag'] == 1]['off_R']
    data.loc[(data['sqc2_flag'] == 1), 'bot_R'] = [max(i, 0) for i in (data[data['sqc2_flag'] == 1]['bot_R'])]
    data.loc[(data['sqc2_flag'] == 1), 'bot_R'] = [min(i, j) for (i, j) in zip((data[data['sqc2_flag'] == 1]['bot_R']),
                                                                               (data[data['sqc2_flag'] == 1]['KTmax']))]

    # If case

    data.loc[(data['sqc2_flag'] == 1) & (data['Xn2'] > data['KNmax']) & (data['Xt2'] <= data['top_R']) & (
                data['Xt2'] >= data['top_L']), 'flag3'] = 1
    data.loc[(data['flag3'] == 1), 'IQC2'] = data[KNvar] - data['KNmax']
    data.loc[(data['flag3'] == 1) & (data['IQC2'] >= 3), qcFlag1] = [(4 * min(i, 23)) for i in
                                                                     data[(data['flag3'] == 1) & (data['IQC2'] >= 3)][
                                                                         'IQC2']]
    data.loc[(data['flag3'] == 1) & (data['IQC2'] >= 3), qcFlag2] = data[qcFlag1] + 1
    data.loc[(data['flag3'] == 1), 'sqc2_flag'] = 0  # updating flag for unnecessary data points.
    # data['flag3'] = 0 # reseting flag to 0.

    # else case
    data.loc[(data['sqc2_flag'] == 1) & (data['flag3'] == 0) & (data['Xn2'] > data['KNmax']) & (
                data['Xt2'] > data['top_R']), 'flag4'] = 1
    a = data[data['flag4'] == 1]['Xn2']
    b = data[data['flag4'] == 1]['KNmax']
    c = data[data['flag4'] == 1]['Xt2']
    d = data[data['flag4'] == 1]['top_R']
    data.loc[(data['flag4'] == 1), 'IQC2'] = [math.sqrt(pow(i - j, 2) + pow(k - l, 2)) for (i, j, k, l) in
                                              zip(a, b, c, d)]
    data.loc[(data['flag4'] == 1) & (data['IQC2'] >= 3), qcFlag2] = [(4 * min(i, 23)) for i in
                                                                     data[(data['flag4'] == 1) & (data['IQC2'] >= 3)][
                                                                         'IQC2']]
    data.loc[(data['flag4'] == 1) & (data['IQC2'] >= 3), qcFlag1] = data[qcFlag2] + 1
    data.loc[(data['flag4'] == 1), 'sqc2_flag'] = 0  # updating flag for unnecessary data points.
    # data['flag3'] = 0 # reseting flag to 0.

    # else case
    data.loc[(data['sqc2_flag'] == 1) & (data['flag3'] == 0) & (data['flag4'] == 0) & (data['Xn2'] < 0) & (
                data['Xt2'] <= data['bot_R']) & (data['Xt2'] >= data['bot_L']), 'flag5'] = 1
    data.loc[(data['flag5'] == 1), 'IQC2'] = -data[KNvar]
    data.loc[(data['flag5'] == 1) & (data['IQC2'] >= 3), qcFlag2] = [(4 * min(i, 23)) for i in
                                                                     data[(data['flag5'] == 1) & (data['IQC2'] >= 3)][
                                                                         'IQC2']]
    data.loc[(data['flag5'] == 1) & (data['IQC2'] >= 3), qcFlag1] = data[qcFlag2] + 1
    data.loc[(data['flag5'] == 1), 'sqc2_flag'] = 0  # updating flag for unnecessary data points.
    # data['flag3'] = 0 # reseting flag to 0.

    # else case
    data.loc[(data['sqc2_flag'] == 1) & (data['flag3'] == 0) & (data['flag4'] == 0) & (data['flag4'] == 0) & (
                data['Xn2'] < 0) & (data['Xt2'] < data['bot_L']), 'flag6'] = 1
    a = data[data['flag6'] == 1]['Xn2']
    b = data[data['flag6'] == 1]['Xt2']
    c = data[data['flag6'] == 1]['bot_L']
    data.loc[(data['flag6'] == 1), 'IQC2'] = [math.sqrt(pow(i, 2) + pow(j - k, 2)) for (i, j, k) in zip(a, b, c)]
    data.loc[(data['flag6'] == 1) & (data['IQC2'] >= 3), qcFlag1] = [(4 * min(i, 23)) for i in
                                                                     data[(data['flag6'] == 1) & (data['IQC2'] >= 3)][
                                                                         'IQC2']]
    data.loc[(data['flag6'] == 1) & (data['IQC2'] >= 3), qcFlag2] = data[qcFlag1] + 1
    data.loc[(data['flag6'] == 1), 'sqc2_flag'] = 0  # updating flag for unnecessary data points.
    # data['flag3'] = 0 # reseting flag to 0.

    # reseting temp flags:
    data['flag3'] = 0
    data['flag4'] = 0
    data['flag5'] = 0
    data['flag6'] = 0

    '''Figure out where the point on the left Gompertz curve corresponding
      to KN is.  This point is (Xt,Xn).
    '''
    data.loc[(data['sqc2_flag'] == 1), 'Xn'] = data['Xn2']
    a = data[data['sqc2_flag'] == 1]['Xn']
    b = data[data['sqc2_flag'] == 1]['KNmax']
    data.loc[(data['sqc2_flag'] == 1), 'Xn'] = [min(i, j) for (i, j) in zip(a, b)]
    data.loc[(data['sqc2_flag'] == 1), 'Xn'] = [max(i, 1) for i in a]
    data.loc[(data['sqc2_flag'] == 1), 'J'] = data['Xn']

    a = data[data['sqc2_flag'] == 1]['Il'].map(int)
    b = data[data['sqc2_flag'] == 1]['J'].map(int)
    c = data[data['sqc2_flag'] == 1]['off_L']
    data.loc[(data['sqc2_flag'] == 1), 'Xt'] = [(curveLeft[i - 1][j - 1] + k) for (i, j, k) in zip(a, b, c)]

    a = data[data['sqc2_flag'] == 1]['Xt']
    b = data[data['sqc2_flag'] == 1]['KTmax']
    data.loc[(data['sqc2_flag'] == 1), 'Xt'] = [min(i, j) for (i, j) in zip(a, b)]
    data.loc[(data['sqc2_flag'] == 1), 'Xt'] = [max(i, 1) for i in a]

    ''' Initialize the direction to UP and the distance to 100 (squared).'''

    data.loc[(data['sqc2_flag'] == 1), 'yDir'] = 1
    data.loc[(data['sqc2_flag'] == 1), 'dPrev'] = 10000

    '''The point (KT,KN) is to the right of (Xt,Xn), as it should be.
      If KN is above KNmax, that counts as "to the left".
    '''

    data.loc[
        (data['sqc2_flag'] == 1) & (data['Xt'] <= data['Xt2']) & (data['Xn2'] <= data['KNmax']), 'label'] = 'label3000'
    data.loc[(data['sqc2_flag'] == 1) & (data['label'] == 'none'), 'label'] = 'label2000'
    data.loc[(data['label'] == 'label2000'), 'tempLabel'] = data['label']

    # operating label2000 = only if we have data with label 2000

    if (list(data.label).count('lable2000') > 0):

        while len(data[data['sqc2_flag'] == 1]['sqc2_flag']) > 0:
            label2000(curveLeft, data)

        '''We have found the local minimum distance.  Convert it into a data
          flag (take the square root, multiply by 4, etc. as in documentation).
        '''

        a = data[data['label'] == 'label2000']['dPrev']
        b = data[data['label'] == 'label2000']['Dist']
        data.loc[(data['label'] == 'label2000'), 'iFlag'] = [int(math.sqrt(min(i, j))) for (i, j) in zip(a, b)]
        data.loc[(data['label'] == 'label2000'), 'IQCLow'] = [4 * min(i, 23) for i in
                                                              data[data['label'] == 'label2000']['iFlag']]
        data.loc[(data['label'] == 'label2000'), 'IQCHigh'] = data['IQCLow'] + 1

        '''The distance is large enough to trigger a 2-component flag. '''

        a = data[(data['label'] == 'label2000') & (data['iFlag'] >= 3)]['IQCHigh']
        b = data[(data['label'] == 'label2000') & (data['iFlag'] >= 3)][qcFlag2]
        data.loc[(data['label'] == 'label2000') & (data['iFlag'] >= 3), qcFlag2] = [(max(i, j)) for (i, j) in zip(a, b)]

        a = data[(data['label'] == 'label2000') & (data['iFlag'] >= 3)]['IQCLow']
        b = data[(data['label'] == 'label2000') & (data['iFlag'] >= 3)][qcFlag1]
        data.loc[(data['label'] == 'label2000') & (data['iFlag'] >= 3), qcFlag1] = [(max(i, j)) for (i, j) in zip(a, b)]
        data.loc[(data['label'] == 'label2000'), 'sqc2_flag'] = 0  # updating the flag

    '''Figure out where the point on the right Gompertz curve corresponding
      to KN is.  This point is (I,KN).
    '''

    # performing operations on data with label3000 only if we have data with label 3000

    if list(data.label).count('label3000') > 0:

        a = data[data['label'] == 'label3000']['Ir'].map(int)
        b = data[data['label'] == 'label3000']['J'].map(int)
        c = data[data['label'] == 'label3000']['off_R']
        data.loc[(data['label'] == 'label3000'), 'Xt'] = [(curveRight[i - 1][j - 1] + k) for (i, j, k) in zip(a, b, c)]
        a = data[data['label'] == 'label3000']['Xt']
        b = data[data['label'] == 'label3000']['KTmax']
        data.loc[(data['label'] == 'label3000'), 'Xt'] = [min(i, j) for (i, j) in zip(a, b)]
        data.loc[(data['label'] == 'label3000'), 'Xt'] = [max(i, 1) for i in a]

        '''The point (KT,KN) is to the left of (Xt,Xn), as it should be.
          If KN is below 0, that counts as "to the right".
        '''
        data.loc[(data['label'] == 'label3000') & (data['Xt'] >= data['Xt2']) & (data['Xn2'] >= 0), 'sqc2_flag'] = 0
        data.loc[(data['label'] == 'label3000') & (data['Xt'] < data['Xt2']) | (data['Xn2'] < 0), 'label'] = 'label4000'
        data.loc[(data['label'] == 'label4000'), 'tempLabel'] = data['label']

        # performing operations on data with label4000 only if we have data with label 4000

        if (list(data.label).count('lable4000') > 0):

            while len(data[data['sqc2_flag'] == 1]['sqc2_flag']) > 0:
                label4000(curveRight, data)

            '''We have found the local minimum distance.  Convert it into a data
              flag (take the square root, multiply by 4, etc. as in documentation).
            '''
            a = data[data['label'] == 'label4000']['dPrev']
            b = data[data['label'] == 'label4000']['Dist']
            data.loc[(data['label'] == 'label4000'), 'iFlag'] = [int(math.sqrt(min(i, j))) for (i, j) in zip(a, b)]
            data.loc[(data['label'] == 'label4000'), 'IQCLow'] = [4 * min(i, 23) for i in
                                                                  data[data['label'] == 'label4000']['iFlag']]
            data.loc[(data['label'] == 'label4000'), 'IQCHigh'] = data['IQCLow'] + 1

            '''The distance is large enough to trigger a 2-component flag. '''

            a = data[(data['label'] == 'label4000') & (data['iFlag'] >= 3)]['IQCLow']
            b = data[(data['label'] == 'label4000') & (data['iFlag'] >= 3)][qcFlag2]
            data.loc[(data['label'] == 'label4000') & (data['iFlag'] >= 3), qcFlag2] = [(max(i, j)) for (i, j) in
                                                                                        zip(a, b)]

            a = data[(data['label'] == 'label4000') & (data['iFlag'] >= 3)]['IQCHigh']
            b = data[(data['label'] == 'label4000') & (data['iFlag'] >= 3)][qcFlag1]
            data.loc[(data['label'] == 'label4000') & (data['iFlag'] >= 3), qcFlag1] = [(max(i, j)) for (i, j) in
                                                                                        zip(a, b)]
            data.loc[(data['label'] == 'label4000'), 'sqc2_flag'] = 0  # updating the flag

    # ------------------------ Calculations Done ------------------------


def splitDate(ipData):
    '''tem=re.findall('HOUR', ipData.columns[1])
           if (len(tem)!=0):  # it means data is hour based
               ipData['date'] = ipData[ipData.columns[0]] + ' ' + ipData[ipData.columns[1]].map(str)+":00:00" # provide raw data
           else:   # it means data is minute based

               ipData['date'] = ipData[ipData.columns[0]] + ' ' + ipData[ipData.columns[1]] # provide raw data'''

    # deg2rad = math.pi / 180

    # to be used on prod
    ipData['date'] = ipData[ipData.columns[0]].map(str) + ' ' + ipData[ipData.columns[1]]  # provide raw data

    ipData['date'] = pd.to_datetime(ipData['date'])
    ipData['month'] = ipData['date'].dt.month_name().str.upper().str[0:3]
    ipData['doy'] = ipData['date'].dt.dayofyear


def utcCoversion(ipData, timeZone, repFreq, measFreq):
    # UTC conversion for SPA

    if (timeZone < 0):
        ipData['date-UTC'] = ipData['date'] + datetime.timedelta(hours=abs(timeZone))
    else:
        if (timeZone > 0):
            ipData['date-UTC'] = ipData['date'] - datetime.timedelta(hours=abs(timeZone))
        else:
            ipData['date-UTC'] = ipData['date']

    ipData['f0'] = ipData['date-UTC']
    for i in range(int(repFreq / measFreq)):
        ipData['f' + str(i + 1)] = ipData['f' + str(i)] - datetime.timedelta(minutes=measFreq)


def calculateZenith(ipData, repFreq, measFreq, avg, latitude, longitude, elevation, pressure, temperature):
    #################################

    # Calculating ETR

    #################################

    ipData['B'] = 2 * math.pi * ipData['doy'] / 365
    ipData['cos(B)'] = [math.cos(i) for i in ipData['B']]
    ipData['sin(B)'] = [math.sin(i) for i in ipData['B']]
    ipData['cos(2*B)'] = [math.cos(2 * i) for i in ipData['B']]
    ipData['sin(2*B)'] = [math.sin(2 * i) for i in ipData['B']]

    ipData['Rfact2'] = 1.00011 + 0.034221 * ipData['cos(B)'] + 0.00128 * ipData['sin(B)'] + 0.000719 * ipData[
        'cos(2*B)'] + 0.000077 * ipData['sin(2*B)']
    # ipData['tempETRN'] = 1361.2 * ipData['Rfact2'] # change to this before releasing
    ipData['tempETRN'] = 1367 * ipData['Rfact2']

    #################################

    # Calculating SZA

    #################################

    # dateTimeIndex=np.array(ipData['date-UTC'])
    lat_lon = np.array([latitude, longitude])
    ipData['ETRN'] = 0.0
    ipData['solzen'] = 0.0
    ipData['sunup'] = 0.0
    ipData['ETR'] = 0.0

    # ipData['SZA'] = SPA.apparent_zenith(dateTimeIndex, lat_lon, elev=elevation, pressure=pressure,
    # temperature=temperature,  atmospheric_refraction=0.5667, delta_t=64.17)
    global interval
    """if avg == 'Yes':
        interval = repFreq
        loopIter = int(repFreq / measFreq)
    else:
        interval = 1
        loopIter = 2
        """

    # fixed for hour based data. Because averaging is done anyways

    interval = repFreq
    # loopIter = interval+1

    if interval == 1:
        loopIter = 2
    else:
        loopIter = int(repFreq / measFreq) + 1

    loopRun = 0
    for i in range(loopIter):
        ipData['tempETR'] = 0
        ipData['tempSZA'] = 0
        if i == 0 or i == interval:
            fraction = 0.5
        else:
            fraction = 1.0
        print(fraction)
        print(i)
        ipData['tempSZA'] = SPA.apparent_zenith(np.array(ipData['f' + str(i)]), lat_lon, elev=elevation,
                                                pressure=pressure, temperature=temperature,
                                                atmospheric_refraction=0.5667, delta_t=64.17)
        ipData['tempETR'] = ipData['tempETRN'] * [math.cos(math.radians(i)) for i in ipData['tempSZA']]

        ipData.loc[(ipData['tempETR'] > 0), 'sunup'] = ipData['sunup'] + 1 * fraction
        ipData.loc[(ipData['tempETR'] > 0), 'solzen'] = ipData['solzen'] + ipData['tempSZA'] * fraction
        ipData.loc[(ipData['tempETR'] > 0), 'ETR'] = ipData['ETR'] + ipData['tempETR'] * fraction
        ipData.loc[(ipData['tempETR'] > 0), 'ETRN'] = ipData['ETRN'] + ipData['tempETRN'] * fraction
        loopRun += 1

    ipData.loc[(ipData['sunup'] > 0), 'solzen'] = ipData['solzen'] / ipData['sunup']
    ipData.loc[(ipData['sunup'] > 0), 'ETR'] = ipData['ETR'] / interval
    ipData.loc[(ipData['sunup'] > 0), 'ETRN'] = ipData['ETRN'] / interval
    ipData.loc[ipData['sunup'] < 0, 'solzen'] = 100.0


def calculatekSpaceVars(ipData, addComp):
    Global = ipData[ipData.columns[2]]
    Direct = ipData[ipData.columns[3]]
    Diffuse = ipData[ipData.columns[4]]
    ipData['KT'] = -999
    ipData['KN'] = -999
    ipData['KD'] = -999
    ipData.loc[Global > 8000, 'IQCGlobal'] = 99
    ipData.loc[Global > 8000, 'KT'] = 9900
    ipData.loc[Direct > 8000, 'IQCDirect'] = 99
    ipData.loc[Direct > 8000, 'KN'] = 9900
    ipData.loc[Diffuse > 8000, 'IQCDiffuse'] = 99
    ipData.loc[Diffuse > 8000, 'KD'] = 9900

    ipData.loc[(ipData['IQCGlobal'] < 99) & (ipData['ETR'] == 0) & (Global < - 10), 'IQCGlobal'] = 7
    ipData.loc[(ipData['IQCGlobal'] < 99) & (ipData['ETR'] == 0) & (Global > 10), 'IQCGlobal'] = 8
    ipData['XT'] = 0
    ipData.loc[(ipData['IQCGlobal'] < 99) & (ipData['ETR'] != 0), 'XT'] = Global / ipData['ETR']

    ipData.loc[(ipData['IQCDirect'] < 99) & (ipData['ETR'] == 0) & (Direct < - 10), 'IQCDirect'] = 7
    ipData.loc[(ipData['IQCDirect'] < 99) & (ipData['ETR'] == 0) & (Direct > 10), 'IQCDirect'] = 8
    ipData['XN'] = 0
    ipData.loc[(ipData['IQCDirect'] < 99) & (ipData['ETR'] != 0), 'XN'] = Direct / ipData['ETRN']

    ipData.loc[(ipData['IQCDiffuse'] < 99) & (ipData['ETR'] == 0) & (Diffuse < - 10), 'IQCDiffuse'] = 7
    ipData.loc[(ipData['IQCDiffuse'] < 99) & (ipData['ETR'] == 0) & (Diffuse > 10), 'IQCDiffuse'] = 8
    ipData['XD'] = 0
    ipData.loc[(ipData['IQCDiffuse'] < 99) & (ipData['ETR'] != 0), 'XD'] = Diffuse / ipData['ETR']

    # Done with processing of night-time values.
    ipData['goAhead'] = 1
    ipData.loc[(ipData['ETR'] == 0), 'goAhead'] = 0

    ipData.loc[(ipData['goAhead'] == 1) & (ipData['KT'] != 9900), 'KT'] = ipData['XT'] * 100 + addComp
    ipData.loc[(ipData['goAhead'] == 1) & (ipData['KN'] != 9900), 'KN'] = ipData['XN'] * 100 + addComp
    ipData.loc[(ipData['goAhead'] == 1) & (ipData['KD'] != 9900), 'KD'] = ipData['XD'] * 100 + addComp

    # Make sure KT, KN, KD are within bounds of int (-32768, 32768)

    ipData.loc[(ipData['goAhead'] == 1) & (ipData['KT'] >= 32768.0), 'KT'] = 32768
    ipData.loc[(ipData['goAhead'] == 1) & (ipData['KT'] <= -32768.0), 'KT'] = -32768
    ipData.loc[(ipData['goAhead'] == 1) & (ipData['KT'] < 32768.0) & (ipData['KT'] > -32768), 'KT'] = ipData['KT'].map(
        int)

    ipData.loc[(ipData['goAhead'] == 1) & (ipData['KN'] >= 32768.0), 'KN'] = 32768
    ipData.loc[(ipData['goAhead'] == 1) & (ipData['KN'] <= -32768.0), 'KN'] = -32768
    ipData.loc[(ipData['goAhead'] == 1) & (ipData['KN'] < 32768.0) & (ipData['KN'] > -32768), 'KN'] = ipData['KN'].map(
        int)

    ipData.loc[(ipData['goAhead'] == 1) & (ipData['KD'] >= 32768.0), 'KD'] = 32768
    ipData.loc[(ipData['goAhead'] == 1) & (ipData['KD'] <= -32768.0), 'KD'] = -32768
    ipData.loc[(ipData['goAhead'] == 1) & (ipData['KD'] < 32768.0) & (ipData['KD'] > -32768), 'KD'] = ipData['KD'].map(
        int)


def calculateAirmass(ipData):
    deg2rad = math.pi / 180
    ipData['cos(solzen*deg2rad)'] = 0
    ipData['pow'] = 0
    ipData.loc[(ipData['goAhead'] == 1), 'cos(solzen*deg2rad)'] = [math.cos(i * deg2rad) for i in
                                                                   ipData[ipData['goAhead'] == 1]['solzen']]
    ipData.loc[(ipData['goAhead'] == 1), 'pow'] = [math.pow(96.07995 - i, 1.6364) for i in
                                                   ipData[ipData['goAhead'] == 1]['solzen']]

    # Calculate airmass.
    ipData['airMass'] = 0
    ipData.loc[(ipData['goAhead'] == 1), 'airMass'] = (1.0 / ipData['cos(solzen*deg2rad)'] + 0.50572 / ipData['pow'])

    # Airmass regimes:  1 = low, 2 = middle, 3 = high.

    ipData['NAM'] = 0
    ipData.loc[(ipData['goAhead'] == 1), 'NAM'] = 1

    ipData.loc[(ipData['airMass'] >= 1.25) & (ipData['airMass'] < 2.5), 'NAM'] = 2
    ipData.loc[(ipData['airMass'] >= 2.5), 'NAM'] = 3


def getElevation(elevation):
    frm.getEntry('Provide Elevation of site', 'Note: Elevation is mandatory.', -999)
    try:
        elevation = float(utills.readList('temp')[0])
    except ValueError:
        elevation = -999
    return elevation


def main():
    #################################

    # Getting input file paths

    #################################
    # path_QC0 = "/Users/rgupta2/Desktop/s_BMS.QC0"
    # path_csv = "/Users/rgupta2/Desktop/minute edited.csv"

    path_QC0 = frm.getPath("qc0")
    # frm.validateFile(path_QC0, '.QC0', '.qc0')

    path_csv = frm.getPath("csv")
    # frm.validateFile(path_csv, '.csv', '.csv')
    #################################

    # importing data

    #################################

    qcData = utills.readFile(path_QC0)

    ipData = pd.read_csv(path_csv)

    #################################

    # Data Preparation 

    #################################

    ipData['IQCGlobal'] = 1
    ipData['IQCDirect'] = 1
    ipData['IQCDiffuse'] = 1
    latitude = utills.pickValue(qcData, 'Latitude:')
    longitude = utills.pickValue(qcData, 'Longitude:')
    timeZone = utills.pickValue(qcData, 'Time Zone:')
    boundData = utills.getBoundariesTable(qcData)
    siteName = qcData.split('\n')[0].split(':')[1].strip()
    # ====================================================================================

    # default values
    measFreq, repFreq, avg = takeValues()
    elevation = utills.pickValue(qcData, 'Elevation:')

    if elevation == 0:
        elevation = -999
        while elevation == -999:
            elevation = getElevation(elevation)

    pressure = [item for item in ipData.columns if 'Pressure' in item]
    if len(pressure) == 0:
        pressure = (101325 * (1 - (2.25577 * 10 ** (-5)) * elevation) ** 5.25588) / 100
    else:
        pressure = statistics.mean(ipData[pressure])

    temperature = 12

    # ====================================================================================

    #################################

    # Variable declarations

    #################################

    Global = ipData[ipData.columns[2]]
    Direct = ipData[ipData.columns[3]]
    Diffuse = ipData[ipData.columns[4]]
    curveLeft = utills.curveLeft
    curveRight = utills.curveRight
    Alog_4 = 1.386294361
    XDm = (0.19, 0.22, 0.24, 0.28, 0.32)

    splitDate(ipData)
    ipData = ipData.merge(boundData, left_on='month', right_on='month')
    utcCoversion(ipData, timeZone, repFreq, measFreq)
    calculateZenith(ipData, repFreq, measFreq, avg, latitude, longitude, elevation, pressure, temperature)
    calculatekSpaceVars(ipData, 0.5)
    calculateAirmass(ipData)

    """

    '''tem=re.findall('HOUR', ipData.columns[1])    
    if (len(tem)!=0):  # it means data is hour based
        ipData['date'] = ipData[ipData.c7olumns[0]] + ' ' + ipData[ipData.columns[1]].map(str)+":00:00" # provide raw data
    else:   # it means data is minute based
        
        ipData['date'] = ipData[ipData.columns[0]] + ' ' + ipData[ipData.columns[1]] # provide raw data'''

    # to be used on prod
    ipData['date'] = ipData[ipData.columns[0]] + ' ' + ipData[ipData.columns[1]]  # provide raw data

    ipData['date'] = pd.to_datetime(ipData['date'])
    ipData['month'] = ipData['date'].dt.month_name().str.upper().str[0:3]
    ipData['doy'] = ipData['date'].dt.dayofyear
    ipData = ipData.merge(boundData, left_on='month', right_on='month')

    # UTC conversion for SPA

    if (timeZone < 0):
        ipData['date-UTC'] = ipData['date'] + datetime.timedelta(hours=abs(timeZone))
    else:
        if (timeZone > 0):
            ipData['date-UTC'] = ipData['date'] - datetime.timedelta(hours=abs(timeZone))
        else:
            ipData['date-UTC'] = ipData['date']

    ipData['f0'] = ipData['date-UTC']
    for i in range(int(repFreq / measFreq)):
        ipData['f' + str(i + 1)] = ipData['f' + str(i)] - datetime.timedelta(minutes=measFreq)

    #################################

    # Variable declarations

    #################################

    Global = ipData[ipData.columns[2]]
    Direct = ipData[ipData.columns[3]]
    Diffuse = ipData[ipData.columns[4]]
    curveLeft = utills.curveLeft
    curveRight = utills.curveRight

    deg2rad = math.pi / 180
    Alog_4 = 1.386294361
    XDm = (0.19, 0.22, 0.24, 0.28, 0.32)


    #################################

    # Calculating ETR

    #################################

    ipData['B'] = 2 * math.pi * ipData['doy'] / 365
    ipData['cos(B)'] = [math.cos(i) for i in ipData['B']]
    ipData['sin(B)'] = [math.sin(i) for i in ipData['B']]
    ipData['cos(2*B)'] = [math.cos(2 * i) for i in ipData['B']]
    ipData['sin(2*B)'] = [math.sin(2 * i) for i in ipData['B']]

    ipData['Rfact2'] = 1.00011 + 0.034221 * ipData['cos(B)'] + 0.00128 * ipData['sin(B)'] + 0.000719 * ipData[
        'cos(2*B)'] + 0.000077 * ipData['sin(2*B)']
    # pData['tempETRN'] = 1361.2 * ipData['Rfact2'] # change to this before releasing
    ipData['tempETRN'] = 1367 * ipData['Rfact2']

    #################################

    # Calculating SZA

    #################################

    # dateTimeIndex=np.array(ipData['date-UTC'])
    lat_lon = np.array([latitude, longitude])
    ipData['ETRN'] = 0
    ipData['solzen'] = 0
    ipData['sunup'] = 0
    ipData['ETR'] = 0

    # ipData['SZA'] = SPA.apparent_zenith(dateTimeIndex, lat_lon, elev=elevation, pressure=pressure,
    # temperature=temperature,  atmospheric_refraction=0.5667, delta_t=64.17)
    if avg == 'Yes':
        interval = repFreq
        loopIter = int(repFreq / measFreq)
    else:
        interval = 1
        loopIter = 2

    for i in range(loopIter):
        ipData['tempETR'] = 0
        ipData['tempSZA'] = 0
        if i == 0 or i == interval:
            fraction = 0.5
        else:
            fraction = 1.0

        ipData['tempSZA'] = SPA.apparent_zenith(np.array(ipData['f' + str(i)]), lat_lon, elev=elevation,
                                                pressure=pressure, temperature=temperature,
                                                atmospheric_refraction=0.5667, delta_t=64.17)
        ipData['tempETR'] = ipData['tempETRN'] * [math.cos(math.radians(i)) for i in ipData['tempSZA']]

        ipData.loc[(ipData['tempETR'] > 0), 'sunup'] = ipData['sunup'] + 1 * fraction
        ipData.loc[(ipData['tempETR'] > 0), 'solzen'] = ipData['solzen'] + ipData['tempSZA'] * fraction
        ipData.loc[(ipData['tempETR'] > 0), 'ETR'] = ipData['ETR'] + ipData['tempETR'] * fraction
        ipData.loc[(ipData['tempETR'] > 0), 'ETRN'] = ipData['ETRN'] + ipData['tempETRN'] * fraction

    ipData.loc[(ipData['sunup'] > 0), 'solzen'] = ipData['solzen'] / ipData['sunup']
    ipData.loc[(ipData['sunup'] > 0), 'ETR'] = ipData['ETR'] / interval
    ipData.loc[(ipData['sunup'] > 0), 'ETRN'] = ipData['ETRN'] / interval
    ipData.loc[ipData['sunup'] < 0, 'solzen'] = 100.0

    ipData['KT'] = -999
    ipData['KN'] = -999
    ipData['KD'] = -999
    ipData.loc[Global > 8000, 'IQCGlobal'] = 99
    ipData.loc[Global > 8000, 'KT'] = 9900
    ipData.loc[Direct > 8000, 'IQCDirect'] = 99
    ipData.loc[Direct > 8000, 'KN'] = 9900
    ipData.loc[Diffuse > 8000, 'IQCDiffuse'] = 99
    ipData.loc[Diffuse > 8000, 'KD'] = 9900

    ipData.loc[(ipData['IQCGlobal'] < 99) & (ipData['ETR'] == 0) & (Global < - 10), 'IQCGlobal'] = 7
    ipData.loc[(ipData['IQCGlobal'] < 99) & (ipData['ETR'] == 0) & (Global > 10), 'IQCGlobal'] = 8
    ipData['XT'] = 0
    ipData.loc[(ipData['IQCGlobal'] < 99) & (ipData['ETR'] != 0), 'XT'] = Global / ipData['ETR']

    ipData.loc[(ipData['IQCDirect'] < 99) & (ipData['ETR'] == 0) & (Direct < - 10), 'IQCDirect'] = 7
    ipData.loc[(ipData['IQCDirect'] < 99) & (ipData['ETR'] == 0) & (Direct > 10), 'IQCDirect'] = 8
    ipData['XN'] = 0
    ipData.loc[(ipData['IQCDirect'] < 99) & (ipData['ETR'] != 0), 'XN'] = Direct / ipData['ETRN']

    ipData.loc[(ipData['IQCDiffuse'] < 99) & (ipData['ETR'] == 0) & (Diffuse < - 10), 'IQCDiffuse'] = 7
    ipData.loc[(ipData['IQCDiffuse'] < 99) & (ipData['ETR'] == 0) & (Diffuse > 10), 'IQCDiffuse'] = 8
    ipData['XD'] = 0
    ipData.loc[(ipData['IQCDiffuse'] < 99) & (ipData['ETR'] != 0), 'XD'] = Diffuse / ipData['ETR']

    # Done with processing of night-time values.
    ipData['goAhead'] = 1
    ipData.loc[(ipData['ETR'] == 0), 'goAhead'] = 0

    ipData.loc[(ipData['goAhead'] == 1) & (ipData['KT'] != 9900), 'KT'] = ipData['XT'] * 100 + 0.5
    ipData.loc[(ipData['goAhead'] == 1) & (ipData['KN'] != 9900), 'KN'] = ipData['XN'] * 100 + 0.5
    ipData.loc[(ipData['goAhead'] == 1) & (ipData['KD'] != 9900), 'KD'] = ipData['XD'] * 100 + 0.5

    # Make sure KT, KN, KD are within bounds of int (-32768, 32768)

    ipData.loc[(ipData['goAhead'] == 1) & (ipData['KT'] >= 32768.0), 'KT'] = 32768
    ipData.loc[(ipData['goAhead'] == 1) & (ipData['KT'] <= -32768.0), 'KT'] = -32768
    ipData.loc[(ipData['goAhead'] == 1) & (ipData['KT'] < 32768.0) & (ipData['KT'] > -32768), 'KT'] = ipData['KT'].map(
        int)

    ipData.loc[(ipData['goAhead'] == 1) & (ipData['KN'] >= 32768.0), 'KN'] = 32768
    ipData.loc[(ipData['goAhead'] == 1) & (ipData['KN'] <= -32768.0), 'KN'] = -32768
    ipData.loc[(ipData['goAhead'] == 1) & (ipData['KN'] < 32768.0) & (ipData['KN'] > -32768), 'KN'] = ipData['KN'].map(
        int)

    ipData.loc[(ipData['goAhead'] == 1) & (ipData['KD'] >= 32768.0), 'KD'] = 32768
    ipData.loc[(ipData['goAhead'] == 1) & (ipData['KD'] <= -32768.0), 'KD'] = -32768
    ipData.loc[(ipData['goAhead'] == 1) & (ipData['KD'] < 32768.0) & (ipData['KD'] > -32768), 'KD'] = ipData['KD'].map(
        int)

    ipData['cos(solzen*deg2rad)'] = 0
    ipData['pow'] = 0
    ipData.loc[(ipData['goAhead'] == 1), 'cos(solzen*deg2rad)'] = [math.cos(i * deg2rad) for i in
                                                                   ipData[ipData['goAhead'] == 1]['solzen']]
    ipData.loc[(ipData['goAhead'] == 1), 'pow'] = [math.pow(96.07995 - i, 1.6364) for i in
                                                   ipData[ipData['goAhead'] == 1]['solzen']]

    # Calculate airmass.
    ipData['airMass'] = 0
    ipData.loc[(ipData['goAhead'] == 1), 'airMass'] = (1.0 / ipData['cos(solzen*deg2rad)'] + 0.50572 / ipData['pow'])

    # Airmass regimes:  1 = low, 2 = middle, 3 = high.

    ipData['NAM'] = 0
    ipData.loc[(ipData['goAhead'] == 1), 'NAM'] = 1

    ipData.loc[(ipData['airMass'] >= 1.25) & (ipData['airMass'] < 2.5), 'NAM'] = 2
    ipData.loc[(ipData['airMass'] >= 2.5), 'NAM'] = 3

    """

    '''
    ipData.loc[(ipData['NAM'] == 1),'AMass'] = 'LA'
    ipData.loc[(ipData['NAM'] == 2),'AMass'] = 'MA'
    ipData.loc[(ipData['NAM'] == 3),'AMass'] = 'HA'''

    '''intBin is an integer from 1 to 4, signifying the place of the digit containing the information in the S_<id>.QC0 file.  If data approximate 1-minute resolution, 1 is chosen; if the resolution approximates 64 minutes, 4 is chosen.  interval should be bounded by 1 and 60.'''

    iRes = max(interval, 1)
    iRes = min(iRes, 60)
    intBin = int(1.49 + math.log(iRes) / Alog_4)

    if intBin == 1:
        pos = '1'
    elif intBin == 2:
        pos = '5'
    elif intBin == 3:
        pos = '15'
    elif intBin == 4:
        pos = '60'

    '''The Gompertz curve numbers were read from the .QC0 file. "l" stands for "left" and "r" stands for "right".  
    "I" represents the shape and "J" represents the position. '''

    ipData['Il'] = 0
    ipData['Jl'] = 0
    ipData['Ir'] = 0
    ipData['Jr'] = 0

    ipData.loc[(ipData['NAM'] == 1), 'Il'] = ipData['LA_Left_S']
    ipData.loc[(ipData['NAM'] == 2), 'Il'] = ipData['MA_Left_S']
    ipData.loc[(ipData['NAM'] == 3), 'Il'] = ipData['HA_Left_S']

    ipData.loc[(ipData['NAM'] == 1), 'Jl'] = ipData['LA_Left_P']
    ipData.loc[(ipData['NAM'] == 2), 'Jl'] = ipData['MA_Left_P']
    ipData.loc[(ipData['NAM'] == 3), 'Jl'] = ipData['HA_Left_P']

    ipData.loc[(ipData['NAM'] == 1), 'Ir'] = ipData['LA_Right_S']
    ipData.loc[(ipData['NAM'] == 2), 'Ir'] = ipData['MA_Right_S']
    ipData.loc[(ipData['NAM'] == 3), 'Ir'] = ipData['HA_Right_S']

    ipData.loc[(ipData['NAM'] == 1), 'Jr'] = ipData['LA_Right_' + pos]
    ipData.loc[(ipData['NAM'] == 2), 'Jr'] = ipData['MA_Right_' + pos]
    ipData.loc[(ipData['NAM'] == 3), 'Jr'] = ipData['HA_Right_' + pos]

    ipData.loc[(ipData['goAhead'] == 1) & (ipData['Il'] == 0), 'goAhead'] = 0  # updating the goAhead flag
    ipData.loc[(ipData['goAhead'] == 1) & (ipData['Jl'] == 0), 'goAhead'] = 0  # updating the goAhead flag
    ipData.loc[(ipData['goAhead'] == 1) & (ipData['Ir'] == 0), 'goAhead'] = 0  # updating the goAhead flag
    ipData.loc[(ipData['goAhead'] == 1) & (ipData['Jr'] == 0), 'goAhead'] = 0  # updating the goAhead flag

    ipData['XDm'] = 0
    ipData['XDmax'] = 0
    ipData['XNmax'] = 0
    ipData['XTmax'] = 0

    ipData.loc[(ipData['goAhead'] == 1), 'XDm'] = [(XDm[int(i) - 1]) for i in ipData[ipData['goAhead'] == 1]['Ir']]
    ipData.loc[(ipData['goAhead'] == 1), 'XDmax'] = ipData['XDm'] + 0.025 * (ipData['Jr'].map(int) + 3)
    ipData.loc[(ipData['goAhead'] == 1), 'XNmax'] = ipData['MC_KN'].map(int) / 100.0
    ipData.loc[(ipData['goAhead'] == 1), 'XTmax'] = ipData['MC_KT_' + pos].map(int) / 100.0

    ipData.loc[(ipData['goAhead'] == 1) & (ipData['MC_KN'] == 0), 'goAhead'] = 0  # updating the goAhead flag
    ipData.loc[(ipData['goAhead'] == 1) & (ipData['MC_KT_' + pos] == 0), 'goAhead'] = 0  # updating the goAhead flag

    '''if (intBin ==1):
        ipData.loc[(ipData['goAhead'] == 1),'XTmax'] = ipData['MC_KT_1'].map(int) / 100.0
    elif (intBin ==2):
        ipData.loc[(ipData['goAhead'] == 1),'XTmax'] = ipData['MC_KT_5'].map(int) / 100.0
    elif (intBin ==3):
        ipData.loc[(ipData['goAhead'] == 1),'XTmax'] = ipData['MC_KT_15'].map(int) / 100.0
    elif (intBin ==4):
        ipData.loc[(ipData['goAhead'] == 1),'XTmax'] = ipData['MC_KT_60'].map(int) / 100.0
    '''
    # As the user guide explains, Ktmax and Knmax must be adjusted downwards for increasing airmass.

    ipData.loc[(ipData['NAM'] == 2), 'XTmax'] = ipData['XTmax'] - 0.025
    ipData.loc[(ipData['NAM'] == 2), 'XNmax'] = ipData['XNmax'] - 0.050

    ipData.loc[(ipData['NAM'] == 3), 'XTmax'] = ipData['XTmax'] - 0.1
    ipData.loc[(ipData['NAM'] == 3), 'XNmax'] = ipData['XNmax'] - 0.15

    ''' Is each parameter within theoretical limits? (1-parameter check)'''

    # Global (NOTE:  Max Kt is 0.10 larger than the Gompertz right boundary):   

    ipData.loc[(ipData['goAhead'] == 1) & (ipData['IQCGlobal'] < 99) & (ipData['XT'] < 0.05), 'IQCGlobal'] = 7
    ipData.loc[(ipData['goAhead'] == 1) & (ipData['IQCGlobal'] < 99) & (ipData['XT'] >= 0.05) & (
            ipData['XT'] > (ipData['XTmax'] + 0.10)), 'IQCGlobal'] = 8

    # Direct:

    ipData.loc[(ipData['goAhead'] == 1) & (ipData['IQCDirect'] < 99) & (Direct < -10), 'IQCDirect'] = 7
    ipData.loc[(ipData['goAhead'] == 1) & (ipData['IQCDirect'] < 99) & (Direct >= -10) & (
            ipData['XN'] > ipData['XNmax']), 'IQCDirect'] = 8

    # Diffuse:

    ipData.loc[(ipData['goAhead'] == 1) & (ipData['IQCDiffuse'] < 99) & (ipData['XD'] < 0.03), 'IQCDiffuse'] = 7
    ipData.loc[(ipData['goAhead'] == 1) & (ipData['IQCDiffuse'] < 99) & (ipData['XD'] >= 0.03) & (
            ipData['XD'] > ipData['XDmax']), 'IQCDiffuse'] = 8

    '''Go no further if the solar zenith angle is greater than 80 degrees. However, don't use a flag of 7 if the GLOBAL or DIFFUSE are not less than -10 W/sq m (thermocouple response effect).  Also, if the ETR is 25 W/sq m or less, a GLOBAL value of 10 W/sq m should not be considered too high.'''

    ipData.loc[(ipData['goAhead'] == 1) & (ipData['solzen'] > 80) & (ipData['IQCGlobal'] == 7) & (
            Global >= -10), 'IQCGlobal'] = 1

    ipData.loc[(ipData['goAhead'] == 1) & (ipData['solzen'] > 80) & (ipData['IQCDiffuse'] == 7) & (
            Diffuse >= -10), 'IQCDiffuse'] = 1

    ipData.loc[
        (ipData['goAhead'] == 1) & (ipData['solzen'] > 80) & (ipData['IQCGlobal'] == 8) & (ipData['ETR'] <= 25) & (
                Global <= -10), 'IQCGlobal'] = 1

    # Flag to identify 
    ipData.loc[(ipData['goAhead'] == 1) & (ipData['solzen'] > 80), 'goAhead'] = 0  # updating the goAhead flag

    # If no more than 2 parameters are present (count them first), stop.

    ipData['numpar'] = 0
    ipData.loc[(ipData['goAhead'] == 1) & (ipData['IQCGlobal'] == 1), 'numpar'] = 1
    ipData.loc[(ipData['goAhead'] == 1) & (ipData['IQCDirect'] == 1), 'numpar'] = ipData['numpar'] + 1
    ipData.loc[(ipData['goAhead'] == 1) & (ipData['IQCDiffuse'] == 1), 'numpar'] = ipData['numpar'] + 1

    ipData.loc[(ipData['numpar'] <= 1), 'goAhead'] = 0  # updating the goAhead flag

    # Do the KN < KT check:

    ipData['kHigh'] = 0

    ipData.loc[(ipData['goAhead'] == 1) & (ipData['IQCGlobal'] == 1) & (ipData['IQCDirect'] == 1), 'kHigh'] = ipData[
                                                                                                                  'KN'] - \
                                                                                                              ipData[
                                                                                                                  'KT']

    ipData.loc[(ipData['kHigh'] >= 5), 'IQCGlobal'] = 94
    ipData.loc[(ipData['kHigh'] >= 5), 'IQCDirect'] = 94

    ipData.loc[(ipData['kHigh'] >= 10), 'IQCGlobal'] = 95
    ipData.loc[(ipData['kHigh'] >= 10), 'IQCDirect'] = 95

    ipData.loc[(ipData['kHigh'] >= 15), 'IQCGlobal'] = 96
    ipData.loc[(ipData['kHigh'] >= 15), 'IQCDirect'] = 96

    ipData.loc[(ipData['kHigh'] >= 20), 'IQCGlobal'] = 97
    ipData.loc[(ipData['kHigh'] >= 20), 'IQCDirect'] = 97

    ipData.loc[(ipData['kHigh'] >= 5), 'goAhead'] = 0  # updating the goAhead flag

    # check for numpar == condition

    # Perform the 3-parameter test.  Exit if it is negative.

    ipData['IQCGlo3'] = 0  # *IQCt3
    ipData['IQCDir3'] = 0  # *IQCn3
    ipData['IQCDif3'] = 0  # *IQCd3
    ipData['IQC'] = 0
    ipData['iTog'] = 0
    ipData.loc[(ipData['goAhead'] == 1) & (ipData['numpar'] == 3), 'IQCGlobal'] = 3
    ipData.loc[(ipData['goAhead'] == 1) & (ipData['numpar'] == 3), 'IQCDirect'] = 3
    ipData.loc[(ipData['goAhead'] == 1) & (ipData['numpar'] == 3), 'IQCDiffuse'] = 3
    ipData.loc[(ipData['goAhead'] == 1) & (ipData['numpar'] == 3), 'IQC'] = ipData['KN'] + ipData['KD'] - ipData['KT']
    ipData.loc[(ipData['goAhead'] == 1) & (ipData['numpar'] == 3), 'iTog'] = 1

    ipData.loc[(ipData['numpar'] == 3) & (ipData['IQC'] < 0), 'iTog'] = -1
    ipData.loc[(ipData['numpar'] == 3) & (ipData['IQC'] < 0), 'IQC'] = -ipData['IQC']

    ipData['IQC0'] = 0
    ipData.loc[(ipData['goAhead'] == 1) & (ipData['numpar'] == 3), 'IQC0'] = [min(i, 23) for i in ipData[
        (ipData['goAhead'] == 1) & (ipData['numpar'] == 3)]['IQC']]
    ipData.loc[(ipData['goAhead'] == 1) & (ipData['numpar'] == 3), 'IQC0'] = 4 * ipData['IQC0'] - 1

    ipData.loc[(ipData['goAhead'] == 1) & (ipData['numpar'] == 3) & (ipData['iTog'] == 1), 'IQC0'] = ipData['IQC0'] - 1

    # IQC1 has to take on the opposite sense (TOO HIGH/TOO LOW) from IQC0.

    ipData['IQC1'] = 0

    ipData.loc[(ipData['goAhead'] == 1) & (ipData['numpar'] == 3), 'IQC1'] = ipData['IQC0'] + ipData['iTog']

    '''The deviation (IQC) is significant enough to be flagged. IQCt3, being on the left side of the equation, gets flagged in a different direction from the other two.'''

    '''ipData.loc[(ipData['goAhead'] == 1) & (ipData['numpar'] == 3) & (ipData['IQC'] >= 3), 'IQCGlo3'] = ipData['IQC0']
    ipData.loc[(ipData['goAhead'] == 1) & (ipData['numpar'] == 3) & (ipData['IQC'] >= 3), 'IQCDir3'] = ipData['IQC1']
    ipData.loc[(ipData['goAhead'] == 1) & (ipData['numpar'] == 3) & (ipData['IQC'] >= 3), 'IQCDif3'] = ipData['IQC1']'''

    ipData.loc[(ipData['goAhead'] == 1) & (ipData['numpar'] == 3) & (ipData['IQC'] >= 3), 'IQCGlobal'] = ipData['IQC0']
    ipData.loc[(ipData['goAhead'] == 1) & (ipData['numpar'] == 3) & (ipData['IQC'] >= 3), 'IQCDirect'] = ipData['IQC1']
    ipData.loc[(ipData['goAhead'] == 1) & (ipData['numpar'] == 3) & (ipData['IQC'] >= 3), 'IQCDiffuse'] = ipData['IQC1']

    # ipData.loc[(ipData['goAhead'] == 1) & (ipData['numpar'] == 3),'goAhead'] = 0 # updating the goAhead flag

    ipData.loc[(ipData['goAhead'] == 1) & (ipData['numpar'] == 3) & (
            ipData['IQCGlobal'] > 3), 'goAhead'] = 0  # updating the goAhead flag

    '''Prepare for the 2-parameter test by establishing the maximum percent KT and KN.

      * 1999/12/09 SMW and MDR changed the following two lines to correct a
      * rounding problem due to floating point representation.  The
      * extra .01 fixes any value that's a low representation and is
      * outside the granularity of the number being rounded.

      * int KNmax = XNmax * 100.0 + 0.5;
      * int KTmax = XTmax * 100.0 + 0.5;'''

    ipData['KNmax'] = 0
    ipData['KTmax'] = 0

    ipData.loc[(ipData['goAhead'] == 1), 'KNmax'] = ipData['XNmax'] * 100 + 0.51
    ipData.loc[(ipData['goAhead'] == 1), 'KTmax'] = ipData['XTmax'] * 100 + 0.51

    # Perform the 2-parameter test.  Try KT/KN. 
    ipData['sqc2_flag'] = 0
    ipData.loc[(ipData['goAhead'] == 1) & (ipData['IQCGlobal'] <= 3) & (ipData['IQCDirect'] <= 3), 'sqc2_flag'] = 1
    ipData['flag2'] = ipData['sqc2_flag']  # temp flag for further operations

    if (len(list(ipData.sqc2_flag)) > 0):
        SQC_2C('KT', 'KN', 'IQCGlobal', 'IQCDirect', ipData, curveLeft, curveRight)

        ipData.loc[(ipData['flag2'] == 1) & (ipData['IQCDiffuse'] != 3), 'goAhead'] = 0  # updating the goAhead flag

        ipData.loc[(ipData['flag2'] == 1) & (ipData['goAhead'] == 1) & (ipData['IQCGlobal'] > 21), 'IQCGlobal'] = 9
        ipData.loc[(ipData['flag2'] == 1) & (ipData['goAhead'] == 1) & (ipData['IQCGlobal'] > 21), 'IQCDirect'] = 9
        ipData.loc[(ipData['flag2'] == 1) & (ipData['goAhead'] == 1) & (ipData['IQCGlobal'] > 21), 'IQCDiffuse'] = 9

        ipData.loc[(ipData['flag2'] == 1) & (ipData['goAhead'] == 1) & (ipData['IQCGlobal'] <= 21), 'IQCGlobal'] = 3
        ipData.loc[(ipData['flag2'] == 1) & (ipData['goAhead'] == 1) & (ipData['IQCGlobal'] <= 21), 'IQCDirect'] = 3

        ipData.loc[(ipData['flag2'] == 1) & (ipData['goAhead'] == 1), 'goAhead'] = 0

    '''If IQCGLO is 1, then test KT/KD.  Otherwise, test KN/KD.'''

    ipData['sqc2_flag'] = 0  # reseting SQC flag for reuse
    ipData['flag2'] = 0  # reseting SQC flag for reuse
    ipData['KN2'] = 0
    ipData['KT2'] = 0

    ipData.loc[(ipData['goAhead'] == 1) & (ipData['IQCGlobal'] == 1), 'sqc2_flag'] = 1
    ipData['flag2'] = ipData['sqc2_flag']  # temp flag for further operations

    ipData.loc[(ipData['goAhead'] == 1) & (ipData['IQCGlobal'] == 1), 'KN2'] = ipData['KT'] - ipData['KD']

    if (len(list(ipData.sqc2_flag)) > 0):
        SQC_2C('KT', 'KN2', 'IQCGlobal', 'IQCDiffuse', ipData, curveLeft, curveRight)

    ipData['sqc2_flag'] = 0  # reseting SQC flag for reuse
    ipData['flag2'] = 0  # reseting SQC flag for reuse

    ipData.loc[(ipData['goAhead'] == 1) & (ipData['IQCGlobal'] != 1), 'sqc2_flag'] = 1
    ipData['flag2'] = ipData['sqc2_flag']  # temp flag for further operations

    ipData.loc[(ipData['goAhead'] == 1) & (ipData['IQCGlobal'] != 1), 'KT2'] = ipData['KN'] + ipData['KD']

    if (len(list(ipData.sqc2_flag)) > 0):
        SQC_2C('KT2', 'KN', 'IQCDiffuse', 'IQCDirect', ipData, curveLeft, curveRight)
        ipData.loc[(ipData['flag2'] == 1) & (ipData['goAhead'] == 1), 'IQCDiffuse'] = ipData['IQCDirect']
    ipData.loc[(ipData['goAhead'] == 1), 'goAhead'] = 0
    print('Successfully completed')

    result = pd.DataFrame({'date': ipData.date, 'Global': ipData[ipData.columns[2]], 'Flag-Global': ipData.IQCGlobal,
                           'Direct': ipData[ipData.columns[3]], 'Flag-Direct': ipData.IQCDirect,
                           'Diffuse': ipData[ipData.columns[4]], 'Flag-Diffuse': ipData.IQCDiffuse})
    name = 'output' + str(time.time()).replace('.', '-')
    """writer = pd.ExcelWriter(name + '.xlsx', engine='xlsxwriter')
    ipData.to_excel(writer, sheet_name='Final')
    result.to_excel(writer, sheet_name='refined')
    writer.save()"""
    ipData.to_csv("Final_"+name+".csv")
    result.to_csv("refined_"+name+".csv")
    dataPlots.plot_graphs(ipData, 'IQCGlobal', repFreq)
    dataPlots.write_report(ipData, latitude, longitude, timeZone, repFreq, siteName)
    frm.thankYou()
    return ipData


if __name__ == '__main__':
    result = main()  # main function will return an excel sheet
