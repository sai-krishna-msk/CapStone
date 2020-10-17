import os


def get_session(session_file):
    try:
        with open(session_file, 'r') as f:
            return int(f.read())

    except:
        raise Exception("Error reading session file")

def get_answer_files(answer_directory):
    files = []
    for filename in os.listdir(answer_directory):
        files.append(answer_directory+filename)

    return files

def get_questions(question_file):
    with open(question_file) as input:
        questions_list = input.read().split("\n")

    return questions_list

def get_curr_answer(filename):
    with open(filename) as f:
        return f.read()


def write_session(session_file, curr_session):
    with open(session_file, "w") as f:
        f.write(str(curr_session))



def init_variables(SESSION_FILE, ANSWER_DOCS, QUESTIONS_FILE):
    curr_session= get_session(SESSION_FILE)
    answer_files= get_answer_files(ANSWER_DOCS)
    questions_list= get_questions(QUESTIONS_FILE)
    curr_answer = get_curr_answer(answer_files[curr_session])

    return  curr_session, curr_answer, questions_list, len(answer_files)