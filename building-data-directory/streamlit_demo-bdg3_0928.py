# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 09:43:54 2022

@author: 靳笑宇
"""

import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

st.title('High-level List Visualization')

st.markdown("""
This app performs simple visualization of the high-level list.
* **Python libraries:** base64, pandas, streamlit
""")

st.sidebar.header('User Input Features')

path_dataset = r'C:\Users\靳笑宇\Desktop\projects in NUS\Building Directory\Dataset intro\visualization\streamlit\dataset'
dataset = pd.read_excel(os.path.join(path_dataset, 'Dataset Intro List 0928.xlsx'), header=None)
#%%
#向下填充column name使得line 2 的column name皆为有效
dataset.loc[2, dataset.loc[2].isna()] = dataset.loc[1, dataset.loc[2].isna()]
dataset.loc[2, dataset.loc[2].isna()] = dataset.loc[0, dataset.loc[2].isna()]
#%%
dataset.columns = dataset.loc[2]
dataset = dataset.drop([0,1,2]).reset_index(drop=True)
dataset = dataset.apply(pd.to_numeric, errors='ignore')
dataset.columns = dataset.columns.str.replace('\u202f', '')
dataset.columns = dataset.columns.str.replace('\xa0', '')
dataset.columns = dataset.columns.str.replace('55154\\u202f', '')
dataset.columns = dataset.columns.str.replace('\u202f\xa0', '')
#dataset_info = [str(x).encode('UTF8') for x in dataset_info]
dataset_info = dataset.iloc[:35, :7]
dataset_info ['Building Type'] = dataset['Building Type']
dataset_info ['URL'] = dataset['URL']
dataset_info.iloc[:,:8] = dataset_info.iloc[:,:8].astype(str)

#%%
country_list = dataset_info['Country'].unique().tolist()
country_list.append('All')
selected_country = st.sidebar.selectbox('Country', country_list)
if selected_country!= 'All':
    dataset_info = dataset_info.loc[dataset_info['Country']==selected_country]
else:
    dataset_info = dataset_info

city_list = dataset_info['City/District'].unique().tolist()
city_list.append('All')   
selected_city = st.sidebar.selectbox('City/District', city_list)
if selected_city!= 'All':
    dataset_info = dataset_info.loc[dataset_info['City/District']==selected_city]
else:
    dataset_info = dataset_info
#%%
var1 = 'Time Interval'
list_var1 = sorted(dataset_info[var1].unique())
selected_var1 = st.sidebar.multiselect(var1, list_var1, list_var1)

#%%
var2 = 'Building Type'
# Sidebar - Building type selection
list_var2 = sorted(dataset_info[var2].unique())
selected_var2 = st.sidebar.multiselect(var2, list_var2, list_var2)

#%%
# Filtering data
dataset_info_filtered = dataset_info[(dataset_info[var1].isin(selected_var1)) & (dataset_info[var2].isin(selected_var2))]

st.write('Data Dimension: ' + str(dataset_info_filtered.shape[0]) + ' rows and ' + str(dataset_info_filtered.shape[1]) + ' columns.')

#%%
def filedownload(df):
   csv = df.to_csv(index=False)
   b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
   href = f'<a href="data:file/csv;base64,{b64}" download="dataset_info.csv">Download CSV File</a>'
   return href

st.dataframe(dataset_info_filtered)
#st.write(dataset_info_filtered.to_html(escape=False, index=False), unsafe_allow_html=True)
st.markdown(filedownload(dataset_info_filtered), unsafe_allow_html=True)

