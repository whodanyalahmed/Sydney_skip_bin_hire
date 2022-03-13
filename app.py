# import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import time
import re
from urllib.parse import urlparse


def main_domain(url):

    t = urlparse(url).netloc
    new_url = '.'.join(t.split('.'))
    if 'www' in new_url:
        new_url = new_url.replace('www.', '')
    new_url = new_url.split('.')[0]
    return new_url


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


def main(url, driver):

    try:
        driver.get("http://google.com.au/")
    except TimeoutException:
        print("The website is not responding")
    except Exception as e:
        print(e)

    # search for skin bin hire price in sydney
    # http://bingoindustries.com.au
    # http://purplecowindustries.com.au
    # http://aussieindustries.com.au
    try:

        search_box = driver.find_element_by_name('q')
        # clear the search box
        search_box.clear()
        search_box.send_keys("Skip bin hire sydney prices site:"+url)
        search_box.send_keys(Keys.RETURN)
    except Exception as e:
        print(e)
# http://purplecowindustries.com.au

    def fill_captcha():
        if 'sorry' in str(driver.current_url):
            print("info : please try to fill the captcha")
            time.sleep(10)
            fill_captcha()
        else:
            pass

    # function to get domain name from string

    def get_domain_name(url):
        # get the domain name
        domain_name = url.split('//')[-1].split('/')[0]
        return domain_name

    fill_captcha()
    driver.implicitly_wait(10)

    def check_url(attach_url, found_url):
        domain = main_domain(attach_url)
        print("Domain: "+domain)
        if re.match(r'^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)'+domain+'.com.au', found_url):
            print("Regex matched: "+str(url))
            return True
        else:
            return False
    # try:
    #     source = driver.page_source
    #     soup = BeautifulSoup(source, 'html.parser')
    #     print("soup done")

    #     # get the class named EDblX DAVP1
    #     divs = soup.find_all('div', attrs={'class': 'mnr-c pla-unit'})
    #     for div in divs:
    #         anchors = div.find_all('a')[1]
    #         print(anchors.get('href'))

    # except Exception as e:
    #     print(e)
    def click_more():
        try:
            driver.find_element_by_xpath("//div[@class='exp-button']").click()
            print("next button clicked")
        except Exception as e:
            print(e)
    click_more()
    try:
        divs = driver.find_elements_by_xpath('//div[@class="mnr-c pla-unit"]')
        for div in divs:
            anchors = div.find_elements_by_xpath('//a')
            domain = get_domain_name(url)
            while(True):
                click_more()
                for anchor in anchors:
                    try:
                        try:

                            searched_url = anchor.get_attribute('href')
                            print("Attached url: "+str(url))
                            print("Found url: "+str(searched_url))
                        except Exception as e:
                            print("info: href not found or "+str(e))
                        if(check_url(str(url), str(searched_url))):
                            print("domain name is in url")

                            driver.get(searched_url)
                            time.sleep(3)
                            driver.back()
                    except Exception as e:
                        print("info : something went wrong - "+str(e))
                        continue    
                        # close the new tab

    except Exception as e:
        print("Something went wrong or "+str(e))
    print("successfully completed")
    driver.quit()


if __name__ == '__main__':
    pass
    # driver=Chrome()
    # main(url, driver)
