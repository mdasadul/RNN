# Copyright 2016 Scribendi Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Utilities for loading data, tokenizing, vocabularies."""
import nltk
import csv
import itertools
import sys
import re
import numpy as np

# file url we will be reding from HDD
FILE_URL= '/home/developer/Desktop/Downloads/arff/hierarchical/test.tsv'

# Regular expressions used to tokenize.
_WORD_SPLIT = re.compile("([.,!?\"':;)(])")
_DIGIT_RE = re.compile(r"\d")

def read_arff_file():
    """ read arff file
        tokenize by sentence 
        tokenize each sentence by word and append SENTENCE_START and SENTENCE_END token 
    Arg:
       arff file name
     Returns:
        tokenize sentence 
        label
    """
    try:
        arff_file = open(FILE_URL)
    except:
        print file
        print "no such file"
        sys.exit()
    # DEFINE CONSTANTS
    sentence_start_token = "SENTENCE_START"
    sentence_end_token = "SENTENCE_END"
    vocabulary_size = 8000
    unknown_token = "UNKNOWN_TOKEN"    
    sentences =[]
    for line in arff_file:
        if not (line.startswith("@")):
            line=line.split("\',")          
            # Split full comments into sentences
            document = line[0][1:].lower().split('.')
            # Append SENTENCE_START and SENTENCE_END
            
            sentences.append(["%s %s %s" % (sentence_start_token, x, sentence_end_token) for x in document][0])
    print "Parsed %d sentences." % (len(sentences))
                 
    # Tokenize the sentences into words
    tokenized_sentences = [basic_tokenizer(sent) for sent in sentences]
     
    # Count the word frequencies
    word_freq = nltk.FreqDist(itertools.chain(*tokenized_sentences))
    print "Found %d unique words tokens." % len(word_freq.items())
     
    # Get the most common words and build index_to_word and word_to_index vectors
    vocab = word_freq.most_common(vocabulary_size-1)
    index_to_word = [x[0] for x in vocab]
    index_to_word.append(unknown_token)
    word_to_index = dict([(w,i) for i,w in enumerate(index_to_word)])
     
    print "Using vocabulary size %d." % vocabulary_size
    print "The least frequent word in our vocabulary is '%s' and appeared %d times." % (vocab[-1][0], vocab[-1][1])
     
    # Replace all words not in our vocabulary with the unknown token
    for i, sent in enumerate(tokenized_sentences):
        tokenized_sentences[i] = [w if w in word_to_index else unknown_token for w in sent]
     
    print "\nExample sentence: '%s'" % sentences[10]
    print "\nExample sentence after Pre-processing: '%s'" % tokenized_sentences[10]
     
    # Create the training data
    X_train = np.asarray([[word_to_index[w] for w in sent[:-1]] for sent in tokenized_sentences])
    y_train = np.asarray([[word_to_index[w] for w in sent[1:]] for sent in tokenized_sentences])
    
    print X_train[10]
    print y_train[10]
    return X_train,y_train


def basic_tokenizer(sentence):
    """Very basic tokenizer: split the sentence into a list of tokens."""
    words = []
    for space_separated_fragment in sentence.strip().split():
        words.extend(re.split(_WORD_SPLIT, space_separated_fragment))
    return [w for w in words if w]

if __name__=="__main__":
    read_arff_file()