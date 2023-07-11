# -*- coding: utf-8 -*-
"""
Desc: Parse HTML file
refactor the code and have 
post list of html file name
"""
from bs4 import BeautifulSoup
import pickle
import glob
import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

#nltk.download('punkt')
#nltk.download('stopwords')

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

inputDict = {}
sourceType = ["cop", "npq", "npt"]

for i in range(len(sourceType)):
    fDir = 'C:\\Users\\anago\\Documents\\CSCI 496\\AI-for-Good\\parsefile\\htmlfiles\\' + sourceType[i] + '\\*.html'
    fileList = []
    for name in glob.glob(fDir):
        fileList.append(name)
    inputDict[sourceType[i]] = fileList

outputDict = {}
globalArtId = 1
articleDict = {}
for key in inputDict:
    if key == "cop":
        filelist = inputDict[key]
        for j in range(len(filelist)):
            articleDict = {}
            with open (filelist[j], 'r', encoding="utf8") as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
                title = (soup.find("div", {"class":"ArticlePage-main-content"}).find("h1", {"class":"ArticlePage-headline"})).get_text().strip()
                author = (soup.find("div",{"class":"ArticlePage-authorName"}))
                if author != None:
                    if author.find("a") != None:
                        author = (author.find("a").find("span")).get_text().strip()
                    else:
                        author = author.get_text().strip()
                else:
                    author = (soup.find("div", {"class": "ArticlePage-bylineText"}))
                    if author != None:
                        author = author.get_text().strip()
                if author == None:
                    print("no author")
                    print(title)
                dateP = (soup.find("div", {"class":"ArticlePage-datePublished"})).get_text().strip()
                content = (soup.get_text(" ", strip=(True))).lower()
                articleDict["title"] = title
                articleDict["author"] = author[:17]
                articleDict["date"] = dateP
                articleDict["content"] = content
                outputDict[globalArtId] = articleDict
                #dummyGraph["label"] = author + " " + dateP
                globalArtId = globalArtId + 1
    
    if key == "npq":
        filelist = inputDict[key]
        for j in range(len(filelist)):
            articleDict = {}
            with open (filelist[j], 'r', encoding="utf8") as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
                title = (soup.find("div", {"class":"post-title"}).find("h1")).get_text().strip()
                author = (soup.find("div", {"class":"user-data"}).find("h5").find("a")).get_text().strip()
                content = (soup.get_text(" ", strip=(True))).lower()
                dateP = (soup.find("div", {"class":"user-data"}).find("span")).get_text().strip()
                articleDict["title"] = title
                articleDict["author"] = author
                articleDict["date"] = dateP
                articleDict["content"] = content
                outputDict[globalArtId] = articleDict
                globalArtId = globalArtId + 1
                
    if key == "npt":
        filelist = inputDict[key]
        for j in range(len(filelist)):
            articleDict = {}
            with open (filelist[j], 'r', encoding="utf8") as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
                title = (soup.find("div", {"class":"h1 text-black"}))
                
                if title != None:
                    title = title.get_text().strip()
                else:
                    title = (soup.find("div", {"class": "title_ud"}))
                    if title != None:
                        title = title.get_text().strip()
                if title == None:
                   print("no title")
                author = (soup.find("div", {"class":"post-meta"}))
                if author != None:
                    if author.find("a") != None:
                        author = (author.find("a")).get_text().strip()
                    else:
                        author = author.get_text().strip()
                else:
                    author = (soup.find("div", {"class": "author_name_and_date"}))
                    if author != None:
                        author = author.get_text().strip()
                if author == None:
                    author = "no author"
                    print("no author")
                    print(title)
                dateP = (soup.find("div", {"class":"post-meta"}))
                if dateP != None:
                    if dateP.find("time") != None:
                        dateP = (dateP.find("time")).get_text().strip()
                    else:
                        dateP = dateP.get_text().strip()
                else:
                    dateP = (soup.find("div", "author_name_and_date"))
                    if dateP != None:
                        dateP = dateP.get_text().strip()
                if dateP == None:
                    dateP = "no date"
                    print("no date")
                    print(title)
                content = (soup.get_text(" ", strip=(True))).lower()
                articleDict["title"] = title
                articleDict["author"] = author
                articleDict["date"] = dateP
                articleDict["content"] = content
                outputDict[globalArtId] = articleDict
                globalArtId = globalArtId + 1

#removing stop words/common words like the, a, to, etc.
stop_words = set(stopwords.words('english'))

def inNodes(idval, nodes):
    for v in nodes:
        if (idval+1) == v["id"]:
            return 1
    return 0    

def normalize_document(txt, stopwords=stop_words):
    articles = re.sub(r'[^a-zA-Z\s]', '', txt, re.I|re.A)
    tokens = word_tokenize(articles)
    filterto = [token for token in tokens if token not in stopwords]
    redoc = ' '.join(filterto)
    return redoc

arttowords = []

#take the content of each article and normalize it
for art in outputDict:
    arti = outputDict[art]
    arttowords.append(normalize_document(arti["content"]))

#create the tf idf with the TfidfVectorizer fromsklearn
tv = TfidfVectorizer(min_df=0., max_df=1., norm='l2', use_idf=True, smooth_idf=True)
tv_matrix = tv.fit_transform(arttowords)
tv_matrix = tv_matrix.toarray()

#compare the similarities of the articles using the tv matrix in the cosine_similarity
#to create the similarity matrix
similarity_matrix = cosine_similarity(tv_matrix)

graphC = {}
nodes = []
ninfo = {}
info1 = {}
sta = 5

edges = []
info2 = {}

for id1 in range(len(similarity_matrix)):
    ninfo = {}
    nodes = []
    edges = []
    arr1 = similarity_matrix[id1]
    for id2 in range(len(arr1)):
        if id1 != id2:
            simil = arr1[id2]
            if simil > 0.25:
                info1 = {}
                info2 = {}
                #nodes and edges
                info1["id"] = (id2+1)
                artic = outputDict[id2+1]
                info1["value"] = sta
                info1["label"] = (artic["date"]).split()[-1]
                info1["title"] = artic["title"]
                info2["from"] = (id1+1)
                info2["to"] = (id2+1)
                info2["value"] = simil
                info2["title"] = "{} {}".format(simil, "similarities")
                if inNodes((id2+1), nodes) == 0:
                    nodes.append(info1)
                edges.append(info2)
        else:
            info3 = {}
            info3["id"] = (id1+1)
            artic = outputDict[id1+1]
            info3["value"] = sta
            info3["label"] = (artic["date"]).split()[-1]
            info3["title"] = artic["title"]
            nodes.append(info3)
        ninfo["nodes"] = nodes
        ninfo["edges"] = edges
    graphC[id1+1] = ninfo

allgraphs = []
#loop though all the article and assign graph
#1. assign similarity graph back into the main dict
#2 create a list of alll graphs
#3. assign the graph to [{"article_id":1, "graph":1...}...]

for key in outputDict:
    graph = {}
    graph["articleId"] = key
    graph["graph"] = graphC[key]
    allgraphs.append(graph)

for i in outputDict:
   articleDict = outputDict[i]
   articleDict["graph"] = graphC


#create pickle file
filename = 'htmlParsed.pkl'
with open(filename, 'wb') as outfile:
    pickle.dump(outputDict, outfile)
    
    
with open(filename, 'rb') as outfile:
    testoutO = pickle.load(outfile)
