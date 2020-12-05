import streamlit as st
import numpy as np
import pandas as pd
import os


from constants import QUESTIONS_Dir, ANSWER_Dir, QUESTIONS_File, SUB_Question_File, SCORE_Dir, IDEAL_Dir , SESSION_File


from helper import write_session ,init_variables,update_score, estimate_similarity, get_key, highlight_text, add_ideal_answer



if __name__=='__main__':



    (curr_question_num, curr_student_num,curr_question,curr_student, curr_question_text ,
     questions, answer_files,  curr_answer, subquestions_list,curr_score )= init_variables()




    selected_question = st.sidebar.selectbox(
    "Select the question ?",
    (questions.pop(curr_question_num), *questions)
    )

    selected_question_num = int(selected_question.split("Q")[1])-1




    

    st.title('Evaluation Assistant')
    reg_num = curr_student.split(".")[0]
    st.subheader(f"{reg_num}")
    
    st.header(f"Q) {curr_question_text}")
    
    
    keys = list()
    print(subquestions_list, curr_answer)
    for question in subquestions_list:
        resp = get_key(question , curr_answer)
        keys.append(curr_answer[ resp["start"]:resp["end"]+1 ])
        curr_answer = highlight_text(curr_answer, resp['start'], resp['end'])
      


    st.write(curr_answer)

    add_to_ideal = st.sidebar.button("Add to Ideal Answer")

    if(add_to_ideal):
        add_ideal_answer(IDEAL_DIR, curr_answer)

    for question, key in zip(subquestions_list, keys):
        st.sidebar.text_input("",question)
        st.sidebar.write(key)


    

    st.markdown("___")
    col21, col22 = st.beta_columns(2)

    semantic_sim_socre = round(estimate_similarity(QUESTIONS_Dir, curr_question, IDEAL_Dir, curr_answer)*100, 2)
    col21.markdown(f"*Semantic Similarity Score **{semantic_sim_socre}%** *")


    if(curr_score):
        updated_score = col22.number_input('Insert a number', value = float(curr_score))

    else:
        updated_score = col22.number_input('Insert a number')

    if(updated_score and updated_score!=curr_score):
        update_score(QUESTIONS_Dir, curr_question, SCORE_Dir, curr_student , updated_score)




    col1, col2 = st.beta_columns(2)
    back_bool = col1.button("back")
    next_bool = col2.button("next")

    if(back_bool):
        if(curr_student_num==0):
            st.text("This is the first file")
        else:
            curr_student_num-=1
            write_session(SESSION_File, curr_student_num, selected_question_num)

    if(next_bool):
        if(curr_student_num==len(answer_files)-1):
            st.text("This is the last file")
        else:
            curr_student_num+=1
            write_session(SESSION_File, curr_student_num, selected_question_num)

    if(selected_question_num!=curr_question_num):
        write_session(SESSION_File, curr_student_num, selected_question_num)



        