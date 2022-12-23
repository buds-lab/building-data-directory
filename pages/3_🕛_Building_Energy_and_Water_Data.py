# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 09:43:54 2022

@author: 靳笑宇
"""

import streamlit as st
import pandas as pd
from pandas import DataFrame
import base64
import altair as alt
import plotly.express as px
from gspread_pandas import Spread,Client
from google.oauth2 import service_account
import ssl 

st.title('Building Energy and Water Data')

st.markdown("""
##### The building energy and water datasets include the measured building energy or water consumption data.\n
##### Some datasets also provide extra information of the buildings.\n
##### The visualization of meta data can be found below the form.
""")

st.sidebar.header('User Input Features')
#%%
# Get the sheet as dataframe
def load_the_spreadsheet(spreadsheetname):
    worksheet = sh.worksheet(spreadsheetname)
    df = DataFrame(worksheet.get_all_records())
    return df
#%% 
#Link to google sheet
ssl._create_default_https_context = ssl._create_unverified_context

# Create a Google Authentication connection object
scope = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"]
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope)
client = Client(scope=scope,creds=credentials)

spreadsheetname = "Dataset_Intro_List"
spread = Spread(spreadsheetname,client = client)
sh = client.open(spreadsheetname)
dataset = load_the_spreadsheet('3.Energy')
#%%
# Get the sheet as dataframe
def load_the_spreadsheet(spreadsheetname):
    worksheet = sh.worksheet(spreadsheetname)
    df = DataFrame(worksheet.get_all_records())
    return df
#%%
#dataset.columns = dataset.loc[0]
dataset = dataset.drop([0,1,2]).reset_index(drop=True)
dataset = dataset.apply(pd.to_numeric, errors='ignore')
dataset.columns = dataset.columns.str.replace('\u202f', '')
dataset.columns = dataset.columns.str.replace('\xa0', '')
dataset.columns = dataset.columns.str.replace('55154\\u202f', '')
dataset.columns = dataset.columns.str.replace('\u202f\xa0', '')
#dataset_info = [str(x).encode('UTF8') for x in dataset_info]
#%%
dataset_info = dataset.iloc[:, :8]
dataset_info ['Building Type'] = dataset['Building Type']
dataset_info ['URL'] = dataset['URL']
dataset_info.iloc[:,:9] = dataset_info.iloc[:,:9].astype(str)

dataset_info ['Start Year of Recording'] = dataset['Starting Year of Recording']
dataset_info ['End Year of Recording'] = dataset['End Year of Recording (by 06/09/2022)']

dataset_info ['Earliest Year of Built'] = dataset['Earliest Year of Built']
dataset_info ['Latest Year of Built'] = dataset['Latest Year of Built']

dataset_info ['Minimum Floor Area'] = dataset['Minimum Floor Area (m2)']
dataset_info ['Maximum Floor Area'] = dataset['Maximum Floor Area (m2)']

dataset_info['Sample Number'] = dataset['Sample Number'] 
dataset_info['Variable Number'] = dataset['Variable Number']

dataset_info[['Dataset Abbreviation','Energy Rating', 'Occupancy','Envelope Information', 'Household Information',
       'Energy Device Installation', 'Green House Gas Emission']] = dataset[['Dataset Abbreviation','Energy Rating', 'Occupancy',
       'Envelope Information', 'Household Information',
       'Energy Device Installation', 'Green House Gas Emission']]

dataset_info[['Total Energy Consumption', 'Electricity Consumption',
       'Gas Consumption', 'Primary Energy Usage']] = dataset[['Total Energy Consumption', 'Electricity Consumption',
       'Gas Consumption', 'Primary Energy Usage']]
#%%
country_list = dataset_info['Country'].unique().tolist()
country_list.append('All')
country_list.sort()
selected_country = st.sidebar.selectbox('Country', country_list)
if selected_country!= 'All':
    dataset_info = dataset_info.loc[dataset_info['Country']==selected_country]
else:
    dataset_info = dataset_info

city_list = dataset_info['City/District'].unique().tolist()
city_list.append('All')
city_list.sort()
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
#list_var2 = sorted(dataset_info[var2].unique())
list_var2 = ['Commercial', 'Residential']
selected_var2 = st.sidebar.multiselect(var2, list_var2, list_var2)

#%%
# Filtering data
if len(selected_var2)<2:
    dataset_info_filtered = dataset_info[(dataset_info[var1].isin(selected_var1)) & (dataset_info[var2].isin(selected_var2))]
    
else:
    dataset_info_filtered = dataset_info[dataset_info[var1].isin(selected_var1)]
    
dataset_info_filtered.columns = dataset_info_filtered.columns.rename(name='#') 
                                                                 
st.write('Data Dimension: ' + str(dataset_info_filtered.shape[0]) + ' rows and ' + str(dataset_info_filtered.shape[1]) + ' columns.')

#%%
def filedownload(df):
   csv = df.to_csv(index=False)
   b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
   href = f'<a href="data:file/csv;base64,{b64}" download="dataset_info.csv">Download CSV File</a>'
   return href
#%%
dataset_info_filtered.reset_index(drop = True, inplace = True)
#%%
for i in range(len(dataset_info_filtered)):
    url = dataset_info_filtered['URL'][i]
    dataset_info_filtered['URL'][i] =  f'<a href="{url}">{url}</a>'
#%%
dataset_info_filtered = dataset_info_filtered.reset_index(drop=True)
dataset_info_filtered.index = dataset_info_filtered.index + 1 
dataset_html = dataset_info_filtered.to_html(escape=False)
st.write(dataset_html, unsafe_allow_html=True)
#st.dataframe(dataset_info_filtered)
st.markdown(filedownload(dataset_info_filtered), unsafe_allow_html=True)
#%%
#Bar plot for recording year
with st.expander("Recording Years"):
    st.markdown("""
    * **Recording Years**
    """)
    y_axis1 = alt.Axis(
        offset=5,
        #labelLimit=500,
        #minExtent=200,
        domain=False
    )
    
    bar1 = alt.Chart(dataset_info_filtered).mark_bar().encode(
        x=alt.X('Start Year of Recording', scale=alt.Scale(domain=[1978, 2023])),
        x2='End Year of Recording',
        y=alt.Y('Dataset Abbreviation', title="Datasets", axis=y_axis1)
    ).properties(
        width=450,
        height=500
    ).configure_axisY(
        titleAngle=0,
        titleY=-10,
        titleX=-10,
    )
    st.altair_chart(bar1.interactive(), use_container_width=True)
#%%
#Bar plot for year of built
with st.expander("Year of Built"):
    st.markdown("""
    * **Year of Built**
    """)
    y_axis2 = alt.Axis(
        offset=5,
        domain=False
    )
    bar2 = alt.Chart(dataset_info_filtered).mark_bar().encode(
        x=alt.X('Earliest Year of Built', scale=alt.Scale(domain=[1900, 2023])),
        x2='Latest Year of Built',
        y=alt.Y('Dataset Abbreviation', title="Datasets", axis=y_axis2)
    ).properties(
        width=450,
        height=500
    ).configure_axisY(
        titleAngle=0,
        titleY=-10,
        titleX=-10,
    )
    st.altair_chart(bar2.interactive(), use_container_width=True)
#%%
#Bar plot for floor area
with st.expander("Floor Areas"):
    st.markdown("""
    * **Floor Areas (square meter)**
    """)
    
    y_axis3 = alt.Axis(
        offset=5,
        domain=False
    )
    bar3 = alt.Chart(dataset_info_filtered).mark_bar().encode(
        x=alt.X('Minimum Floor Area', scale=alt.Scale(domain=[0, 1000000])),
        x2='Maximum Floor Area',
        y=alt.Y('Dataset Abbreviation', title="Datasets", axis=y_axis3)
    ).properties(
        width=450,
        height=500
    ).configure_axisY(
        titleAngle=0,
        titleY=-10,
        titleX=-10,
    )
    st.altair_chart(bar3.interactive(), use_container_width=True)    
#%%
#Bubble plot for sample number
with st.expander("Sample Numbers"):
    st.markdown("""
    * **Sample Numbers**
    """)
    
    bub1 = alt.Chart(dataset_info_filtered).mark_circle().encode(
        alt.X('Sample Number', scale=alt.Scale(zero=False)),
        alt.Y('Dataset Abbreviation', title="Datasets",scale=alt.Scale(zero=False, padding=1)),
        #color='Dataset Abbreviation',
        size='Sample Number'
    ).properties(
        width=600,
        height=450
    ).configure_axisY(
        titleAngle=0,
        titleY=-10,
        titleX=-10,
    )
    st.altair_chart(bub1.interactive(), use_container_width=True)   
#%%
#Bubble plot for variable number
with st.expander("Variable Numbers"):
    st.markdown("""
    * **Variable Numbers**
    """)
    
    bub1 = alt.Chart(dataset_info_filtered).mark_circle().encode(
        alt.X('Variable Number', scale=alt.Scale(zero=False)),
        alt.Y('Dataset Abbreviation', title="Datasets",scale=alt.Scale(zero=False, padding=1)),
        #color='Dataset Abbreviation',
        size='Variable Number'
    ).properties(
        width=600,
        height=450
    ).configure_axisY(
        titleAngle=0,
        titleY=-10,
        titleX=-10,
    )
    st.altair_chart(bub1.interactive(), use_container_width=True)   
#%%Heatmap for variable types
source1 = dataset_info_filtered[['Dataset Abbreviation','Energy Rating', 'Occupancy',
       'Envelope Information', 'Household Information',
       'Energy Device Installation', 'Green House Gas Emission']]
df1 = source1.set_index('Dataset Abbreviation')
df1.columns = df1.columns.rename(name='Variable Type (0 = not included, 1 = included)')
with st.expander("Variable Type"):
    st.markdown("""
    * **Variable Type Distribution of the Datasets**
    """)
    fig1 = px.imshow(df1,text_auto=True,aspect="auto",width=900, height=600)
    fig1.update_xaxes(tickangle=45,side="bottom",tickfont=dict(family='Rockwell', size=10))
    fig1.update_yaxes(tickfont=dict(family='Rockwell', size=10))
    fig1.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig1, use_container_width=True)
#%%Heatmap for energy consumption variable types
source2 = dataset_info_filtered[['Dataset Abbreviation','Total Energy Consumption', 'Electricity Consumption',
       'Gas Consumption', 'Primary Energy Usage']]
df2 = source2.set_index('Dataset Abbreviation')
df2.columns = df2.columns.rename(name='Variable Categories of Energy Consumption')
with st.expander("Variable Categories of Energy Consumption"):
    st.markdown("""
    * **Variable Categories of Energy Consumption**
    (0 for not having this variable, 1 for having numerical variable, 2 for having categorical variable)
    """)
    fig2 = px.imshow(df2,text_auto=True,aspect="auto",width=900, height=600)
    fig2.update_xaxes(tickangle=45,side="bottom",tickfont=dict(family='Rockwell', size=10))
    fig2.update_yaxes(tickfont=dict(family='Rockwell', size=10))
    fig2.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig2, use_container_width=True)
