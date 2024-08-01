from flask import Flask, render_template, request, redirect, url_for
import random
import openai
import os

app = Flask(__name__)

# OpenAI API 키 설정
openai.api_key = 'sk-proj-hzjl9hIZdIS1Zwjwop6FT3BlbkFJu2di6ybGcqFd2T9j5nTa'

# 일기 저장 폴더 설정
DIARY_FOLDER = 'diaries'
if not os.path.exists(DIARY_FOLDER):
    os.makedirs(DIARY_FOLDER)

fixed_questions = [
    "나이가 어떻게 되나요?",
    "성별이 어뗳게 되나요?"
]

random_questions = [
    "오늘 드신 음식 중에 가장 맛있었던 것은 무엇인가요?",
    "오늘 날씨는 어땠나요?",
    "오늘 누구와 대화를 나누셨나요?"
    "오늘 드신 음식 중에 가장 맛있었던 것은 무엇인가요?",
    "오늘 날씨는 어땠나요?",
    "오늘 누구와 대화를 나누셨나요?"
]

responses = []

@app.context_processor
def utility_processor():
    return dict(enumerate=enumerate)

@app.route('/')
def index():
    selected_random_questions = random.sample(random_questions, 2)  # 랜덤 질문 2개 선택
    return render_template('index.html', fixed_questions=fixed_questions, random_questions=selected_random_questions)

@app.route('/submit', methods=['POST'])
def submit():
    global responses
    answers = []
    for i, question in enumerate(fixed_questions):
        answer = request.form.get(f'answer{i}')
        answers.append((question, answer))
    
    # 랜덤 질문 처리
    for i in range(2):
        random_question = request.form.get(f'random_question{i}')
        random_answer = request.form.get(f'random_answer{i}')
        answers.append((random_question, random_answer))
    
    # GPT-3.5 Turbo API를 사용하여 일기 생성
    diary_content = generate_diary(answers)
    
    
    responses.append({
        'answers': answers,
        'diary': diary_content
    })
    return redirect(url_for('diary'))

@app.route('/diary')
def diary():
    return render_template('diary.html', responses=responses)

def generate_diary(answers):
    prompt = "사용자의 대답을 바탕으로 일기를 작성해 주세요:\n"
    for question, answer in answers:
        prompt += f"Q: {question}\nA: {answer}\n"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that writes diary entries based on user's answers."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200
    )
    
    diary_content = response['choices'][0]['message']['content'].strip()
    return diary_content

