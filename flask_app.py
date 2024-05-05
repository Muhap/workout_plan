from flask import Flask, request, jsonify
import json

app = Flask(__name__)


def retrieve_workout_plan(gender, age, bmi, goal, days, filename='workout_plans.json'):
    with open(filename, 'r') as file:
        workout_plans = json.load(file)

    for plan in workout_plans:
        if (plan['Gender'] == gender and
                plan['Age'] == age and
                plan['BMI'] == bmi and
                plan['Goal'] == goal and
                plan['No_Days'] == days):
            return plan['Workout_Plan']

    return "No matching workout plan found."


@app.route('/workout_plan', methods=['GET'])
def get_workout_plan():
    gender = request.args.get('gender')
    age = request.args.get('age')
    bmi = request.args.get('bmi')
    goal = request.args.get('goal')
    days = int(request.args.get('days'))

    workout_plan = retrieve_workout_plan(gender, age, bmi, goal, days)

    return jsonify({'workout_plan': workout_plan})


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
