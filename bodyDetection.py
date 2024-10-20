import cv2
import mediapipe as mp
import time

class PoseDetector:
    def __init__(self, detection_conf=0.8, tracking_conf=0.8):
        self.ctime = 0
        self.ptime = 0
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(min_detection_confidence=detection_conf, min_tracking_confidence=tracking_conf)
        self.mpDraw = mp.solutions.drawing_utils

    def get_frame(self, frame):
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(imgRGB)
        return frame, results

    def draw_landmarks(self, frame, results):
        if results.pose_landmarks:
            self.mpDraw.draw_landmarks(frame, results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)

    def show_fps(self, frame):
        self.ctime = time.time()
        fps = 1 / (self.ctime - self.ptime)
        self.ptime = self.ctime
        frame = cv2.putText(frame, f"{int(fps)} fps", (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
        return frame