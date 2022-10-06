
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

import streamlit as st


from DepSniffer import analyze_label, analyze_json
pd.set_option('display.max_rows', 10000)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)

JS_DIR = './nodejs_code/'

analyze_json('../DependencySniffer')