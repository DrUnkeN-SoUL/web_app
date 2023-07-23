from keras.models import model_from_json
from flask import Flask, render_template, Response, jsonify
from collections import defaultdict
import time
import cv2
import numpy as np

app = Flask(__name__)

emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}
json_file = open('model/emotion_model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
emotion_model = model_from_json(loaded_model_json)
# load weights into the new model
emotion_model.load_weights("model/emotion_model.h5")
print("Loaded model from disk")

# Global variables
camera_started = False
camera = None
emotion_count = defaultdict(int)
total_faces_count = 0
total_emotions_identified_count = 0
emotion_counts_db = {
    "Angry": 0,
    "Disgusted": 0,
    "Fearful": 0,
    "Happy": 0,
    "Neutral": 0,
    "Sad": 0,
    "Surprised": 0
}


def capture_by_frames():
    global camera
    global camera_started
    global emotion_count
    global total_faces_count
    global total_emotions_identified_count
    global emotion_counts_db

    if not camera_started:
        return

    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            emotion_count = defaultdict(lambda: "No face identified")
            break
        detector = cv2.CascadeClassifier('Haarcascades/haarcascade_frontalface_default.xml')
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)
        emotion_counts = defaultdict(int)

        # Processing obtained faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x - 20, y - 50), (x + w + 20, y + h + 10), (0, 255, 0), 4)
            roi_gray_frame = gray_frame[y:y + h, x:x + w]
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray_frame, (48, 48)), -1), 0)
            total_faces_count += 1
            # predict the emotions
            try:
                emotion_prediction = emotion_model.predict(cropped_img)
                maxindex = int(np.argmax(emotion_prediction))
                emotion = emotion_dict[maxindex]
                emotion_counts[emotion] += 1
                confidence = float(emotion_prediction[0, maxindex]) * 100
                conf = "{:.2f}".format(confidence)
                text = emotion + " - " + conf
                cv2.putText(frame, text, (x + 5, y - 20),cv2.FONT_HERSHEY_DUPLEX, 0.7 , (255, 0, 0), 1, cv2.LINE_AA)
                emotion_counts_db[emotion] += 1
                total_emotions_identified_count += 1

            except:
                print("no face found")

        # Update the emotion_count with the latest counts
        emotion_count = {emotion: count for emotion, count in emotion_counts.items()}

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start', methods=['POST'])
def start():
    global camera_started
    global camera
    global emotion_count

    session_id = None  # Declare session_id here to ensure availability in the entire function scope

    if not camera_started:
        camera = cv2.VideoCapture(0)
        camera_started = True
        # Set emotion_count to an empty dictionary when the camera starts
        emotion_count = defaultdict(int)

    # Pass the session_id to the frontend
    return render_template('index.html')


@app.route('/emotion_counts', methods=['GET'])
def get_emotion_counts():
    global emotion_count
    global total_faces_count
    global total_emotions_identified_count
    global emotion_counts_db

    # Create a dictionary to hold all the data to be sent to the frontend
    response_data = {
        "emotion_count": emotion_count,
        "total_faces_count": total_faces_count,
        "total_emotions_identified_count": total_emotions_identified_count,
        "emotion_counts_db": emotion_counts_db
    }

    # Convert the dictionary to JSON and return it as the response
    return jsonify(response_data)



@app.route('/stop', methods=['POST'])
def stop():
    global camera_started
    global camera
    global emotion_count

    if camera is not None and camera.isOpened():
        camera.release()
    camera_started = False
    # Introduce a 1-second delay before resetting emotion_count
    time.sleep(1)
    # Reset emotion_count to "No face identified" for all emotions
    emotion_count = defaultdict(lambda: "No face identified")
    return render_template('index.html')


@app.route('/video_capture')
def video_capture():
    return Response(capture_by_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, port=8000)
