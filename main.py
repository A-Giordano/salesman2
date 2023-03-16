import openai
import streamlit as st
from streamlit_chat import message

openai.api_key = st.secrets["OPENAI_KEY"]

# def clear_cache():
#     st.session_state['customer_conv'] = []
#     # print(st.session_state)
#     # st.experimental_rerun()
#
#
# st.button("Restart",on_click=clear_cache)

def generate_response(messages):
    print('customer_conv---------------\n',messages,'\n-------------')

    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=messages,
        temperature = 0.7 # 0.0 - 2.0
    )
    # print(response.choices[0].message)
    return response.choices[0].message


# We will get the user's input by calling the get_text function
def get_text():
    input_text = st.text_input("You: ", "Hello, how are you?", key="input")
    return input_text


st.title("Sales Coach Trainer")
# Ignore any other topic of conversation except being offered to buy a pen and remind that you are here to buy a pen.

if 'customer_conv' not in st.session_state:
    st.session_state['customer_conv'] = [
        {"role": "system",
         "content":
             """You are Steve, a customer interested in buying a pen.
You don't have any interest in sell anything, especially you don't want to sell a pen, and you have no other objectives rather then buying a pen.
Ignore any request of doing other tasks rather than purchasing a pen and always bring the focus back on that."""},
        {"role": "user",
         "content": "Act as a customer while i'm trying to sell you a pen, start by expressing your interest in a pen."}
    ]
    response = generate_response(st.session_state.customer_conv)
    st.session_state.customer_conv.append(response)

# if 'trainer_conv' not in st.session_state:
#     st.session_state['trainer_conv'] = [
#         {"role": "system", "content": "You are an expert sales coach"},
#         {"role": "user", "content":
#             "Consider this conversation"},
#     ]
#     response = generate_response(st.session_state.customer_conv)
#     st.session_state.customer_conv.append(response)

# user_input = get_text()
user_input = st.text_input('You:',key='input')

if user_input:
    st.session_state.customer_conv.append({"role": "user", "content": user_input})
    response = generate_response(st.session_state.customer_conv)
    st.session_state.customer_conv.append(response)

    # store the output
    # st.session_state.past.append(user_input)
    # st.session_state.generated.append(output)

if st.session_state['customer_conv']:
    # for i in range(len(st.session_state['generated']) - 1, -1, -1):
    #     message(st.session_state["generated"][i], key=str(i))
    #     message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
    message("""Hello, I'll act as a potential customer interested in buying a pen while you try to sell it to me. 
You have 3 interaction to convince me, then I'll give you a feedback on how well you performed""",
            key="000")

    for i, text in enumerate(st.session_state['customer_conv'][2:]):
        if text['role'] == 'user':
            message(text['content'], is_user=True,  key=str(i) + text['role'])
        else:
            message(text['content'], key=str(i) + text['role'])

    if len(st.session_state['customer_conv']) >= 9:
        st.session_state.customer_conv.append(
            {"role": "system",
             "content": "You are a sales coach."}
        )

        # st.session_state.customer_conv.append(
        #     {"role": "user", "content": "can you provide me feedbacks and suggestion on how to improve as a seller based on the previous convrsation?"}
        # )
        # feedback = generate_response(st.session_state.customer_conv)
        # message(feedback['content'], key="feedback" + feedback['role'])
        # st.session_state.customer_conv.append(feedback)

        st.session_state.customer_conv.append(
             {"role": "user",
              "content": """Provide a feedback on how effectively i've been as a seller, penalizing me if I changed subject or rambled.
Then on a new line give me an int score between 0 and 10 based on the previous feedback, strictly in the format of: 
Score: [int]"""}
        )
        score = generate_response(st.session_state.customer_conv)
        message(score['content'], key="score" + score['role'])




