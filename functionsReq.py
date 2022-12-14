import random

import requests
import config
def formatPayload(prompt, temp, token):
    defaultTemp = 1
    if token != '':
        token = token
    else:
        token = 20
    finalToken = int(token)

    if temp != '':
        temp = temp
    else:
        temp = defaultTemp
    finalTemp = float(temp)

    payload = {
        "model": "text-davinci-003",
        "prompt": prompt,
        "temperature": finalTemp,
        "max_tokens": finalToken,
        "top_p": 1,
        "n": 1,
    }
    return payload


def formatHeader():
    bearer = "Bearer " + config.API_KEY
    headers = {
        "Authorization": bearer,
        "Content-Type": "application/json"
    }
    return headers

def formatImgPayload(prompt, size):

    sizeDict = {
        256: "256x256",
        512: "512x512",
        1024: "1024x1024"
    }

    if size == 256 or 512 or 1024:
        sizeFinal = sizeDict.get(size)
    else:
        sizeFinal = sizeDict.get(512)

    payload = {
    "prompt": prompt,
    "n": 1,
    "size": sizeFinal
    }

    print(payload)
    return payload

def sendIT(payload, headers):
    answer = requests.post(url = "https://api.openai.com/v1/completions", json=payload, headers=headers)
    return answer

def sendITImg(payload, headers):
    answer = requests.post(url = "https://api.openai.com/v1/images/generations", json=payload, headers=headers)
    return answer
def formatAnswer(answer):
    answerDict = answer.json()
    choices = answerDict.get("choices")[-1]
    text = choices.get("text")
    print(text)
    return text

def formatImg(answer):
    answerDict = answer.json()
    choices = answerDict.get("data")[-1]
    text = choices.get("url")
    print(text)
    return text

def randomFooter():
    footerDict = {
        1 : "hello world",
        2 : "honk!" # add your fancy footers here ;)
    }
    answer = footerDict.get(random.randint(1, len(footerDict)+1))
    return answer

