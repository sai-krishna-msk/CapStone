import os
from transformers import pipeline
import streamlit as st
import numpy as np
from nltk import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 
from num2words import num2words
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json
from constants import QUESTIONS_Dir, ANSWER_Dir, QUESTIONS_File, SUB_Question_File, SCORE_Dir, IDEAL_Dir , SESSION_File



def load_assets():
    nlp= pipeline("question-answering")

    return nlp

nlp, model, stop_words, tokenizer, lemmatizer = load_assets(), SentenceTransformer('distilbert-base-nli-mean-tokens'), set(stopwords.words()), RegexpTokenizer(r'\w+'), WordNetLemmatizer()


def get_session(session_file):
    try:
        with open(session_file, 'r') as f:
            session = f.read()

        return session.split(" ")[0], session.split(" ")[1]


    except:
        raise Exception("Error reading session file")


def get_questions(QUESTIONS_Dir):

    questions = []
    for question in os.listdir(QUESTIONS_Dir):
        questions.append(question)

    return questions 

def get_curr_question_text(QUESTIONS_Dir, curr_question,question_file="question.txt" ):
    with open(QUESTIONS_Dir+"/"+curr_question+"/"+question_file) as f:
        return f.read()



def get_answer_files(QUESTIONS_Dir, curr_question ,ANSWER_Dir):
    answer_files=[]
    for answer_file in os.listdir(QUESTIONS_Dir+curr_question+"/"+ANSWER_Dir):
        answer_files.append(answer_file)

    return answer_files


def get_subquestions(QUESTIONS_Dir, curr_question, SUB_Question_File):
    with open(QUESTIONS_Dir+ curr_question+"/"+SUB_Question_File) as inputs:
        subquestions_list = inputs.read().split("\n")

    return subquestions_list

def get_curr_answer(QUESTIONS_Dir ,curr_question,ANSWER_Dir, curr_student):
    with open(QUESTIONS_Dir+ curr_question+ "/"+ANSWER_Dir +curr_student) as f:
        return f.read()


def write_session(SESSION_File, curr_student_num, selected_question_num):
    with open(SESSION_File, "w") as f:
        f.write(str(selected_question_num)+" "+str(curr_student_num))


def getKeywords(KEYWORDS_FILE):
    with open(KEYWORDS_FILE) as f:
        keywords = f.read()

    return keywords.split("\n")



def write_results(resp, first_call=False):
    if(first_call):
        if(os.path.isfile("cache.json") ):
            return

    with open("cache.json", "w") as f:
        json.dump(resp, f)

def cache(func):
    write_results({}, True)

    def wrapper(*args):
        with open("cache.json") as f:
            cache= json.load(f)

        if(str(args) in cache):
            return cache[str(args)]
            
        else:
            cache[str(args)] = func(*args)
            write_results(cache)
            return cache[str(args)]



    return wrapper


@cache
def get_key(question, doc):
    result = nlp(question=question, context=doc)
    return result

def add_ideal_answer(IDEAL_DIR, curr_answer):
    ideal_files = os.listdir(IDEAL_DIR)
    new_ideal_num = int(ideal_files[-1].split("_")[1].split(".txt")[0])+1
    with open(IDEAL_DIR+f"ideal_{new_ideal_num}.txt", "w") as f:
        f.write(curr_answer.replace("**", ""))




# @st.cache(allow_output_mutation=True, suppress_st_warning=True)
def highlight_text(doc, start , end):
    return doc[:start]+"**"+doc[start:end+1]+"**"+doc[end+1:]



def buildAnswer(raw_text, keywords):
    pass


def read_score(QUESTIONS_Dir,  curr_question,SCORE_DIR, reg):
    if(os.path.exists(QUESTIONS_Dir+ curr_question+"/"+ SCORE_DIR+reg)):
        with open(QUESTIONS_Dir+ curr_question+"/"+ SCORE_DIR+reg) as f:
            return f.read()
    else:
        open(QUESTIONS_Dir+ curr_question+"/"+ SCORE_DIR+reg, 'a').close()

    return None

def update_score(QUESTIONS_Dir, curr_question, ANSWER_Dir, curr_student , updated_score):
    with open(QUESTIONS_Dir +"/"+ curr_question+"/"+ANSWER_Dir+"/"+curr_student, 'w') as f:
        f.write(str(updated_score))





def prepreprocess_text(doc):
    filtered_sentence = []
    doc = doc.lower()
    word_tokens = tokenizer.tokenize(doc)
    for word in word_tokens:
        if(word not in stop_words):
            if(word.isdigit()):
                try:
                    word = num2words(word)
                except:
                    pass
            filtered_sentence.append( lemmatizer.lemmatize(word) )
    return (" ".join(filtered_sentence))


def get_emb(sent):
    sent = prepreprocess_text(sent)
    return model.encode(sent)


def calculate_score(ideal_doc, curr_doc):
    ideal_doc_emb, curr_doc_emb = get_emb(ideal_doc), get_emb(curr_doc)
    
    return cosine_similarity([ideal_doc_emb], [curr_doc_emb])[0][0]


def estimate_similarity(QUESTIONS_Dir, curr_question, IDEAL_Dir, curr_doc):
    ideal_files = os.listdir(QUESTIONS_Dir +"/"+ curr_question+"/"+IDEAL_Dir)
    score = 0
    for files in ideal_files:
        with open(QUESTIONS_Dir +"/"+ curr_question+"/"+IDEAL_Dir+"/"+files) as f:
            text = f.read()
        
        score+=calculate_score(text, curr_doc)
    
    return score/len(ideal_files)




def init_variables():
    curr_question_num, curr_student_num = get_session(SESSION_File)

    curr_question_num, curr_student_num  , =  int(curr_question_num), int(curr_student_num)

    questions =  get_questions(QUESTIONS_Dir)
  
    answer_files= get_answer_files(QUESTIONS_Dir ,questions[curr_question_num] ,ANSWER_Dir)
    
    curr_question = questions[curr_question_num]
    curr_student = answer_files[curr_student_num]

    subquestions_list= get_subquestions(QUESTIONS_Dir, curr_question, SUB_Question_File)
    curr_answer = get_curr_answer(QUESTIONS_Dir, curr_question, ANSWER_Dir, curr_student)

    curr_score = read_score(QUESTIONS_Dir, curr_question, SCORE_Dir, curr_student)

    curr_question_text = get_curr_question_text(QUESTIONS_Dir, curr_question)

    return  (curr_question_num, curr_student_num,curr_question,curr_student, curr_question_text, questions, 
                answer_files,  curr_answer, subquestions_list,curr_score)





