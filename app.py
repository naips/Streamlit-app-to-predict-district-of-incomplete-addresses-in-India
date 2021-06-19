import streamlit as st
import os
from googlesearch import search
import sys
import time
import ssl
from collections import Counter
import re
import pandas as pd
from dictionary import model_dis_to_state
import nltk
#########################################################################################
ssl._create_default_https_context = ssl._create_unverified_context


def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)


local_css("style.css")
 

try:        
    from googlesearch import search
except ImportError: 
    print("No module named 'google' found")
 
stopwords=['mandir',"complex","taluk",'thaluk' ,"taluqa", "tq","branch","town",'thana','lane','br',
           'colony','post','ps','village','distt','dist','ds','dis','distict','di','disst','jila','dsit','village','near','of','off', # 'behind','ta','vil','vill','th','teh','tah','tehsil','ps','new',
           'gram','heera','rani','oppo','opposite','opp','late','mr','mrs','miss','ms'
           'pick','late','basavana','taj','moh','sangam','sarita','qutub','tal','po','pargana']


dislist = model_dis_to_state.keys()
wordlist = []
cmnwords = ['co', 'org','net','of','html','com','in','www','http:','https:','pincode'] # Words to ignore from each search result url

def simillarity(address, match):
    for i,a in enumerate(address):
        for m in match:
            if nltk.edit_distance(a,m) <=2:
                address[i] = m
    return address

##################################################################################################################################3

primary_clr = st.get_option("theme.primaryColor")
txt_clr = st.get_option("theme.textColor")



st.title('District predicting and address correcting app')


st.header('Find Distict and state for an incomplete adress')     

searchstr = st.text_input('Provide your incomplete address')

if searchstr:
    st.write('Address you provided: ', searchstr)


    searchstr = searchstr.split()
    searchstr = list(map((lambda x:x.lower()),searchstr)) # convert argument to lowercase
    wordlist=[]
    for j in search(" ".join(searchstr), num_results=50):
        tmp = re.split("[/,_,\.,-]+",j)
        tmp = list(map(lambda x:x.lower(), tmp))
        tmp = list(filter((lambda x:x not in cmnwords + searchstr), tmp))


        wordlist = wordlist + tmp 

    wordc = Counter(wordlist).most_common(10) #get word frequencies of top 10 words
    wordc = [w[0] for w in wordc]

    correct_add = simillarity(searchstr, wordc)

    problist = []  
    problist2 = None
    state  = None
    data_2 = None
    #for i in sorted(wordc,key=wordc.get, reverse=True):
    for w in wordc:
        if w in dislist:
            print( "Probable distt is:",w.capitalize())
            problist.append(w)

    if len(problist) <= 1: # if only one dist found in top 10, it is certain
        print ("Final distt is:", problist[0].capitalize())
        state = model_dis_to_state[problist[0]].lower()
        print ("Final state is:", state.capitalize())
    else:
        print ("Found more than 1 distt")
        print (problist)
        problist2 = problist[1]

    
    if st.button('Find district name', key=1):
        st.write("District: " + "<font color='blue'> {district} </font>".format(district=problist[0].capitalize()), unsafe_allow_html=True)
    
            
            
    if st.button('Find state name', key=2):
        st.write("State: " + "<font color='blue'> {district} </font>".format(district=state.capitalize()), unsafe_allow_html=True)

    if st.button('Correct the spellings if wrong'):
     #   st.write(' '.join(correct_add))
        t = ' '.join(correct_add) + ' '+problist[0].capitalize() +' '+ state.capitalize()
        st.write('Corrected address: ' + "<font color='blue'> {district} </font>".format(district=t), unsafe_allow_html=True)

