from flask import Flask, request, jsonify
import json

app = Flask(__name__)

def retrieve_workout_plan(gender, age, height, weight, goal, days, filename='/home/muhap/workout_plan/jsonified_workout_plans.json'):
    # Convert age to the correct age range
    if 18 <= age <= 29:
        age_range = "18 - 29"
    elif 30 <= age <= 49:
        age_range = "30 - 49"
    elif 50 <= age <= 69:
        age_range = "50 - 69"
    else:
        return "Age out of range."

    # Calculate BMI
    height = height/100
    bmi = weight / (height ** 2)
    if bmi < 18.5:
        bmi_range = "is less than 18.5"
    elif 18.5 <= bmi < 25:
        bmi_range = "is from 18.5 to 24.9"
    elif 25 <= bmi < 30:
        bmi_range = "is from 25 to 29.9"
    else:
        bmi_range = "is more than 29.9"

    # Load workout plans from file
    try:
        with open(filename, 'r') as file:
            workout_plans = json.load(file)
    except FileNotFoundError:
        return "Workout plans file not found."

    # Find matching workout plan
    for plan in workout_plans:
        if (plan['Gender'] == gender and
                plan['Age'] == age_range and
                plan['BMI'] == bmi_range and
                plan['Goal'] == goal and
                plan['No_Days'] == days):
            return plan['Workout_Plan']

    return "No matching workout plan found."

@app.route('/workout_plan', methods=['GET'])
def get_workout_plan():
    try:
        gender = request.args.get('gender')
        age = int(request.args.get('age'))
        height = float(request.args.get('height'))
        weight = float(request.args.get('weight'))
        goal = request.args.get('goal')
        days = int(request.args.get('days'))
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid input parameters'}), 400

    workout_plan = retrieve_workout_plan(gender, age, height, weight, goal, days)

    if "No matching workout plan found." in workout_plan or "Age out of range." in workout_plan or "Workout plans file not found." in workout_plan:
        return jsonify({'error': workout_plan}), 404

    return jsonify({'workout_plan': workout_plan})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
