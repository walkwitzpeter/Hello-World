import random
import time
import webbrowser

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import QuizAnswers
""" 
I DON'T PROMISE THE SECURITY OF THIS PROGRAM!!!!!!

However if you still want to use it, enter your username and password below.
This program should complete 10 quizzes for you, 
 HOWEVER you will have to answer the captcha at the end of each quiz. 
 After you answer the captcha you will need to enter a user input into the program
 (I run the program in PyCharm and so I just enter it in the PyCharm terminal)

Sorry I still am very new at this and don't know how to get it to auto answer the captcha,
 and much of my code is still pretty messy
 
Things that stop it from working:
    Having already completed one quiz today (especially one of the quizzes on here)
    Navigating to a different part of the website at any point (except for clicking the captcha)

Author: Peter Walkwitz
Date Last Modified: (1/21/2022)
"""
import QuizLinks

USERNAME = "your username"
PASSWORD = "your password"
WIZURL = "https://www.wizard101.com/game/"

tenTriviaNames = ['Ancient Egypt Trivia', 'Early American History Trivia', 'Famous World Leaders',
                  'Greek Mythology Trivia', 'Norse Mythology Trivia', 'Solar System Trivia', 'State Nicknames Trivia',
                  'Weather Trivia', 'Apollo Missions Trivia', 'World Capitols Trivia']


def navigateToQuizzes(driver, quizName):
    # This takes you to the Quizzes
    try:
        earnCrownsButton = driver.find_element(By.XPATH, "//*[@id='subMenu1_lockOpen']/ul/li/div/a[5]")
        earnCrownsButton.click()
        playTriviaButton = driver.find_element(By.XPATH, "//*[@id='img_8ad6a41245d5c0cb01461af1244b1400']")
        playTriviaButton.click()
        educationalTriviaButton = driver.find_element(By.LINK_TEXT, "View More Educational Trivia »")
        educationalTriviaButton.click()
        # Using my dictionary to get the XPATH to find the right quiz
        quizButton = driver.find_element(By.XPATH, QuizLinks.QuizLinksDict[quizName])
        quizButton.click()
    except:
        print("failed to get to quiz")


def getCrowns():
    print("start of browser")

    driver = webdriver.Chrome(r"chromedriver")
    driver.get(WIZURL)
    print()

    # Process to Log in
    try:
        # Typing in username and password
        username = driver.find_element(By.XPATH, "//*[@id='loginUserName']")
        password = driver.find_element(By.XPATH, "//*[@id='loginPassword']")
        username.send_keys(USERNAME)
        password.send_keys(PASSWORD)

        # Clicking Login
        login_button = driver.find_element(By.XPATH, "//*[@id='wizardLoginButton']/tbody/tr/td[1]/div/div/input")
        login_button.click()
    except:
        print("failed to find login")

    for quizNumber in range(10):
        quizName = tenTriviaNames[quizNumber]
        navigateToQuizzes(driver, quizName)

        # Solving quizzes
        for questionNumber in range(12):
            content = driver.page_source
            soup = BeautifulSoup(content, 'lxml')
            answerQuizQuestion(soup, driver, QuizAnswers.ArrayOfDictionaries[quizNumber])

        # Starting a new quiz (I need to first click claim button and get the captcha right)
        claimRewardButton = driver.find_element(By.CLASS_NAME, "kiaccountsbuttongreen")
        claimRewardButton.click()
        # I might need to re-grab the content here to get the captcha solved
        # TODO this is what is breaking (i am currently manually doing the captcha)
        time.sleep(1)
        # Adding a user input here because we need to know that they clicked the captcha
        userInput = input("Clicked Captcha?")
        # Taking another quiz
        takeAnotherQuizButton = driver.find_element(By.CLASS_NAME, "kiaccountsbuttongreen")
        takeAnotherQuizButton.click()

    done = False
    print("All done!")
    while not done:
        time.sleep(10)


def answerQuizQuestion(soup, driver, dictionary):
    # This grabs the quiz question
    webQuestion = soup.find('div', attrs={'class':'quizQuestion'})
    # Creating a wait time because the answers fade in
    # TODO I should really change this to (when interactable)
    time.sleep(5)

    # Creating Answer here, so I can reference outside the for loop
    answer = ""

    # Looping through the dictionary to find the right answer
    for quizQuestion in dictionary:
        if webQuestion.__contains__(quizQuestion):
            print("answer found: " + quizQuestion)
            answer = dictionary[quizQuestion]
            print("answer is: " + answer)
            break

    # Keeping an array of all the buttons to find the right one
    allButtons = driver.find_elements(By.CLASS_NAME, "largecheckbox")
    checkBox = 0
    # Looping through the options
    for webAnswer in soup.find_all('span', attrs={'class': 'answerText'}):
        answerButton = allButtons[checkBox]
        print(allButtons[checkBox])
        if checkBox < 3:
            checkBox += 1

        if webAnswer.text.__contains__(answer):
            print("the real answer is: " + answer)
            print("finding answer button, webanswer: " + webAnswer.text)
            answerButton.click()
            break
        else:
            print("didnt find answer, clicking last option")
            answerButton.click()

    # Moving on to the next question
    try:
        nextQuestionButton = driver.find_element(By.ID, "nextQuestion")
        print("About to click next question button")
        nextQuestionButton.click()
    except:
        print("failed to find next question button")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    getCrowns()


# Sources
# https://www.youtube.com/watch?v=f7LEWxX4AVI
#     Used to figure out how to type (send keys function)

# Code taken from https://www.geeksforgeeks.org/click-button-by-text-using-python-and-selenium/
#     Used to get the basic framework for opening and editing/messing with a browser

# https://www.edureka.co/blog/web-scraping-with-python/
#     Used to help parse the quiz questions and learn how to parse the page

# https://www.geeksforgeeks.org/python-dictionary/
#     Used for understanding how to make dictionaries

# https://github.com/AmusingThrone/wizard101-trivia-solver
#     Inspiration that I could actually accomplish this (even if I didn't use any of his code)
