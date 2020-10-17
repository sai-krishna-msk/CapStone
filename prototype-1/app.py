import streamlit as st
import numpy as np
import pandas as pd
import os


QUESTIONS_FILE = "questions.txt"
ANSWER_DOCS = "asnwer_docs/"
SESSION_FILE = "session.txt"
files = list()

st.title('Evaluation Assistant')

with open(SESSION_FILE, "r") as f:
    curr_session = int(f.read())



for filename in os.listdir(ANSWER_DOCS):
    files.append(ANSWER_DOCS+filename)
    

with open(QUESTIONS_FILE) as input:
    questions_list = input.read().split("\n")



st.header("Answer Paper")
with open(files[curr_session]) as f:
    st.write(f.read())


for question in questions_list:
    st.sidebar.text_input("",question)
    st.sidebar.text("Answer appears here")


def write_session(curr_session):
    with open(SESSION_FILE, "w") as f:
        f.write(str(curr_session))



col1, col2 = st.beta_columns(2)
back_bool = col1.button("back")
next_bool = col2.button("next")
if(back_bool):
    if(curr_session==0):
        st.text("This is the first file")
    else:
        curr_session-=1
        write_session(curr_session)


if(next_bool):
    if(next_bool==len(files)-1):
        st.text("This si the last file")
    else:
        curr_session+=1
        write_session(curr_session)

