# -*- coding: utf-8 -*-
from __future__ import division  # Python 2 users only
import os
from bs4 import BeautifulSoup
import re
import collections
from sets import Set
 

# Cleans a word by removing special characters from it
def cleanword(word):
  word=word.replace("!", "")
  word=word.replace(".", "")
  word=word.replace(",", "")
  word=word.replace("=", "")
  word=word.replace(":", "")
  word=word.replace("?", "")
  word=word.replace("(", "")
  word=word.replace(")", "")
  word=word.replace("$", "")
  word=word.replace("", "")
  word=word.replace("/", "")
  word=word.replace("]", "")
  word=word.replace("[", "")
  word=word.replace("{", "")
  word=word.replace("}", "")
  word=word.replace("%", "")
  word=word.replace("&", "")
  word=word.replace(";", "")
  word=word.replace("", "")
  word=word.replace("","")
  word=word.replace("|", "")
  word=word.replace("~", "")
  word=word.replace("Â", "")
  word=word.replace("•", "")
  word=word.replace("€", "")
  word=word.replace("â", "")
  word=word.replace(" ", "")
  word=word.replace("<", "")
  word=word.replace(">", "")
  word=word.replace("+", "")
  word=word.replace("\\", "")
  word=word.rstrip()
  word=word.lstrip()

  return word


def makedictionary(spam_directory, ham_directory, dictionary_filename):    
     
  spamfiles = os.listdir(spam_directory)
       
  hamfiles = os.listdir(ham_directory)
     
  dictionary={}
    
  # Read all spam files from the spam directory for building the dictionary
  for filename in spamfiles:
    try:
      # Read the file content
      spamfile = os.path.join(spam_directory, filename)
      f=open(spamfile)
      filedata=f.read()
      f.close()
      filedata=filedata.lower() #taking all the lower cases
      
      # Read the body part of email   
      ind1=filedata.index('\n\n')
      body=filedata[ind1:] 
      body=BeautifulSoup(body).get_text().encode('utf-8')

      # Read the subject part of email
      ind1=filedata.index('subject:')
      ind2=filedata[ind1:].index("\n")
      subject=filedata[(ind1+9):(ind1+ind2)]

      # Read the sender part of email   
      ind1=filedata.index('from:')
      if "<" in filedata[ind1:] and ">" in filedata[ind1:]: #if email sender info is tagged
        ind2=filedata[ind1:].index("<")
        ind3=filedata[ind1:].index(">") 
      else:   #if email sender info is not tagged
        ind2=ind1+5
        ind3=filedata[ind1:].index("\n")     
      sender=filedata[(ind1+ind2+1):(ind1+ind3)]
      
      # Merge the body, subject and sender to get the email string for parsing   
      emailbody = body+"\n"+subject+"\n"+sender
      
      # Get list of words for processing   
      words=re.split(' |; |, |\*|\n|_|-|#|\'|\"|',emailbody)

      finalwordsset = Set()

      # Clean each word of unwanted character and put in a set

      for word in words:
        if any(c.isalpha() for c in word):
          word = cleanword(word)
          if word != "":
            finalwordsset.add(word)       
      
      # Add the word occurrence to dictionary

      for word in finalwordsset:
        if dictionary.has_key(word):
          dictionary[word][0] = dictionary[word][0] + 1
        else:
          dictionary[word]=[1.0, 0.0]
    except:
      pass

  # Read all ham files from the ham directory for building the dictionary as above in case of spam files
  for filename in hamfiles:
    try:
      # Read the file content
      hamfile = os.path.join(ham_directory, filename)
      f=open(hamfile)
      filedata=f.read()
      f.close()
      filedata=filedata.lower() #taking all the lower cases
      
      # Read the body part of email   
      ind1=filedata.index('\n\n')
      body=filedata[ind1:] 
      body=BeautifulSoup(body).get_text().encode('utf-8')

      # Read the subject part of email
      ind1=filedata.index('subject:')
      ind2=filedata[ind1:].index("\n")
      subject=filedata[(ind1+9):(ind1+ind2)]

      # Read the sender part of email   
      ind1=filedata.index('from:')
      if "<" in filedata[ind1:] and ">" in filedata[ind1:]: #if email sender info is tagged
        ind2=filedata[ind1:].index("<")
        ind3=filedata[ind1:].index(">") 
      else:   #if email sender info is not tagged
        ind2=ind1+5
        ind3=filedata[ind1:].index("\n")     
      sender=filedata[(ind1+ind2+1):(ind1+ind3)]
      
      # Merge the body, subject and sender to get the email string for parsing   
      emailbody = body+"\n"+subject+"\n"+sender
      
      # Get list of words for processing   
      words=re.split(' |; |, |\*|\n|_|-|#|\'|\"|',emailbody)

      finalwordsset = Set()

      # Clean each word of unwanted character and put in a set

      for word in words:
        if any(c.isalpha() for c in word):
          word = cleanword(word)
          if word != "":
            finalwordsset.add(word)       
      
      # Add the word occurrence to dictionary

      for word in finalwordsset:
        if dictionary.has_key(word):
          dictionary[word][1] = dictionary[word][1] + 1
        else:
          dictionary[word]=[0.0, 1.0]
    except:
      pass  
     
  # Calculate the spam and ham probability for each word in dictionary
  spamfilecount = len(spamfiles)
  hamfilecount = len(hamfiles)
  for (key, value) in dictionary.iteritems():
    dictionary[key][0] = value[0]/spamfilecount
    dictionary[key][1] = value[1]/hamfilecount    
         
  # Make an ordered dictionary
  ordereddict = collections.OrderedDict(sorted(dictionary.items()))

  # Write this sorted dictionary to file
  wf=open(dictionary_filename, 'word')
  for (key, value) in ordereddict.iteritems():
    wf.write(str(key)+" "+str(value[0])+" "+str(value[1])+"\n")
  wf.close()      
   

def spamsort(mail_directory, spam_directory, ham_directory, dictionary_filename, spam_prior_probability):   
  return
                                             
def main():
  makedictionary('spam', 'easy_ham', 'dictionary.txt')

if __name__ == "__main__":
	main()
