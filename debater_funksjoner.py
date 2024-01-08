from debater_python_api.api.debater_api import DebaterApi
from debater_python_api.api.sentence_level_index.client.sentence_query_base import SimpleQuery
from debater_python_api.api.sentence_level_index.client.sentence_query_request import SentenceQueryRequest
from debater_python_api.api.sentence_level_index.client.article_retrieval_request import ArticleRetrievalRequest
from DebaterApi_key import DebaterApiKey
from funksjoner import wiki_sentences

debater_api = DebaterApi(DebaterApiKey)

setninger= wiki_sentences("Doping in sports")


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


# sentences = ['Doping in sport is very illegal, and should be banned', 
#              "EPO or doping is not very good in sports"]

# titles = wiki_term_extractor(sentences)
# print(titles)


