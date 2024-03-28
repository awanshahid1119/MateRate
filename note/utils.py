# # import openai
# # import main.settings as settings
# # def get_feedback(title, content):
# #     openai.api_key = settings.OPENAI_API_KEY
# #     # Initial prompt with specific instructions for detailed corrections
# #     prompt = f"{title}\n{content}\nCheck if the solution is correct. If not point out the line number in the solution provided from where the solution should be corrected.\n"
# #     for iteration in range(3):
# #         response = openai.ChatCompletion.create(
# #             model="gpt-3.5-turbo",
# #             messages=[
# #                 {
# #                     "role": "system",
# #                     "content": prompt
# #                 }
# #             ],
# #             max_tokens=150,
# #             temperature=0,
# #             stop=None
# #         )
# #         print(f"Iteration {iteration + 1} - Model Response:")
# #         print(response['choices'][0]['message']['content'].strip())
# #         # Analyze the response and refine the prompt based on patterns in mistakes
# #         prompt += f"{title}\n{content}\nCheck if the solution is correct. If not point out the line number in the solution provided from where the solution should be corrected.\n"
# #     # Final response after iterations
# #     final_response = response['choices'][0]['message']['content'].strip()
# #     print(f"Final Response after Iterations:")
# #     print(final_response)
# #     return final_response
# import openai
# import main.settings as settings

# def get_feedback(title, content):
#     openai.api_key = settings.OPENAI_API_KEY
    
#     # Step 1: Check if the content is correct
#     prompt_step1 = f"{title}\n{content}\n Identify the problem, Provide a detailed solution to the problem."
#     response_step1 = openai.Completion.create(
#         engine="text-davinci-003",  # Use the Davinci model here
#         prompt=prompt_step1,
#         max_tokens=450,
#         temperature=0.7,
#         stop=None
#     )

#     # Step 2: Identify calculation mistakes
#     prompt_step2 = f"{title}\n{content}\n Check whether the actual content is correct with comparison to provided solution. {response_step1['choices'][0].get('message', {}).get('content', '').strip()}"
    
#     response_step2 = openai.Completion.create(
#         engine="text-davinci-003",  # Use the Davinci model here
#         prompt=prompt_step2,
#         max_tokens=450,
#         temperature=0.7,
#         stop=None
#     )

#     # Step 3: Provide guidance on correcting mistakes
#     prompt_step3 = f"{title}\n{content}\n Identify and specify the line number(s) where mistakes are present in the actual content. {response_step2['choices'][0].get('message', {}).get('content', '').strip()}"
#     response_step3 = openai.Completion.create(
#         engine="text-davinci-003",  # Use the Davinci model here
#         prompt=prompt_step3,
#         max_tokens=450,
#         temperature=0.7,
#         stop=None
#     )

#     # Debug information
#     print("Response Step 1:", response_step1)
#     print("Response Step 2:", response_step2)
#     print("Response Step 3:", response_step3)

#     # Error handling and final response
#     corrected_solution = response_step1['choices'][0].get('text', '').strip()
#     correctness = response_step2['choices'][0].get('message', {}).get('content', '').strip()
#     identify_mistakes = response_step3['choices'][0].get('text', '').strip()

#     final_response = (
#         f"1) Corrected solution:\n{corrected_solution}\n\n"
#         f"2) Correctness:\n{correctness}\n\n"
#         f"3) Identify the mistakes:\n{identify_mistakes}\n\n"
#     )

#     print("Final Response:")
#     print(final_response)

#     return final_response




# import openai
# import main.settings as settings

# def get_feedback(title, content):
#     openai.api_key = settings.OPENAI_API_KEY
    
#     # Step 1: Check if the content is correct
#     prompt_step1 = f"{title}\n{content}\n Check whether the content is correct or not."
#     response_step1 = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {
#                 "role": "system",
#                 "content": prompt_step1
#             }
#         ],
#         max_tokens=450,
#         temperature=0.7,
#         stop=None
#     )

#     # Step 2: Identify calculation mistakes
#     prompt_step2 = f"{title}\n{content}\n  specify the line number(s) where the mistakes are present. {response_step1['choices'][0]['message']['content'].strip()}"
#     response_step2 = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {
#                 "role": "system",
#                 "content": prompt_step2
#             }
#         ],
#         max_tokens=450,
#         temperature=0.7,
#         stop=None
#     )

#     # Step 3: Provide guidance on correcting mistakes
#     prompt_step3 = f"{title}\n{content}\n correct these mistakes and give detailed solution . {response_step2['choices'][0]['message']['content'].strip()}"
#     response_step3 = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {
#                 "role": "system",
#                 "content": prompt_step3
#             }
#         ],
#         max_tokens=450,
#         temperature=0.7,
#         stop=None
#     )

#     # Final response
#     final_response = (
#         f"1) correctness:\n{response_step1['choices'][0]['message']['content'].strip()}\n\n"
#         f"2) Identify the mistakes:\n{response_step2['choices'][0]['message']['content'].strip()}\n\n"
#         f"3) Corrected solution:\n{response_step3['choices'][0]['message']['content'].strip()}"
#     )

#     print("Final Response:")
#     print(final_response)

#     return final_response



import openai
import main.settings as settings

def get_feedback(title, content):
    openai.api_key = settings.OPENAI_API_KEY
    
    # Step 1: Provide a complete solution
    prompt_step1 = f"{title}\n{content}\n Identify the problem, Provide a detailed solution to the problem."
    response_step1 = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": prompt_step1
            }
        ],
        max_tokens=450,
        temperature=0.7,
        stop=None
    )

    # Step 2: Check if the content is correct
    prompt_step2 = f"{title}\n{content}\n Check whether the actual content is correct with comaprison to provided solution. {response_step1['choices'][0]['message']['content'].strip()}"
    response_step2 = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": prompt_step2
            }
        ],
        max_tokens=450,
        temperature=0.7,
        stop=None
    )

    # Step 3: Identify calculation mistakes
    prompt_step3 = f"{title}\n{content}\n Identify and specify the line number(s) where mistakes are present in the actual content. {response_step2['choices'][0]['message']['content'].strip()}"
    response_step3 = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": prompt_step3
            }
        ],
        max_tokens=450,
        temperature=0.7,
        stop=None
    )

    # Final response
    final_response = (
        f"1) Complete Solution:\n{response_step1['choices'][0]['message']['content'].strip()}\n\n"
        f"2) Correctness Check:\n{response_step2['choices'][0]['message']['content'].strip()}\n\n"
        f"3) Identify Mistakes:\n{response_step3['choices'][0]['message']['content'].strip()}"
    )

    print("Final Response:")
    print(final_response)

    return final_response


