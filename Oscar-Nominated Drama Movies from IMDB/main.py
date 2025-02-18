from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from pprint import pprint
import pandas as pd
import openpyxl

URL = 'https://www.imdb.com/'


def acceptCookies(driver):
    accept_button = driver.find_element(By.XPATH, '//button[text()="Accept"]')
    accept_button.click()

def goPage(driver, actions):
    driver.find_element(By.ID, 'suggestion-search-button').click() #search button 
    sleep(1)

    driver.find_element(By.CSS_SELECTOR, 'a[data-testid="advanced-search-chip-tt"]').click() #movies 
    sleep(1)

    driver.find_element(By.CSS_SELECTOR, 'button[data-testid="test-chip-id-movie"]').click()
    sleep(1)
    
    driver.find_element(By.CSS_SELECTOR, 'button[data-testid="test-chip-id-Comedy"]').click()
    sleep(1)

    awards_title = driver.find_element(By.CSS_SELECTOR, 'label[data-testid="accordion-item-awardsAccordion"]')
    actions.move_to_element(awards_title).perform()
    awards_title.click()
    sleep(2)

    oscar_button = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="test-chip-id-oscar-nominated"]')
    actions.move_to_element(oscar_button).perform()
    oscar_button.click()
    sleep(1)

    driver.find_element(By.CSS_SELECTOR, 'button[data-testid="adv-search-get-results"]').click()
    sleep(1)


def scrollPage(driver, actions):
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        sleep(1)
        try:
            more_button = driver.find_element(By.CLASS_NAME, 'ipc-see-more__button')        
            actions.move_to_element(more_button).perform()
            more_button.click()
        except: 
            break
        sleep(1)
        

def getData(driver):
    movies = driver.find_elements(By.CLASS_NAME, 'ipc-metadata-list-summary-item')

    movie_dict = {
        'name': [],
        'year': [],
        'duration': [],
        'stars': [],
        'votes': [],
        'metascore': [],
        'description': [],
    }

    for movie in movies:
        name = movie.find_element(By.CLASS_NAME, 'ipc-title__text').text
        movie_dict['name'].append(name)

        yearDurationContainer = movie.find_elements(By.CLASS_NAME, 'sc-d5ea4b9d-7')
        year = yearDurationContainer[0].text
        duration = yearDurationContainer[1].text
        movie_dict['year'].append(year)
        movie_dict['duration'].append(duration)

        stars = movie.find_element(By.CLASS_NAME, 'ipc-rating-star--rating').text
        movie_dict['stars'].append(stars)

        votes = movie.find_element(By.CLASS_NAME, 'ipc-rating-star--voteCount').text.strip()[1:-1]
        movie_dict['votes'].append(votes)

        try: 
            metascore = movie.find_element(By.CLASS_NAME, 'metacritic-score-box').text
            movie_dict['metascore'].append(metascore)
        except:
            metascore = 'NONE'
            movie_dict['metascore'].append(metascore)

        desc = movie.find_element(By.CLASS_NAME, 'ipc-html-content-inner-div').text
        movie_dict['description'].append(desc)

        print(f"Scraping movie: {name}")
        
    print("Scraping completed!")
    return movie_dict


def convertExcel(data):
    df = pd.DataFrame(data)
    df.to_excel('movies.xlsx')

def main():
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_experimental_option(name='detach', value=True)

    driver =  webdriver.Chrome(options=options)
    actions = ActionChains(driver)
    driver.implicitly_wait(5)
    driver.get(URL)

    acceptCookies(driver)
    goPage(driver, actions)
    scrollPage(driver, actions)
    data = getData(driver)
    convertExcel(data)


if __name__ == '__main__':
    main()