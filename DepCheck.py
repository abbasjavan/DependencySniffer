import re
import pandas as pd
import json
from sqlalchemy import create_engine
import sqlite3
import re
import os
import shutil

from github import Github


from colorama import Fore, Back, Style
import datetime
import dateutil

import time
import matplotlib.pyplot as plt

import git
from unidiff import PatchSet

from io import StringIO

from parser import is_package

pd.set_option('display.max_rows', 10000)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)


def run_depcheck():
    sql_engine = create_engine('sqlite:///')
    sql_engine.execute("attach database 'smelldataset.db' as smelldataset;")
    exclude = pd.read_sql_query("SELECT project_id FROM smelldataset.data_table WHERE dconstraint='no_root' or dconstraint='empty_dependency' or dconstraint='no_runtime'", sql_engine)
    forks = pd.read_csv('forked_projects.csv')['project_id']


    rootdir = '/Volumes/Samsung_T5/repos/'

    dir_cnt=0

    for dir in os.listdir(rootdir):
        try:
            print('after entering loop dir is ' + dir)

            if str(dir) in str(exclude) or str(dir) in str(forks):
                continue
            if is_package(rootdir + str(dir) + "/package.json") == "no":
                print('no package')
                continue
            if dir.startswith('.'):
                continue

            dir_cnt += 1
            print('\n'+dir+'\n')
            print(dir_cnt)

            os.system('depcheck ' + str(rootdir) + str(dir) + ' --json > ' + str(rootdir) + str(dir) + '/depcheck_results.json')


        except:
            print(Back.RED + Fore.BLACK + 'exception raised' + dir)
            print(Style.RESET_ALL)
            pass

def parse_depcheck():

    sql_engine = create_engine('sqlite:///')
    sql_engine.execute("attach database 'smelldataset.db' as smelldataset;")
    exclude = pd.read_sql_query("SELECT project_id FROM smelldataset.data_table WHERE dconstraint='no_root' or dconstraint='empty_dependency' or dconstraint='no_runtime'", sql_engine)
    forks = pd.read_csv('forked_projects.csv')['project_id']

    rootdir = '/Volumes/Samsung_T5/repos/'

    dir_cnt = 0
    dep_checks = pd.DataFrame(columns=['project_id', 'unused_dep', 'missing_dep'])
    dep_counts = pd.DataFrame(columns=['project_id', 'unused_cnt', 'missing_cnt'])

    for dir in os.listdir(rootdir):

        unused_cnt = 0
        missing_cnt = 0

        try:
            print('after entering loop dir is ' + dir)

            if str(dir) in str(exclude) or str(dir) in str(forks):
                continue
            if is_package(rootdir + str(dir) + "/package.json") == "no":
                print('no package')
                continue
            if dir.startswith('.'):
                continue

            dir_cnt += 1
            print('\n' + dir + '\n')
            print(dir_cnt)

            with open(str(rootdir) + str(dir) + '/depcheck_results.json') as jsonfile:
                data = json.load(jsonfile)


            for value in data["dependencies"]:
                dep_checks = dep_checks.append({
                    "project_id": str(dir),
                    "unused_dep": str(value),

                }, ignore_index=True)
                unused_cnt = unused_cnt + 1


            for key, value in data["missing"].items():
                dep_checks = dep_checks.append({
                    "project_id": str(dir),
                    "missing_dep": str(key),
                }, ignore_index=True)
                missing_cnt = missing_cnt + 1

        except:
            print(Back.RED + Fore.BLACK + 'exception raised' + dir)
            print(Fore.RED)
            print(Style.RESET_ALL)

        dep_counts = dep_counts.append({
            "project_id": str(dir),
            "unused_cnt": unused_cnt,
            "missing_cnt": missing_cnt,
        }, ignore_index=True)

    print(dep_checks)
    print(dep_counts)

    #dep_checks.to_csv('dep_checks.csv',index=False)
    dep_counts.to_csv('full_dep_counts.csv',index=False)


    #return dep_checks

# run_depcheck()
# parse_depcheck()

cdf = pd.read_csv('full_dep_counts.csv')
print(cdf)
#print(cdf)
print(cdf[cdf["unused_cnt"]!=0].nunique())
print(cdf[cdf["missing_cnt"]!=0].nunique())

print(cdf.describe())