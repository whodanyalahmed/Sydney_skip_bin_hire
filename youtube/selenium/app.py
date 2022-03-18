import datetime
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import os
# get data from excel Book1.xlsx


def get_excel_data(file_name, sheet_name, column_name):
    df = pd.read_excel(file_name, sheet_name=sheet_name)
    return df[column_name]


def Chrome(port, profile_path, profile, headless=False):
    # add fake user agent
    chrome_options = Options()

    # return webdriver
    # support to get response status and headers
    # d = webdriver.DesiredCapabilities.CHROME
    # d['loggingPrefs'] = {'performance': 'ALL'}

    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-web-security")
    # chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    chrome_options.add_experimental_option(
        "debuggerAddress", "127.0.0.1:"+port)
    chrome_options.add_argument(
        "--user-data-dir="+profile_path)
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--profile-directory="+profile)

    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--incognito")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("user-agent={}".format(
    #     fake_useragent.UserAgent().random))
    # chrome_options.add_experimental_option(
    #     'excludeSwitches', ['enable-logging'])
    # chrome_options.add_argument("--disable-popup-blocking")
    driver = webdriver.Chrome(
        executable_path=r'i://clients//chromedriver.exe', options=chrome_options
        # , desired_capabilities=d
    )
    driver.implicitly_wait(10)
    driver.maximize_window()
    return driver


def Click_on(driver, tag, text):

    driver.implicitly_wait(10)
    try:
        xpath_for_OK_btn = "//*[contains(text(), '"+text+"')]"

        driver.find_element_by_xpath(
            '//'+tag+'[.'+xpath_for_OK_btn + ']').click()
        print('info: '+text+' button/text clicked')
    except Exception as e:
        print("error: "+text+" button/text not found")
        print(e)


# def Click_on_like(tag, text):

#     try:
#         xpath_for_OK_btn = "//div[@id='top-level-buttons-computed']/ytd-toggle-button-renderer[1]/a"

#         driver.find_element_by_xpath(
#             '//'+tag+'[.'+xpath_for_OK_btn + ']').click()
#         print('info: '+text+' button/text clicked')
#     except Exception as e:
#         print("error: "+text+" button/text not found")
#         print(e)


# try getting url http://bingoindustries.com.au/
# url = "https://bingoindustries.com.au"

def main():

    logFile = open("log.txt", "a+")
    logFile.write("\nStarted at: " + str(datetime.datetime.now()))
    # To list folders
    profile = "Automation"

    port = "8989"
    profile_path = "C:\\Users\\Daniyal\\AppData\\Local\\Google\\Chrome\\User Data"
    try:

        os.popen('chrome.exe --remote-debugging-port="{}" --user-data-dir="{}"'.format(port,
                                                                                       profile_path+"\\"+profile))
        print("chrome opened")
    except Exception as e:
        print(e)
    driver = Chrome(port, profile_path, profile)
    links = get_excel_data('data.xlsx', 'Sheet1', 'links')
    comments = get_excel_data('data.xlsx', 'Sheet1', 'comments')
    for i in range(len(links)):

        # while (True):

        try:
            # open in new tab
            # driver.execute_script(
            #     "window.open('"+url+"', '_blank');")
            driver.switch_to.window(driver.window_handles[0])
            # check if its already there in log file
            # if not, then add it
            if links[i] not in logFile.read():

                driver.get(links[i])

                # press space
                try:

                    driver.find_element_by_tag_name('body').send_keys(Keys.SPACE)
                    print("press space")
                except Exception as e:
                    print(e)
                try:
                    pressed = driver.find_element_by_xpath(
                        "//div[@id='top-level-buttons-computed']/ytd-toggle-button-renderer[1]")
                    # get the class name of the button
                    class_name = pressed.get_attribute('class')
                    # print(class_name)
                    if("style-default-active" not in class_name):
                        driver.find_element_by_xpath(
                            "//div[@id='top-level-buttons-computed']/ytd-toggle-button-renderer[1]/a").click()
                        print("Clicked liked button")
                    else:
                        print("Already liked")
                except Exception as e:
                    print("like button not found")
                # scroll 400px
                driver.execute_script("window.scrollBy(0,400)")
                try:
                    try:
                        driver.find_element_by_xpath(
                            "//div[@id='placeholder-area']"
                        ).click()
                        print("clicked on placeholder")
                    except Exception as e:
                        print("placeholder not found")
                    # comment = driver.find_element_by_xpath(
                    #     "//yt-formatted-string[@id='contenteditable-textarea']")
                    comment = driver.find_element_by_xpath(
                        "//div[@id='contenteditable-root']")
                    # click using javascript
                    try:

                        driver.execute_script("arguments[0].click();", comment)
                        print("click comment using js")
                    except Exception as e:
                        print(e)
                    # try:

                    #     comment.click()
                    #     print("click comment using sele")
                    # except Exception as e:
                    #     print(e)
                    # send keys using js
                    try:
                        driver.execute_script(
                            "arguments[0].innerHTML='"+comments[i]+"';", comment)
                        # comment.send_keys("  "+comment_text)
                        print("send comment using js")
                    except Exception as e:
                        print(e)
                    # select all text in comment
                    try:
                        comment.send_keys(Keys.CONTROL + 'a')
                        print("select all text in comment")
                    except Exception as e:
                        print(e)
                    # press enter
                    try:
                        Click_on(driver, 'a', 'Comment')
                        # write the url in logFile
                        logFile.write("\n"+links[i])
                        print("comment sent")
                    except Exception as e:
                        print(e)
                except Exception as e:
                    print("Comment not added")

                time.sleep(15)
                print("sleep 15")

                # close tab
                driver.find_element_by_tag_name(
                    'body').send_keys(Keys.CONTROL + 'w')

                print("close tab")

                # try:

                #     driver.close()
                # except Exception as e:
                #     print("closing tab")
            else:
                print("Already commented")

        except TimeoutException:
            print("The website is not responding")
        except Exception as e:
            print(e)
    driver.quit()
    print("Successfully completed")    


if __name__ == '__main__':
    # pass
    # url = "https://www.youtube.com/watch?v=BYuQOtmIBZE"
    main()
