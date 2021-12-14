from flask import jsonify
import json

def get_problem():
    prob = {}

    return prob


def create_problem(problem):
    return jsonify({
        "problem": "사용자가 직접 만든 문제",
        "solution": "직접 만든 문제의 answer은 요거",
        "option":
            [
                {"word": "오답1",
                 "flag": False,
                 "check": False
                 },
                {
                    "word": "오답2",
                    "flag": False,
                    "check": False
                },
                {
                    "word": "정답",
                    "flag": True,
                    "check": False
                },
                {
                    "word": "오답3",
                    "flag": False,
                    "check": False
                }
            ]
    })

def make_problem_with_solution():
    new_problem = {}
    
    with open("json/kdict_dummy.json", "r") as kdict_json:
        kdict_data = json.load(kdict_json)

    with open("json/problem_dummy.json", "r") as problem_json:
        problem_data = json.load(problem_json) 

    new_problem["context"] = problem_data["problems"][0]["context"]
    new_problem["option"] = []
    
    for i in range(4): 
        new_problem["option"].append(kdict_data["data"][i])
        del new_problem["option"][i]["example"]
    
    new_problem["solution"] = 1

    return jsonify(new_problem)
