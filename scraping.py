import numpy as numpy
import pandas as pd
#data = pd.read_csv('https://example.com/passkey=wedsmdjsjmdd')
import urllib
import csv
import requests
import os
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
import copy
import time
import numpy as np
from urllib.request import urlopen
from utils.read_write import string_to_file
import feature_engineering

def get_driver():
    DRIVER_PATH = '/home/veronica/Downloads/chromedriver_linux64_112/chromedriver'
    options = webdriver.ChromeOptions()
    options.add_argument('/home/veronica/.config/google-chrome/Default')
    options.add_argument("user-data-dir=/tmp/veronica")
    driver = webdriver.Chrome(executable_path=DRIVER_PATH, chrome_options=options)
    return driver

def scrape():
    DRIVER_PATH = '/home/veronica/Downloads/chromedriver_linux64_107/chromedriver'
    options=webdriver.ChromeOptions()
    options.add_argument('/home/veronica/.config/google-chrome/Default')
    driver = webdriver.Chrome(executable_path=DRIVER_PATH, chrome_options=options)
    #driver = webdriver.Chrome('./chromedriver')
    driver.get('https://hockey.sportlogiq.com/login')
    #login = driver.find_element("//input[@id='mat-input-0']")
    driver.implicitly_wait(10)
    #WebDriverWait(driver, 10)
    login = driver.find_element(By.XPATH, "//input[@id='mat-input-0']")#.send_keys('eriksson@kth.se')
    login.send_keys('eriksson@kth.se')
    pwd = driver.find_element(By.XPATH, "//input[@id='mat-input-1']")
    pwd.send_keys('B1llyfjant.1')

    submit = driver.find_element(By.XPATH, "//button[@type='submit']")
    WebDriverWait(driver,3).until(EC.element_to_be_clickable(submit))
    submit.click()

    #un_available = True
    #while un_available:
    #    print(len(driver.find_elements(By.TAG_NAME, "app-root")))
    #    if len(driver.find_elements(By.TAG_NAME, "league-selector")) > 0:
    #        un_available = False

    #    print(un_available)

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "league-selector")))
    #*[@id="section-65"]/report-section/div[1]/div/div[1]/i

    #action_chain.move_to_element(element).click().perform()

    #driver.get('https://hockey.sportlogiq.com/games/league/98743/report/post')
    driver.get('https://hockey.sportlogiq.com/games/league/5665/report/post')
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//*[@id='main-content']/app-games/div/app-games-for-league/sl-game-report/div/div[1]/div[1]/div/button[1]")))
    #driver.find_elements(By.CLASS_NAME, "simple-button")

    #action_chain = ActionChains(driver)
    #element=driver.find_elements(By.XPATH, "//*[@id='section-65']/report-section/div[2]")
    click_chain = ActionChains(driver)
    elements=driver.find_elements(By.XPATH, "//*[@id='section-65']/report-section/div")
    '''
    for element in elements[0:]: #driver.find_elements(By.XPATH, "//*[@id='section-65']/report-section"):
        if element.get_attribute('innerHTML').find("clickable") >= 0:
            click_chain.move_to_element(element).click().perform()
            #click_chain.move_to_element(element).click().perform()
            #WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='main-content']/app-games/div/app-games-for-league/sl-game-report/div/div[1]/div[1]/div/button[1]")))
            time.sleep(3)
    '''


    #WebDriverWait(driver,3)
    #time.sleep(10)

    #db = driver.find_elements(By.XPATH, "//*[@id='main-content']/app-games/div/app-games-for-league/sl-game-report/div/div[1]/div[1]/div/button[1]")
    #print(len(driver.find_elements(By.XPATH, "//*[@id='main-content']/app-games/div/app-games-for-league/sl-game-report/div/div[1]/div[1]/div/button[1]")))
    click_chain.move_to_element(driver.find_element(By.XPATH, "//*[@id='main-content']/app-games/div/app-games-for-league/sl-game-report/div/div[1]/div[1]/div/button[1]")).click().perform()
    print('apa')
    print('apa2')
    time.sleep(10)
    #action_chain = ActionChains(driver)
    #download_button = driver.find_element(By.XPATH, "//*[@id='main-content']/app-games/div/app-games-for-league/sl-game-report/div/div[1]/div[1]/div/button[1]")

    #download_button = driver.find_element(By.XPATH, "/html/body/app-root/div/ng-component/div/div[3]/app-games/div/app-games-for-league/sl-game-report/div/div[1]/div[1]/div/button[1]")
    #download_chain = ActionChains(driver)


    #action_chain.move_to_element(driver.find_element(By.XPATH, "//*[@id='main-content']/app-games/div/app-games-for-league/sl-game-report/div/div[1]/div[1]/div/button[1]")).click().perform()
    #action_chain = ActionChains(driver)
    #action_chain.move_to_element(element[0]).click().perform()

    #ids = driver.find_elements(By.XPATH, '//*[@id]')
    #for ii in ids:
        #print ii.tag_name
        #print(ii.get_attribute('id'))

    #//*[@id="section-65"]/report-section/div[1]/div

    #WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//mat-select[@role='combobox' and @id='mat-select-24']")))

    #league = driver.find_element(By.XPATH, "//mat-select[@role='combobox']")
    #print('apa')
    #league = driver.find_element(By.XPATH,"//mat-option[@id='mat-options-26']")
    #league = driver.find_element_by_xpath("//select[@name='element_name']/option[text()='option_text']").click()
    #WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.NAME, "Submit"))).click()

    #driver.get('https://hockey.sportlogiq.com/Strengths_WeaknessesSweden_Team_Sweden.csv')
    #res = urllib.urlopen('https://hockey.sportlogiq.com/Strengths_WeaknessesSweden_Team_Sweden.csv')
    #res = requests.get('https://hockey.sportlogiq.com/Strengths_WeaknessesSweden_Team_Sweden.csv')
    #t = res.iter_lines()
    #data = csv.reader(res)#, delimiter=',')
    #data = csv.reader(res)

    #print('apa')
    #data = pd.read_csv('https://hockey.sportlogiq.com/Strengths_WeaknessesSweden_Team_Sweden.csv')
    #data = pd.read_csv('/home/veronica/Downloads/Strengths_WeaknessesSweden_Team_Sweden.csv')
    #print(data)
    #print('a')

def download_gamefiles(start, end):
    DRIVER_PATH = '/home/veronica/Downloads/chromedriver_linux64_112/chromedriver'
    options=webdriver.ChromeOptions()
    options.add_argument('/home/veronica/.config/google-chrome/Default')
    driver = webdriver.Chrome(executable_path=DRIVER_PATH, chrome_options=options)
    #driver = webdriver.Chrome('./chromedriver')
    driver.get('https://hockey.sportlogiq.com/login')
    driver.implicitly_wait(10)
    login = driver.find_element(By.XPATH, "//input[@id='mat-input-0']")#.send_keys('eriksson@kth.se')
    login.send_keys('eriksson@kth.se')
    pwd = driver.find_element(By.XPATH, "//input[@id='mat-input-1']")
    pwd.send_keys('B1llyfjant.1')
    submit = driver.find_element(By.XPATH, "//button[@type='submit']")
    WebDriverWait(driver,3).until(EC.element_to_be_clickable(submit))
    submit.click()
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "league-selector")))

    for i in range(start,end):
        url = 'https://hockey.sportlogiq.com/games/league/{game_id}/report/post'.format(game_id=i)
        url = 'https://hockey.sportlogiq.com/games/league/84480/video'.format(game_id=i)
        print(url)
        driver.get(url)
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='main-content']/app-games/div/app-games-for-team/game-video/div/div[1]/div[1]/div[2]")))
        # WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='main-content']/app-games/div/app-games-for-league/sl-game-report/div/div[1]/div[1]/div/button[1]")))
        click_chain = ActionChains(driver)
        elements = driver.find_elements(By.XPATH, "//*[@id='section-65']/report-section/div")
        print(elements)
        elements = driver.find_element(By.XPATH, "//*[@id='main-content']/app-games/div/app-games-for-team/game-video/div/div[1]/div[1]/div[2]/button")
        click_chain.move_to_element(elements[0])
        click_chain.click()
        click_chain.perform()

        #click_chain.move_to_element(driver.find_element(By.XPATH, "//*[@id='main-content']/app-games/div/app-games-for-team/game-video/div/div[1]/div[1]/div[2]/button")[0]).click().perform()
        #click_chain.move_to_element(driver.find_element(By.XPATH, "//*[@id='main-content']/app-games/div/app-games-for-league/sl-game-report/div/div[1]/div[1]/div/button[1]")).click().perform()
        time.sleep(1)

def download_gamefiles_2(start, end):
    DRIVER_PATH = '/home/veronica/Downloads/chromedriver_linux64_112/chromedriver'
    options=webdriver.ChromeOptions()
    options.add_argument('/home/veronica/.config/google-chrome/Default')
    driver = webdriver.Chrome(executable_path=DRIVER_PATH, chrome_options=options)
    #driver = webdriver.Chrome('./chromedriver')
    driver.get('https://hockey.sportlogiq.com/login')
    driver.implicitly_wait(10)
    login = driver.find_element(By.XPATH, "//input[@id='mat-input-0']")#.send_keys('eriksson@kth.se')
    login.send_keys('eriksson@kth.se')
    pwd = driver.find_element(By.XPATH, "//input[@id='mat-input-1']")
    pwd.send_keys('B1llyfjant.1')
    submit = driver.find_element(By.XPATH, "//button[@type='submit']")
    WebDriverWait(driver,3).until(EC.element_to_be_clickable(submit))
    submit.click()
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "league-selector")))

    for i in range(start,end):
        print('Game: ', i)
        url = 'https://hockey.sportlogiq.com/games/league/{game_id}/video'.format(game_id=i)
        print(url)
        # driver.get(url)
        # test = driver.find_element(By.XPATH, "/html/body/app-root")
        # test.get_attribute("innerHTML")

        time.sleep(10)

        elements = driver.find_elements(By.XPATH, "//*[@id='main-content']/app-games/div/app-games-for-league/game-video/div/div[1]/div[1]/div[2]/button")
        if len(elements) < 1:
            print('Game number ' + str(i) + ' does not exist')
        else:
            elements[0].click()
            print('Game number ' + str(i) + ' downloaded')
            time.sleep(5)

def login(driver):
    # driver = webdriver.Chrome('./chromedriver')
    driver.get('https://hockey.sportlogiq.com/login')
    driver.implicitly_wait(10)
    login = driver.find_element(By.XPATH, "//input[@id='mat-input-0']")  # .send_keys('eriksson@kth.se')
    login.send_keys('eriksson@kth.se')
    pwd = driver.find_element(By.XPATH, "//input[@id='mat-input-1']")
    pwd.send_keys('B1llyfjant.1')
    submit = driver.find_element(By.XPATH, "//button[@type='submit']")
    WebDriverWait(driver, 3).until(EC.element_to_be_clickable(submit))
    submit.click()
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "league-selector")))

def get_web_driver():

    DRIVER_PATH = '/home/veronica/Downloads/chromedriver_linux64_112/chromedriver'
    options=webdriver.ChromeOptions()
    options.add_argument('/home/veronica/.config/google-chrome/Default')
    options.add_argument("user-data-dir=/tmp/veronica")
    driver = webdriver.Chrome(executable_path=DRIVER_PATH, chrome_options=options)
    return driver

def wait_and_click(driver, xpath):
    WebDriverWait(driver, 50).until(EC.presence_of_element_located(
        (By.XPATH, xpath)))
    select_element = driver.find_element(By.XPATH, xpath)
    select_element.click()
    return driver

def select_team(driver, team_order, regular_season=True):
    select_xpath = "/html/body/app-root/div/ng-component/div/div[2]/div/main-navigator/div/button"
    driver = wait_and_click(driver, select_xpath)
    element_xpath = f"/html/body/div[3]/div[2]/div/mat-dialog-container/team-selector/div/mat-selection-list/mat-list-option[{team_order}]"
    driver = wait_and_click(driver, element_xpath)

    if regular_season:
        el = "//*[@id='mat-button-toggle-1']"
    else:
        el = "//*[@id='mat-button-toggle-2']"
    driver = wait_and_click(driver, el)


    cancel_xpath = "/html/body/div[3]/div[2]/div/mat-dialog-container/team-selector/div/action-button-bar/div/button[1]"
    apply_xpath = "/html/body/div[3]/div[2]/div/mat-dialog-container/team-selector/div/action-button-bar/div/button[2]"
    cancel_element = driver.find_element(By.XPATH, cancel_xpath)
    apply_element = driver.find_element(By.XPATH, apply_xpath)

    time.sleep(2)
    if apply_element.is_enabled():
        print("Clicking APPLY")
        apply_element.click()
        return driver
    else:
        return False
        # print("Clicking CANCEL")
        # cancel_element.click()

    return driver

def create_team_list(league):
    "/html/body/div[3]/div[2]/div/mat-dialog-container/team-selector/div/mat-selection-list/mat-list-option[20]"


def download_schedule(url, team_order, path, regular_season=True):
    DRIVER_PATH = '/home/veronica/Downloads/chromedriver_linux64_112/chromedriver'
    options=webdriver.ChromeOptions()
    options.add_argument('/home/veronica/.config/google-chrome/Default')
    options.add_argument("user-data-dir=/tmp/veronica")
    driver = webdriver.Chrome(executable_path=DRIVER_PATH, chrome_options=options)
    # login(driver)

    driver.get(url)
    driver = select_team(driver, team_order, regular_season=regular_season)
    if driver:
        # Wait for "season reports" to load since that means all games are read into the page.
        el = "//*[@id='mat-tab-link-18']"
        WebDriverWait(driver, 50).until(EC.presence_of_element_located(
            (By.XPATH, el)))

        '''
        # Click on combobox to select regular season or playoffs
        el = "/html/body/app-root/div/ng-component/div/div[2]/div/main-navigator/div/button/span[1]"
    
        WebDriverWait(driver, 50).until(EC.presence_of_element_located(
            (By.XPATH, el)))
        el = driver.find_element(By.XPATH, el)
        el.click()
    
        # Wait for and click on Regular season or Playoffs
        if regular_season:
            el = "//*[@id='mat-button-toggle-1']"
        else:
            el = "//*[@id='mat-button-toggle-2']"
    
    
        WebDriverWait(driver, 50).until(EC.presence_of_element_located(
            (By.XPATH, el)))
        el = driver.find_element(By.XPATH, el)
        el.click()
    
        # Wait for and try to click the apply button. If it fails (since the selection is already loaded) press
        # Cancel when exception is caught
        cancel_xpath = "/html/body/div[3]/div[2]/div/mat-dialog-container/team-selector/div/action-button-bar/div/button[1]"
        cancel_element = driver.find_element(By.XPATH, cancel_xpath)
        apply_xpath = "/html/body/div[3]/div[2]/div/mat-dialog-container/team-selector/div/action-button-bar/div/button[2]"
        apply_element = driver.find_element(By.XPATH, apply_xpath)
        if apply_element.is_enabled:
            print("Clicking APPLY")
            apply_element.click()
        else:
            print("Clicking CANCEL")
            cancel_element.click()
        '''
        time.sleep(15)

        # Grab the body of the page and get the innerHTML
        body_xpath = "/html/body/app-root"
        body_element = driver.find_element(By.XPATH, body_xpath)
        inner_html=body_element.get_attribute("innerHTML")
        print(inner_html)
        team_xpath="/html/body/app-root/div/ng-component/div/div[2]/div/main-navigator/div/button/span[1]/span/span[1]"
        team_element = driver.find_element(By.XPATH, team_xpath)
        team_name = team_element.get_attribute("innerHTML")
        if regular_season:
            filename = team_name + '_regular_season.txt'
        else:
            filename = team_name + '_playoffs.txt'

        string_to_file(inner_html, path, filename)
        #with open('kallekula3.html','w+') as f:
        #    f.write(inner_html)
        #print('apa')
def get_all_game_numbers(root_dir):
    """Returns a list of game-numbers given a directory of the html-files
    for each team's schedule"""
    root_dir = '/home/veronica/hockeystats/SHL/2022-23/regular-season/schedules'
    files = [os.path.join(root_dir, f) for f in os.listdir(root_dir)]
    games = []
    for file in files:
        str = open(file,'r').read()
        game_numbers = [int(n.split('/')[0]) for n in re.findall(r'\d+/video', str)]
        new_game_numbers = [n for n in game_numbers if n not in games]
        games = games + new_game_numbers
        print(file)
        print(len(games))
        return games

def teams_from_gamefile_names(root_dir):
    files = os.listdir(root_dir)
    games=[]
    for file in files:
        teams=file.split('-')[3]
        games.append(tuple(teams.split('vs')))
    print(games)


def extract_game_info_from_schedule_html(filename):
    html = open(filename,'r').read()
    months=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    year_adds = [1,1,1,1,1,1,1,0,0,0,0,0]
    year = 2022
    months_start_pos = []
    for (idx, month) in enumerate(months):
        res = re.search(f"\"month-label\">{month}", html)
        if res:
            months_start_pos.append((idx, res.start()))


    months_start_pos = sorted(months_start_pos, key=lambda x:(x[1]))
    months_end_pos = months_start_pos[1:]+[tuple(np.array(months_start_pos[-1]) + ((0,len(html))))]
    parts = []
    for i in range(0, len(months_start_pos)):
        parts.append(months_start_pos[i] + (months_end_pos[i][1],))
    games = []
    for (month, start, end) in parts:
        crop = html[start:end]
        rows = crop.split('season-schedule-row')[1:]
        for row in rows:
            home_team = row.split('matchup-content\">')[2].split('<')[0].replace(' ','')
            away_team = row.split('matchup-content\">')[1].split('<')[0].replace(' ','')
            date = str(year + year_adds[month]) + str(month + 1).zfill(2)  +\
                   re.findall('\d+', row.split('date-container')[1])[0].zfill(2)
            sl_game_id = row.split('/games/league/')[1].split('/')[0]
            games.append((home_team, away_team, date, sl_game_id))
            print(date + ' ' + home_team + ' ' + away_team)


    return games
