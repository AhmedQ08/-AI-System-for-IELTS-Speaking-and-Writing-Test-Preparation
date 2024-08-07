from openai import OpenAI

import os


# Initialization
client = OpenAI(
    api_key=os.environ['openai_api_key']
)

intro_format_json = str({
    "statement":"question statement here",
    "statement_answer":["A brief introduction of a user for IELTS speaking innterview part 1"]
    })
answer_intro = """Good afternoon, esteemed examiner. My name is Sarah, and I'm delighted to meet you today. I originate from the bustling metropolis of Toronto, Canada, a city renowned for its cultural diversity and vibrant atmosphere. At the age of 24, I stand on the threshold of new experiences, eager to embrace the challenges and opportunities that lie ahead.

Currently, I am deeply immersed in the field of environmental science, pursuing my passion for understanding and protecting our planet. Whether it's analyzing data on climate patterns or conducting field research to assess the impact of human activity on ecosystems, I approach my studies with fervor and dedication.

Beyond academia, I find solace in the art of photography, capturing moments that evoke emotion and tell stories without words. There's a certain magic in freezing time through the lens of a camera, and it's a passion that allows me to express myself creatively amidst the demands of academic life.

Moreover, I believe in the power of effective communication to bridge divides and foster understanding. Whether it's engaging in discussions with peers or presenting my research findings at conferences, I strive to communicate with clarity and conviction.

This IELTS speaking test is an opportunity for me to showcase my proficiency in the English language and demonstrate my ability to express myself confidently and coherently. I approach this test with a mixture of excitement and determination, ready to give it my all. Thank you for this opportunity, and I look forward to our conversation."""

intro_example_json = str({
    "statement":"Could you introduce yourself and provide some background information?",
    "statement_answer":[answer_intro]
})

def generate_system_prompt_message_questions_intro():
    return(
        "You are an IELTS expert. Your job is to create technical, meaningful and reality based questions on various subjects like Academic IELTS speaking test part 1 .\n"
        
        "You MUST return your response in the requested JSON format."
    )

def generate_user_prompt_message_questions_intro():
    return(
        "You are an IELTS expert. Your job is to create introductive questions for candidate of IELTS speaking test.\n"
        "These questions are to be included in the Academic IELTS speaking test part 1 . You must start question in that way Could you introduce yourself and provide some background information?\n"
        "A question statement in English language with easy to moderate level of vocabulary used."
        "Example :\n"
        f"{intro_example_json}\n"
        "Your response must be in the following format:\n"
        f"{intro_format_json}"
    )




# ============================================================= ANSWER ANALYSIS============================     
intro_answer_analysis_json =str({
    "user_answer":"show here user original answer ",
    "language":"user answer must be in standard english",
    "name":"ensure user has mentioned his/her name in answer",
    "country":"ensure user has mentioned his/her city/country in answer",
    "age":"ensure user has mentioned his/her city/country in answer",
    "student_major":"ensure user has mentioned his/her major in studies or their academic background in answer",
    "studying_or_working":"Make sure the user specifies whether they are studying or working, and provide details in the response.",
    "hobby":"ensure user has mentioned his/her hobby in answer",
    "describe_hobby":"ensure user has describe his/her hobby in detail in answer",
    "conclusion":"ensure user has conclued his/her  answer",
    "score" : "score out of 10 (at max 9)",
    "fillers":"find out fillers words in answer",
    "filler_count":"count number of fillers in anser",
    "rating" : "below 6 is 'Worst', 6-6.9 is 'Band 6', 7-7.9 is 'Band 7', 8-8.9 is 'Band 8', 9-9.9 is 'Band 9' ",
    "grammatical_mistakes" : "Find out any grammatical mistakes and give in form of a statement",
    "vocabulary_mistakes" : "Find out any vocabulary mistakes and give in form of a statement",
    "check_context" : "Ensure that the response remains pertinent to the question, regardless of whether it agree with or disagree the statement",
    "sentiment_analysis":"Analyze the sentiment of the  answer",
    "first_answer":"Give the  first best answer of Statement and  answer should be in full detail atleast use 250 words and answer should be context of question and always give answer in english",
    "Second_answer":"Give the  Second best answer of Statement and  answer should be in full detail atleast use 250 words and answer should be context of question and always give answer in english",
    "third_answer":"Give the  third best answer of Statement and  answer should be in full detail atleast use 250 words and answer should be context of question and always give answer in english",
    "fourth_answer":"Give the  fourth best answer of Statement and  answer should be in full detail atleast use 250 words and answer should be context of question and always give answer in english"
})
def generate_system_prompt_message_ans_intro():
    return(
        "You are an IELTS expert. Your job is to analyze and find mistakes in the answer of a user as compared to a benchmark answer to a question.\n"
        
        "You MUST return your response in the requested JSON format."
    )

def generate_user_prompt_message_ans_intro(user_answer_intro, comparison_statement_intro):
    return(
        "You are an IELTS expert. Your job is to analyze and find mistakes in the answer of a user as compared to a benchmark answer to a question.\n"
        f"{comparison_statement_intro}\n"
        "THE ABOVE PROVIDED JSON IS ONLY FOR COMPARISON. THIS IS NOT THE FORMAT OF RESPONSE REQUIRED. THE REQUIRED RESPONSE FORMAT IS GIVEN AT THE END OF THE PROMPT"
        "This question was given to a student in an automated exam. Following is the answer of the student to this question statement \n"
        f"{user_answer_intro}\n"
        "Based on the given question statement, analyze the answer by student, find out mistakes in it and give it a score out of 10 as compared to the given benchmark answer.\n"
        "The following example and response format json includes how the response MUST be formatted.\n"
        
        "Your response MUST be in the following format:\n"
        f"{intro_answer_analysis_json}"
    )


# ========================================================================================================
def get_response_type_text(system_prompt_message_intro, user_prompt_message_intro, model="gpt-4-turbo"):
    print("\nHEREEEeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
    messages = [
        {"role": "system", "content": system_prompt_message_intro},
        {"role": "user", "content": user_prompt_message_intro}
    ]

    try:
        response = client.chat.completions.create(
            model=model,
            response_format={ "type": "json_object" },
            messages=messages,
            temperature=1,
            max_tokens=3000,
        )
        return response
    except Exception as e:
        print("Error: ", e)
        response = e
    print("\n*****\nRaw response:\n",response,"\n*****\n")
    return 


