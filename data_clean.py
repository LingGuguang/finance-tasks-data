
from utils import *
import re
import time

"""
    data from: finance-tasks/Headline
    
    time consumption:88.37561106681824(s)
    count of QA: 92014
    for more data, you need bucket+hash or Vector Database.

    tips: class_id cause duplicate QA.
"""


def clean_query(query:str, id="None"):
    """
        templates:
            Headline: \"{Headline}\" Now answer this question: \"{Question}\" 
            Headline: {Headline}\nQuestion: {Question}
            Please answer a question about the following headline: \"{Headline} \"\n{Question} No or Yes? 
            Read this headline: \"{Headline}\"\nNow answer this question: \"{Question}\"\nOptions:\n- No\n- Yes 
            {Headline}\nQ: {Question}
            Answer a question about this headline:\n{Headline}\n{Question}\nOptions:\n- Yes\n- No 
            {Headline}\n{Question} Yes or No? 
            "{Headline}" {Question}
            Read this headline and answer the question\n{Headline}\n{Question}
            and more ...
    """
    chock_the_head = r"(Given the headline|Headline:|Please answer a question about the following headline:|Read this headline:|Answer a question about this headline:|Read this headline and answer the question)"
    split_from_question = r'(Now answer this question:|Question:|Q:|what is the answer to the question|" )'
    remove_tail = r"(No or Yes?|Options:\n- No\n- Yes|Options:\n- Yes\n- No|Answer:)"
    _strip_regex = '[ ",]*'

    # strip
    query = query.strip().strip(_strip_regex).strip()
    # head strip
    query_without_head = re.split(chock_the_head, query, 1)
    # strip 
    query_without_head = query_without_head[-1].strip().strip(_strip_regex).strip()
    # tail strip 
    query_without_head_tail = re.split(remove_tail, query_without_head, 1)[0].strip().strip(_strip_regex).strip()
    # split headline and question 
    headline_and_question = re.split(split_from_question, query_without_head_tail, 1)
    if "" in headline_and_question or len(headline_and_question) != 3:
        headline_and_question = re.split(r'\n', query_without_head_tail, 1)    
    # strip
    headline, question = headline_and_question[0].strip().strip(_strip_regex).strip(), headline_and_question[-1].strip().strip(_strip_regex).strip()
    
    return (headline, question)


time_start = time.time()
path = "test.json"
raw_data = read_json(path,encoding='utf-8')

cleaned_data_set = set()
for id, data in enumerate(raw_data):
    if id % 500 == 0 :
        print(f"{id}/{len(raw_data)}")
    # basic info
    few_shot_QA = data['input']
    ai_answer = data['options'][data['gold_index']]

    # split few-shot string
    regex = r'(Yes\n\n|No\n\n)'
    QA_split = re.split(regex, few_shot_QA) + [ai_answer]
    
    assert len(QA_split) % 2 == 0, f"id:{id}\ndirty data format:{data['input']}"

    # clean each few-shot string
    QA_pairs_temp = []
    for id in range(0, len(QA_split), 2):
        headline, question = clean_query(QA_split[id], id)
        QA_pairs_temp.append({
            "Headline":headline,
            "Question" : question,
            "Answer" : re.sub("\n\n" , "" , QA_split[id+1])
        })
    
    QA_pairs_temp_set = set(tuple(QA_pair.items()) for QA_pair in QA_pairs_temp)
    cleaned_data_set = cleaned_data_set | QA_pairs_temp_set

cleaned_data = [ {"id":id, **dict(t)} for id, t in enumerate(cleaned_data_set)]
save_json("cleaned_data.json", cleaned_data)

time_end = time.time()
print(f"time:{time_end-time_start}")


        
            
