# -*- coding: utf-8 -*-

import pandas as pd
from matplotlib import pyplot as plt

LAT = 'Land Average Temperature'
LOAT = 'Land And Ocean Average Temperature'
TG = 'Total GHG'
gas = ['EN.ATM.CO2E.KT', 'EN.ATM.METH.KT.CE', 'EN.ATM.NOXE.KT.CE', 'EN.ATM.GHGO.KT.CE', 'EN.CLC.GHGR.MT.CE']

def clean_data():
    df_y = pd.read_excel("ClimateChange.xlsx")
    df_y = df_y[df_y['Series code'].isin(gas)].iloc[:, 6:-1]
    df_y.replace({'..': pd.np.NaN}, inplace=True)
    df_y = df_y.fillna(method='ffill', axis=1).fillna(method='bfill', axis=1)
    df_y.replace({pd.np.NaN: 0}, inplace=True)
    df_y = df_y.sum()
    df_y.index = pd.to_datetime(df_y.index, format='%Y')

    df_q = pd.read_excel("GlobalTemperature.xlsx")
    df_q['Date'] = pd.to_datetime(df_q['Date'])
    df_q.set_index('Date', inplace=True)
    df_q = df_q[[LAT, LOAT]].replace({pd.np.NaN: 0})

    tmpA = df_q.resample('AS').mean() 
    df_q = df_q.resample('QS').mean()
    tmpA = tmpA.loc["1990-1-1":"2010-1-1", :]
    
    df_y = pd.concat([tmpA, df_y], axis=1)
    df_y.columns = [LAT, LOAT, TG]
    df_y = (df_y - df_y.min()) / (df_y.max() - df_y.min())
    return df_y, df_q

def climate_plot():
    df_y, df_q = clean_data()
    fig, axes = plt.subplots(2, 2)
    ax1 = df_y.plot(kind='line', figsize=(16,9), ax=axes[0,0])    
    ax2 = df_y.plot(kind='bar', figsize=(16,9), ax=axes[0,1])    
    ax3 = df_q.plot(kind='area', figsize=(16,9), ax=axes[1,0])    
    ax4 = df_q.plot(kind='kde', figsize=(16,9), ax=axes[1,1])    
    ax1.set_xlabel('Years')
    ax1.set_ylabel('Values')
    ax2.set_xlabel('Years')
    ax2.set_ylabel('Values')
    ax3.set_xlabel('Quarters')
    ax3.set_ylabel('Temperature')
    ax4.set_xlabel('Values')
    ax4.set_ylabel('Values')

    fig.show()
    return fig

climate_plot()
