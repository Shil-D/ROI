# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 16:06:37 2017

@author: shil.d
"""

import pandas as pd
import os
import sys
import argparse
import logging as log

BASE_COLS = ['Amount']

def add_to_portfolio(folder, base):
    if os.path.exists(base):
        log.info('output file ' + base + ' already exists')
        df = pd.read_excel(base)
    else:
        log.info("output file ' + base + ' doesn't exists. Creating new one.")
        df = pd.DataFrame(columns=BASE_COLS)
        
    for file in os.listdir(folder):
        log.info('folud file ' + file)
        htmlf = pd.read_html(os.path.join(folder,file))
        
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
    parser.add_argument('base', type = str)
    parser.add_argument('folder', type=str,help='Input html folder')
    args = parser.parse_args(sys.argv[1:])
    add_to_portfolio(args.folder, args.base)