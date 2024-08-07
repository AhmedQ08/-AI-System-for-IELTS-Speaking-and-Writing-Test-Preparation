from openai import OpenAI

import os


# Initialization
client = OpenAI(
    api_key=os.environ['openai_api_key']
)

task_2_format_json = str({
    "statement":"question statement here",
    "statement_answer":["A brief logical explanation of the provided statement to be used for further analysis."]
    })
answer_task_2 = """I would lean towards agreeing with the statement that the average standard of people's health is likely to be lower in the future than it is now. Here's a detailed explanation: 
There's a concerning trend of increasingly sedentary lifestyles and poor dietary habits in many parts of the world. Sedentary behavior, coupled with high-calorie, low-nutrient diets, contributes to a range of health issues including obesity, cardiovascular disease, and metabolic disorders.

Obesity rates have been steadily climbing, particularly in developed nations, but also in emerging economies. This epidemic has far-reaching consequences for public health, as obesity is linked to numerous chronic conditions such as type 2 diabetes, hypertension, and certain types of cancer.

Environmental degradation, pollution, and climate change pose significant threats to public health. Air pollution, for example, is associated with respiratory diseases and cardiovascular problems. Climate change exacerbates health risks through extreme weather events, food and water insecurity, and the spread of infectious diseases.

The global population is aging, leading to an increased burden of age-related health conditions. As life expectancy rises, so does the prevalence of chronic diseases and disabilities, placing strain on healthcare systems and potentially lowering the overall health standard.

Disparities in access to healthcare and socioeconomic factors contribute to health inequities, which can widen the gap in health outcomes between different population groups. Without addressing these underlying social determinants of health, certain communities may experience declining health standards.

While medical advancements hold promise for improving healthcare outcomes, they also come with challenges such as rising healthcare costs and ethical considerations. Access to cutting-edge treatments and technologies may be unevenly distributed, exacerbating health disparities.

In summary, while advancements in medicine and technology offer potential benefits, the collective impact of lifestyle trends, environmental factors, aging populations, and health inequities suggests that the average standard of people's health may indeed decline in the future if proactive measures are not taken to address these challenges."""

task_2_example_json = str({
    "statement":"The average standard of people's health is likely to be lower in the future than it is now.\nTo what extent do you agree or disagree with this statement?\nGive reasons for your answer and include any relevant examples from your own knowledge or experience.",
    "statement_answer":[answer_task_2]
})

def generate_system_prompt_message_questions_task_2():
    return(
        "You are an IELTS expert. Your job is to create technical, meaningful and reality based questions on various subjects like Academic IELTS test Task 2 .\n"
        
        "You MUST return your response in the requested JSON format."
    )

def generate_user_prompt_message_questions_task_2():
    return(
        "You are an IELTS expert. Your job is to create technical, meaningful and reality based questions on various subjects.\n"
        "These questions are to be included in the Academic IELTS Task-2 . You must create questions that have 2 distinct parts:\n"
        "1. A question statement in English language with easy to moderate level of vocabulary used.\n"
        "2. you have to given point of view, argument or problem which user need to discuss .\n"
        "Example :\n"
        f"{task_2_example_json}\n"
        "Your response must be in the following format:\n"
        f"{task_2_format_json}"
    )




# ============================================================= ANSWE ANALYSIS============================
task_2_answer_analysis_json =str({
    "user_answer":"show here user original answer ",
    "score" : "score out of 10 (at max 9)",
    "rating" : "below 6 is 'Worst', 6-6.9 is 'Band 6', 7-7.9 is 'Band 7', 8-8.9 is 'Band 8', 9-9.9 is 'Band 9' ",
    "grammatical_mistakes" : "Find out any grammatical mistakes and give in form of a statement",
    "vocabulary_mistakes" : "Find out any vocabulary mistakes and give in form of a statement",
    "spelling_mistakes" : "Find out any spelling mistakes and give in form of a statement",
    "check_context" : "Ensure that the response remains pertinent to the question, regardless of whether it agree with or disagree the statement",
    "first_answer":"Give the  first best answer of Statement and  answer should be in full detail atleast use 250 words and answer should be context of question",
    "Second_answer":"Give the  Second best answer of Statement and  answer should be in full detail atleast use 250 words and answer should be context of question",
    "third_answer":"Give the  third best answer of Statement and  answer should be in full detail atleast use 250 words and answer should be context of question",
    "fourth_answer":"Give the  fourth best answer of Statement and  answer should be in full detail atleast use 250 words and answer should be context of question"
})
def generate_system_prompt_message_ans_task_2():
    return(
        "You are an IELTS expert. Your job is to analyze and find mistakes in the answer of a user as compared to a benchmark answer to a question.\n"
        
        "You MUST return your response in the requested JSON format."
    )

def generate_user_prompt_message_ans_task_2(user_answer_task_2, comparison_statement_task_2):
    return(
        "You are an IELTS expert. Your job is to analyze and find mistakes in the answer of a user as compared to a benchmark answer to a question.\n"
        "Following is a  question statement, a related bar chart details used to perceive a better understanding of question statement and an answer (graph_explanation) in the end which is the best answer (benchmark) for the given question.\n"
        f"{comparison_statement_task_2}\n"
        "THE ABOVE PROVIDED JSON IS ONLY FOR COMPARISON. THIS IS NOT THE FORMAT OF RESPONSE REQUIRED. THE REQUIRED RESPONSE FORMAT IS GIVEN AT THE END OF THE PROMPT"
        "This question was given to a student in an automated exam. Following is the answer of the student to this question statement and related bar chart:\n"
        f"{user_answer_task_2}\n"
        "Based on the given question statement, analyze the answer by student, find out mistakes in it and give it a score out of 10 as compared to the given benchmark answer.\n"
        "The following example and response format json includes how the response MUST be formatted.\n"
        
        "Your response MUST be in the following format:\n"
        f"{task_2_answer_analysis_json}"
    )


# ========================================================================================================
def get_response_type_text(system_prompt_message_task_2, user_prompt_message_task_2, model="gpt-4-turbo"):
    print("\nHEREEEeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
    messages = [
        {"role": "system", "content": system_prompt_message_task_2},
        {"role": "user", "content": user_prompt_message_task_2}
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


