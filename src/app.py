from flask import Flask, request, jsonify
import cv2
import mediapipe as mp
import math
import numpy as np

app = Flask(__name__)
app.config["DEBUG"] = True

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


def is_wrist_ergonomic(landmarks, image_width, image_height):
    '''
    Check if the wrist is approximately in the middle of the line from the elbow to the midpoint.

    Parameters:
    - landmarks: A dictionary containing the landmarks of the pose.
    - image_width: The width of the image.
    - image_height: The height of the image.

    Returns:
    - True if the wrist is approximately in the middle of the line from the elbow to the midpoint, False otherwise.
    '''
    # Get the coordinates of the relevant landmarks
    left_elbow = np.array([landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x * image_width, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y * image_height])
    right_elbow = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x * image_width, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y * image_height])
    left_wrist = np.array([landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x * image_width, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y * image_height])
    right_wrist = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x * image_width, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y * image_height])
    left_midpoint = np.array([(landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].x + landmarks[mp_pose.PoseLandmark.LEFT_PINKY.value].x) / 2 * image_width, (landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].y + landmarks[mp_pose.PoseLandmark.LEFT_PINKY.value].y) / 2 * image_height])
    right_midpoint = np.array([(landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value].x + landmarks[mp_pose.PoseLandmark.RIGHT_PINKY.value].x) / 2 * image_width, (landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value].y + landmarks[mp_pose.PoseLandmark.RIGHT_PINKY.value].y) / 2 * image_height])

    # Check if the wrist is approximately in the middle of the line from the elbow to the midpoint
    left_distance = np.linalg.norm(left_wrist - left_elbow) / np.linalg.norm(left_midpoint - left_elbow)
    right_distance = np.linalg.norm(right_wrist - right_elbow) / np.linalg.norm(right_midpoint - right_elbow)

    print(left_distance, right_distance)
    if 0.4 < left_distance < 0.805 and 0.4 < right_distance < 0.805:
        return True
    else:
        return False
    

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Test</h1>
                <p>A flask api implementation   </p>'''


@app.route('/check_ergonomics', methods=['POST'])
def check_ergonomics_api():
    app.logger.info('Received request to /check_ergonomics')
    data = request.files['image'].read()
    npimg = np.frombuffer(data, np.uint8)
    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    

    with mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5, model_complexity=2) as pose:
        results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    app.logger.info('Successfully processed request to /check_ergonomics')
    
    # Get the image width and height
    image_height, image_width, _ = frame.shape

    if results.pose_landmarks:
        is_ergonomic = is_wrist_ergonomic(results.pose_landmarks.landmark, image_width, image_height)
    else:
        is_ergonomic = None

    landmarks = [{'name': landmark_name, 'x': landmark.x, 'y': landmark.y, 'z': landmark.z} 
                     for landmark, landmark_name in zip(results.pose_landmarks.landmark, mp_pose.PoseLandmark)]

    return jsonify({'is_ergonomic': is_ergonomic, 'landmarks': landmarks})


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=5000)
