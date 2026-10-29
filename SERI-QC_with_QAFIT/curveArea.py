#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 12/26/19 12:15 PM

@author : rahul gupta (rgupta2)

"""
import numpy as np
import pandas as pd
import utills as ut

#col =["y"]


def getArea(shape):
    y = (np.linspace(1, 100, 100))
    y = [int(i) for i in y]
    if shape == "left":
        curve = ut.curveLeft
        end = 7
    elif shape == "right":
        curve = ut.curveRight
        end = 6
    else:
        print("Shape should be <left> or <right>")
        return

    cols = {"y": y}
    for i in range(1, end):
        for j in range(1, 21):
            val = []
            toAdd = 0
            shift = (j - 1) * 2.5
            for k in y:
                if curve[i - 1][(k - 1)] < 0:
                    toAdd += 0
                    val.append(toAdd)
                else:
                    toAdd += min(curve[i - 1][(k - 1)] + shift, 100)
                    val.append(toAdd)
            cols[str(i) + "-" + str(j)] = val

    table = pd.DataFrame(cols)
    return table
tl = getArea("left")
tr = getArea("right")



"""

import matplotlib.pyplot as plt
y = (np.linspace(1, 100, 100))
y = [int(i) for i in y]
plt.plot()

plt.xlim(1,100)
plt.ylim(1,100)
plt.plot(y,y)
plt.plot(ut.curveLeft[0], y )
plt.plot(ut.curveLeft[0]+50, y )

plt.plot(ut.curveRight[0], y )


"""




















































































































































