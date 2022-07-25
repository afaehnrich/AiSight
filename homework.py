import streamlit as st
import pandas as pd
import requests
import json
import plotly.express as px
from datetime import datetime

src_url = 'https://opendata.ecdc.europa.eu/covid19/nationalcasedeath_eueea_daily_ei/json/'

features = {\
    'cases per 100000': (lambda x: x['cases'] / x['popData2020'] * 100000),\
    'deaths per 100000': (lambda x: x['deaths'] / x['popData2020'] * 100000),\
    'cases':  (lambda x: x['cases']),\
    'deaths':  (lambda x: x['deaths'])\
}

DATE_COL_RAW = 'dateRep'
DATE_COL = 'date'
COUNTRY_COL_RAW = 'countriesAndTerritories'
COUNTRY_COL = 'country'
POPULATION_DATA_COL = 'popData2020'

@st.cache
def getRawData(url):
    res  = requests.get(src_url)
    #print('getRawData')
    return res.content    

@st.cache
def transformData(raw_data):    
    raw_data = pd.DataFrame(json.loads(raw_data)['records'])
    raw_data[POPULATION_DATA_COL] = raw_data[POPULATION_DATA_COL].astype('int')    
    data = pd.DataFrame()
    data[DATE_COL] = pd.to_datetime(raw_data[DATE_COL_RAW], format='%d/%m/%Y')
    data[COUNTRY_COL] = raw_data[COUNTRY_COL_RAW]
    for feature, lambda_func in features.items():
        data[feature] = raw_data.apply(lambda_func, axis=1)
    return data

def showPlot(data, countries, feature):    
    fig = px.line(data[data[COUNTRY_COL].isin(countries)], x=DATE_COL, y = feature, color=COUNTRY_COL)
    st.plotly_chart(fig )

def main():
    data = transformData(getRawData(src_url))
    st.title('Covid Cases WorldWide')
    countries = st.multiselect('Select Countries', data[COUNTRY_COL].unique())
    feature = st.selectbox('Select Data to show', features.keys())
    showPlot(data, countries, feature)


if __name__ == '__main__':
    if st._is_running_with_streamlit:
        main()
