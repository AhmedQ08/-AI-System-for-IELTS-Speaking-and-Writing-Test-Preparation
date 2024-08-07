import os
from openai import OpenAI
import re
import json

# Set your OpenAI API key here
client = OpenAI()
default_model = "gpt-4-turbo"
example_json = str({
    "statement":"question statement here",
    "graph":"visual representation of statement",
    "labels":["label 1",  "label 2"],
    "values":["value 1","value 2","value 3","value 3","value 4","value 5"],
    "graph_explain":["graph explaination here"]
    })
    
def generate_question():
    response = client.chat.completions.create(
        model=default_model,
        response_format = {"type":"json_object"},
        messages=[{"role":"user","content":f" Generate a question for IELTS having a statement and generate graph labels that should be two and values with its unit and values must be numbers of it and make sure datapoints are according chart js library and in the end explain correct whole graph explaination in atleast 150 words . You must return a response in provided JSON format:\n{example_json}"}
        ],
        temperature=1,
        max_tokens=3000
    )
    print(response)
    question = response .choices[0].message.content
    print(question)
    return question


# def analyze_statement(statement):
#     response = client.chat.completions.create(
#         model=default_model,
#         messages=[
#             {"role": "system", "content": "You will be provided with statements, and your task is to convert them to standard English also mention what are the spelling mistakes in statement. Check the grammar in statement and mention it. Check whether the statement is answering the question or not. If it is answering, determine the percentage of correctness. If it is not answering, specify the percentage of non-compliance."},
#             {"role": "user", "content": statement}
#         ]
#     )
#     corrected_statement = response['choices'][0]['message']['content'].strip()
#     return corrected_statement


# def correct_english_statement(statement):
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo-1106",
#         messages=[
#             {"role": "system", "content": "You will be provided with statements, and your task is to convert them to standard English also mention what are the spelling mistakes in statement. Check the grammar in statement and mention it. Check whether the statement is answering the question or not. If it is answering, determine the percentage of correctness. If it is not answering, specify the percentage of non-compliance."},
#             {"role": "user", "content": statement}
#         ]
#     )
#     corrected_statement = response['choices'][0]['message']['content'].strip()
#     return corrected_statement

# if __name__ == "__main__":
#     responses = []

#     for i in range(2):
#         system_question = generate_question()
#         user_statement = input(f"\nSystem Question {i+1}: {system_question}\nEnter your statement: ")
#         corrected_statement = correct_english_statement(user_statement)

#         responses.append({
#             "Question": system_question,
#             "User Statement": user_statement,
#             "Corrected Statement": corrected_statement
#         })

#     print("\nResults:")
#     for i, response in enumerate(responses, start=1):
#         print(f"\nQuestion {i}: {response['Question']}")
#         print(f"Original Statement: {response['User Statement']}")
#         print(f"Corrected Statement: {response['Corrected Statement']}")


prompt = "You are an IELTS expert. Your job is to create technical, meaningful and reality based questions on various subjects to be included in the IELTS exam. You must create questions that has 2 parts: A statement in english language."