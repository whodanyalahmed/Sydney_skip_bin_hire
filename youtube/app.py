import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options


def Chrome(headless=False):
    # add fake user agent
    chrome_options = Options()

    # return webdriver
    # support to get response status and headers
    d = webdriver.DesiredCapabilities.CHROME
    d['loggingPrefs'] = {'performance': 'ALL'}

    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("user-agent={}".format(
    #     fake_useragent.UserAgent().random))
    # chrome_options.add_experimental_option(
    #     'excludeSwitches', ['enable-logging'])
    chrome_options.add_argument("--disable-popup-blocking")
    driver = webdriver.Chrome(
        executable_path=r'i://clients//chromedriver.exe', options=chrome_options, desired_capabilities=d)
    driver.implicitly_wait(10)
    driver.maximize_window()
    return driver


# try getting url http://bingoindustries.com.au/
# url = "https://bingoindustries.com.au"


def main(url):
    while (True):
        driver = Chrome()
        try:
            driver.get(url)
            # press space
            try:

                driver.find_element_by_tag_name('body').send_keys(Keys.SPACE)
                print("press space")
            except Exception as e:
                print(e)

            time.sleep(15)
            print("sleep 15")
            try:
                driver.find_element_by_tag_name(
                    'body').send_keys(Keys.CONTROL + 't')
                # close the 1st tab
                driver.switch_to.window(driver.window_handles[0])
                print("open new tab")
            except Exception as e:
                print(e)
            # clsoe the tab
            time.sleep(2)
            try:

                driver.close()
            except Exception as e:
                print("closing tab")
        except TimeoutException:
            print("The website is not responding")
        except Exception as e:
            print(e)


if __name__ == '__main__':
    pass
    # url = "https://www.youtube.com/watch?v=BYuQOtmIBZE"

    # main(url)
