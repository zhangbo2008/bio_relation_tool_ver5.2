from flashtext import KeywordProcessor
keyword_processor = KeywordProcessor()
# keyword_processor.add_keyword(<unclean name>, <standardised name>)
# keyword_processor.add_keyword('Big Apple', 'New York')
# keyword_processor.add_keyword('Bay Area')
keyword_processor.add_keywords_from_list(['张某','李某'])
keywords_found = keyword_processor.extract_keywords('ywords_from_list([张某,李某])王某',span_info=True)
print(keywords_found)
keywords_found = keyword_processor.extract_keywords('贴入你要处理的sdfsadf张某,李某,sdfsdfasfasd王某他们杀人了fas]',span_info=True)
print(keywords_found)
# ['New York', 'Bay Area']