#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 16:14:16 2018

@author: yiwenjiang
"""
import xlrd
from rake_nltk import Rake
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import os
import re

# global variables
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

request = ""
flag = 0
dict_total = {}
topic_index = 0
follow_up = {}
follow_term = {}

file_name = ['Captive Insurance Companies State Law Comparison Report',
             'Data Breach Notification State Law Comparison Report',
             'Discrimination, Harassment, and Retaliation State Law Comparison Report',
             'EBEC - Restrictive Covenants State Law Comparison Report',
             'IP - Trade Secret Protection State Law Comparison Report',
             'Leave Law State Law Comparison Report',
             'Medical and Recreational Cannabis Insurance State Law Comparison Report',
             'Restrictive Covenants State Law Comparison Report',
             'Screening and Hiring State Law Comparison Report',
             'Terminations State Law Comparison Report',
             'Trade Secret Protection State Law Comparison Report',
             'Wage and Hour State Law Comparison Report']


for name in file_name:
    # for each file    
    dict_each = {}
    sheet = xlrd.open_workbook(dir_path + "\\data\\" + name + '.xlsx').sheet_by_index(0)

    r_num = sheet.nrows
    c_num = sheet.ncols

    for i in range(0, r_num): # all the rows
        if(sheet.cell_value(i, 0)!=""):
            # it is a question
            if(i+2 < r_num and sheet.cell_value(i+2, 0)==""):
                # has follow up questions
                d = dict_each.setdefault((sheet.cell_value(i, 0), 1), {}) # question-{}
                cur_i = i
                for j in range(2, c_num):
                    d1 = d.setdefault(sheet.cell_value(0, j), {}) # state-{}
                    i = cur_i
                    while(i+1 < r_num):
                        if(sheet.cell_value(i+1, 0)==""):
                            d1.setdefault(sheet.cell_value(i+1, 1), sheet.cell_value(i+1, j))
                            i = i+1
                        else:
                            break
            
            else:   
                # no follow up questions
                d = dict_each.setdefault((sheet.cell_value(i, 0)+" "+sheet.cell_value(i+1, 1), 0), {})
                for j in range(2, c_num):
                    d.setdefault(sheet.cell_value(0, j), sheet.cell_value(i+1,j)) # state -- answer
     
    dict_total.setdefault(topic_index, dict_each)
    topic_index = topic_index + 1
################################### End Load Data ########################################

################################### Estimate Topic ########################################

def que_topic(usrQue):
    os.chdir( dir_path+"\\data\\txtFile")
    listOfFiles = os.listdir("./")
    
    # Get topic keywords. Store in a dictionary of list.
    t = 0  
    topic_key = {}
    query_key = []
    
    for l in listOfFiles:
        topic_key[t] = keyword(readFile(l))
        t += 1
    
    # Get the query keywords. Store in a list.
    query_key = keyword(usrQue)
    
    sim_dict = {}
    
    for i in range(len(topic_key)):
        sim_dict[i] = similarity(topic_key[i], query_key)

    sorted_sim = sort_similarity(sim_dict)
    if(sorted_sim[0][1] == 0):
        return "no" # invalid input
    else:
        return listOfFiles[sorted_sim[0][0]]     

def readFile(l):
    f = open(l, 'rb')
    txtContent = str(f.read())[2:-3]
    return txtContent

# Use rake nltk package to retrieve keywords.
# Stemming the keywords.
# I: Str. O: List.
def keyword(str):
    # Remove stop words, etc.
    r = Rake()
    r.extract_keywords_from_text(str)
    rake_list = list(r.get_word_degrees().keys())
  
    # Special case for topic: remove "xd".
    
    for i in range(len(rake_list)):
        if re.search(r'^xd\d', rake_list[i]):
            rake_list[i] = rake_list[i][3:]
            if len(rake_list[i]) <= 1:
                rake_list[i] = ""
    
    for word in rake_list:
        if re.search(r'^xd\d', word):
            word = word[3:]
            if len(word) <= 1:
                word = ""
                    
    # Stem the list.
    ps = PorterStemmer()
    stemmed_list = []

    for word in rake_list:
        stemmed_list.append(ps.stem(word))
    stemmed_list = list(filter(None, stemmed_list))

    return list(set(stemmed_list))

# Calculate similary between query and topic.
# Use count of same words.
# I: two lists. O: int.
def similarity(ls1, ls2):
    sim = 0
    
    for i in range(len(ls1)):
        if ls1[i] in ls2:
            sim += 1
    
    return sim

# Dictionary sort by value.
# Return list of tupple.
def sort_similarity(dict):
    return [(k, dict[k]) for k in sorted(dict, key=dict.get, reverse=True)]


################################### End Estimate Topic #######################################

################################### Contain State ############################################
def find_state(query):
   states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
        }
   
   state = 'None'
   for (k,v) in states.items():
       if k in query or v in query:
           state = v
   return state

################################### End Contain State #########################################

################################### Estimate Question #########################################
def stem(str):
    stemmed = ""
    ps = PorterStemmer()
    for word in str.split(" "):
        stemmed += ps.stem(word)
    return stemmed
    
#input (string of query input, list of questions)
#output a list of similarity for each questions[1:]
def query_question_sim(usrQue, question_list):   
    #vectoring
     #for i in range(len(question_list)):
     #    question_list[i] = stem(question_list[i])
     question_list.insert(0,usrQue)
     vectorizer = CountVectorizer()
     vector=vectorizer.fit_transform(question_list)
     distance = cosine_similarity(vector[0:1],vector)
     return distance[0][1:].tolist()
 
#input (string of query input, list of questions)
#output largest similarity and its position in the original question list
def find_max_sim(usrQue,question_list):
    results=query_question_sim(usrQue,question_list)
    t = max(enumerate(results),key=(lambda x:x[1]))
    doc_num=t[0]
    simi=t[1]
    #print(doc_num, simi)
    return doc_num


################################### End Estimate Question #####################################

#usrQue = input("\nPlease enter your query (If you want to quit, enter quit):")
# Contains State?
def findanswer(usrQue):
    global follow_up
    global follow_term
    state = find_state(usrQue)
    topic = que_topic(usrQue)

    if topic == 'no':
        return "Sorry we don't have answer for you right now!Please input another question!"
    else:
        topic_index = int(topic.split(".")[0])-1
        # Which question
        topic_questions = dict_total.get(topic_index, {})
        question_list = []
        for question in topic_questions.keys(): # question tuples
            question_list.append(question[0])
        q_l = question_list[:]
        esti_question = q_l[find_max_sim(usrQue, question_list)]
        for question in topic_questions.keys():
            if question[0] == esti_question:
                question_flag = question[1]
    
       
        if(question_flag == 0): # no follow up question, return answer
            return topic_questions.get((esti_question, question_flag), {}).get(state,"Sorry! No answers for this state! Please choose another one:)")
        else: # has follow up question
            follow_up = topic_questions.get((esti_question, question_flag), {}).get(state,{})  # dict {followup questions, answers}
            follow_up_q = follow_up.keys()
            new_qlist = []

            retstr = ""
            con = 1
            for follow_question in follow_up_q:
                if (follow_question!= "Short Answer"):
                    new_qlist.append(esti_question + " " + follow_question)            
                    follow_term.setdefault(con,follow_question)
                    con = con + 1
            new_qlist.append(esti_question)
            n_q = new_qlist[:]
            esti_q = n_q[find_max_sim(usrQue, new_qlist)]
            if esti_q == esti_question: # user did not input follow up
                retstr += "\nShort Answer: " + follow_up['Short Answer'] + "\n"
                retstr += "\nPlease choose one topic from above choices(If enough, press 0):"
                for key, value in follow_term.items():
                    retstr += "\n" + str(key) + ":" + value + "\n"
                return retstr
            else:        
                return "\n"+follow_up[esti_q[esti_q.index("?")+2:]]


def find_followups(qnum):
    global follow_up
    global follow_term
    if qnum == '0':
        return "Thanks! Bye!"
    else:
        if int(qnum) <= len(follow_term):
            return "\n"+follow_term[int(qnum)] +": "+follow_up[follow_term[int(qnum)]]
        else:
            return "Wrong Number!"


