from bs4 import BeautifulSoup
# from dotenv import load_dotenv
import requests
import os


def search_word(word):
    load_dotenv()
    openApiKey = os.environ.get("URMSAPIKEY")

    params = f"?certkey_no=3114&key={openApiKey}&target_type=search&q={word}"
    openUrl = "https://opendict.korean.go.kr/api/search"+params

    paramsForExample = f"?certkey_no=3114&key={openApiKey}&target_type=search&q={word}&part=exam"
    openUrlForExample = "https://opendict.korean.go.kr/api/search"+paramsForExample

    res = requests.get(openUrl)
    soup = BeautifulSoup(res.content, 'html.parser')

    resEx = requests.get(openUrlForExample)
    soupEx = BeautifulSoup(resEx.content, 'html.parser')

    ret_json = {"word":word, "items":[], "example":[]}

    check = soup.find('total').get_text()
    if check == '0':
        return ret_json

    wordPos = soup.find_all('pos')
    wordDef = soup.find_all('definition')
    wordEx = soupEx.find_all('example')

    for i in range(3):
        item = {}
        item["pos"] = wordPos[i].get_text().strip()
        item["definition"] = wordDef[i].get_text().strip()
        ret_json["items"].append(item)

    for i in wordEx:
        ret_json["example"].append(i.get_text().strip())

    return ret_json