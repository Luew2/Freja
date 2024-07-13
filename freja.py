import cv2
import time
import base64
from openai import OpenAI
import pyttsx3
import re

# Initialize OpenAI client
client = OpenAI(api_key='')
engine = pyttsx3.init()
def capture_image():
    # Initialize webcam
    cap = cv2.VideoCapture(-1)
    
    # Capture multiple frames to ensure a clear image
    for _ in range(10):  # Capture 10 frames
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image")
            cap.release()
            return None
        
        # Display the current frame
        cv2.imshow('Captured Image', frame)
        cv2.waitKey(10)  # This line is necessary to update the imshow window
    
    # Release the camera
    cap.release()
    
    # Display the final captured frame
    cv2.imshow('Final Captured Image', frame)
    cv2.waitKey(10)
    
    # Encode the image to base64
    ret, buffer = cv2.imencode('.jpg', frame)
    base64_image = base64.b64encode(buffer).decode('utf-8')
    return base64_image

def analyze_image(base64_image):
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Analyze the following image that contains a dog. Any dog you see is named Freja and is. Then respond as if you were Freja and her intenal thoughts. If Freja isn't there respond with a descrition of what you see."},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                        },
                    ],
                }
            ],
            max_tokens=300,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

from gtts import gTTS
import os

def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("output.mp3")
    os.system("mpg321 output.mp3")  # You might need to install mpg321 or use another audio player

def process_and_speak_response(response):    
    # Extract the content within quotes
    quoted_text = re.findall(r'["""]([^"""]*)["""]', response)
    
    if quoted_text:
        freja_thoughts = quoted_text[0]
        print("Freja's thoughts:", freja_thoughts)
        speak(freja_thoughts)
    else:
        print("No quoted text found in the response.")
        speak(response)

# Loop to capture image, analyze, and print result
for _ in range(1):
    base64_image = capture_image()
    if base64_image:
        analysis = analyze_image(base64_image)
        if analysis:
            process_and_speak_response(analysis)
        else:
            print("Failed to analyze the image.")
    else:
        print("Failed to capture the image.")
    
    # Add a break condition if needed, for example, press 'q' to quit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()