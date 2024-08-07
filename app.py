from flask import Flask, render_template, request, url_for, redirect, flash, jsonify, send_from_directory,send_file
from flask_pymongo import PyMongo
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
from datetime import *
import os
from bson import ObjectId
from datetime import datetime
from flask_mail import Mail, Message
from utils import *
from ahmed import *
from introduction_interview import *
from discussion_interview import *
from text_to_speech import generate_audio
from speech_to_text import transcribe_audio
from task_2 import *
from record import *
from flask_cors import CORS
import json
from flask_login import *
from werkzeug.utils import secure_filename
from voice_analysis import *
from PIL import *
import io
from bson.binary import Binary
import io
from flask import send_file
from threading import Thread
from subprocess import Popen



app = Flask(__name__)

app.secret_key = os.urandom(24)

load_dotenv(find_dotenv())
password = os.environ.get("MONGODB_PWD")
connection_string = f"mongodb+srv://ahmed:{password}@cluster0.0veqxyb.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(connection_string)


try:
    client.admin.command('ismaster')
    print("Connect to MongoDB successfully")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")



db=client.flask_login
collection = db.users
task_1_collection = db.task_1_response
task_2_collection = db.task_2_response
intro_interview_collection = db.intro_interview_response
discuss_interview_collection = db.discuss_interview_response


##############################################

emotion_detection_process = None

def start_emotion_detection():
    global emotion_detection_process
    emotion_detection_process = Popen(['python', 'emotion.py'])

def stop_emotion_detection():
    global emotion_detection_process
    if emotion_detection_process:
        emotion_detection_process.terminate()
@app.route('/start_emotion_detection', methods=['POST'])
def start_emotion_detection_route():
    start_emotion_detection()
    return "Emotion detection started"

@app.route('/stop_emotion_detection', methods=['POST'])
def stop_emotion_detection_route():
    stop_emotion_detection()
    return "Emotion detection stopped"



##############################################


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/start_recording', methods=['POST'])
def start_recording_route():
    start_recording()
    return "Recording started"

@app.route('/stop_recording', methods=['POST'])
def stop_recording_route():
    stop_recording()
    save_audio()
    transcribed_text = transcribe_audio()
    session['transcribed_text'] = transcribed_text
    return "Recording stopped and audio file is saved"



    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = db.users
        login_user = users.find_one({'email': request.form['email']})

        if login_user:
            if check_password_hash(login_user['password'], request.form['password']):
                session['email'] = request.form['email']
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid password. Please try again.', 'danger')
                return redirect(url_for('login'))
        else:
            flash('User not found. Please register.', 'danger')
            return redirect(url_for('register'))

    return render_template('login.html')



@app.route('/logout')
def logout():
    session.pop('email',None)
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = db.users
        existing_user = users.find_one({'email': request.form['email']})

        if existing_user is None:
            password = request.form['password']
            if len(password) >= 8:
                hash_password = generate_password_hash(password, method='pbkdf2:sha256')
                user_data = {
                    'email': request.form['email'],
                    'username': request.form['username'],
                    'password': hash_password,
                }
                
                users.insert_one(user_data)
                session['email'] = request.form['email']
                return redirect(url_for('dashboard'))
            else:
                flash('Password must be 8 characters or more.', 'warning')
                return redirect(url_for('register'))
        else:
            flash('Email already exists, please login instead!', 'warning')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        
        user_data = db.users.find_one({'email': session['email']})
        
        return render_template('dashboard.html', email=session['email'], user_data=user_data)
    return redirect(url_for('login'))
# 

@app.route('/quicktestboard', methods=['GET', 'POST'])
def quicktestboard():
    if request.method == 'POST':
        ans = request.form['ans']
        prev_response = request.form['prev_response']
        
        system_prompt_message = generate_system_prompt_message_ans()
        user_prompt_message = generate_user_prompt_message_ans(ans, prev_response)
        response = get_response_type_text(system_prompt_message, user_prompt_message)
        inner_json = response.choices[0].message.content
        json_response = json.loads(inner_json)

        
        user_email = session.get('email')
        json_response['user_email'] = user_email

        
        task_1_collection.insert_one(json_response)

        return render_template('writtentest.html')

    system_prompt_message = generate_system_prompt_message_questions()
    user_prompt_message = generate_user_prompt_message_questions()
    response = get_response_type_text(system_prompt_message, user_prompt_message)
    inner_json = response.choices[0].message.content
    json_response = json.loads(inner_json)

    if 'email' in session:
        return render_template('quicktestboard.html', email=session['email'], response=json_response)
    return redirect(url_for('login'))

@app.route('/task_2', methods=['GET', 'POST'])
def task_2():
    if request.method == 'POST':
        ans_task_2 = request.form['ans_task_2']
        prev_response_task_2 = request.form['prev_response_task_2']
        
        system_prompt_message_task_2 = generate_system_prompt_message_ans_task_2()
        user_prompt_message_task_2 = generate_user_prompt_message_ans_task_2(ans_task_2, prev_response_task_2)
        response = get_response_type_text(system_prompt_message_task_2, user_prompt_message_task_2)
        print(response)
        inner_json = response.choices[0].message.content
        json_response = json.loads(inner_json)

        
        user_email = session.get('email')
        json_response['user_email'] = user_email

        
        task_2_collection.insert_one(json_response)

        return render_template('writtentest.html')
        
    system_prompt_message_task_2 = generate_system_prompt_message_questions_task_2()
    user_prompt_message_task_2 = generate_user_prompt_message_questions_task_2()
    response = get_response_type_text(system_prompt_message_task_2, user_prompt_message_task_2)
    inner_json = response.choices[0].message.content
    json_response = json.loads(inner_json)

    if 'email' in session:
        return render_template('task_2.html', email=session['email'], response=json_response)
    return redirect(url_for('login'))


@app.route('/introductionInterview', methods=['GET', 'POST'])
def intro():
    if request.method == 'POST':
        
        if os.path.exists("./static/audio/user_audio.wav"):
            
            ans_intro = transcribe_audio("./static/audio/user_audio.wav")
        else:
            ans_intro = "No audio recorded"

        prev_response_intro = ans_intro
        
        system_prompt_message_intro = generate_system_prompt_message_ans_intro()
        user_prompt_message_intro = generate_user_prompt_message_ans_intro(ans_intro, prev_response_intro )
        response = get_response_type_text(system_prompt_message_intro, user_prompt_message_intro)
        inner_json = response.choices[0].message.content
        json_response = json.loads(inner_json)



        user_email = session.get('email')
        json_response['user_email'] = user_email

        voice_analysis_response = analyze_audio()
        json_response['voice_analysis'] = voice_analysis_response
        intro_interview_collection.insert_one(json_response)
        print(json_response)
        return render_template('interview.html')
    
    system_prompt_message_intro = generate_system_prompt_message_questions_intro()
    user_prompt_message_intro = generate_user_prompt_message_questions_intro()
    response = get_response_type_text(system_prompt_message_intro, user_prompt_message_intro)
    inner_json = response.choices[0].message.content
    json_response = json.loads(inner_json)

    if 'email' in session:
            
            response_statement = json_response.get('statement', '')

            generate_audio(response_statement)

            return render_template('introductionInterview.html', email=session['email'], response=json_response)
        
    return redirect(url_for('login'))




@app.route('/discussioninterview', methods=['GET', 'POST'])
def discuss():
    if request.method == 'POST':
       
        if os.path.exists("./static/audio/user_audio.wav"):

            ans_discuss = transcribe_audio("./static/audio/user_audio.wav")
        else:
            ans_discuss = "No audio recorded"

        prev_response_discuss = ans_discuss
        
        system_prompt_message_discuss = generate_system_prompt_message_ans_discuss()
        user_prompt_message_discuss = generate_user_prompt_message_ans_discuss(ans_discuss, prev_response_discuss)
        response = get_response_type_text(system_prompt_message_discuss, user_prompt_message_discuss)
        inner_json = response.choices[0].message.content
        json_response = json.loads(inner_json)

        
        user_email = session.get('email')
        json_response['user_email'] = user_email

        discuss_interview_collection.insert_one(json_response)     

        return render_template('interview.html')
        
    system_prompt_message_discuss = generate_system_prompt_message_questions_discuss()
    user_prompt_message_discuss = generate_user_prompt_message_questions_discuss()
    response = get_response_type_text(system_prompt_message_discuss, user_prompt_message_discuss)
    inner_json = response.choices[0].message.content
    json_response = json.loads(inner_json)

    if 'email' in session:
           
            response_statement = json_response.get('statement', '')

            
            generate_audio(response_statement)

            return render_template('discussioninterview.html', email=session['email'], response=json_response)
        
    return redirect(url_for('login'))





@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        users = db.users
        existing_user = users.find_one({'email': session['email']})

        if existing_user:
            existing_user['username'] = request.form.get('username', existing_user['username'])
            
            new_password = request.form.get('password')
            if new_password:
                existing_user['password'] = generate_password_hash(new_password, method='pbkdf2:sha256')

            # Handle profile picture upload
            profile_picture = request.files.get('profile_picture')
            if profile_picture and profile_picture.filename != '':
                image_binary = Binary(profile_picture.read())
                existing_user['profile_picture'] = image_binary

            users.update_one({'_id': existing_user['_id']}, {'$set': existing_user})

        return redirect(url_for('settings'))

    current_user_data = db.users.find_one({'email': session['email']})
    return render_template('settings.html', current_user=current_user_data)

@app.route('/profile_picture/<user_id>')
def profile_picture(user_id):
    user = db.users.find_one({'_id': ObjectId(user_id)})
    if user and 'profile_picture' in user:
        return send_file(io.BytesIO(user['profile_picture']), mimetype='image/jpeg')
    else:
        return redirect(url_for('static', filename='images/user.png'))




@app.route('/writtentest_report', methods=['GET'])
def writtentest_report():
  
    user_email = session.get('email')

    pipeline_task_1 = [
        {'$match': {'user_email': user_email}},
        {'$project': {
            'datetime': {'$dateToString': {'format': '%Y-%m-%d %H:%M:%S', 'date': '$timestamp'}},
            'response': '$$ROOT'
        }},
        {'$group': {
            '_id': {'date': {'$substrCP': ['$datetime', 0, 10]}, 'time': {'$substrCP': ['$datetime', 11, 8]}},
            'responses': {'$push': '$response'}
        }}
    ]

    grouped_responses_task_1 = task_1_collection.aggregate(pipeline_task_1)


    pipeline_task_2 = [
        {'$match': {'user_email': user_email}},
        {'$project': {
            'datetime': {'$dateToString': {'format': '%Y-%m-%d %H:%M:%S', 'date': '$timestamp'}},
            'response': '$$ROOT'
        }},
        {'$group': {
            '_id': {'date': {'$substrCP': ['$datetime', 0, 10]}, 'time': {'$substrCP': ['$datetime', 11, 8]}},
            'responses': {'$push': '$response'}
        }}
    ]

    grouped_responses_task_2 = task_2_collection.aggregate(pipeline_task_2)

    if 'email' in session:
        return render_template('writtentest_report.html', email=session['email'], grouped_responses_task_1=grouped_responses_task_1, grouped_responses_task_2=grouped_responses_task_2)
    else:
        return redirect(url_for('login'))
    

@app.route('/interview_report', methods=['GET'])
def interview_report():
  
    user_email = session.get('email')

    pipeline_intro = [
        {'$match': {'user_email': user_email}},
        {'$project': {
            'datetime': {'$dateToString': {'format': '%Y-%m-%d %H:%M:%S', 'date': '$timestamp'}},
            'response': '$$ROOT'
        }},
        {'$group': {
            '_id': {'date': {'$substrCP': ['$datetime', 0, 10]}, 'time': {'$substrCP': ['$datetime', 11, 8]}},
            'responses': {'$push': '$response'}
        }}
    ]

    grouped_responses_intro = intro_interview_collection.aggregate(pipeline_intro)


    pipeline_discuss = [
        {'$match': {'user_email': user_email}},
        {'$project': {
            'datetime': {'$dateToString': {'format': '%Y-%m-%d %H:%M:%S', 'date': '$timestamp'}},
            'response': '$$ROOT'
        }},
        {'$group': {
            '_id': {'date': {'$substrCP': ['$datetime', 0, 10]}, 'time': {'$substrCP': ['$datetime', 11, 8]}},
            'responses': {'$push': '$response'}
        }}
    ]

    grouped_responses_discuss = discuss_interview_collection.aggregate(pipeline_discuss)

    if 'email' in session:
        return render_template('interview_report.html', email=session['email'], grouped_responses_intro=grouped_responses_intro, grouped_responses_discuss=grouped_responses_discuss)
    else:
        return redirect(url_for('login'))



@app.route('/test_report_detail_task_1/<response_id>')
def test_report_detail_task_1(response_id):
    response_data = task_1_collection.find_one({'_id': ObjectId(response_id)})
    if response_data:
        return render_template('test_report_detail.html', response=response_data)
    else:
        return 'Response not found'

@app.route('/test_report_detail_task_2/<response_id>')
def test_report_detail_task_2(response_id):
    response_data = task_2_collection.find_one({'_id': ObjectId(response_id)})
    if response_data:
        return render_template('test_report_detail.html', response=response_data)
    else:
        return 'Response not found'

@app.route('/delete_response_task_1/<response_id>', methods=['POST'])
def delete_response_task_1(response_id):
    if request.method == 'POST':
        result = task_1_collection.delete_one({'_id': ObjectId(response_id)})
        if result.deleted_count > 0:
            return redirect(url_for('writtentest_report'))
        else:
            return 'Response not found or already deleted'

@app.route('/delete_response_task_2/<response_id>', methods=['POST'])
def delete_response_task_2(response_id):
    if request.method == 'POST':
        result = task_2_collection.delete_one({'_id': ObjectId(response_id)})
        if result.deleted_count > 0:
            return redirect(url_for('writtentest_report'))
        else:
            return 'Response not found or already deleted'



@app.route('/interview_report_detail_intro/<response_id>')
def interview_report_detail_intro(response_id):
    response_data = intro_interview_collection.find_one({'_id': ObjectId(response_id)})
    if response_data:
        return render_template('interview_report_detail.html', response=response_data)
    else:
        return 'Response not found'

@app.route('/interview_report_detail_discuss/<response_id>')
def interview_report_detail_discuss(response_id):
    response_data = discuss_interview_collection.find_one({'_id': ObjectId(response_id)})
    if response_data:
        return render_template('interview_report_detail.html', response=response_data)
    else:
        return 'Response not found'


@app.route('/delete_response_intro/<response_id>', methods=['POST'])
def delete_response_intro(response_id):
    if request.method == 'POST':
        result = intro_interview_collection.delete_one({'_id': ObjectId(response_id)})
        if result.deleted_count > 0:
            return redirect(url_for('interview_report'))
        else:
            return 'Response not found or already deleted'

@app.route('/delete_response_discuss/<response_id>', methods=['POST'])
def delete_response_discuss(response_id):
    if request.method == 'POST':
        result = discuss_interview_collection.delete_one({'_id': ObjectId(response_id)})
        if result.deleted_count > 0:
            return redirect(url_for('interview_report'))
        else:
            return 'Response not found or already deleted'


@app.route('/progressreport')
def progressreport():

    if 'email' in session:
        return render_template('progressreport.html', email=session['email'],)
    return render_template(url_for('login'))

@app.route('/writtentest')
def writtentest():
    if 'email' in session:
        return render_template('writtentest.html', email=session['email'])
    return render_template(url_for('login'))


@app.route('/testreports')
def testreports():
    if 'email' in session:
        return render_template('testreports.html', email=session['email'])
    return render_template(url_for('login'))


@app.route('/interview')
def interview():
    if 'email' in session:
        return render_template('interview.html', email=session['email'])
    return render_template(url_for('login'))

@app.route('/introductionInterview')
def introductionInterview():
    if 'email' in session:
        return render_template('introductionInterview.html', email=session['email'])
    return render_template(url_for('login'))

@app.route('/individualinterview')
def individualinterview():
    if 'email' in session:
        return render_template('individualinterview.html', email=session['email'])
    return render_template(url_for('login'))

@app.route('/discussioninterview')
def discussioninterview():
    if 'email' in session:
        return render_template('discussioninterview.html', email=session['email'])
    return render_template(url_for('login'))

app.config['MAIL_SERVER'] = 'smtp.gmail.com'  
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'ahmedqamar3333@gmail.com'  
app.config['MAIL_PASSWORD'] = 'kqbr mtsv ffxp djif'  

mail = Mail(app)

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    if request.method == 'POST':
      
        name = request.form['name']
        feedback = request.form['feedback']

        
        msg = Message('Feedback Received', sender='ahmedqamar3333@gmail.com', recipients=['ahmedqamar3333@gmail.com'])
        msg.body = f"Name: {name}\nFeedback: {feedback}"
        
        try:
            mail.send(msg)
            flash('Feedback submitted successfully! We will get back to you soon.', 'success')
        except Exception as e:
            print(f"Error sending email: {e}")
            flash('An error occurred while submitting feedback. Please try again later.', 'error')

       

    return redirect(url_for('index'))



@app.route('/submit_task_1', methods=['POST'])
def submit_task_1():
    if request.method == 'POST':

        ans = request.form['ans']

        return render_template('dashboard.html') 
    else:
        return 'Method Not Allowed', 405  


if __name__ =="__main__":
    app.run(debug=True)


