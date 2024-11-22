import numpy as np
import cv2
from tensorflow.keras.models import load_model
import gdown


# Using --fuzzy to handle Drive URLs more flexibly
url = 'https://drive.google.com/file/d/1q-C6W573bSLkSt-uq5yiFYf1hlzSllPu/view?usp=drive_link'
output = 'model_file_30epochs.h5'
gdown.download(url, output, quiet=False, fuzzy=True)


# Load the trained model
model = load_model("model_file_30epochs.h5")

# Emotion labels
EMOTION_LABELS = ["Angry", "Disgusted", "Fear", "Happy", "Sad", "Surprise", "Neutral"]

def preprocess_frame(frame):
    """
    Preprocess the input frame for the emotion detection model.
    Converts the frame to grayscale, resizes it to 48x48, and normalizes it.
    """
    try:
        # Convert to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Resize to 48x48
        resized_frame = cv2.resize(gray_frame, (48, 48))
        # Normalize pixel values
        normalized_frame = resized_frame / 255.0
        # Add batch and channel dimensions
        return np.expand_dims(normalized_frame, axis=(0, -1))  # Shape: (1, 48, 48, 1)
    except Exception as e:
        print(f"[Error] Preprocessing failed: {e}")
        return None

def predict_emotion(frame):
    """
    Predict the emotion from a given frame.
    """
    try:
        # Preprocess the frame
        preprocessed_frame = preprocess_frame(frame)
        if preprocessed_frame is None:
            return "Waiting..."

        # Debug: Log frame shape
        print(f"[Debug] Preprocessed Frame Shape: {preprocessed_frame.shape}")
        
        # Predict emotion
        predictions = model.predict(preprocessed_frame)

        # Debug: Log predictions
        print(f"[Debug] Model Predictions: {predictions}")

        # Get emotion with the highest probability
        emotion_index = np.argmax(predictions)
        return EMOTION_LABELS[emotion_index]
    except Exception as e:
        print(f"[Error] Prediction failed: {e}")
        return "Error"
