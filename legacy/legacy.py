def download_schedule(url, team_order, path, regular_season=True):
    DRIVER_PATH = '/home/veronica/Downloads/chromedriver_linux64_112/chromedriver'
    options = webdriver.ChromeOptions()
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
        inner_html = body_element.get_attribute("innerHTML")
        print(inner_html)
        team_xpath = "/html/body/app-root/div/ng-component/div/div[2]/div/main-navigator/div/button/span[1]/span/span[1]"
        team_element = driver.find_element(By.XPATH, team_xpath)
        team_name = team_element.get_attribute("innerHTML")
        if regular_season:
            filename = team_name + '_regular_season.txt'
        else:
            filename = team_name + '_playoffs.txt'

        string_to_file(inner_html, path, filename)
        # with open('kallekula3.html','w+') as f:
        #    f.write(inner_html)
        # print('apa')