# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 10:29:01 2022

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

st.set_page_config(
    page_title="Smart Grid Data"
)
st.write("# Smart Grid Data")
#%%
# Get the sheet as dataframe
def load_the_spreadsheet(spreadsheetname):
    worksheet = sh.worksheet(spreadsheetname)
    df = DataFrame(worksheet.get_all_records())
    return df
#%%
# Function of file download
def filedownload(df):
   csv = df.to_csv(index=False)
   b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
   href = f'<a href="data:file/csv;base64,{b64}" download="dataset_info.csv">Download CSV File</a>'
   return href
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
dataset = load_the_spreadsheet('7.Smart Grid')
#%%
dataset= dataset.reset_index(drop=True)

for i in range(len(dataset)):
    url = dataset['URL'][i]
    dataset['URL'][i] =  f'<a href="{url}">{url}</a>'

dataset.index = dataset.index + 1 
dataset_html = dataset.to_html(escape=False)
st.write(dataset_html, unsafe_allow_html=True)
#st.dataframe(dataset_info_filtered)
st.markdown(filedownload(dataset), unsafe_allow_html=True)         