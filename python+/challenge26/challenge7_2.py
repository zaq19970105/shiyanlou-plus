# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt

def data_clean():
    data = pd.read_excel("ClimateChange.xlsx")
    data = data[(data['Series code'] == 'EN.ATM.CO2E.KT') | (data['Series code'] == 'NY.GDP.MKTP.CD')].set_index('Country code')
    temp = data['Series code']
    data = data.iloc[:, 5:]
    data.replace({'..': pd.np.NaN}, inplace=True)
    data = data.fillna(method='ffill', axis=1).fillna(method='bfill', axis=1)
    data.replace({pd.np.NaN: 0}, inplace=True)
    data['Sum'] = data.sum(axis=1)
    data['Series code'] = temp
    data = data[['Series code', 'Sum']]

    dCO2 = data[data['Series code'] == 'EN.ATM.CO2E.KT']
    dGDP = data[data['Series code'] == 'NY.GDP.MKTP.CD']
    
    Xmin = dCO2['Sum'].min()
    Xmax = dCO2['Sum'].max()
    Ymin = dGDP['Sum'].min()
    Ymax = dGDP['Sum'].max()

    dCO2['Sum'] = dCO2['Sum'].apply(lambda x: (x-Xmin) / (Xmax-Xmin))
    dGDP['Sum'] = dGDP['Sum'].apply(lambda y: (y-Ymin) / (Ymax-Ymin))
    return dCO2, dGDP 


def co2_gdp_plot():
    df_CO2, df_GDP = data_clean()
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.set_title('GDP-CO2')
    ax.set_xlabel('Countries')
    ax.set_ylabel('Values')
    y = ['CHN', 'FRA', 'GBR', 'RUS', 'USA']
    x = [t[0] for t in enumerate(df_GDP.index) if t[1] in y]
    plt.xticks(x, y, rotation=90)
    ax.plot(df_CO2['Sum'].values, label='CO2-SUM')
    ax.plot(df_GDP['Sum'].values, label='GDP-SUM')
    ax.legend()
    plt.show()

    china = [pd.np.around(i, 3) for i in [float(df_CO2.loc[['CHN'], ['Sum']].values), float(df_GDP.loc[['CHN'], ['Sum']].values)]]
    #china = ['{:.3f}'.format(float(df_CO2.loc[['CHN'], ['Sum']].values)), '{:.3f}'.format(float(df_GDP.loc[['CHN'], ['Sum']].values))]
    return ax, china

if __name__ == '__main__':
    print(co2_gdp_plot())
