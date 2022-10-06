
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

import sys

pd.set_option('display.max_rows', 10000)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)

JS_DIR = './nodejs_code/'
def view_database():
    con = sqlite3.connect("Databases/smelldataset.db")

    cur = con.cursor()

    # The result of a "cursor.execute" can be iterated over by row
    df = pd.read_sql_query("SELECT * from data_table WHERE package='yes' and package_lock='no' and pinned='yes' and url = 'no' ", con)
    print(df.head())
    # Be sure to close the connection
    con.close()


def analyze_label(constraint):

    if bool(re.search('<', constraint)):
        out = 'dunno'
        #print(out)
        return out

    if bool(re.search('\*|>|latest', constraint)):
        out = 'permissive'
        # print(out)
        return out

    if bool(re.search('git|http', constraint)):
        return 'url'

    result = subprocess.check_output(['node', 'range-eval.js', constraint], cwd=JS_DIR, text=True)
    range = result.strip("\n")
    #print(range)
    versions = range.split()

    # TODO: bring min_version and max version befoe pinned and then check if if min_version[0] == '0': then its not pinned
    #  its compliant because we later tag pinnedas restrictive
    #  make sure to change names for the files

    # effectively pinned
    if len(versions) == 1:

        min_version = versions[0].split('.')

        # pinned to a specific version for pre-1.0.0 is considered compliant
        if min_version[0] == '0':
            out = 'compliant'
            return out

        out = 'pinned'
        return out

    min_version = versions[0][2:].split('.')
    max_version = versions[1][1:-2].split('.')


    # if it is a pre-1.0.0 version and not pinned then it is permissive
    if min_version[0] == '0':
        out = 'permissive'
    else:
        # print(min_version)
        # print(max_version)

        if min_version[0] == max_version[0]:
            out = 'restrictive'

        else:
            out = 'compliant'

    # min_version = min_version.removeprefix('<')
    # print(out)
    return (out)
def is_smell(constraint):
    smell='pinned dependency'

    if bool(re.search('~', constraint)):
        return 'restrictive'

    # if bool(re.search('\^', constraint)):
    #     return 'none'

    if bool(re.search('<', constraint)):
        return 'none'

    if bool(re.search('\*|>|latest', constraint)):
        return 'permissive'

    if bool(re.search('file', constraint)):
        return 'none'

    if bool(re.search('git|http', constraint)):
        return 'url'

    return analyze_label(constraint)
    # if bool(re.search('\d+\.(x|X)\.(x|X|\d+)', constraint)):
    #     return 'none'
    #
    # if bool(re.search('\d+\.\d+\.(x|X)', constraint)):
    #     return 'restrictive'
    #
    # if bool(re.search('\d+\.(x|X)', constraint)):
    #     return 'none'
    #
    # return 'pinned'

def is_package_lock(path):
    if os.path.exists(path) == True:
        return 'yes'
    return 'no'

# run separately
def run_depcheck(path):
    out_path = os.path.join(path, 'depcheck_results.json')
    try:

        os.system('depcheck ' + path + ' --json > ' + out_path)


    except:
        print(Back.RED + Fore.BLACK + 'exception raised' + dir)
        print(Style.RESET_ALL)
        pass

    with open(out_path) as jsonfile:
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

def analyze_json(path):
    joined_path = os.path.join(path, 'package.json')
    with open(joined_path, 'r') as f:
        try:
            data = json.load(f)
        except ValueError as e:
            print('Invalid package.json file: %s' % e)
            return None
    warning = 0
    cnt = 0

    for x in data["dependencies"]:
        dep=x
        cons=data["dependencies"][x]
        smell=is_smell(cons)
        if (smell!='none' and smell!='compliant'):
            cnt += 1
            if warning == 0:
                print('\n'+Back.RED + '\n\n ***   DEPENDENCY SMELL WARNING   ***')
                print(Style.RESET_ALL)
                print('\n')
                warning = 1

                #print(Back.RED)

            print(str(cnt)+') "'+dep+'"'+' has a '+smell+' dependency smell')
        #print(dep+' '+cons)

    lock_path = os.path.join(path, 'package-lock.json')

    if is_package_lock(lock_path) == 'no':
        cnt += 1
        if warning == 0:
            print('\n' + Back.RED + '\n\n ***   DEPENDENCY SMELL WARNING   ***')
            print(Style.RESET_ALL)
            print('\n')
        print(str(cnt)+') package-lock does not exist')

    print(Back.YELLOW)
    print("\nFound " + str(cnt) + ' dependency smells in ' + path)
    print(Style.RESET_ALL)
    print('\n')

analyze_json('../DependencySniffer')