from debater_python_api.api.debater_api import DebaterApi
from debater_python_api.api.sentence_level_index.client.sentence_query_base import SimpleQuery
from debater_python_api.api.sentence_level_index.client.sentence_query_request import SentenceQueryRequest
from debater_python_api.api.sentence_level_index.client.article_retrieval_request import ArticleRetrievalRequest
from DebaterApi_key import DebaterApiKey
from funksjoner import wiki_sentences

debater_api = DebaterApi(DebaterApiKey)


#Extracting wikified titles

def wiki_term_extractor(sentences): 

    wikified_titles = []

    term_wikifier_client = debater_api.get_term_wikifier_client()

    annotation_arrays = term_wikifier_client.run(sentences)

    for annotation_array in annotation_arrays:
            for annotation in annotation_array:
                title = annotation['concept']['title']
                wikified_titles.append(title)

    return wikified_titles




def index_searcher(dc,topic):
    searcher = debater_api.get_index_searcher_client()
    candidates = set()
    query_size = 20

    #Query 1
    query = SimpleQuery(is_ordered=True, window_size=1)
    query.add_concept_element(dc)
    query_request = SentenceQueryRequest(query=query.get_sentence_query(), size=query_size, sentenceLength=(7, 100))
    result = searcher.run(query_request)
    candidates.update(result)

    #Query 2
    query = SimpleQuery(is_ordered=True, window_size=12)
    query.add_normalized_element(['that'])
    query.add_concept_element(dc)
    query_request = SentenceQueryRequest(query=query.get_sentence_query(), size=query_size, sentenceLength=(7, 60))
    candidates.update(searcher.run(query_request))

    #Query 3
    query = SimpleQuery(is_ordered=True, window_size=12)
    query.add_concept_element(dc)
    query.add_type_element(['Causality'])
    query_request = SentenceQueryRequest(query=query.get_sentence_query(), size=query_size, sentenceLength=(7, 60))
    candidates.update(searcher.run(query_request))

    #Query 4
    query = SimpleQuery(is_ordered=False, window_size=7)
    query.add_concept_element(dc)
    query.add_type_element(['Causality', 'Sentiment'])
    query_request = SentenceQueryRequest(query=query.get_sentence_query(), size=query_size, sentenceLength=(7, 60))
    candidates.update(searcher.run(query_request))

    #Query 5
    query = SimpleQuery(is_ordered=False, window_size=60)
    query.add_normalized_element(['observation', 'researches', 'explorations', 'meta - analyses', 'observations',
                                  'documentation', 'exploration', 'studies', 'poll', 'polls', 'meta analyses',
                                  'surveys', 'analyses', 'reports', 'research', 'survey'])
    query.add_normalized_element(['that'])
    query.add_concept_element(dc)
    query_request = SentenceQueryRequest(query=query.get_sentence_query(), size=query_size, sentenceLength=(7, 60))
    candidates.update(searcher.run(query_request))

    #Query 6
    query = SimpleQuery(is_ordered=False, window_size=10)
    query.add_normalized_element(['observation', 'researches', 'explorations', 'meta - analyses', 'observations',
                                  'documentation', 'exploration', 'studies', 'poll', 'polls', 'meta analyses',
                                  'surveys', 'analyses', 'reports', 'research', 'survey'])
    query.add_type_element(['Person'])
    query.add_normalized_element(['that'])
    query.add_concept_element(dc)
    query.add_type_element(['Causality'])
    query_request = SentenceQueryRequest(query=query.get_sentence_query(), size=query_size, sentenceLength=(7, 60))
    candidates.update(searcher.run(query_request))

    candidates_list = list(candidates)

    candidate_motion_pairs = [{'sentence' : candidate, 'topic' :topic } for candidate in candidates_list]
    evidence_scores = debater_api.get_evidence_detection_client().run(candidate_motion_pairs)
    evidence_threshold = 0.5

    evidences = [candidates_list[i] for i in range(len(evidence_scores)) if evidence_scores[i] > evidence_threshold]
    print('Number of evidences: {}'.format(len(evidences)))

    
    return evidences




#Test the queries, with doping in sport as an example topic:
# setninger= wiki_sentences("Doping in sport")
# print(setninger)
# konsepter = wiki_term_extractor(["Doping in sports"])
# print(konsepter)
# results = index_searcher(konsepter,"Doping in sport")
# print(results)

