from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import csv
import re
import time

# function for getting text of any element
def get_element_text(element=''):
    if element is None:
        return "None"
    else:
        return element.getText() 

class matrixscraper:
    
    url = "https://matrix.southfloridamls.com/Matrix/Public/Portal.aspx?k=1347965XLP20&p=DE-12136351-101/"
    
    def __init__(self):
        print("This is matrixscraper created by isopooh")
        # self.browser = webdriver.Chrome()
        self.browser = webdriver.PhantomJS()
        self.browser.get(self.url)

    def get_browser(self):
        return self.browser

    def stop_browser(self):
        self.browser.close()

    #========================================================
    # store the result into csv file
    #========================================================    
    def store_csv(self, result):
        print("saving the lists....")
        with open('result.csv', 'w') as csvfile:
            fieldnames = ["price", "status", "link", "position", "bedrooms", "baths", "sqft", "housetype", "housestyle", "other", "description"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for item in result:
                writer.writerow(item)

    # =====================================================
    # Main code : Start to scrape
    # =====================================================     
    def run_parser(self):
        print("Start to run parser...")
        browser = self.get_browser()
       
        # click "See More Results" button until appearing again
        while (True):
            try:
                nextbutton = browser.find_element_by_xpath("//div[@style!='display: none;']/a[@id='_ctl0_m_DisplayCore_dpy1a']")
                nextbutton.click()
                time.sleep(5)        
            except NoSuchElementException:
                print("NoSuchElementException fire")
                break
            except ElementNotVisibleException:
                print("!!ElementNotVisibleException fire!!!!!!!!!!!")
                break
            finally:
                print("This button is clicked")


        # parse the whole page
        print("Extracting the lists....")
        time.sleep(10)

        page = BeautifulSoup(browser.page_source, "html5lib")
        lists = page.find("div",{"id":"_ctl0_m_divAsyncPagedDisplays", "class":"j-resultsPageAsyncDisplays"}).findAll("div",{"class":"multiLineDisplay"})
        self.stop_browser()
        result = []
        for item in lists:
            price = item.find("span", {"class":"d-fontSize--largest"})
            status = item.find("span", {"class":re.compile("Status_*")})
            link = item.find("div",{"class":" col-sm-12 d-fontSize--largest d-text d-color--brandDark"}).find("a")
            position = item.find("div",{"class":" col-sm-12 d-fontSize--small d-textSoft"}).find("span")
            
            info = item.find("div", {"class":" col-lg-7 col-md-6 col-sm-12"})
            bedrms = info.find("span",{"class":"d-textStrong d-paddingRight--4 "})
            baths = info.findAll("span",{"class":"d-textStrong d-paddingRight--4 "})[1]
            sqft = info.find("span",{"class":"d-text d-fontWeight--bold"})
            housetype = info.find("span",{"class":"d-textStrong d-fieldsSeparatorComma d-paddingRight--4 "})
            housestyle = info.findAll("span",{"class":"d-textStrong d-fieldsSeparatorComma d-paddingRight--4 "})[1]
            other = info.findAll("span",{"class":"d-text d-fontWeight--bold"})[1]
            description = info.find("div", {"class":"col-sm-12 hidden-sm d-paddingTop--4 d-paddingBottom--4 hidden-md hidden-xs"}).find("span",{"class":"d-textSoft"})
            re_item={}
            re_item["price"] = get_element_text(element=price)
            re_item["status"] = get_element_text(element=status)
            re_item["link"] = get_element_text(element=link)
            re_item["position"] = get_element_text(element=position)
            re_item["bedrooms"] = get_element_text(element=bedrms)
            re_item["baths"] = get_element_text(element=baths)   
            re_item["sqft"] = get_element_text(element=sqft) 
            re_item["housetype"] = get_element_text(element=housetype)
            re_item["housestyle"] = get_element_text(element=housestyle)
            re_item["other"] = get_element_text(element=other)
            re_item["description"] = get_element_text(element=description)
            result.append(re_item)
        # ================================================================
        self.store_csv(result)


def main():
    s = matrixscraper()
    s.run_parser()

if __name__ == "__main__":
    main()