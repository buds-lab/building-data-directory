# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 10:03:01 2022

@author: 靳笑宇
"""

import streamlit as st 
from pandas import DataFrame
import pandas as pd
from gspread_pandas import Spread,Client
from google.oauth2 import service_account
import ssl 

ssl._create_default_https_context = ssl._create_unverified_context

# Create a Google Authentication connection object
scope = ["https://www.googleapis.com/auth/spreadsheets",
         'https://www.googleapis.com/auth/drive']

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope)

#%%
client = Client(scope=scope,creds=credentials)

spreadsheetname = "Energy_Dataset_Intro_List_1017"
spread = Spread(spreadsheetname,client = client)

#%%
# Check the connection
st.write(spread.url)

sh = client.open(spreadsheetname)
worksheet_list = sh.worksheets()
# Functions 
@st.cache()
# Get our worksheet names
def worksheet_names():
    sheet_names = []   
    for sheet in worksheet_list:
        sheet_names.append(sheet.title)  
    return sheet_names

# Get the sheet as dataframe
def load_the_spreadsheet(spreadsheetname):
    worksheet = sh.worksheet(spreadsheetname)
    df = DataFrame(worksheet.get_all_records())
    return df

# Update to Sheet
def update_the_spreadsheet(spreadsheetname,dataframe):
    #col = ['Dataset Full Name','URL']
    spread.df_to_sheet(dataframe,sheet = spreadsheetname,index= False)
    st.sidebar.info('✅ Submitted succussfully! Thank you for contributing!')
#%%  
st.header('Building Energy and Water Data')
what_sheets = 'Aggregation'
worksheet = sh.worksheet(what_sheets)
#%%
#Load the datasets
df = DataFrame(worksheet.get_all_records(head=1))
#%%
add = st.sidebar.checkbox('Add New Dataset')
if add :  
    name_entry = st.sidebar.text_input('Dataset Name')
    url_entry = st.sidebar.text_input('URL')
    confirm_input = st.sidebar.button('Confirm')
    
    if confirm_input:
        opt = {'Dataset Full Name': [name_entry],
              'URL' :  [url_entry]} 
        opt_df = DataFrame(opt)
        df = load_the_spreadsheet('Aggregation')
        new_df = pd.concat([df, opt_df], sort=False)
        update_the_spreadsheet('Aggregation',new_df)