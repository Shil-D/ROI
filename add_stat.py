# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 16:06:37 2017

@author: shil.d
"""

import pandas as pd
import os
import sys
import argparse

BASE_COLS = ['Amount']
def add_to_portfolio(file, base):
    if os.path.exists(base):
        df = pd.read_excel(base)
    else:
        df = pd.DataFrame(columns=BASE_COLS)
        
    htmlf = pd.read_html(file)
    
    acc_df = htmlf[1]
    acc_df.columns = ['Name', 'Start', 'End', 'Diff']
    start_date = pd.to_datetime(acc_df['Start'][0][-10:], dayfirst = True)
    start_amnt = float(acc_df['Start'][7].replace(',', '.').replace(' ', ''))
    
    df.loc[start_date] = {
        'Amount' : start_amnt
    }
    
    df.sort_index(inplace = True)
    ex_writer = pd.ExcelWriter(base, engine='xlsxwriter',
                               datetime_format = 'dd.mm.yyyy',
                               date_format = 'dd.mm.yyyy')
    df.to_excel(ex_writer)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str)
    parser.add_argument('base', type = str)
    args = parser.parse_args(sys.argv[1:])
    add_to_portfolio(args.filename, args.base)