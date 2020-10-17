import streamlit as st
import numpy as np
import pandas as pd
import os

from constants import QUESTIONS_FILE, ANSWER_DOCS, SESSION_FILE
from helper import write_session ,init_variables



curr_session, curr_answer, questions_list, num_files = init_variables(SESSION_FILE, ANSWER_DOCS, QUESTIONS_FILE)

st.title('Evaluation Assistant')




st.header("Answer Paper")


st.text(curr_answer)



for question in questions_list:
    st.sidebar.text_input("",question)
    st.sidebar.text("Answer appears here")








col1, col2 = st.beta_columns(2)
back_bool = col1.button("back")
next_bool = col2.button("next")

if(back_bool):
    if(curr_session==0):
        st.text("This is the first file")
    else:
        curr_session-=1
        write_session(SESSION_FILE, curr_session)


if(next_bool):

    if(curr_session==num_files-1):
        st.text("This is the last file")
    else:
        curr_session+=1
        write_session(SESSION_FILE, curr_session)






        
