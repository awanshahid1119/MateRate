
import openai
import settings

def get_feedback(question, incorrect_answer):
    openai.api_key = settings.OPENAI_API_KEY

    # prompt = f"Here is a math question:\n\nWhat is the correct answer to the following equation?\n\n{incorrect_answer}\n\nCorrect Answer:"

    # prompt = f"This is the question: {question}\n The answer given by the student: {incorrect_answer}\n\nIs the answer right? If not what is the right answer?"

    # prompt = f"Is this answer {incorrect_answer} right to the question {question}?"

    # prompt = f"This is the question: {question}\nThe answer given by the student: {incorrect_answer}\nIs the answer correct? If not, what is the correct answer?"
    prompt = f"Question: {question}\n Answer: {incorrect_answer}\nIs the answer correct? If not, what is the correct answer?"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0,
        top_p=1.0,
        frequency_penalty=0,
        presence_penalty=0
    )
    print(response)
    corrected_answer = response.choices[0].text.strip()
    # print(corrected_answer)
    return corrected_answer

# get_feedback("What is the powerhouse of the cell?", "The mitochondria is the powerhouse of the cell.")


def get_feedback_line_by_line(question, incorrect_answer):
    openai.api_key = settings.OPENAI_API_KEY

    lines = incorrect_answer.split('\n')
    prompt = f"Question: {question}\n"
    
    for line in lines:
        prompt += f"Answer: {line.strip()}\nIs this line correct? If not, what is the correct answer?\n"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0,
        top_p=1.0,
        frequency_penalty=0,
        presence_penalty=0
    )
    print(response)
    corrected_answers = response.choices[0].text.strip().split('\n')
    return corrected_answers

get_feedback_line_by_line("What is the powerhouse of the cell?", "The nucleus is the powerhouse of the cell.\nIt is responsible for producing ATTP.")
