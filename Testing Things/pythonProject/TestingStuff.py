import json
import time
import QuizAnswers
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

# url = "http://kite.com"
# html = url.open(url).read()
# soup = BeautifulSoup(html)
#
# for script in soup(["script", "style"]):
#     script.decompose()
#
# strips = list(soup.stripped_strings)
# print(strips[:5])
import QuizLinks

WIZURL = "https://www.wizard101.com/quiz/trivia/game/educational-trivia"
from selenium.webdriver.remote.webelement import WebElement

# WIZURL = "http://demo.guru99.com/test/radio.html"


def solveWizardCity():

    # driver = webdriver.Chrome(r"chromedriver")
    # driver.get(WIZURL)

    for quizNumber in range(10):
        print(QuizAnswers.ArrayOfDictionaries[quizNumber])


    # done = False
    # while not done:
    #     time.sleep(10)


if __name__ == '__main__':
    solveWizardCity()
