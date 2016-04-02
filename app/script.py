"""Module to hold scripts."""
import os
import time
import numpy as np
import pandas as pd

def avg(lnums):
    """
    Return average of values in list.

    return np.array(lnums).mean()
    """
    arr = np.array(lnums)
    return arr.mean()


def std(lnums):
    """Return Standard Deviation and Standard Error."""
    arr = np.array(lnums)
    std = arr.std()
    count = len(lnums)
    stderror = std/float(count)
    return std, stderror


# def median(lnums):
#     arr = np.array(lnums)
#     med = arr.median()
#     return med

def getDescription(lnums):
    """Return dataframe description as just values in description."""
    df = pd.DataFrame(lnums)
    des = df.describe()
    count, med, std, minn, q1, q2, q3, maxx = des[0]
    return count, med, std, minn, q1, q2, q3, maxx

def stripinputlist(liststring):
    """
    Take string version of some list and returns the list of it.

    ex) "[ 1,2, 3]" -> [1, 2, 3]
    """
    while not liststring[-1].isdigit():
        liststring = liststring[:-1]
    nospace = filter(lambda x: x != ' ', liststring)
    noparen = filter(lambda x: x != '(' and x != ')', nospace)
    nobracket = filter(lambda x: x != '[' and x != ']', noparen)
    noblank = filter(lambda x: x != '', nobracket)
    nolets = filter(lambda x : not x.isalpha(), noblank)
    stringarr = nolets.split(',')
    print stringarr
    avginp = map(float, stringarr)
    return avginp
