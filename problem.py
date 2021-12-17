import fasttext
from konlpy.tag import Komoran
import numpy as np
import random
import re
import requests
from bs4 import BeautifulSoup


model = fasttext.load_model('cc.ko.300.bin')
komoran = Komoran()
re = re.compile("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]")
openApiKey = "BD099954D410A11253DA35DEB404198B"
conv_length = 6
quiz_threshold = 5000



def get_similar_word(word):
    print("Get Similar Word : ", word)
    return model.get_nearest_neighbors(word, k=1)


def search_word(word):
    ret_json = {"word": word, "items": []}

    # 명사 혹은 대명사면 그대로
    if komoran.pos(word)[0][1] == 'NN' or 'NP':
        word = komoran.pos(word)[0][0]

    params = f"?certkey_no=3114&key={openApiKey}&target_type=search&q={word}"
    openUrl = "https://opendict.korean.go.kr/api/search"+params

    paramsForExample = f"?certkey_no=3114&key={openApiKey}&target_type=search&q={word}&part=exam"
    openUrlForExample = "https://opendict.korean.go.kr/api/search"+paramsForExample

    res = requests.get(openUrl)
    soup = BeautifulSoup(res.content, 'html.parser')

    resEx = requests.get(openUrlForExample)
    soupEx = BeautifulSoup(resEx.content, 'html.parser')

    check = soup.find('total').get_text()
    if check == '0':
        return ret_json

    wordPos = soup.find_all('pos')
    wordDef = soup.find_all('definition')
    wordEx = soupEx.find_all('example')

    for i in range(min(3, len(wordPos))):
        item = {}
        item["pos"] = wordPos[i].get_text().strip()
        item["definition"] = wordDef[i].get_text().strip()
        ret_json["items"].append(item)

    return ret_json


def cos(A, B):
    return (A.dot(B.T)/(np.linalg.norm(A) * np.linalg.norm(B)))


def create_answer(problem):
    sentence_vector = model.get_sentence_vector(problem)
    result = []
    problem = problem.replace("?", " ")
    problem = problem.replace(".", " ")
    problem = problem.replace("!", " ")
    problem = problem.replace("~", " ")

    for word in problem.split(" "):
        word_vector = model.get_word_vector(word)
        result.append([cos(sentence_vector, word_vector), word])

    result = sorted(result, key=lambda x: -x[0])
    answer = result[0][1]
    return answer


def create_candidate(answer):
    answer_morphs = komoran.morphs(answer)
    candidate = model.get_nearest_neighbors(answer)

    candidate = map(lambda x: x[1], candidate)

    candidate = filter(lambda x: re.search(x) == None, candidate)

    candidate = filter(lambda x: komoran.morphs(x) != answer_morphs, candidate)

    candidate = filter(lambda x: 3 * len(answer) > len(x), candidate)

    candidate = list(candidate)
    if len(candidate) < 3:
        return None
    else:
        return candidate[:3]


def change_speaker(context):
    speaker = ['승열', '돌맹', '붕어', '감자']
    random.shuffle(speaker)
    s = []

    for c in context:
        if c["speaker"] not in s:
            s.append(c["speaker"])
        c["speaker"] = speaker[s.index(c["speaker"])]

    return context


def quiz_generator(sentence):
    problem_commit = {
        "context": [{
            "content" : sentence,
            "speaker" : ""    
        }],
        "solution": 0
    }

    # answer
    answer = create_answer(sentence)
    option = create_candidate(answer)
    
    if (answer or option is None):
        return {
            "context": [{
                "content": 'Your sentence is unable to create new question. try longer sentence.',
                "speaker": ""
            }],
            "solution": 0
        }
    option.append(answer)
    random.shuffle(option)
    problem_commit['solution'] = option.index(answer)
    problem_commit['option'] = option
    
    return problem_commit

