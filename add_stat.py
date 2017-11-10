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

BASE_COLS = ['Amount', 'Total Commision']

def add_to_portfolio(folder, base):
    if os.path.exists(base):
        log.info('output file ' + base + ' already exists')
        df = pd.read_excel(base)
    else:
        log.info("output file ' + base + ' doesn't exists. Creating new one.")
        df = pd.DataFrame(columns=BASE_COLS)
        
    for file in os.listdir(folder):
        log.info('folud file ' + file)
        htmlf = pd.read_html(os.path.join(folder,file), thousands='', decimal = ',')
        
        #fetching dfs
        acc_df = htmlf[1]
        acc_df.columns = ['Name', 'Start', 'End', 'Diff']
        netorg_ops_df = htmlf[7]
        netorg_ops_df.columns = ['Date', 'Type', 'Instr', 'Currency',
                                 'Income', 'Outcome', 'Value', 'Comments']
        ops_df = htmlf[9]
        
        #fetch acc amount
        start_date = pd.to_datetime(acc_df['Start'][0][-10:], dayfirst = True)
        start_amnt = float(acc_df['Start'][7].replace(',', '.').replace(' ', ''))
        
         #fetch depositary commision
        field = netorg_ops_df['Type']=='Комиссия депозитария (итого)'
        if field.any():
            dep_com_amnt = -float(netorg_ops_df['Value'][field])
        else:
            dep_com_amnt = 0
    
        #fetch commision
        field = ops_df[2]=='ИТОГО:'
        if field.any():
            com_amnt = float(ops_df[14][field])
        else:
            com_amnt = 0 
        
        total_com = dep_com_amnt + com_amnt

        df.loc[start_date] = {
            'Amount' : start_amnt,
            'Total Commision' : total_com
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