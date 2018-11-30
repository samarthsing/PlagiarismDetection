# PlagiarismDetection
Plagiarism Detection using Symantic Analysis

The code tries to find semantic similarity between two documents. The output of the program gives the similarity in terms of percentage.

Below is the flow of the algorithm. Briefly we can say, tokenization and lemmatization of the important words in the documents are done and then object-action mapping of these words is created for a better representation of the document.  The object-action mapping colloquially means key subjects in the documents mapped to their descriptors like adjectives, adverbs, verbs, etc. Then first while comparing these documents, we first find the common subjects, and then find the similarity between these subjects using their mapped keywords.


![alt text](https://github.com/samarthsing/PlagiarismDetection/blob/master/Code_Flow.jpg)

Stanford Dependency Parser is used, which is state of the art as far as Part of Speech Tagging is concerned. So before running, you need to get the package installed and path_to_jar and path_to_models_jar need to be set.
Also, the semantic similarity is calculated using WUP similarity.
