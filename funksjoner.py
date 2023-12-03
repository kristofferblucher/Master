import openai
from OpenAiKey import OPENAI_API_KEY

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
def generate_article(chosen_sentences):
    try:

        if isinstance(chosen_sentences, list):
            chosen_sentences = ' '.join(chosen_sentences)
            chosen_sentences = translate_to_english(chosen_sentences)
            

        response = openai.chat.completions.create(
            model="gpt-4",  # valgte gpt modellen
            messages=[
                {"role": "system", "content": "You are an article generator. Generate an short journalistic article based on the given sentences from user. Include the sentences within the article."},
                {"role": "user", "content": chosen_sentences}
            ]

        )

        article = response.choices[0].message.content
        article = translate_to_norwegian(article)
        return article
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
