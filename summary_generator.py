# coding=UTF-8
from __future__ import division
import re

# This is a simple text highlighting and summarization algorithm 
# Created By :  PavanKumar PC
# Date : October 31, 2014


"""
 Rank based algorithm to summarize the given review/ document.

 Algorithm:

    1. Split the document into sentences

    2. Calculate the similarity score between every pair of sentences (Stored as graph/ matrix with edge waits as scores).
        a. Split each sentence into tokens after removing stop words
        b. Count the number of common words between two sentences (score) ie find intersection (similar to dot product in vector space model)
        c. Normalize the score using below formula
                Norm(s1,s2)= |{w | w in s1 and w in s2}| / ((|s1| + |s2|) / 2)

    3. Calculate rank of a sentence using above score and store it in a dictionary
        Rank(sentence)= Sum of all similartiy score with every other sentence

    4. Split the document into paragraphs.

    5. Sort sentences in every paragraph by rank in decreasing order and select the best N sentences 

    6. Combine the best sentences from all paragraphs and add them to create final summary 



 Why this algorithm works?

    1. Paragraph is a logical unit of the text and cosidered to hold some specific information or context

    2. If two sentences have a common words/ similarity, they probably holds the same information.

    3. If one sentence has a good similarity with many other sentences, 
       it probably holds some information from each one of them- or in other words, this is probably a key sentence in our text!


 OTHER APPROACHES/ALGORITHMS OR EXTENSIONS:

 1. Using Latent Semantic Analysis(LSA) to find similarity between sentences as it captures latent meaning(synonymy)
    unlike naive algorithm which finds common words.
        a. Represent each sentence as a vector and apply Singular Value Decomposition(SVD) and LSA
        b. This gives good results when documents are lengthy and has more sentences(higher dimensions)

 2. Select sentences based on Word frequency. Sentenes with high word frequencies get higher ranks. This might not 
    give accurate results

 3. The graph built can be used with different Centality measures like 
        a. Degree centrality (node with high degree is considered)
        b. Eigen vector Centality 
 
"""


##//////////////////////////////////////////////////////
## Document Summarizer
##//////////////////////////////////////////////////////

class DocumentSummarizer(object):

    def read_document(self, file_name):

        """
         The method reads text/content/review from the file specified

         file_name - File name from which input to be read (string)

        Returns:

          Document/File content (string)
        """
        with open(file_name) as myfile:
            document="".join(line for line in myfile)

        return document

    

    def remove_stop_words(self,text):

        """
         The method removes all stop words from the text. More words can be added to the list
           

         text - Document or Paragraph or Sentence(string)

        Returns:

        A list of words which are not stop words (list)
        """

         # a list of stop words to be removed
        stop_words =  ['a','able','about','across','after','all','almost','also','am','among','an','and','any','are','as','at','be','because','been','but','by','can','cannot','could','dear','did','do','does','either','else','ever','every',
                        'for','from','get','got','had','has','have','he','her','hers','him','his',
                        'how','however','i','if','in','into','is','it','its','just','least','let',
                        'like','likely','may','me','might','most','must','my','neither','no','nor',
                        'not','of','off','often','on','only','or','other','our','own','rather','said',
                        'say','says','she','should','since','so','some','than','that','the','their',
                        'them','then','there','these','they','this','tis','to','too','twas','us',
                        'wants','was','we','were','what','when','where','which','while','who',
                        'whom','why','will','with','would','yet','you','your']

        return [w for w in text if w.lower() not in stop_words]

 
    
    def sentence_tokenizer(self,paragraph):
        """
         The method generates sentences  from the given document or paragraph. The method handles cases of
            a.abreviations
            b. Punctuations like ! , ' , " etc
         New rules can be added and the methos is extendible

         paragraph - Document or Paragraph (string)

        Returns:

        A list of sentences (list)
        """

        sentenceEnders = re.compile(r"""
            # Split sentences on whitespace between them.
            (?:               # Group for two positive lookbehinds.
              (?<=[.!?])      # Either an end of sentence punct,
            | (?<=[.!?]['"])  # or end of sentence punct and quote.
            )                 # End group of two positive lookbehinds.
            (?<!  Mr\.   )    # Don't end sentence on "Mr."
            (?<!  Mrs\.  )    # Don't end sentence on "Mrs."
            (?<!  Jr\.   )    # Don't end sentence on "Jr."
            (?<!  Dr\.   )    # Don't end sentence on "Dr."
            (?<!  Prof\. )    # Don't end sentence on "Prof."
            (?<!  Sr\.   )    # Don't end sentence on "Sr."
            \s+               # Split on whitespace between sentences.
            """, 
            re.IGNORECASE | re.VERBOSE)
        sentenceList = sentenceEnders.split(paragraph)
        return sentenceList


    def generate_sentences(self, content):
        """
         The method generates sentences  from the given document or paragraph. 
        content - Document or Paragraph (string)

        Returns:

        A list of sentences (list)
        """
        return self.sentence_tokenizer(content)

    
    def paragragh_generator(self, content):
        """
         The method generates paragraphs from the given doc. It assumes paragraphs end with \n\n and
         it can be easily extended

        content - Document (string)

        Returns:

        A list of paragraphs (list)
        """

        return content.split("\n\n")

    def format_sentence(self, sentence):
        """
         Format a sentence - remove all non-alphabetic chars from the sentence
         We'll use the formatted sentence as a key in our sentences dictionary
         TODO : This method to be changed so that it can use EMOTICONS which gives some knowledge or context on reviews.

        Args:

        sentence - A sentence in the document (string)

        Returns:

        A Formatted sentence  (string)

        """

        sentence = re.sub(r'\W+', '', sentence)
        return sentence

    
    def get_sentences_similarity_score(self, sentence1, sentence2):

        """
         This function receives two sentences, and returns a score for the intersection between them.
         We just split each sentence into words/tokens, count how many common tokens we have, and 
         then we normalize the result with the average length of the two sentences.
        
         sim(s1, s2) = |{w | w in s1 and w in s2}| / ((|s1| + |s2|) / 2)


        Args:

        sentence1 - A sentence in the document (string)

        sentence2- Some other sentence in the document (string)

        Returns:

        Similarity score between snetence1 and sentence2 (Decimal)

        """

        # split the sentence into words/tokens and remove stop words
        s1 = set(self.remove_stop_words(sentence1))
        s2 = set(self.remove_stop_words(sentence2))

        # If there is not intersection, just return 0
        if (len(s1) + len(s2)) == 0:
            return 0

        # Normalize the result by the average number of words
        return len(s1.intersection(s2)) / ((len(s1) + len(s2)) / 2)

    
    

    
    def rank_sentences(self, sentences):

        """
        The method calculates the rank for every sentence in the dcoument and stores it in the form of a graph/ 2D matrix

        Args:

        sentences - A list of all sentences

        Returns:

        A dictionary containing Key =Sentence and Value= Rank(Sentence)  (Dictionary)

        """

        # Calculate the intersection of every two sentences
        n = len(sentences)
        rank_graph = [[0 for x in xrange(n)] for x in xrange(n)]

        # Below code can be compactly written in one line. For readability written like C or C++ 
        for i in range(0, n):
            for j in range(0, n):
                rank_graph[i][j] = self.get_sentences_similarity_score(sentences[i], sentences[j])

        # Build the dictionary of sentences
        # Score of a sentence =  Sum of all intersection counts
        sentences_ranks_dictionary = {}
        for i in range(0, n):
            score = 0
            for j in range(0, n):
                if i == j:
                    continue
                score += rank_graph[i][j]
            sentences_ranks_dictionary[self.format_sentence(sentences[i])] = score
        return sentences_ranks_dictionary

    
    def select_best_sentences(self, paragraph, sentences_ranks_dictionary, number_of_sentences=1):

        """
        The method generates first N(number_of_sentences) high rank sentences for a given paragraph using  sentences_ranks_dictionary.

        Args:

        paragraph - A Paragraph in the gievn document(string)

        sentences_ranks_dictionary - It contains every sentence and its rank of the entire document (Dictionary). Key= sentence, Value= Rank

        number_of_sentences- It specifies the number of high rank sentences(sorted in decreasing order of rank) required in a given parageaph.
                             It also controls the final summary length. (Integer) 


        Returns:

        A list of first N(number_of_sentences) rank sentences in a given paragraph (list)

        """

        # Split the paragraph into sentences
        sentences = self.generate_sentences(paragraph)

        # Skip Short paragrahs as this might not give enough information
        if len(sentences) < 2:
            return []

        sentences_rank_for_given_paragrah={}

        # # If senetences in this paragraph is found in  sentences_ranks_dictionary add it to local sentences_rank_for_given_paragrah dictionary
        # # use formatted sentence as key in dictionary 
        
        # for s in sentences:
        #     strip_s = self.format_sentence(s)
        #     if strip_s:
        #         if sentences_ranks_dictionary[strip_s] > max_value:
        #             max_value = sentences_ranks_dictionary[strip_s]
        #             best_sentence = s
        #             sentences_rank_for_given_paragrah[strip_s]=sentences_ranks_dictionary[strip_s]


        # # Get first high N (number_of_sentences) rank sentences from local hash
        # # If number_of_sentences==1 it will return the highest rank sentence
        # high_rank_sentences= list(sorted(sentences_rank_for_given_paragrah, key= lambda x:sentences_rank_for_given_paragrah[x], reverse=True))


        # BELOW IS THE COMPACT AND ONE LINER CODE FOR ABOVE CODE SNIPPET

        sentences_rank_for_given_paragrah={ s :sentences_ranks_dictionary[self.format_sentence(s)] for s in sentences if self.format_sentence(s) in sentences_ranks_dictionary}
        high_rank_sentences= list(sorted(sentences_rank_for_given_paragrah, key= lambda x:sentences_rank_for_given_paragrah[x], reverse=True))

        # Get only required number of sentences
        high_rank_sentences= high_rank_sentences[0:number_of_sentences]
        
        return high_rank_sentences


    def add_highligt_tags_to_summary(self, summary,query, start_tag='[[HIGHLIGHT]]', end_tag='[[ENDHIGHLIGHT]]'):

        """
        The method takes start and end tags with default values and adds tags to review summary. 
        The user can pass any highlight tags like <b> </b> etc, so that the code works for any tags.

        Args:

        summary - Review summary generated after appylying ranking algortihm(string)

        query­- The search query(string)

        start_tag- Starting tag with default value [[HIGHLIGHT]] (string) 

        end_tag- Ending tag with default value [[ENDHIGHLIGHT]] (string)

        Returns:

        The final summary with Highlight tags added to query terms (string)

        """
        # split query into words after removing stop words
        query_words_list= self.remove_stop_words(query.split())

        # add tags to induvidual words
        for word in query_words_list:
            summary=summary.replace(word, start_tag+word+ end_tag )

        # this is to remove consecutive tags if added above. Ex: [[HIGHLIGHT]] deep [[ENDHIGHLIGHT]][[HIGHLIGHT]] dish [[ENDHIGHLIGHT]]'
        summary=summary.replace(end_tag+" "+start_tag, ' ')

        return summary


    
    def summary_generator(self, doc,query, sentences_ranks_dictionary):
        """
        The method generates the required review summary. 
        The lenght of it is controlled by the argument(number_of_sentences) in get_high_rank_sentences method


        Args:

        doc­ - Document/review to be shortnened(string)

        query­- The search query(string)

        sentences_ranks_dictionary- Contains ranks of formatted and trimmed sentences (dictionary)

        Returns:

        The most relevant summary (string)

        """


        summary=[]
        best_sentences_containing_query_words=[]



        # Split the document content into paragraphs using below helper method
        paragraphs = self.paragragh_generator(doc)


        # split the query into words after removing stop words
        query_words_list= self.remove_stop_words(query.split())
        query_string_length= len(query)


      
        # Add first N high rank sentences from each paragraph
        # Here N is controlled by arugument to get_high_rank_sentences method
        # Here N=1, the highest rank sentence in each paragraph
        for p in paragraphs:
            sentences_list = self.select_best_sentences(p, sentences_ranks_dictionary, 1)

            for sentence in sentences_list:
                if sentence:
                    # get best sentence containing whole query or induvidual query word
                    if sentence.find(query)!=-1 or  len(set(query_words_list) & set(sentence.strip().split())) > 0 :
                        print "--With words--"
                        best_sentences_containing_query_words.append(sentence)
                    else:
                        # If query words not found add it to another list summary
                        summary.append(sentence) 
                

        
        # Add best sentence with query terms first and append summary list
        # Set is used to include only unique sentences
        final_summary= list(set(best_sentences_containing_query_words+summary))
        final_summary= ("").join(final_summary)

        return final_summary



    
    def highlight_doc(self, doc,query):


        """

        Args:

        doc­ - Document to behighlighted(string)

        query­- The search query(string)

        Returns:

        The most relevant summary with the query terms highlighted(string)

        """

        # Split the content into sentences
        sentences = self.generate_sentences(doc)


        # Build the sentences dictionary which contains ranks of all sentences
        sentences_ranks_dictionary = self.rank_sentences(sentences)

        # Genereate summary for the document and query using sentences_ranks_dictionary
        review_summary= self.summary_generator(doc,query,sentences_ranks_dictionary)

        
        # Highlight the generated summary with highlight tags
        # Here instead of [[HIGHLIGHT]] tag we can send <b> , <i> tags etc
        highlighted_review_summary= self.add_highligt_tags_to_summary(review_summary,query,'[[HIGHLIGHT]]','[[ENDHIGHLIGHT]]')


        return highlighted_review_summary

        
        


# Main method
def main():


    query ="deep dish pizza"

    # Create a DocumentSummarizer object
    doc_sum = DocumentSummarizer()

    document= doc_sum.read_document('document.txt')

    
    # Function signature as mentioned in the question
    highlighted_review_summary= doc_sum.highlight_doc(document,query)

    print highlighted_review_summary


if __name__ == '__main__':
    main()
