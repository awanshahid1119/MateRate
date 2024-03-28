import openai
import main.settings as settings

def get_feedback(question, steps, answer):
    openai.api_key = settings.OPENAI_API_KEY

    prompt = f"Give feedback.\n{question}\n{steps}\nFinal answer: {answer}\n"

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
    print(corrected_answer)
    # note.educator_feedback = corrected_answer
    return corrected_answer