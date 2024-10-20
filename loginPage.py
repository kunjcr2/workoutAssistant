from flask import Flask, request, render_template, redirect, url_for, Response
from loginGPT import GPT2
import ast
import cv2
from bodyDetection import PoseDetector
import math
import json
import time

app = Flask(__name__)
gpt = GPT2()
detector = PoseDetector()
cap = cv2.VideoCapture(0)

currEx = ""
target_reps = 0
counter = 0
exercise_list = []
current_ex_index = 0
filtered_exercises = []
name1 = "" 
exercise_landmarks = {
        "Bicep Curls": [(12, 14, 16)],
        "Squats": [(24, 26, 28)],
        "Push Ups": [(12, 14, 16)],
        "Lunges": [(24, 26, 28)],
        "Shoulder Presses": [(11, 13, 15)],
        "Deadlifts": [(24, 26, 28)],
        "Plank": [(11, 13, 15)],
        "Mountain Climbers": [(12, 14, 16), (24, 26, 28)],
        "Jumping Jacks": [(12, 14, 16), (24, 26, 28)],
        "Burpees": [(12, 14, 16), (24, 26, 28)],
        "Side Plank": [(11, 13, 15), (23, 25, 27)],
        "Tricep Dips": [(12, 14, 16)],
        "Bent Over Row": [(12, 14, 16)],
        "Glute Bridges": [(24, 26, 28)],
        "High Knees": [(24, 26, 28)],
        "Crunches": [(12, 24, 26)],
        "Leg Raises": [(24, 26, 28)],
        "Side Lunges": [(24, 26, 28)],
        "Reverse Lunges": [(24, 26, 28)],
        "Jump Squats": [(24, 26, 28)],
        "Front Raises": [(12, 14, 16)],
        "Calf Raises": [(24, 26, 28)],
        "Russian Twists": [(12, 24, 26)],
        "Leg Press": [(24, 26, 28)],
        "Leg Extension": [(24, 26, 28)],
        "Bicycle Crunches": [(12, 14, 16), (24, 26, 28)],
        "Plank To Push-Ups": [(11, 13, 15), (12, 14, 16)],
        "Side Plank To Push-Ups": [(11, 13, 15), (12, 14, 16)],
        "Dumbbell Shoulder Press": [(11, 13, 15)],
        "Dumbbell Chest Press": [(12, 14, 16)],
        "Pull Ups": [(12, 14, 16)],
        "Bench Press": [(12, 14, 16)],
        "Rowing Machine": [(12, 14, 16), (24, 26, 28)],
        "Kettlebell Swings": [(12, 14, 16), (24, 26, 28)],
        "Box Jumps": [(24, 26, 28)],
        "Step Ups": [(24, 26, 28)],
        "Lat Pulldown": [(12, 14, 16)],
        "Clapping Push Ups": [(12, 14, 16)],
        "Medicine Ball Slams": [(12, 14, 16)],
        "Seated Shoulder Press": [(11, 13, 15)],
    }
    

def calAngle(pointA, pointB, pointC):
    AB = [pointA[0] - pointB[0], pointA[1] - pointB[1]]
    BC = [pointC[0] - pointB[0], pointC[1] - pointB[1]]

    dotProduct = AB[0] * BC[0] + AB[1] * BC[1]
    magnitudeAB = math.sqrt(AB[0] ** 2 + AB[1] ** 2)
    magnitudeBC = math.sqrt(BC[0] ** 2 + BC[1] ** 2)

    angleRad = math.acos(dotProduct / (magnitudeAB * magnitudeBC))
    return math.degrees(angleRad)

def update_counter(pointA, pointB, pointC):
    global counter
    angle = calAngle(pointA, pointB, pointC)

    if angle > 160:  
        curl_stage = "down"
    elif angle < 30 and curl_stage == "down": 
        curl_stage = "up"
        counter += 1
        print(f"Counter updated to {counter}")

def get_exercise(exercise):
    global exercises
    exercises = gpt.chat(exercise)
    print(exercises)
    exercises = ast.literal_eval(exercises)
    
    return exercises

@app.route("/", methods=["GET", "POST"])
def login():
    global name1
    if request.method == "POST":
        name1 = request.form.get("name")
        weight1 = request.form.get("weight")
        height1 = request.form.get("height")
        age1 = request.form.get("age")
        bmi1 = round(float(weight1) / (float(height1) ** 2), 2)
        return redirect(url_for("exercise"))
    return render_template("login.html")

@app.route("/exercise", methods=["GET", "POST"])
def exercise():
    global currEx, counter, target_reps, filtered_exercises, name1
    if request.method == "POST":
        exercise = request.form.get("exercise")
        exercises = get_exercise(exercise)
        if exercises:
            currEx, target_reps = exercises[0][0], exercises[0][1]
        return render_template("exercise.html", name=name1, exercises=exercises)
    return render_template("exercise.html", exercises=[], name=name1)

@app.route("/confirm", methods=["GET", "POST"])
def confirm():
    return redirect(url_for("video_feed"))

@app.route("/video_feed", methods=["GET", "POST"])
def video_feed():
    return Response(generate_video(), mimetype="multipart/x-mixed-replace; boundary=frame")

curl_stage = "down"  # Declare curl_stage globally

def update_counter(pointA, pointB, pointC):
    global counter, curl_stage  # Add curl_stage here to make it global
    angle = calAngle(pointA, pointB, pointC)

    # Update the curl stage based on angle
    if angle > 160:  
        curl_stage = "down"
    elif angle < 30 and curl_stage == "down": 
        curl_stage = "up"
        counter += 1
        print(f"Counter updated to {counter}")  # Print to console for debugging

# In generate_video(), ensure exercises are initialized
def generate_video():
    global counter, currEx, target_reps, exercises, exercise_landmarks
    exercise_index = 0
    if not exercises:
        print("No exercises available")
        return  # Add this to avoid errors if exercises are empty

    current_reps = exercises[exercise_index][1] 
    required_landmarks = exercise_landmarks[currEx]

    while True:
        success, frame = cap.read()
        if not success:
            time.sleep(0.1)
            continue

        frame, results = detector.get_frame(frame)
        detector.draw_landmarks(frame, results)
        frame = detector.show_fps(frame)

        if results.pose_landmarks:
            if required_landmarks:
                try:
                    # Extract points using the required landmarks
                    pointA = (results.pose_landmarks.landmark[required_landmarks[0][0]].x, 
                              results.pose_landmarks.landmark[required_landmarks[0][0]].y)
                    pointB = (results.pose_landmarks.landmark[required_landmarks[0][1]].x, 
                              results.pose_landmarks.landmark[required_landmarks[0][1]].y)
                    pointC = (results.pose_landmarks.landmark[required_landmarks[0][2]].x, 
                              results.pose_landmarks.landmark[required_landmarks[0][2]].y)

                    update_counter(pointA, pointB, pointC)

                    cv2.putText(frame, f"Currently: {currEx}", (10, 100), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                    cv2.putText(frame, f"Counter: {counter}/{target_reps}", (10, 60), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

                    if counter >= target_reps:
                        counter = 0  
                        exercise_index += 1 
                        if exercise_index < len(exercises):
                            currEx = exercises[exercise_index][0] 
                            target_reps = exercises[exercise_index][1] 
                            required_landmarks = exercise_landmarks[currEx] 
                        else:
                            print("All exercises completed.")
                            break 

                except Exception as e:
                    print(f"Error processing landmarks: {e}")  # Debugging
                    time.sleep(0.1)
                    continue

        ret, buffer = cv2.imencode(".jpg", frame)
        frame = buffer.tobytes()

        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

if __name__ == "__main__":
    app.run(debug=True)
