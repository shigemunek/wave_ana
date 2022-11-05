# -*- coding: utf-8 -*-

# typical usage
# python .\ana.py -span '6h' -sdt '2022-10-06 12:00' -edt '2022-10-07 12:00' -scale 1000
# Remember to add an apostrophe to the string.

# Use python version 3.10 or higher.
# Line 28 of the file to be read should be as follows
# date,presure[MPa],depth[m],volt[V],unknown,

# The file to be read must be encoded in UTF-8.

# statistic
# mean:arithmetic average
# median:arithmetic median
# std:arithmetic standard deviation

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import argparse
import datetime
from enum import IntEnum

class MesurementType(IntEnum):
    # Do not change the number
    PRESSURE = 0
    DEPTH = 1
    VOLTAGE = 2
    unknown = 3
    Unnamed = 4

class SpanType(IntEnum):
    TEN_MIN = 1
    ONE_HOUR = 2
    SIX_HOUR = 3
    ONE_DAY = 4
    ONE_WEEK = 5
    ONE_MONTH = 6
    UNKNOWN = 7

class dataset:

    def __init__(self, filename, row, type, l_range, u_range, startdatetime, enddatetime, span, fontsize, scale):
        self.filename = filename
        self.row = int(row)
        if type=='depth':
            self.type = MesurementType.DEPTH
        elif type == 'pressure':
            self.type = MesurementType.PRESSURE
        elif type == 'volt':
            self.type = MesurementType.VOLTAGE

        self.l_range = float(l_range)
        self.u_range = float(u_range)
        #2022-10-06 12:00
        s = startdatetime.split()
        s1 = s[0].split('-')
        s2 = s[1].split(':')
        sdt = datetime.datetime(int(s1[0]), int(s1[1]), int(s1[2]), int(s2[0]), int(s2[1]))
        self.startdatetime = sdt
        e = enddatetime.split()
        e1 = e[0].split('-')
        e2 = e[1].split(':')
        edt = datetime.datetime(int(e1[0]), int(e1[1]), int(e1[2]), int(e2[0]), int(e2[1]))
        self.enddatetime = edt

        if span=='10min':
            self.span = SpanType.TEN_MIN
        elif span == '1h':
            self.span = SpanType.ONE_HOUR
        elif span == '6h':
            self.span = SpanType.SIX_HOUR
        elif span == '1day':
            self.span = SpanType.ONE_DAY
        elif span == '1week':
            self.span = SpanType.ONE_WEEK
        elif span == '1month':
            self.span = SpanType.ONE_MONTH
        else:
            self.span = SpanType.UNKNOWN

        self.fontsize = int(fontsize)

        self.std_scale = int(scale)



def genDateTimeList(starttime, endtime, span):
    list=[]
    match SpanType(span):
        case SpanType.TEN_MIN:
            td_delta = datetime.timedelta(minutes=10)
        case SpanType.ONE_HOUR:
            td_delta = datetime.timedelta(hours=1)
        case SpanType.SIX_HOUR:
            td_delta = datetime.timedelta(hours=6)
        case SpanType.ONE_DAY:
            td_delta = datetime.timedelta(days=1)
        case SpanType.ONE_WEEK:
            td_delta = datetime.timedelta(days=7)
        case SpanType.ONE_MONTH:
            td_delta = datetime.timedelta(days=31)
        case _:
            td_delta = datetime.timedelta(hours=1)
    endflag = False
    while True:

        if endflag:
            return list

        str_s1 =  starttime.strftime("%Y-%m-%d %H:%M")
        starttime = starttime + td_delta
        str_s2 =  starttime.strftime("%Y-%m-%d %H:%M")
        if starttime>=endtime:
            endflag = True
      
        #date >= "2022-10-06 12:00" and date < "2022-10-06 13:00"
        list.append('date >="' + str_s1 + '" and date < "' + str_s2 + '"')
    
def genTitleList(starttime, endtime, span):
    list=[]
    match SpanType(span):
        case SpanType.TEN_MIN:
            td_delta = datetime.timedelta(minutes=10)
        case SpanType.ONE_HOUR:
            td_delta = datetime.timedelta(hours=1)
        case SpanType.SIX_HOUR:
            td_delta = datetime.timedelta(hours=6)
        case SpanType.ONE_DAY:
            td_delta = datetime.timedelta(days=1)
        case SpanType.ONE_WEEK:
            td_delta = datetime.timedelta(days=7)
        case SpanType.ONE_MONTH:
            td_delta = datetime.timedelta(days=31)
        case _:
            td_delta = datetime.timedelta(hours=1)
            
    endflag = False
    while True:

        if endflag:
            return list

        str_s1 =  starttime.strftime("%Y-%m-%d %H_%M")
        starttime = starttime + td_delta
        str_s2 =  starttime.strftime("%Y-%m-%d %H_%M")
        if starttime>=endtime:
            endflag = True
        
        #2022-10-06 12_00_2022-10-06 13_00
        list.append(str_s1 + '___' + str_s2)

def genGraphTextList(starttime, endtime, span):
    list=[]
    match SpanType(span):
        case SpanType.TEN_MIN:
            td_delta = datetime.timedelta(minutes=10)
        case SpanType.ONE_HOUR:
            td_delta = datetime.timedelta(hours=1)
        case SpanType.SIX_HOUR:
            td_delta = datetime.timedelta(hours=6)
        case SpanType.ONE_DAY:
            td_delta = datetime.timedelta(days=1)
        case SpanType.ONE_WEEK:
            td_delta = datetime.timedelta(days=7)
        case SpanType.ONE_MONTH:
            td_delta = datetime.timedelta(days=31)
        case _:
            td_delta = datetime.timedelta(hours=1)
            
    endflag = False
    while True:

        if endflag:
            return list

        draw_x = dates.date2num(starttime)
        
        starttime = starttime + td_delta

        if starttime>=endtime:
            endflag = True
        
        list.append(draw_x)

def convType(type):
    match MesurementType(type):
        case MesurementType.PRESSURE:
            return 'pressure'

        case MesurementType.DEPTH:
            return 'depth'

        case MesurementType.VOLTAGE:
            return 'volt'
    
    return ''

parser = argparse.ArgumentParser()
parser.add_argument('-file', default='20221003_0000_AWH-USB_0004_141336_A.csv')
parser.add_argument('-row',default=27)
# pressure:圧力, depth:深さ, volt:電圧
parser.add_argument('-type',default='pressure')
#parser.add_argument('-type',default='depth')
#parser.add_argument('-type',default='volt')
parser.add_argument('-lower_range',default=0.04)
parser.add_argument('-upper_range',default=0.06)
parser.add_argument('-sdt',default='2022-10-06 12:00')
parser.add_argument('-edt',default='2022-10-06 18:00')
parser.add_argument('-fontsize',default=36)
#span -> 10min, 1h, 6h, 1day, 1week, 1month
#parser.add_argument('-span',default='10min')
parser.add_argument('-span',default='1h')
#parser.add_argument('-span',default='6h')
#parser.add_argument('-span',default='1day')
#parser.add_argument('-span',default='1week')
#parser.add_argument('-span',default='1month')

parser.add_argument('-scale',default=1)

args = parser.parse_args()

ds = dataset(args.file, args.row, args.type, 
            args.lower_range, args.upper_range, 
            args.sdt, args.edt, args.span, 
            args.fontsize,args.scale)

df = pd.read_csv(ds.filename,header=ds.row)
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

query_list = genDateTimeList(ds.startdatetime,ds.enddatetime,ds.span)
#print(query_list)
title_list = genTitleList(ds.startdatetime,ds.enddatetime, ds.span)
graphtext_list = genGraphTextList(ds.startdatetime,ds.enddatetime, ds.span)

plt.rcParams["figure.figsize"] = [32,24]
count=0
for l in query_list:
    #print(l)
    df_tmp = df.query(l)
    max = df_tmp.max(axis=0)
    min = df_tmp.min(axis=0)
    mean = df_tmp.mean(axis=0)
    median = df_tmp.median(axis=0)
    std = df_tmp.std(axis=0)
    std_facted = std[ds.type]*float(ds.std_scale)

    max_str='{:.3f}'.format(max[ds.type])
    min_str='{:.3f}'.format(min[ds.type])
    mean_str='{:.3f}'.format(mean[ds.type])
    median_str='{:.3f}'.format(median[ds.type])
    std_str='{:.3f}'.format(std_facted)

    print('max=' + max_str)
    print('min=' + min_str)
    print('mean=' + mean_str)
    print('median=' + median_str)
    print('std=' + std_str)
    
    match MesurementType(ds.type):
        case MesurementType.PRESSURE:
            df_tmp.iloc[:,0:1].plot()
            plt.ylabel("pressure[MPa]", fontsize=ds.fontsize)

        case MesurementType.DEPTH:
            df_tmp.iloc[:,1:2].plot()
            plt.ylabel("depth[m]", fontsize=ds.fontsize)

        case MesurementType.VOLTAGE:
            df_tmp.iloc[:,2:3].plot()
            plt.ylabel("voltage[V]", fontsize=ds.fontsize)
            

    plt.title(title_list[count], fontsize=ds.fontsize)
    plt.xlabel('datetime', fontsize=ds.fontsize)
    plt.ylim(ds.l_range, ds.u_range)
    plt.grid()
    plt.legend(fontsize=ds.fontsize)
    plt.xticks(rotation=30)
    plt.tick_params(labelsize=ds.fontsize)
    dx = graphtext_list[count]
    drawtext = 'max=' + max_str + '\n' + \
    'min=' + min_str + '\n' + \
    'mean=' + mean_str + '\n' + \
    'median=' + median_str + '\n' + \
    'std=' + std_str + ' scale:X' + str(ds.std_scale)
    #print(drawtext)
    plt.text(dx,ds.u_range-((ds.u_range-ds.l_range)/5.0),drawtext, fontsize=ds.fontsize)
    plt.savefig(title_list[count] + '_' + convType(ds.type) +'.png')
    plt.clf()
    count = count + 1
