#imports
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time
import csv

#function for checking whether an element exists or not on the webpage
def check_exists(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

#website url
url = "https://www.tripadvisor.it/Restaurants-g187791-Rome_Lazio.html"

#Chrome session
#Here, Selenium accesses the Chrome browser driver in incognito mode and without actually opening a browser window (headless argument). 
options = webdriver.ChromeOptions()
options.add_argument('start-maximized')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("C:/Users/donat/Desktop/master/chromedriver", chrome_options=options)
driver.implicitly_wait(30) 
driver.get(url)
time.sleep(3)

#Open "Neighborhood" filter and select "Prenestino Centocelle" and "Prenestino-Centocelle", then press "Applica" button
driver.find_element_by_xpath("//*[@id='component_108']/div/div[10]/div[2]/div[5]/span[1]").click()
driver.execute_script("arguments[0].click();", driver.find_element_by_xpath("//span[@class='common-filters-LinkableFilterLabel__label--XOPWc'][contains(text(),'Prenestino Centocelle')]"))
time.sleep(3)
driver.execute_script("arguments[0].click();", driver.find_element_by_xpath("//span[@class='common-filters-LinkableFilterLabel__label--XOPWc'][contains(text(),'Prenestino-Centocelle')]"))
driver.find_element_by_xpath("//button[@class='ui_button primary']").click()


#Save all restaurant links in a list
restaurant_links = []

#Selenium navigates all the pages with results clicking "Next" button
while (1):
    soup = BeautifulSoup(driver.page_source, 'lxml')
    for link in soup.findAll('a',{'class':'_15_ydu6b'}):
       restaurant = 'https://www.tripadvisor.it' + str(link['href'])
       restaurant_links.append(restaurant)
       time.sleep(3)
    if (check_exists("//a[@class='nav next rndBtn ui_button primary taLnk']")):
        print("prossima pagina")
        next_button = driver.find_element_by_xpath("//a[@class='nav next rndBtn ui_button primary taLnk']")
        next_button.click()
        time.sleep(3)
    else: break
    
# I strategia
# open the file to save the reviews
csvFile1 = open("C:/Users/donat/Desktop/reviews1.csv", 'w', newline='', errors="ignore")
csvWriter1 = csv.writer(csvFile1, delimiter=',')

# for every restaurant in list, save first 5 reviews with username, rating and review date
for i in restaurant_links:
    print("prossimo ristorante")
    url = str(i)
    driver = webdriver.Chrome("C:/Users/donat/Desktop/master/chromedriver", chrome_options=options)
    driver.implicitly_wait(30) 
    driver.get(url)
    
    #Expand, if any, "Mostra di Più" button
    element_list = driver.find_elements_by_xpath("//span[@class='taLnk ulBlueLinks']")[:5]
    for e in element_list:
        try:
            e.click()
            time.sleep(3)
        except:
            pass
    
    # collect data    
    soup = BeautifulSoup(driver.page_source, 'lxml')
    if (check_exists("//div[@class='reviewSelector']")):
        reviews = soup.findAll('div', {'class':'reviewSelector'})[:5]
    else: pass
    
    # for each review collected, get some information (rating, data, username, review) and save them into csv
    if(len(reviews)>0):
        for rev in reviews:
            rating = rev.find('span', {'class':'ui_bubble_rating'}).get('class')[1].split("_")[1]
            data_review = rev.find('span', {'class':'ratingDate'}).get('title')
            username = rev.find('div', {'class':'info_text pointer_cursor'}).find('div').get_text()
            review_text = rev.find('p', {'class':'partial_entry'}).get_text().replace("\n", " ")
            row = [rating,data_review,username,review_text]
            csvWriter1.writerow(row)
            print("riga scritta")
            time.sleep(3)
    else: pass
        
    time.sleep(3)
    
csvFile1.close()

# II strategia
# open the file to save the reviews
csvFile2 = open("C:/Users/donat/Desktop/reviews2.csv", 'w', newline='', errors="ignore")
csvWriter2 = csv.writer(csvFile2, delimiter=',')

# for the first 20 restaurants in list, save the first 50 reviews with username, rating and review date
for i in restaurant_links[:20]:
    print("prossimo ristorante")
    url = str(i)
    driver = webdriver.Chrome("C:/Users/donat/Desktop/master/chromedriver", chrome_options=options)
    driver.implicitly_wait(30) 
    driver.get(url)
    
    n=0
    while(1):
        #Expand, if any, "Mostra di Più" button
        element_list = driver.find_elements_by_xpath("//span[@class='taLnk ulBlueLinks']")
        for e in element_list:
            try:
                e.click()
                time.sleep(3)
            except:
                pass
        
        # collect data
        soup = BeautifulSoup(driver.page_source, 'lxml')
        if (check_exists("//div[@class='reviewSelector']")):
            reviews = soup.findAll('div', {'class':'reviewSelector'})
        else: pass
        
        # for each review collected, get some information (rating, data, username, review) and save them into csv
        if(len(reviews)>0):
            for rev in reviews:
                rating = rev.find('span', {'class':'ui_bubble_rating'}).get('class')[1].split("_")[1]
                data_review = rev.find('span', {'class':'ratingDate'}).get('title')
                username = rev.find('div', {'class':'info_text pointer_cursor'}).find('div').get_text()
                review_text = rev.find('p', {'class':'partial_entry'}).get_text().replace("\n", " ")
                row = [rating,data_review,username,review_text]
                csvWriter2.writerow(row)
                print("riga scritta")
                n+=1
                time.sleep(3)
        else: pass
        
        # if 50 comment are reached, stop
        if (n==50):
            print("raggiunti 50 commenti")
            break
        
        # else go to next page by clicking on "Next" button
        else:
            if (check_exists("//a[@class='nav next ui_button primary']")):
                next_button = driver.find_element_by_xpath("//a[@class='nav next ui_button primary']")
                next_button.click()
                print("pagina successiva")
                time.sleep(3)
            else: 
                break
    
csvFile2.close()

driver.quit()
    
    




