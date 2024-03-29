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
        if(os.path.isfile("updated_cache.json") ):
            return

    with open("updated_cache.json", "w") as f:
        json.dump(resp, f)

def cache(func):
    write_results({}, True)

    def wrapper(*args):
        with open("updated_cache.json") as f:
            cache= json.load(f)


        if(args[0] in cache):
            if(args[1] in cache[args[0]]):
                if(args[2] in cache[args[0]][args[1]]):
                    
                    return cache[args[0]][args[1]][args[2]]

                else:
                   
                    cache[args[0]][args[1]][args[2]]= func(*args)
            else:
               
                cache[args[0]][args[1]] = dict() 
                cache[args[0]][args[1]][args[2]]= func(*args)
        else:
            
            cache[args[0]] = dict()
            cache[args[0]][args[1]] = dict()
            cache[args[0]][args[1]][args[2]]= func(*args)




        
        
      
        write_results(cache)
        return cache[args[0]][args[1]][args[2]]



    return wrapper


@cache
def get_key(curr_question_text , curr_answer, subquestion):
    nlp= pipeline("question-answering")
    result = nlp(question=subquestion, context=curr_answer)
    return result

def add_ideal_answer(QUESTIONS_Dir, curr_question, IDEAL_Dir, curr_answer):
    if(not os.path.isdir(QUESTIONS_Dir +"/"+ curr_question+"/"+IDEAL_Dir)): os.mkdir(QUESTIONS_Dir+"/"+curr_question +"/"+IDEAL_Dir)
    ideal_files = os.listdir(QUESTIONS_Dir+"/"+curr_question +"/"+IDEAL_Dir)
    new_ideal_num = len(ideal_files)+1
    with open(QUESTIONS_Dir+"/"+curr_question +"/"+IDEAL_Dir+f"ideal_{new_ideal_num}.txt", "w") as f:
        f.write(curr_answer.replace("**", ""))




# @st.cache(allow_output_mutation=True, suppress_st_warning=True)
def highlight_text(doc, start, end):
    
    return doc[:start]+"**"+doc[start:end+1]+"**"+doc[end+1:]


def add_highlights(curr_answer, highlight_positions):
    # cnt=0

    # for start, end in highlight_positions:
    #     if(cnt>0):
    #         curr_answer = highlight_text(curr_answer, (start+4**cnt), (end+4**cnt))
    #     else:
    #         curr_answer = highlight_text(curr_answer, start, end)

    #     cnt+=1
 
    return curr_answer

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
    stop_words  =  set(stopwords.words())
    tokenizer =  RegexpTokenizer(r'\w+')
    lemmatizer = WordNetLemmatizer()
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
    model = SentenceTransformer('distilbert-base-nli-mean-tokens')
    sent = prepreprocess_text(sent)
    return model.encode(sent)


def calculate_score(ideal_doc, curr_doc):
    ideal_doc_emb, curr_doc_emb = get_emb(ideal_doc), get_emb(curr_doc)
    
    return cosine_similarity([ideal_doc_emb], [curr_doc_emb])[0][0]


def estimate_similarity(QUESTIONS_Dir, curr_question, IDEAL_Dir, curr_doc):
    if(not os.path.isdir(QUESTIONS_Dir +"/"+ curr_question+"/"+IDEAL_Dir)): return None
    ideal_files = os.listdir(QUESTIONS_Dir +"/"+ curr_question+"/"+IDEAL_Dir)
    score = 0
    for files in ideal_files:
        with open(QUESTIONS_Dir +"/"+ curr_question+"/"+IDEAL_Dir+"/"+files) as f:
            text = f.read()
        
        score+=calculate_score(text, curr_doc)

    if(score==0):
        return None
    return score/len(ideal_files)




def init_variables():
    curr_question_num, curr_student_num = get_session(SESSION_File)

    curr_question_num, curr_student_num  , =  int(curr_question_num), int(curr_student_num)

    questions =  get_questions(QUESTIONS_Dir)
  
    answer_files= get_answer_files(QUESTIONS_Dir ,questions[curr_question_num] ,ANSWER_Dir)
    
    curr_question = questions[curr_question_num]
    if(curr_student_num> len(answer_files)-1):
        curr_student_num=0

    curr_student = answer_files[curr_student_num]

    subquestions_list= get_subquestions(QUESTIONS_Dir, curr_question, SUB_Question_File)
    curr_answer = get_curr_answer(QUESTIONS_Dir, curr_question, ANSWER_Dir, curr_student)

    curr_score = read_score(QUESTIONS_Dir, curr_question, SCORE_Dir, curr_student)

    curr_question_text = get_curr_question_text(QUESTIONS_Dir, curr_question)

    return  (curr_question_num, curr_student_num,curr_question,curr_student, curr_question_text, questions, 
                answer_files,  curr_answer, subquestions_list,curr_score)


