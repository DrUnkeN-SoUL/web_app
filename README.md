# Emotion Detection App
The Emotion Detection App is a real-time computer vision application that uses deep learning to detect emotions from live webcam streams or video files. The app employs a pre-trained deep learning model to recognize human emotions, such as anger, disgust, fear, happiness, neutrality, sadness, and surprise.

## Overview
The Emotion Detection App uses the power of OpenCV for image processing and face detection. It leverages a Haar Cascade classifier to identify human faces in each frame of the video feed. After detecting the faces, the app processes them to predict the associated emotion using a pre-trained deep learning model.

## Features
-Real-time emotion detection from live webcam feeds.
-Emotion recognition from video files.
-Accurate classification of emotions into seven categories: Angry, Disgusted, Fearful, Happy, Neutral, Sad, and Surprised.
-User-friendly interface to visualize the detected emotions.


## Requirements
To run the Emotion Detection App, you need the following dependencies:

-Python 3.x
-OpenCV
-NumPy
-Keras


## Installation
Clone this repository to your local machine.

```bash
git clone https://github.com/DrUnkeN-SoUL/web_app.git
cd web_app
```
> 💡Recommended :Create and activate virtual environment for devolopment                   
to crate virtualenv:                            
`pip install virtualenv`                     
`virtualenv env` #you can use any name for env                                                            
`source env/bin/activate`                         



Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

## Run the app:

```python emotion_detection_app.py```

## How to Use
Ensure your webcam is connected and working (if using the live webcam feed).
Launch the app by executing the script.
A link will we be available in the terminal (connect to localhost:8000).
Faces will be highlighted with a bounding box, and the corresponding emotion will be displayed on each detected face.

# License
This project is licensed under the MIT License.
