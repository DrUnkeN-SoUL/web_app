from keras.models import model_from_json
from flask import Flask, render_template, Response
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

# Global flag for camera start
camera_started = False
camera = None


def capture_by_frames():
    global camera
    global camera_started

    if not camera_started:
        return

    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        detector = cv2.CascadeClassifier('Haarcascades/haarcascade_frontalface_default.xml')
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

        # Processing obtained faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
            roi_gray_frame = gray_frame[y:y + h, x:x + w]
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray_frame, (48, 48)), -1), 0)

            # predict the emotions
            emotion_prediction = emotion_model.predict(cropped_img)
            maxindex = int(np.argmax(emotion_prediction))
            emotion = emotion_dict[maxindex]
            confidence = float(emotion_prediction[0, maxindex]) * 100
            conf = "{:.2f}".format(confidence)
            text = emotion + " - " + conf
            cv2.putText(frame, text, (x + 5, y - 20), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 0, 0), 1, cv2.LINE_AA)

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

    if not camera_started:
        camera = cv2.VideoCapture(0)
        camera_started = True

    return render_template('index.html')


@app.route('/stop', methods=['POST'])
def stop():
    global camera_started
    global camera

    if camera is not None and camera.isOpened():
        camera.release()
    camera_started = False

    return render_template('stop.html')


@app.route('/video_capture')
def video_capture():
    return Response(capture_by_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=8000)
