
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


def analyze_json():
    with open('/Users/abbas/Desktop/repos/98910776/package.json', 'r') as f:
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
                print('\n'+Back.RED + Fore.BLACK + '\n ***   DEPENDENCY SMELL WARNING   ***\n')
                warning = 1
                print(Fore.RED)

            print('"'+dep+'"'+' has a '+smell+' dependency smell')
        #print(dep+' '+cons)
    print(Fore.YELLOW)
    print("Found " + str(cnt) + ' dependency smells in package.json')
    print(Style.RESET_ALL)


analyze_json()