# ai_helper.py

import google.generativeai as genai
from app import Config
import re

genai.configure(api_key=Config.GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


def get_ai_insights(title, body):
    prompt = f"Analyze this programming question and provide insights:\n\nTitle: {title}\n\nBody: {body}\n\nProvide a brief analysis, potential solution approaches, and any relevant tips or best practices."

    response = model.generate_content(prompt, stream=True)
    insights = ""
    for chunk in response:
        insights += chunk.text

    return insights


def get_ai_answer_review(question_body, answer_body):
    prompt = f"Review this answer to a programming question:\n\nQuestion: {question_body}\n\nAnswer: {answer_body}\n\nProvide a brief review of the answer, including its correctness, completeness, and any suggestions for improvement."

    response = model.generate_content(prompt)
    return response.text


def get_ai_suggested_tags(title, body):
    prompt = f"Suggest 3-5 relevant tags for this programming question:\n\nTitle: {title}\n\nBody: {body}\n\nProvide the tags as a comma-separated list."

    response = model.generate_content(prompt)
    return response.text.split(",")


def get_ai_question_summary(title, body):
    prompt = f"Summarize this programming question in 2-3 sentences:\n\nTitle: {title}\n\nBody: {body}"

    response = model.generate_content(prompt)
    return response.text


def get_ai_answer_ranking(question_body, answers):
    prompt = f"Rank the following answers to this programming question from best to worst:\n\nQuestion: {question_body}\n\n"

    for i, answer in enumerate(answers, 1):
        prompt += f"Answer {i}: {answer.body}\n\n"

    prompt += "Provide the ranking as a comma-separated list of answer numbers."

    response = model.generate_content(prompt)

    try:
        return [int(x.strip()) for x in response.text.split(",") if x.strip().isdigit()]
    except ValueError:
        return []


def get_ai_code_explanation(code_snippet):
    prompt = f"Explain the following code snippet in simple terms:\n\n{code_snippet}"

    response = model.generate_content(prompt)
    return response.text


def get_ai_similar_questions(title, body, existing_questions):
    prompt = (
        f"Find similar questions to this one:\n\nTitle: {title}\n\nBody: {body}\n\n"
    )
    prompt += "Existing questions:\n"

    for i, question in enumerate(existing_questions, 1):
        prompt += f"{i}. {question.title}\n"

    prompt += "\nProvide the numbers of similar questions, separated by commas."

    response = model.generate_content(prompt)

    numbers = re.findall(r"\d+", response.text)

    try:
        return [int(num) for num in numbers]
    except ValueError:
        return []
