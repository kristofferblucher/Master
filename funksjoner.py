import openai
import re
from OpenAiKey import OPENAI_API_KEY
from DebaterApi_key import DebaterApiKey
from debater_python_api.api.debater_api import DebaterApi

openai.api_key = OPENAI_API_KEY

#Oversettelsesfunksjon norsk til engelsk
def translate_to_english(norwegian_text):
    try:
        response = openai.chat.completions.create(
            model="gpt-4",  # valgte gpt modellen
            messages=[
                {"role": "system", "content": "You are a translation assistant. Translate from Norwegian to English."},
                {"role": "user", "content": norwegian_text}
            ]
        )
        
        translation = response.choices[0].message.content
        return translation
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

#Oversettelsesfunksjon engelsk til norsk
def translate_to_norwegian(english_text):
    try:
        response = openai.chat.completions.create(
            model="gpt-4",  # valgte gpt modellen
            messages=[
                {"role": "system", "content": "You are a translation assistant. Translate from English to Norwegian."},
                {"role": "user", "content": english_text}
            ]
        )
        
        translation = response.choices[0].message.content
        return translation
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


#Function for generating article
def generate_article(chosen_sentences, word_count=300):
    try:

        if isinstance(chosen_sentences, list):
            chosen_sentences = ' '.join(chosen_sentences)
            chosen_sentences = translate_to_english(chosen_sentences)
            
        system_prompt = f"""You are an article generator. Generate a journalistic article based on the given sentences from the user. 
        Include the sentences within the article. The article should be around {word_count} words long. Always include a title for the article as 
        a heading. """

        response = openai.chat.completions.create(
            model="gpt-4",  # valgte gpt modellen
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": chosen_sentences}
            ]

        )

        article = response.choices[0].message.content
        article = translate_to_norwegian(article)
        return article
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_pro_con_scores(arguments_string, topic):
    # Initialize the Debater API
    api_key = DebaterApiKey  # Ensure this is your valid API key
    debater_api = DebaterApi(api_key)

    # Split the string into individual sentences
    # Assuming each argument starts with a number and a dot (e.g., "1. Argument")
    sentences = re.findall(r'\d+\.\s+(.+)', arguments_string)


    # Prepare the data for the Debater API
    sentence_topic_dicts = [{'sentence': sentence, 'topic': topic} for sentence in sentences]

    try:
        # Get pro/con scores
        pro_con_scores = debater_api.get_pro_con_client().run(sentence_topic_dicts)

        # Process and return the results
        results = []
        for sentence, pro_con_score in zip(sentence_topic_dicts, pro_con_scores):
            results.append((sentence['sentence'], round(pro_con_score, 3)))
        return results

    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    
def translate_tuple_norwegian(english_sentences_with_scores):
    translated_sentences_with_scores = []

    for english_text, score in english_sentences_with_scores:
        try:
            response = openai.chat.completions.create(
                model="gpt-4",  # specify the GPT model
                messages=[
                    {"role": "system", "content": "You are a translation assistant. Translate from English to Norwegian."},
                    {"role": "user", "content": english_text}
                ]
            )
            
            translation = response.choices[0].message.content
            translated_sentences_with_scores.append((translation, score))
        except Exception as e:
            print(f"An error occurred while translating '{english_text}': {e}")
            translated_sentences_with_scores.append((english_text, score))  # Keep original text on error

    return translated_sentences_with_scores
