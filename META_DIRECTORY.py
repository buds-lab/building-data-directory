# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 13:56:34 2022

@author: Xiaoyu Jin
"""

import streamlit as st
import pandas as pd
from pandas import DataFrame
#from gspread_pandas import Spread,Client
from google.oauth2 import service_account
import ssl


#Page title
st.set_page_config(
    page_title="Building Data Genome Directory",
)

#Text contents
st.title("# Building Data Genome Directory")
st.subheader('👋 Welcome to Building Data Genome Directory!')

st.markdown(
    """
##### This is a comprehensive building dataset collection, where you can find the links for the datasets related with building energy research.\n
##### You are also more than welcome to contribute the link of your own datasets, by clicking the check button *'Add New Dataset'* on the left bar.\n
##### Please note that we are looking forward to datasets with the geospatial granularity levels of **_individual buildings_** or **_communities_**, instead of aggregated data of a city.\n
##### Please also note that we are maintaining the dataset links, rather than a database. Looking for places to upload your own dataset? Check the [Open Energy Platform](https://openenergy-platform.org/). You can update your link here after uploading your dataset.""")

st.subheader('Dataset Categories')
st.markdown(
    """
##### What kinds of datasets are you looking for?
""")
st.image("https://github.com/buds-lab/building-data-directory/raw/main/meta%20directory.png")


col1, col2, col3 = st.columns(3)
with col1:
    st.subheader(
    """
    👈 Check the category buttons on the left bar!
""")
    
with col2:
    st.markdown("![Alt Text](https://github.com/buds-lab/building-data-directory/raw/main/browsing.gif)")
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
#scope = ["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive"]
#credentials = service_account.Credentials.from_service_account_info(
   #st.secrets["gcp_service_account"],
   #st.secrets["gcp_service_account"],
   #scopes=scope)
#client = Client(scope=scope,creds=credentials)

#spreadsheetname = "Dataset_Intro_List"
#spread = Spread(spreadsheetname,client = client)
#sh = client.open(spreadsheetname)
dataset = load_the_spreadsheet('contributed from users')

from streamlit_gsheets import GSheetsConnection
# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)
dataset = conn.read()
#%%
st.subheader(
    """
    Datasets contributed by users 
""")
st.markdown("""*Note: These datasets will be added to the directory after review*""")
for i in range(len(dataset)):
    url = dataset['URL'][i]
    dataset['URL'][i] =  f'<a href="{url}">{url}</a>'
dataset.index = dataset.index + 1 
users_html = dataset.iloc[:,:-1].to_html(escape=False)
st.write(users_html, unsafe_allow_html=True)
st.markdown(""" """)
st.markdown(""" """)
st.markdown(""" """)
st.subheader('To cite the Building Data Genome Directory:')
st.markdown(""" The Building Data Genome Directory – An open, comprehensive data sharing platform for building performance research.arXiv:2307.00793. https://doi.org/10.48550/arXiv.2307.00793""")
st.markdown(""" """)
st.subheader('Other relevant publications:')
st.markdown(""" A review and reflection on open datasets of city-level building energy use and their applications. https://10.1016/j.enbuild.2023.112911""")

st.markdown(""" """)
st.markdown(""" """)
st.markdown("""*Any questions or ideas? Join our GitHub community at [building-data-directory Discussions](https://github.com/buds-lab/building-data-directory/discussions)*""")
st.markdown("""*Further questions? Contact us📧: xiaoyu.jin@connect.polyu.hk*""")
st.markdown(""" """)
st.markdown("""*<p style="font-size: 12px;">Acknowledge for the support by the National Key Research and Development Program of China (2021YFE0107400), and the joint effort of the Annex 81 community.*</p>""",unsafe_allow_html=True)
st.image("https://github.com/buds-lab/building-data-directory/blob/main/Annex%2081%20logo.png?raw=true")

#%%
def update_the_spreadsheet(spreadsheetname,dataframe):
    #col = ['Dataset Full Name','URL']
    spread.df_to_sheet(dataframe,sheet = spreadsheetname,index= False)
    st.sidebar.info('✅ Submitted succussfully! Thank you for contributing.You can check your dataset on the right (contribution from users).')
#%%
add = st.sidebar.checkbox('Add New Dataset')
if add:  
    name_entry = st.sidebar.text_input('Dataset Name')
    url_entry = st.sidebar.text_input('URL')
    
    Type = ['1 🧱 Building Energy Ontologies',
            '2 🏚️ Building Energy Models',
            '3 🕛 Building Energy and Water Data',
            '4 🚎 Electric Vehicle Data',
            '5 🌦️ Weather Data',
            '6 📄 Building_Information_Data',
            '7 🏭 Smart Grid Data',
            '8 📚 Text Mining Based Research Data',
            '9 ⚠️ Fault Detection Diagnosis Data',
            '10 👩‍🦯 Occupant Data',
            '11 Other Categories']
    select_type = st.sidebar.selectbox('Dataset Type',Type)
    
    email = st.sidebar.text_input('Please leave your email (optional)')
    confirm_input = 0
    
    if (len(name_entry) != 0) & (len(url_entry) != 0):      
        confirm_input = st.sidebar.button('Confirm')
    
    if confirm_input:
        opt = {'Dataset Full Name': [name_entry],
              'URL' :  [url_entry],
              'Type':[select_type],
              'Email': [email]} 
        opt_df = DataFrame(opt)
        df = load_the_spreadsheet('contributed from users')
        new_df = pd.concat([df, opt_df], sort=False)
        update_the_spreadsheet('contributed from users',new_df)
        st.experimental_rerun()
