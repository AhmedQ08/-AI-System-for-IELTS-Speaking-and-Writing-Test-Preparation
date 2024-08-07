
import json
mysp=__import__("my-voice-analysis")


def analyze_audio():
    p = "user_audio" 
    c = r"C:\Users\Ahmed Qamar\Desktop\flask\static\audio" 
    response = {}

    response['mysppron'] = mysp.mysppron(p, c)
    response['myspsr'] = mysp.myspsr(p, c)

    return response

if __name__ == "__main__":
    result = analyze_audio()
    json_result = json.dumps(result, indent=4)
    print(json_result)