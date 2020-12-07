import streamlit as st
import numpy as np
import pandas as pd
import os

from constants import QUESTIONS_FILE, ANSWER_DOCS, SESSION_FILE, SCORE_FOLDER, IDEAL_DIR
from helper import write_session ,init_variables,update_score, estimate_similarity, get_key, highlight_text, add_ideal_answer



if __name__=='__main__':
    curr_session, curr_answer, questions_list, curr_score,  reg,num_files = init_variables(SESSION_FILE, ANSWER_DOCS, QUESTIONS_FILE, SCORE_FOLDER)


    

    st.title('Evaluation Assistant')
    reg_num = reg.split(".")[0]
    st.subheader(f"{reg_num}")
    
    st.header(f"Q) what is critical section problem and how to solve it ?")
    
    keys = list()
    for question in questions_list:
        resp = get_key(question , curr_answer)
        keys.append(curr_answer[ resp["start"]:resp["end"]+1 ])
        curr_answer = highlight_text(curr_answer, resp['start'], resp['end'])
      

    st.write(curr_answer)

    add_to_ideal = st.sidebar.button("Add to Ideal Answer")

    if(add_to_ideal):
        add_ideal_answer(IDEAL_DIR, curr_answer)

    for question, key in zip(questions_list, keys):
        st.sidebar.text_input("",question)
        st.sidebar.write(key)


    

    st.markdown("___")
    col21, col22 = st.beta_columns(2)

    semantic_sim_socre = round(estimate_similarity(IDEAL_DIR, curr_answer)*100, 2)
    col21.markdown(f"*Semantic Similarity Score **{semantic_sim_socre}%** *")


    if(curr_score):
        updated_socre = col22.number_input('Insert a number', value = float(curr_score))

    else:
        updated_socre = col22.number_input('Insert a number')

    if(updated_socre and updated_socre!=curr_score):
        update_score(SCORE_FOLDER, reg, updated_socre)




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



    # annotated_text(
    # "This ",
    # ("is","","yellow"),
    # " some ",
    # ("annotated", "adj", "#faa"),
    # ("text", "noun", "#afa"),
    # " for those of ",
    # ("you", "pronoun", "#fea"),
    # " who ",
    # ("like", "verb", "#8ef"),
    # " this sort of ",
    # ("thing", "noun", "#afa"),
    # )

    






        
