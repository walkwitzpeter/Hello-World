import time

from bs4 import BeautifulSoup
from playsound import playsound
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import QuizAnswers
import QuizLinks

""" 
I DON'T PROMISE THE SECURITY OF THIS PROGRAM OR THAT YOU WONT BE BANNED

However if you still want to use it, enter your username and password below.
This program should complete 10 quizzes for you, 
 HOWEVER you will have to answer the captcha at the end of each quiz. 
 After you answer the captcha you will need to enter a user input into the program
 (I run the program in PyCharm and so I just enter it in the PyCharm terminal)

This was written for myself so it is kinda messy and not always easy to figure out where
 it fails. But it works perfect for me, so write one yourself to practice if this doesn't
 work for you!
 
I got the free sound from the following website
https://www.dreamstime.com/demonqten_info (Nkolay Smirnov - is the author)
 
Things that stop it from working:
    Having already completed one quiz today (especially one of the quizzes on here)
    Navigating to a different part of the website at any point (except for clicking the captcha)

Author: Peter Walkwitz
Date Last Modified: (7/3/2022)
"""

USERNAME = "Username"
PASSWORD = "Password"
WIZURL = "https://www.wizard101.com/game"
# Starts at 0 not 1
STARTING_QUIZ = 0

tenTriviaNames = ['Ancient Egypt Trivia', 'Early American History Trivia', 'Famous World Leaders',
                  'Greek Mythology Trivia', 'Norse Mythology Trivia', 'Solar System Trivia', 'State Nicknames Trivia',
                  'Weather Trivia', 'Apollo Missions Trivia', 'World Capitols Trivia']


def checkCaptcha(messageString):
    playsound("DoneDing.mp3")
    userInput = input(messageString)


def getCrowns():
    driver = webdriver.Chrome(ChromeDriverManager().install())
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
        checkCaptcha("Logged In? ")

    except:
        print("failed to find login")

    for quizNumber in range(STARTING_QUIZ, 10):
        quizName = tenTriviaNames[quizNumber]
        driver.get("https://www.wizard101.com/quiz/trivia/game/" + QuizLinks.QuizLinksDict[quizName])

        # Solving quizzes
        for questionNumber in range(12):
            try:
                content = driver.page_source
                soup = BeautifulSoup(content)
                answerQuizQuestion(soup, driver, QuizAnswers.ArrayOfDictionaries[quizNumber])
            # In case the connection drops, trys to refresh the page and keep it going
            except AttributeError:
                driver.refresh()
                questionNumber -= 1
                print("Question Number: " + questionNumber)

        # Claiming the crowns
        claimRewardButton = driver.find_element(By.CLASS_NAME, "kiaccountsbuttongreen")
        claimRewardButton.click()
        checkCaptcha("Clicked Captcha? ")

        # Taking another quiz
        takeAnotherQuizButton = driver.find_element(By.CLASS_NAME, "kiaccountsbuttongreen")
        takeAnotherQuizButton.click()

    print("All done!")
    done = False
    while not done:
        time.sleep(10)


def answerQuizQuestion(soup, driver, dictionary):
    # This grabs the quiz question
    webQuestion = soup.find('div', attrs={'class': 'quizQuestion'})
    # Creating a wait time because the answers fade in
    # TODO I should probably change this to (when interactable)
    time.sleep(5)

    # Creating Answer here, so I can reference outside the for loop
    answer = ""

    # Looping through the dictionary to find the right answer
    for quizQuestion in dictionary:
        if webQuestion.__contains__(quizQuestion):
            print("answer found: " + quizQuestion)
            answer = dictionary[quizQuestion]
            break

    # Keeping an array of all the buttons to find the right one
    allButtons = driver.find_elements(By.CLASS_NAME, "largecheckbox")
    checkBox = 0
    # Looping through the options
    for webAnswer in soup.find_all('span', attrs={'class': 'answerText'}):
        answerButton = allButtons[checkBox]
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
        nextQuestionButton.click()
    except:
        print("failed to find next question button")


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
