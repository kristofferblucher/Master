import openai
import re,os
from debater_python_api.api.debater_api import DebaterApi

#import api keys
open_ai_key = os.environ.get('OPENAI_API_KEY')
debater_key = os.environ.get('DEBATER_API_KEY')
openai.api_key = open_ai_key
debater_api = DebaterApi(debater_key)




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
    
def finn_bakgrunnsinfo(topic, word_count=250):
            
        system_prompt = f"""You are an background discoverer. Find background info on the given topic from the user. 
        Give the user some general facts and knowledge on the topic. The article should be around {word_count} words long. 
        Always include a title for the article as a heading. The heading should be "Background info on" and then the name of the topic. """

        response = openai.chat.completions.create(
            model="gpt-4",  # valgte gpt modellen
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": topic},
            ]

        )

        bakgrunnsinfo_engelsk= response.choices[0].message.content
        return bakgrunnsinfo_engelsk


#Function for generating article
def generate_article(chosen_sentences, word_count=100):
    try:

        if isinstance(chosen_sentences, list):
            chosen_sentences = ' '.join(chosen_sentences)
            chosen_sentences = translate_to_english(chosen_sentences)
            print("This is the chosen sentences:",chosen_sentences)
            
        system_prompt = f"""You are an article generator. Generate a journalistic article based on the given sentences from the user. 
        Include the sentences within the article. The article should be around {word_count} words long. Always include a title for the article as 
        a heading. """

        response = openai.chat.completions.create(
            model="gpt-4o",  # valgte gpt modellen
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": chosen_sentences},
            ]

        )

        article_english = response.choices[0].message.content
        
        return article_english
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_evidence_scores(arguments_list, topic):
    # Initialize the Debater API
    api_key = debater_key # Ensure this is your valid API key
    debater_api = DebaterApi(api_key)

    # Split the string into individual sentences
    # Assuming each argument starts with a number and a dot (e.g., "1. Argument")
    #sentences = re.findall(r'\d+\.\s+(.+)', arguments_string)


    # Klargjør data til Debater API
    sentence_topic_dicts = [{'sentence': sentence, 'topic': topic} for sentence in arguments_list]

    try:
        # Hent evidence scores
        evidence_scores = debater_api.get_evidence_detection_client().run(sentence_topic_dicts)

        # Process and return the results
        results = []
        for sentence, evidence_scores in zip(sentence_topic_dicts, evidence_scores):
            results.append((sentence['sentence'], round(evidence_scores, 2)))
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
                    {"role": "system", "content": """You are a translation assistant. Translate from English to Norwegian. Focus on using norwegian words, 
                    and do not use too direct translation. For example: Translating 'manifesting' to 'manifestere', is too direct."""},
                    {"role": "user", "content": english_text}
                ]
            )
            
            translation = response.choices[0].message.content
            translated_sentences_with_scores.append((translation, score))
        except Exception as e:
            print(f"An error occurred while translating '{english_text}': {e}")
            translated_sentences_with_scores.append((english_text, score))  # Keep original text on error

    return translated_sentences_with_scores

def translate_list_to_english(norske_setninger):

    translations_list = []

    for tekst in norske_setninger:
        try:
            response = openai.chat.completions.create(
                model = "gpt-4",
                messages=[
                    {"role": "system", "content": "You are a translation assistant. Translate from Norwegian to English."},
                    {"role": "user", "content": tekst}
                ]
            )
            
            translation = response.choices[0].message.content
            translations_list.append(translation)


        except Exception as e:
            print(f"An error occurred while translating '{tekst}': {e}")
            translation = response.choices[0].message.contentt
            translations_list.append(translation)
    return translations_list

def wiki_sentences(theme):

    system_prompt = "Generate one argumentative sentence about the theme which is given to you as a input from user. Use maximum 1 words in the sentence. "

    response = openai.chat.completions.create(
            model="gpt-4",  # valgte gpt modellen
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": theme}
            ]

        )
    
    sentences = response.choices[0].message.content
    sentences = sentences.split('\n')
    sentences = [sentence.lstrip('0123456789). ') for sentence in sentences]
    return sentences

def split_sentences(text):
    """
    Takes a string containing one or more sentences and returns a list of sentences.
    Sentences are assumed to end with '.', '!', or '?'.
    """
    import re
    # Split the text into sentences based on '.', '!', or '?' followed by a space or end of string
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])|(?<=[.!?])(?=[A-Z])', text)
    # Filter out any empty strings that might result from the split operation
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    return sentences

def legg_til_chatgpt(argument_liste):
    forbedret_liste= []

    for argument in argument_liste:
        forbedret_setning = forbedre_med_chatgpt(argument)
        forbedret_liste.append(forbedret_setning)
    
    print("Her er den forbedrede listen:", forbedret_liste)

    return forbedret_liste

def forbedre_med_chatgpt(setning):
    try:
         system_prompt = f"""You are an assistant to improve the argumentation quality of the input. 
                 Improve the wording, improve the arguments and use 3 sentences per content from the user. 
                 The arguments are supposed to inspire journalists in their process before writing an article. 
                 Make sure that the sentences makes sense for them, giving them some type of context. Maximum 4 sentences.  """
         
         response = openai.chat.completions.create(
             model="gpt-4",  # valgte gpt modellen
             messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": setning},
            ])
         
         forbedret_setning = response.choices[0].message.content
        
    except Exception as e:
        print(f"An error occurred: {e}")
        forbedret_setning = "Error in improving the sentence."
          
    return forbedret_setning

# def sjekk_om_gyldig_ord(ord):
#     sjekk = enchant.Dict("nb_NO")
#     return sjekk.check(ord)

import openai

def translate_list_with_score_to_english(norske_setninger):
    translations_list = []

    for tekst, score in norske_setninger:
        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a translation assistant. Translate from Norwegian to English."},
                    {"role": "user", "content": tekst}
                ]
            )
            
            translation = response.choices[0].message.content
            translations_list.append((translation, score))

        except Exception as e:
            print(f"An error occurred while translating '{tekst}': {e}")
            translations_list.append((tekst, score))  # Fallback to original sentence in case of error

    return translations_list



