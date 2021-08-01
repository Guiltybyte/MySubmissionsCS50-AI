import nltk
import sys
import os
import string
from math import log

FILE_MATCHES = 1
SENTENCE_MATCHES = 1

def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    name_contents = dict()
    for document in os.scandir(path=directory):
        with open(document.path, "r") as contents:
            name_contents.update({document.name : contents.read()})
    return name_contents

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    to_remove = set(nltk.corpus.stopwords.words("english")) | set(string.punctuation)
    word_tokens = nltk.word_tokenize(document.lower())

    relevant_tokens = [
        token for token in word_tokens if not token in to_remove
        ]
    return relevant_tokens

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    # 1 get set of all words in every doc
    unique_words = set()
    for words in documents.values():
        for word in words:
            unique_words.add(word)

    # 2 for every word, count how many times it appears
    idf_dict = dict()
    for word in unique_words:
        doc_freq = 0
        for doc_body in documents.values():
            if word in doc_body:
                doc_freq += 1
        idf_dict.update({word : log(len(documents) / doc_freq)})

    return idf_dict

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    file_ranks = dict()

    for file_name, words in files.items():
        sum_tf_idf = 0
        for q_word in query:
            sum_tf_idf = idfs[q_word] * words.count(q_word)
        file_ranks.update({sum_tf_idf : file_name})
    return [x[1] for x in sorted(file_ranks.items(), reverse=True)][:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentence_ranks = list()

    for sentence, words in sentences.items():
        query_words = query.intersection(words)

        idf = 0
        for q_word in query_words:
            idf += idfs[q_word]

        num_q_words = 0
        for word in words:
            if word in query_words:
                num_q_words += 1
        q_term_density = num_q_words / len(words)
        sentence_ranks.append((sentence, idf, q_term_density))

    return [
        x[0] for x in sorted(
            sentence_ranks,
            key=lambda x: (x[1], x[2]),
            reverse=True
        )
    ][:n]

if __name__ == "__main__":
    main()
