from flask import Flask, render_template, Response, jsonify
import cv2
from emotion_model import predict_emotion  # Import for the emotion detection function
from spotify_utils import get_recommendations  # Import your recommendation logic
import logging
from threading import Lock

app = Flask(__name__)

# Initialize the webcam
video_capture = cv2.VideoCapture(0)

# Global variables for emotion detection
detected_emotion = "Waiting..."
emotion_lock = Lock()  # Lock to manage threading issues with global variables

# Setup logging
logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    return render_template('index.html')
def gen_frames():
    global detected_emotion
    while True:
        success, frame = video_capture.read()
        if not success:
            print("[Error] Failed to read frame from webcam.")
            break

        # Debugging: Ensure the frame is being processed
        print("[Debug] Capturing frame for emotion prediction...")

        # Predict the emotion
        emotion = predict_emotion(frame)
        print(f"[Debug] Predicted Emotion: {emotion}")  # Log predictions

        # Update the detected emotion safely
        with emotion_lock:
            detected_emotion = emotion
        
        # Debugging: Confirm detected_emotion is updated
        print(f"[Debug] Updated detected_emotion: {detected_emotion}")

        # Overlay the emotion on the frame
        cv2.putText(frame, f"Emotion: {detected_emotion}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Convert frame to JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            print("[Error] Failed to encode frame.")
            continue

        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/recommend', methods=['GET'])
def recommend():
    global detected_emotion

    with emotion_lock:
        current_emotion = detected_emotion

    print(f"[Debug] Current Emotion in /recommend: {current_emotion}")

    if current_emotion not in ["Waiting...", "Error"]:
        recommendations = get_recommendations(current_emotion)
        print(f"[Debug] Recommendations for {current_emotion}: {recommendations}")
        return jsonify({"emotion": current_emotion, "recommendations": recommendations})
    else:
        print(f"[Debug] Emotion not ready: {current_emotion}")
        return jsonify({"message": "Emotion not detected yet. Please wait."}), 400



if __name__ == '__main__':
    app.run(debug=True)
