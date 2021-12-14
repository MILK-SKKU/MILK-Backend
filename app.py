from flask import Flask, request
from flask_restx import Api
from flask_cors import CORS
from problem import get_problem, create_problem, make_problem_with_solution
import k_dictionary as kd


app = Flask(__name__)
CORS(app)
api = Api(app)


@app.route('/')
def index():
    return 'Welcome to Flask server!'


@app.route('/dict/<word>')
def dictionary(word):
    return kd.search_word(word)


@app.route('/prob')
def prob():
    custom = request.args.get('custom', default="False", type=str)

    if custom == "True":
        return create_problem()
    else:
        problem_not_blanked = get_problem()

        target = problem_not_blanked["solution"]
        for conv in problem_not_blanked["problem"]:
            if target in conv["content"]:
                conv["content"] = conv["content"].replace(target,'__________')
                break 

        return problem_not_blanked

@app.route('/problem')
def problem():
    return make_problem_with_solution()



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)