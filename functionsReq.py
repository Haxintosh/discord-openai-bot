import requests

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


def formatHeader(path):
    key = open(path, 'r')
    bearer = "Bearer " + key.read()
    headers = {
        "Authorization": bearer,
        "Content-Type": "application/json"
    }
    return headers


def sendIT(payload, headers):
    answer = requests.post(url = "https://api.openai.com/v1/completions", json=payload, headers=headers)
    return answer



def formatAnswer(answer):
    answerDict = answer.json()
    choices = answerDict.get("choices")[-1]
    text = choices.get("text")
    print(text)
    return text

'''
payload = formatPayload("say this is a test", 1, 16)
header = formatHeader("key.txt")
answer = sendIT(payload, header)
formatAnswer(answer)
'''
