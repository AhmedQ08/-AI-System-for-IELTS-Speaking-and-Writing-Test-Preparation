from openai import OpenAI

import os


# Initialization
client = OpenAI(
    api_key=os.environ['openai_api_key']
)

discuss_format_json = str({
    "statement":"question statement here",
    "statement_answer":["A brief logical explanation of the provided statement to be used for further analysis."]
    })
answer_discuss = """Artificial intelligence is undoubtedly reshaping the landscape of work in various industries, presenting both opportunities and challenges. On one hand, AI has the potential to greatly enhance productivity, efficiency, and innovation across different sectors. For example, in manufacturing, AI-powered robots can perform repetitive tasks with greater speed and precision, freeing up human workers to focus on more complex and creative aspects of production. In healthcare, AI algorithms can analyze vast amounts of medical data to assist doctors in making more accurate diagnoses and developing personalized treatment plans, ultimately improving patient outcomes.

Furthermore, AI technologies like natural language processing and machine learning are revolutionizing customer service and support functions. Chatbots and virtual assistants can handle routine inquiries and transactions, providing faster response times and 24/7 availability. This not only improves customer satisfaction but also allows human employees to concentrate on higher-value interactions that require empathy and problem-solving skills.

However, the widespread adoption of AI in the workplace also presents significant challenges and concerns. One major issue is the potential displacement of jobs due to automation. As AI systems become more sophisticated, there is a risk that certain tasks and roles traditionally performed by humans could be rendered obsolete. This raises questions about the future of employment and the need for retraining and upskilling programs to ensure that workers can adapt to evolving job requirements.

Additionally, there are ethical considerations surrounding the use of AI, particularly regarding privacy, bias, and accountability. AI algorithms are only as good as the data they are trained on, which means they can inadvertently perpetuate existing biases and discrimination present in the data. Ensuring fairness and transparency in AI decision-making processes is crucial to prevent unintended consequences and maintain trust in these technologies.

Moreover, there are concerns about the concentration of power and wealth among companies that develop and control AI technologies. The rise of automation could exacerbate income inequality if not accompanied by policies that promote equitable distribution of wealth and opportunities.

In conclusion, while artificial intelligence holds immense potential to transform the future of work for the better, it also presents complex challenges that must be addressed proactively. By fostering collaboration between policymakers, businesses, educators, and workers, we can harness the benefits of AI while mitigating its negative impacts, ensuring a more inclusive and sustainable future of work."""

discuss_example_json = str({
    "statement":"How do you anticipate artificial intelligence impacting the future of work, and what potential benefits and challenges might arise as a result?",
    "statement_answer":[answer_discuss]
})

def generate_system_prompt_message_questions_discuss():
    return(
        "You are an IELTS expert. Your job is to create technical, meaningful and reality based discussion questions on various subjects like Academic IELTS speaking test .\n"
        
        "You MUST return your response in the requested JSON format."
    )

def generate_user_prompt_message_questions_discuss():
    return(
        "You are an IELTS expert. Your job is to create technical, meaningful and reality based questions on various subjects.\n"
        "These questions are to be included in the Academic IELTS Speaking interview part 3 . You must create questions that have 2 distinct parts:\n"
        "1. A question statement in English language with easy to moderate level of vocabulary used.\n"
        "2. you have to given point of view, argument or problem which user need to discuss .\n"
        "Example :\n"
        f"{discuss_example_json}\n"
        "Your response must be in the following format:\n"
        f"{discuss_format_json}"
    )




# ============================================================= ANSWER ANALYSIS============================     
discuss_answer_analysis_json =str({
    "user_answer":"show here user original answer ",
    "score" : "score out of 10 (at max 9) and it depends on ",
    "rating" : "below 6 is 'Worst', 6-6.9 is 'Band 6', 7-7.9 is 'Band 7', 8-8.9 is 'Band 8', 9-9.9 is 'Band 9' ",
    "fillers":"find out fillers words in answer",
    "filler_count":"count number of fillers in anser",
    "grammatical_mistakes" : "Find out any grammatical mistakes and give in form of a statement",
    "vocabulary_mistakes" : "Find out any vocabulary mistakes and give in form of a statement",
    "check_context" : "Ensure that the response remains pertinent to the question, regardless of whether it agree with or disagree the statement",
    "sentiment_analysis":"Analyze the sentiment of the  answer",
    "first_answer":"Give the  first best answer of Statement and  answer should be in full detail atleast use 250 words and answer should be context of question and always give answer in english",
    "Second_answer":"Give the  Second best answer of Statement and  answer should be in full detail atleast use 250 words and answer should be context of question and always give answer in english",
    "third_answer":"Give the  third best answer of Statement and  answer should be in full detail atleast use 250 words and answer should be context of question and always give answer in english",
    "fourth_answer":"Give the  fourth best answer of Statement and  answer should be in full detail atleast use 250 words and answer should be context of question and always give answer in english"
})
def generate_system_prompt_message_ans_discuss():
    return(
        "You are an IELTS expert. Your job is to analyze and find mistakes in the answer of a user as compared to a benchmark answer to a question.\n"
        
        "You MUST return your response in the requested JSON format."
    )

def generate_user_prompt_message_ans_discuss(user_answer_discuss, comparison_statement_discuss):
    return(
        "You are an IELTS expert. Your job is to analyze and find mistakes in the answer of a user as compared to a benchmark answer to a question.\n"
        "Following is a  question statement, a related bar chart details used to perceive a better understanding of question statement and an answer (graph_explanation) in the end which is the best answer (benchmark) for the given question.\n"
        f"{comparison_statement_discuss}\n"
        "THE ABOVE PROVIDED JSON IS ONLY FOR COMPARISON. THIS IS NOT THE FORMAT OF RESPONSE REQUIRED. THE REQUIRED RESPONSE FORMAT IS GIVEN AT THE END OF THE PROMPT"
        "This question was given to a student in an automated exam. Following is the answer of the student to this question statement and related bar chart:\n"
        f"{user_answer_discuss}\n"
        "Based on the given question statement, analyze the answer by student, find out mistakes in it and give it a score out of 10 as compared to the given benchmark answer.\n"
        "The following example and response format json includes how the response MUST be formatted.\n"
        
        "Your response MUST be in the following format:\n"
        f"{discuss_answer_analysis_json}"
    )


# ========================================================================================================
def get_response_type_text(system_prompt_message_discuss, user_prompt_message_discuss, model="gpt-4-turbo"):
    print("\nHEREEEeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
    messages = [
        {"role": "system", "content": system_prompt_message_discuss},
        {"role": "user", "content": user_prompt_message_discuss}
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


