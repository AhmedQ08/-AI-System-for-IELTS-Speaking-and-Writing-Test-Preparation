from openai import OpenAI
client = OpenAI()

def transcribe_audio(audio_file="./static/audio/user_audio.wav"):
    audio_file = open(audio_file, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )
    return transcription.text

if __name__ == "__main__":
    print(transcribe_audio())