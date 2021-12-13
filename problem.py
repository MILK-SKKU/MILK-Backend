from flask import jsonify


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
