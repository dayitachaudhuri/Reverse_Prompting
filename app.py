import streamlit as st
import json
import random
from Levenshtein import ratio

def get_similarity(str1, str2):
    return ratio(str1, str2) 

# Load prompts and responses from a JSON file
def load_prompts():
    with open("prompts.json", "r") as file:
        return json.load(file)

data = load_prompts()

# Initialize session state if not already set
if "current_question" not in st.session_state:
    st.session_state.current_question = random.choice(list(data.items()))
    st.session_state.answered_correctly = False

def new_question():
    st.session_state.current_question = random.choice(list(data.items()))
    st.session_state.answered_correctly = False

# Extract current question and response
random_prompt, random_response = st.session_state.current_question

# Function to check user's answer
def check_answer():
    user_answer = st.session_state.answer.strip().lower()
    actual_answer = random_prompt.strip().lower()
    similarity = get_similarity(user_answer, actual_answer)
    
    if similarity > 0.5:
        st.session_state.answered_correctly = True
        st.success("✅ Well done! Click 'Next Question' to continue.")
    elif similarity > 0.3:
        st.warning("Too Close!")
    elif similarity > 0.1:
        st.warning("You're in the Right Direction.")
    elif similarity > 0.01:
        st.warning("Good Attempt! Try Again.")
    else:
        st.error(f"❌ Incorrect! Try Again{similarity}.")

# Streamlit UI
st.title("Guess the Prompt Game")
st.subheader("Guess the correct prompt for the given response:")

st.write(f"**Response:** {random_response}")

st.text_input("Your Guess:", key="answer")

col1, col2 = st.columns(2)
with col1:
    st.button("Submit", on_click=check_answer)
with col2:
    st.button("Next Question", on_click=new_question)