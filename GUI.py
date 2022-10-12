
import re
import pandas as pd
import json
import subprocess
import sqlite3
import re
import os
import shutil

from colorama import Fore, Back, Style
import datetime
import dateutil

import streamlit as st
import sys

import plotly.express as px
import streamlit as st


from DepSniffer import analyze_label, analyze_json
pd.set_option('display.max_rows', 10000)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)

JS_DIR = './nodejs_code/'
path = './'

if 'load' not in st.session_state:
    st.session_state.load = False
if 'analyze' not in st.session_state:
    st.session_state.analyze = False

st.set_page_config(layout="wide")

st.header(":male-detective:   Dependency Sniffer")

with st.expander('Settings', expanded=True):


    path=st.text_input('Input Project Directory', value=path)

    file=st.file_uploader('or Add Dependency File')

    st.write('Which smells should I search for?')

    col1, col2 = st.columns([1,1])

    with col1:
        s_pinned=st.checkbox('Pinned Dependency', value=True)
        s_url=st.checkbox('URL Dependency', value=True)
        s_restrictive=st.checkbox('Restrictive Constraint', value=True)
        s_permissive=st.checkbox('Permissive Constraint', value=True)

    with col2:
        s_lock=st.checkbox('No Package Lock', value=True)
        s_unused=st.checkbox('Unused Dependency', value=True)
        s_missing=st.checkbox('Missing Dependency', value=True)
    #
    # options = st.multiselect(
    #     'What are your favorite colors',
    #     ['Pinned Dependency', 'URL Dependency', 'Restrictive Constraint', 'Permissive Constraint'],
    #     ['Pinned Dependency', 'URL Dependency', 'Restrictive Constraint', 'Permissive Constraint'])

load = st.button('Load Project')

if load:
    st.session_state.load = True

if st.session_state.load:
    with st.expander('We found the following dependencies:', expanded=True):
        col1, col2 = st.columns([1, 1])

        with col1:
            df, json = analyze_json('./')
            st.write(json['dependencies'])
        with col2:
            # st.write(json)
            # st.write(len(json['devDependencies']))
            st.info('The project has "' + str((len(json['dependencies']))) + '" runtime dependencies')
            st.info('The project has "' + str((len(json['devDependencies']))) + '" development dependencies')
            st.info('The project has "' + str((len(json['optionalDependencies']))) + '" optional dependencies')
            # st.info('The project has "' + str((len(json['peerDependencies']))) + '" peer dependencies')



if st.session_state.load:
    analyze = st.button('Analyze Project')
    if analyze:
        st.session_state.analyze = True

if st.session_state.analyze:

    col1, col2 = st.columns([1,1])
    df, json = analyze_json('./')
    for index, row in df.iterrows():
        if row['Smell'] != 'none':
            with col1:
                st.error('"' + row['Dependency'] + '"' + ' is infected with a ' + row['Smell'] + ' Dependency Smell')
        else:
            with col1:
                st.success('"' + row['Dependency'] + '"' + ' is not infected')

    plot_df = df.groupby(['Smell'])['Dependency'].count().reset_index(name='Count')
    with col2:
            # st.write('pie chart for different smells + clean')
            # st.write(plot_df)
            # st.write(df)
            fig = px.pie(plot_df, values = 'Count', names='Smell', hole=.5, color_discrete_sequence=px.colors.sequential.RdBu)
            fig.update_layout(uniformtext_minsize=18, uniformtext_mode='hide', autosize=False, width=750, height=600)
            #
            fig.update_layout(
                legend=dict(
                    x=0.9,
                    y=1,
                    font=dict(
                        size=14,
                        color="white"
                    ),
                )
            )

            st.write(fig)

