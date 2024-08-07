from openai import OpenAI
import os
# Initialization
client = OpenAI(
    api_key=os.environ['openai_api_key']
)

def generate_audio(text):
    response = client.audio.speech.create(
        model="tts-1-hd",
        voice="echo",
        input=text,
    )

    response.stream_to_file("./static/audio/statement.wav")

if __name__ == "__main__":
    # Example usage
    text = "Hello! This is a test."
    generate_audio(text)