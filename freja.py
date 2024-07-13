import cv2
import base64
import openai
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

openai.api_key = ''
https://onetimesecret.com/secret/7ki2wu2qwuescfdj4e3wot0kd88ppqb
def capture_image():
    # Initialize webcam
    cap = cv2.VideoCapture(0)

    # Capture frame-by-frame
    ret, frame = cap.read()

    ret, buffer = cv2.imencode('.jpg', frame)
    base64_image = base64.b64encode(buffer)
    
    cap.release()
    return base64_image

def analyze_image_and_generate_prompt(base64_image):
    # Create the prompt with the image for analysis
    prompt = ChatPromptTemplate.from_template(
        "Analyze the following image and describe what is happening from the dogs perspective, if there is no dog say Freja is not here: {image}"
    )
    
    # Send the prompt to OpenAI for analysis
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=prompt.format(image=base64_image),
        max_tokens=150
    )

    # Extract the analysis from the response
    analysis = response.choices[0].text.strip()

    # Create a second prompt pretending to be the dog in the image
    dog_prompt = ChatPromptTemplate.from_template(
        f"You are the dog Freja in the image, act like her and say what she is thinking. If she is not there return with no response {analysis}"
    )
    
    return dog_prompt


def freja_response(dog_prompt):
    # Send the prompt to OpenAI for response
    freja_thoughts_response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=dog_prompt.format(image=base64_image),
            max_tokens=150
        )

    freja_thoughts = freja_thoughts_response.choices[0].text.strip()

    return freja_thoughts


    # Loop to capture image, analyze, and print result
while True:
    base64_image = capture_image()
    dog_prompt = analyze_image_and_generate_prompt(base64_image)
    freja_thoughts = freja_response(dog_prompt)
    
    print(freja_thoughts)
    # Add a break condition if needed, for example, press 'q' to quit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

