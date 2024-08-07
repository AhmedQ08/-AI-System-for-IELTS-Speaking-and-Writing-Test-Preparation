from openai import OpenAI

import os


# Initialization
client = OpenAI(
    api_key=os.environ['openai_api_key']
)

format_json = str({
    "statement":"question statement here",
    "graph":"visual representation of statement",
    "Y-Axis Range":["Ranges for the Y-Axis (How high the bars go)"],
    "X-Axis Range":["Ranges for the Y-Axis (Items)"],
    "Values":["Values of Y-Axis for each item (How high each item bar goes)"],
    "graph_explanation":["A brief logical explanation of the provided graph to be used for further analysis."]
    })
answer = """The chart demonstrates a clear shift in adult participation trends for major sports within the surveyed area between 1997 and 2017. Most notably, sports like basketball, football (soccer), and hiking experienced significant growth. Basketball witnessed the most dramatic surge, with participation nearly tripling. Football enjoyed a substantial increase as well.  Conversely, cricket faced a marked decline in popularity over the twenty-year period.

These changes likely reflect broader societal trends. The rise in team-oriented sports like basketball and football suggests a growing interest in activities that foster social interaction and a sense of community. This could indicate a cultural shift towards prioritizing both physical and mental well-being. The decline of cricket is more difficult to interpret without additional context; factors such as changing sport preferences, accessibility of facilities, or shifts in demographics could be at play."""
example_json = str({
    "statement":"The chart below shows a number of adults participating in different major sports in one area, in 1997 and 2017.\nSummarize the information by selecting and reporting the main features, and make comparisons where relevant.",
    "graph":"visual representation of statement",
    "labels":["Major Sport",  "Number of adults in thousands"],
    "Y-Axis Range":["0","10","20","30","40","50","60"],
    "X-Axis Range":["Tennis","Basketball","Cricket","Golf","Swimming","Football","Rugby"],
    "Values":["50","8","25","31","34","31","32"],
    "graph_explanation":[answer]
})
def generate_system_prompt_message_questions():
    return(
        "You are an IELTS expert. Your job is to create technical, meaningful and reality based questions on various subjects.\n"
        
        "You MUST return your response in the requested JSON format."
    )

def generate_user_prompt_message_questions():
    return(
        "You are an IELTS expert. Your job is to create technical, meaningful and reality based questions on various subjects.\n"
        "These questions are to be included in the IELTS exam. You must create questions that have 2 distinct parts:\n"
        "1. A question statement in English language with easy to moderate level of vocabulary used.\n"
        "2. A bar chart relating logically to the question statement. This chart must have values and labels that corresspond to reality. The x-axis must only have one value for each item on it.\n"
        "It must be easy for the student to deduce reliable and reality based information from this graph. You must provide X, Y labels for the graph and a between 5 - 8 total x,y value sets.\n"
        "The following example and response format json includes how the response MUST be formatted.\n"
        "Example :\n"
        f"{example_json}\n"
        "Your response must be in the following format:\n"
        f"{format_json}"
    )




# ============================================================= ANSWE ANALYSIS============================
answer_analysis_json =str({
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
def generate_system_prompt_message_ans():
    return(
        "You are an IELTS expert. Your job is to analyze and find mistakes in the answer of a user as compared to a benchmark answer to a question.\n"
        
        "You MUST return your response in the requested JSON format."
    )

def generate_user_prompt_message_ans(user_answer, comparison_statement):
    return(
        "You are an IELTS expert. Your job is to analyze and find mistakes in the answer of a user as compared to a benchmark answer to a question.\n"
        "Following is a  question statement, a related bar chart details used to perceive a better understanding of question statement and an answer (graph_explanation) in the end which is the best answer (benchmark) for the given question.\n"
        f"{comparison_statement}\n"
        "THE ABOVE PROVIDED JSON IS ONLY FOR COMPARISON. THIS IS NOT THE FORMAT OF RESPONSE REQUIRED. THE REQUIRED RESPONSE FORMAT IS GIVEN AT THE END OF THE PROMPT"
        "This question was given to a student in an automated exam. Following is the answer of the student to this question statement and related bar chart:\n"
        f"{user_answer}\n"
        "Based on the given question statement, bar-chart and benchmark answer, analyze the answer by student, find out mistakes in it and give it a score out of 10 as compared to the given benchmark answer.\n"
        "The following example and response format json includes how the response MUST be formatted.\n"
        
        "Your response MUST be in the following format:\n"
        f"{answer_analysis_json}"
    )


# ========================================================================================================
def get_response_type_text(system_prompt_message, user_prompt_message, model="gpt-4-turbo"):
    print("\nHEREEEeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
    messages = [
        {"role": "system", "content": system_prompt_message},
        {"role": "user", "content": user_prompt_message}
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
    return response


