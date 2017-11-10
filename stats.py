# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 15:58:17 2017

@author: shil.d
"""

import pandas as pd
import os
import numpy as np
import argparse
import sys
import matplotlib.pyplot as plt

def max_dd(ser):
    max2here = ser.expanding().max()
    dd2here = ser - max2here
    return -dd2here.min()

def max_ddd(ser):
    ddd = ser.copy()
    ddd[0] = 0
    max2here = ser.expanding().max()
    dd2here = max2here - ser
    for i in range(1,len(dd2here != 0)):
        if dd2here[i-1] == 0:
            ddd[i] = 0
        else:
            ddd[i] = ddd[i-1] + 1
    return ddd.max()

def main(base_file, risk_free_file):
    df = pd.read_excel(base_file)
    risk_free = pd.read_excel(risk_free_file)
    amnt = df.Amount
    risk_free = risk_free.reindex(index = df.index, method='ffill', copy=False)
    df['Daily_Profits'] = amnt.diff()
    df['Daily_Returns'] = amnt.pct_change()
    daily_rets = df['Daily_Returns']
    cum_rets = daily_rets.cumsum() + 1
    risk_free_rates = risk_free['RiskFreeRate'] / 252
    df['Excess_Returns'] = daily_rets - risk_free_rates
    exc_rets = df['Excess_Returns']
    exc_cum_rets = exc_rets.cumsum() + 1
    sharpe = np.sqrt(252)*exc_rets.mean()/exc_rets.std()
    mdd = max_dd(cum_rets)
    mddd = max_ddd(cum_rets)
    props = dict(boxstyle= 'round', facecolor='wheat', alpha=0.5)
    textstr = 'Sharpe = %.2f\nMaxDD = %.3f%%\nMaxDDD = %d' % (sharpe, mdd*100, mddd)
    fig, ax = plt.subplots(1)
    cum_rets.plot(ax = ax)
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', bbox=props)
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('base', type = str)
    parser.add_argument('risk_free', type=str)
    args = parser.parse_args(sys.argv[1:])
    main(args.base, args.risk_free)