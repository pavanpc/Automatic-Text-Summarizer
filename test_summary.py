import unittest
import time
import warnings 
import re
import summary_generator

"""
	Test class to cover unit tests on all methods of summary_generator class 

	It uses pyunit/ unitest module and its test_suites features
"""

class TestDocumentSummarizer(unittest.TestCase):

	def setUp(self):
         self.doc_sum = summary_generator.DocumentSummarizer()
         self.document= self.doc_sum.read_document('document.txt')
         self.sentences = self.doc_sum.generate_sentences(self.document)
         self.sentences_ranks_dictionary = self.doc_sum.rank_sentences(self.sentences)
         self.query= "deep dish pizza"

	def test_read_document(self):
		# assert when document is not read properly
		content= self.doc_sum.read_document('document.txt')
		assert len(content) !=0, "Should have returned document content" 

	def test_remove_stop_words(self):
		# When stop words not removed
		text_with_stop_words= self.doc_sum.read_document('tests/test_remove_stop_words_doc.txt')
		text_without_stop_words= self.doc_sum.remove_stop_words(text_with_stop_words.split())
		self.assertEqual (['People', 'use', 'Yelp', 'search', 'everything', "city's", 'tastiest', 'burger', 'renowned', 'cardiologist'],text_without_stop_words, "Stop words are not removed")

	def test_paragragh_generator(self):
		#When paragraphs are not generated
		paragraphs_content= self.doc_sum.read_document('tests/test_paragragh_generator_doc.txt')
		paragraphs_list=self.doc_sum.paragragh_generator(paragraphs_content)
		self.assertEqual( len(paragraphs_content.split("\n\n")) , len(paragraphs_list), "Paragraphs are not generated properly!!")


	def test_sentence_tokenizer(self):
		# Check if sentences are generated properly
		content= self.doc_sum.read_document('tests/test_sentence_tokenizer_doc.txt')
		self.assertEqual ([''], self.doc_sum.sentence_tokenizer(self.doc_sum.read_document('tests/empty_doc.txt')), "Should have returned empty array of tokens" )
		self.assertEqual (['The feeling of unboxing is exhilerating.'], self.doc_sum.sentence_tokenizer(self.doc_sum.read_document('tests/test_sentence_tokenizer_doc.txt')), "Should have returned expected array of tokens" )
		

	def test_format_sentence(self):
		# Test if special or non alphabetic characters are removed
		content= self.doc_sum.read_document('tests/test_format_sentence_doc.txt')
		self.assertEqual(re.sub(r'\W+', '', content), self.doc_sum.format_sentence(content), "Sentence is not formatted properly")

	def test_get_sentences_similarity_score(self):
		# Check the similarity score generated between sentences
		content= self.doc_sum.read_document('tests/test_get_sentences_similarity_score_doc.txt')
		sentences= self.doc_sum.generate_sentences(content)
		sent1= sentences[0]
		sent2= sentences[1]

		self.assertEqual(1.0, self.doc_sum.get_sentences_similarity_score(sent1,sent2), "Wrong similarity score!!")

	def test_rank_sentences(self):
		# Check if sentences are properly rankes
		content= self.doc_sum.read_document('tests/test_get_sentences_similarity_score_doc.txt')
		sentences= self.doc_sum.generate_sentences(content)
		rank_dict=self.doc_sum.rank_sentences(sentences)

		assert len(rank_dict.keys()) !=0, "Failed to rank sentences" 


	def test_select_best_sentences(self):
		#Check if best sentences are returned
		content= self.doc_sum.read_document('tests/test_get_sentences_similarity_score_doc.txt')
		sentences= self.doc_sum.generate_sentences(content)
		rank_list= self.doc_sum.select_best_sentences(content, {}, 1)
		
		self.assertEqual(0, len(rank_list), "This should have returnes empty list")

	def test_add_highligt_tags_to_summary(self):
		# Check if highlight tags are added properly
		content= self.doc_sum.read_document('tests/test_add_highligt_tags_to_snippet_doc.txt')
		summary_with_tags= self.doc_sum.add_highligt_tags_to_summary(content, "deep dish pizza",'[[HIGHLIGHT]]', '[[ENDHIGHLIGHT]]')
		
		self.assertEqual('[[HIGHLIGHT]]deep dish pizza pizza[[ENDHIGHLIGHT]]', summary_with_tags, "Higlight tags are not added properly!!")

	def test_summary_generator(self):
		# Check if summary can be generated as expected
		content= self.doc_sum.read_document('tests/test_summary_generator_doc.txt')
		query= "deep dish pizza"
		required_summary="My family and I waited about an hour before we were seated.You're gonna be talking pretty loudly to each other the whole time but it might be worth it for some great pizza."
		sentences = self.doc_sum.generate_sentences(content)
		sentences_ranks_dictionary = self.doc_sum.rank_sentences(sentences)
		generated_summary= self.doc_sum.summary_generator(content,query,sentences_ranks_dictionary)
			
		self.assertEqual(required_summary,generated_summary, "Summary generated is not appropriate")

	def test_highlight_doc(self):
		# Check if Highlighted summary can be generated as expected
		content= self.doc_sum.read_document('tests/test_summary_generator_doc.txt')
		query= "deep dish pizza"
		required_summary="My family and I waited about an hour before we were seated.You're gonna be talking pretty loudly to each other the whole time but it might be worth it for some great [[HIGHLIGHT]]pizza[[ENDHIGHLIGHT]]."
		sentences = self.doc_sum.generate_sentences(content)
		sentences_ranks_dictionary = self.doc_sum.rank_sentences(sentences)
		generated_summary= self.doc_sum.summary_generator(content,query,sentences_ranks_dictionary)
		highlighted_summary=self.doc_sum.add_highligt_tags_to_summary(generated_summary,query,'[[HIGHLIGHT]]','[[ENDHIGHLIGHT]]')

		self.assertEqual(required_summary,highlighted_summary, "Summary generated is not appropriate")




def suite():
	suite = unittest.TestSuite()
	suite.addTest(TestDocumentSummarizer("test_highlight_doc"))
	suite.addTest(TestDocumentSummarizer("test_sentence_tokenizer"))
	suite.addTest(TestDocumentSummarizer("test_read_document"))
	suite.addTest(TestDocumentSummarizer("test_remove_stop_words"))
	suite.addTest(TestDocumentSummarizer("test_paragragh_generator"))
	suite.addTest(TestDocumentSummarizer("test_format_sentence"))
	suite.addTest(TestDocumentSummarizer("test_get_sentences_similarity_score"))
	suite.addTest(TestDocumentSummarizer("test_rank_sentences"))
	suite.addTest(TestDocumentSummarizer("test_select_best_sentences"))
	suite.addTest(TestDocumentSummarizer("test_add_highligt_tags_to_summary"))
	suite.addTest(TestDocumentSummarizer("test_summary_generator"))

	return suite

if __name__ == "__main__":
	unittest.TextTestRunner(verbosity=1).run(suite())


        