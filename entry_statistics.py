import feature_engineering
import pandas as pd
import requests

import requests
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


def getFilename_fromCd(cd):
    """
    Get filename from content-disposition
    """
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]


url = 'http://google.com/favicon.ico'
r = requests.get(url, allow_redirects=True)
filename = getFilename_fromCd(r.headers.get('content-disposition'))


open(filename, 'wb').write(r.content)
url = 'https://hockey.sportlogiq.com/games/team/308/8114840/video'
r = requests.get(url, allow_redirects=True)
open('test2.csv', 'wb').write(r.content)
df = pd.read_csv('C:\\Users\\vereriks\\Downloads\\playsequence-20230416-Hockey Allsvenskan-DIFvsMODO-20222023-17149.csv')

teams, teams_bytes = feature_engineering.generate_entry_statistics(df=df)



