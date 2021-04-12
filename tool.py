
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

import sys


def is_smell(constraint):
    smell='pinned dependency'

    if bool(re.search('~', constraint)):
        return 'restrictive'

    if bool(re.search('\^', constraint)):
        return 'none'

    if bool(re.search('<', constraint)):
        return 'none'

    if bool(re.search('\*|>|latest', constraint)):
        return 'permissive'

    if bool(re.search('file', constraint)):
        return 'none'

    if bool(re.search('git|http', constraint)):
        return 'url'

    if bool(re.search('\d+\.(x|X)\.(x|X|\d+)', constraint)):
        return 'none'

    if bool(re.search('\d+\.\d+\.(x|X)', constraint)):
        return 'restrictive'

    if bool(re.search('\d+\.(x|X)', constraint)):
        return 'none'

    return 'pinned'

def is_package_lock(path):
    if os.path.exists(path) == True:
        return 'yes'
    return 'no'

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

    #TODO : here instead of appending just print out the values but need to think how
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
        if smell!='none':
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

analyze_json(str(sys.argv[1]))