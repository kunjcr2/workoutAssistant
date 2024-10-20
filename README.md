# WORKOUT ASSISTANT

This project is a Python-based web application designed to track and analyze exercise quality through real-time webcam input. Using OpenCV and MediaPipe, the application identifies key body landmarks and evaluates exercise form. Additionally, it fetches exercise routines using the OpenAI API, providing users with interactive and personalized workout suggestions.

# Features
1. Real-time exercise tracking: Uses webcam input and MediaPipe for body landmark detection.
2. Form assessment: Evaluates the quality of exercises based on detected landmarks.
3. Custom exercise routines: Fetches routines from OpenAI API, tailored to the user’s preferences.

# Prerequisites
Before running the application, ensure you have the following installed:
1. Python 3.x
2. Flask
3. OpenCV
4. MediaPipe
5. OpenAI API Key

You can install the necessary Python libraries using the following command:
#bash
pip install -r requirements.txt

# Directory Structure
In order to run the program properly, the following files should be saved in their respective directories:

project-root/
│
├── loginPage.py                # Main application script
├── loginGPT.py
├── bodyDetection.py
├── templates/
│   ├── login.html        # registration webpage
│   └── exercise.html       # exercise selector page
|   └── main.html          # main webpage
├── static/
│   ├── css/
│       └── paper.css    # Styles for the login page
|       └── paper2.css    # Styles for exercise page
└── README.md             # Project documentation (this file)
Make sure that all the files are saved in the correct directory as shown above for the program to work smoothly.

# Running the Application

1.Clone this repository:
# bash
git clone https://github.com/username/repository.git
Navigate to the project directory:

# bash
cd project-root

2. Start the Flask app:
# bash
python app.py
Open your web browser and go to http://127.0.0.1:5000/ to access the application.

# PRIVACY NOTE (IMPORTANT)
Due to privacy reasons, I had to keep the repository private. If you have access to the repository and need any further assistance with setup or running the project, feel free to reach out to me.
