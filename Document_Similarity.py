
import nltk
from nltk.corpus import stopwords
import numpy
from nltk import word_tokenize
from nltk.corpus import wordnet as wn
from nltk.parse.stanford import StanfordDependencyParser
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import re
threshold = 0.40
lmtzr = WordNetLemmatizer()
path_to_jar = 'C:/Users/samar/Downloads/stanford-parser-full-2018-10-17/stanford-parser-full-2018-10-17/stanford-parser.jar'
path_to_models_jar = "C:/Users/samar/Downloads/stanford-english-corenlp-2018-10-05-models.jar"
dependency_parser = StanfordDependencyParser(path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)

#import os
#java_path = "C:/Program Files/Java/jdk1.8.0_191/bin/java.exe"
#os.environ['JAVA_HOME'] = java_path

def removeSigns(str,arrayOfChars):

	charFound = False

	newstr = ""

	for letter in str:
		for char in arrayOfChars:
			if letter == char:
				charFound = True
				break
		if charFound == False:
			newstr += letter
		charFound = False

	return newstr

stops = set(stopwords.words('english'))
adverbs=['RB', 'RBR', 'RBS']
adjectives=['JJ', 'JJR', 'JJS']
nouns=['NN','NNP','NNS','NNPS']
verbs=['VB','VBD','VBG','VBN']
l=[]
def preprocessing(k):
	fl={}
	for j in l[k]:
		fl={}
		len_list=len(l[k][j])
		l[k][j].sort()
		cn=1
		if(len(l[k][j])==1):
			fl[l[k][j][0]]=1
		if(len(l[k][j])>0):
			tmp=l[k][j][0]
		for i in range(1,len_list):
			if(l[k][j][i]==l[k][j][i-1] and i!=len_list-1):
				cn+=1
			elif(i==len_list-1):
				if(l[k][j][i]==l[k][j][i-1]):
					cn+=1
					fl[tmp]=cn
				else:
					fl[tmp]=cn
					fl[l[k][j][i]]=1
			else :
				fl[tmp]=cn
				tmp=l[k][j][i]
				cn=1
		l[k][j]=fl

def doc_simi():
	count_simi = 0
	count_all = 0
	i=1
	#print l
	pair=0
	for j in l[0]: #document 0

		for k in l[1]: #document 1
			if j.lower()==k.lower(): # subject equality
				for n in l[0][j]:
					flag = 0
					wd=''
					for m in l[i][k]:
						x=n
						y=m
						if(x==y and l[0][j][x]!=0 and l[1][k][y]!=0):
							wd=y
							break
						max=0
						if l[0][j][x]==0 or l[1][k][y]==0 :
							continue
						p1 = wn.synsets(x)
						p2 = wn.synsets(y)
						if len(p1) == 0 or len(p2) == 0:
							continue
						if p1[0].wup_similarity(p2[0]) > threshold:
							if(p1[0].wup_similarity(p2[0])>max):
								max=p1[0].wup_similarity(p2[0])
								wd=y
					if(wd!=''):
						if(l[0][j][n]>=1):
							l[0][j][n]-=1

						if(l[1][k][wd]>1):
							l[1][k][wd]-=1

						count_simi+=1


	#print count_simi
	return count_simi




def word_to_add(word,tag):
	if tag in adverbs:
		return str(lmtzr.lemmatize(word,pos=wn.ADV))
	elif tag in adjectives:
		return str(lmtzr.lemmatize(word,'a'))
	elif tag in verbs:
		return str(lmtzr.lemmatize(word,'v'))
	else:
		return str(lmtzr.lemmatize(word))

def new_doc_repr(doc,ts):
	f=open(doc+".txt","r")
	l1=f.read()
	l2=nltk.sent_tokenize(l1)
	l3=[]
	m={}
	subj=""
	he=""
	they=""
	list_of_modifiers=['amod','nmod','advmod','conj','root','dobj']

	for sent in l2:
		rc=re.sub('\W+',' ', sent )
		#print rc
		l3=dependency_parser.raw_parse(sent)
		dep = l3.__next__()
		for triple in dep.triples():
			if(triple[1]=='nsubj'):

				if(triple[2][0]=='I' or triple[2][0]=='We'):
					subj='author'
				elif(triple[2][1]=='NN'or triple[2][1]=='NNP' or triple[2][1]=='NNS'):
					subj=str(triple[2][0])
					he=subj
					if triple[2][0] in m :
						li = m[triple[2][0]]
						del(m[triple[2][0]])
						temp=[]
						if str(triple[0][0]).lower() not in stops:
							temp.append(word_to_add(str(triple[0][0]),str(triple[0][1])))

						li += temp
						m[str(triple[2][0])] = li
					else:

						temp=[]
						if str(triple[0][0]).lower() not in stops:
							temp.append(word_to_add(str(triple[0][0]),str(triple[0][1])))
							m[str(triple[2][0])]=(temp)
				else:

					if he in m :
						li = m[he]
						del(m[he])
						temp=[]
						if str(triple[0][0]).lower() not in stops:
							temp.append(word_to_add(str(triple[0][0]),str(triple[0][1])))
						li += temp
						m[he] = li
					else:
						temp=[]
						if str(triple[0][0]).lower() not in stops:
							temp.append(word_to_add(str(triple[0][0]),str(triple[0][1])))
							m[he]=temp



			elif(triple[1]=='nsubjpass'):

				for tckycase in dep.triples():
					if(tckycase[1]=='nmod' or tckycase[1]=='dobj'):
						if(tckycase[2][0]=='me' or tckycase[2][0]=='us'):
							subj='author'

						if(tckycase[2][1]=='NN'or tckycase[2][1]=='NNP' or tckycase[2][1]=='NNS'):
							subj=str(tckycase[2][0])
							he=subj

						temp=[]
						if str(triple[2][0]).lower() not in stops:
							temp.append(word_to_add(str(triple[2][0]),str(triple[2][1])))
							m[str(tckycase[2][0])]=(temp)


							if str(tckycase[0][0]).lower() not in stops:
								temp.append(word_to_add(str(tckycase[0][0]),str(tckycase[0][1])))
								m[str(tckycase[2][0])]=(temp)

			elif(triple[1] in list_of_modifiers):

				if subj in m :
					li = m[subj]
					del(m[subj])
					temp=[]
					if str(triple[2][0]).lower() not in stops :
						temp.append(word_to_add(str(triple[2][0]),str(triple[2][1])))

						if str(triple[0][0]).lower() not in stops:
							temp.append(word_to_add(str(triple[0][0]),str(triple[0][1])))
					li += temp
					m[str(subj)] = li
					continue
				else:
					temp=[]
					if str(triple[2][0]).lower() not in stops:
						temp.append(word_to_add(str(triple[2][0]),str(triple[2][1])))

						if str(triple[0][0]).lower() not in stops:
							temp.append(word_to_add(str(triple[0][0]),str(triple[0][1])))
						m[str(subj)]=temp




	"""for i in m:
		st=set(m[i]);
		m[i]=list(st); 
		#print i +" "+str(m[i])+" "+str(len(m[i]))
		"""

	l.append(m)
	print(m)

	preprocessing(ts)


def calc_percent():
	#myfile = open("inpute.txt","r")
	#lines = myfile.readlines()
	#print lines


	#for i in lines:
	#i=i[0:len(i)-1]
	#new_doc_repr("//home//bip//taske//"+i,0)
	new_doc_repr("doc1",0)
	new_doc_repr("doc2",1)
	#new_doc_repr("orig_taske",1)
	m=l[0]
	first_sz=0
	for tx in m:
		first_sz = first_sz +(len(m[tx]))
	#print first_sz
	#print i
	sim=doc_simi()
	#print sim
	print(l)
	print(sim*(1.0)/first_sz*100)
	l[:] = []

calc_percent()
