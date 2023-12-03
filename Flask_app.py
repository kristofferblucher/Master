from flask import Flask, render_template, request, redirect, url_for, session
from OpenAiKey import OPENAI_API_KEY
import openai 
from funksjoner import translate_to_norwegian, generate_article, translate_to_english
from debater_python_api.api.debater_api import DebaterApi
from DebaterApi_key import DebaterApiKey
from debater_python_api.api.sentence_level_index.client.sentence_query_base import SimpleQuery
from debater_python_api.api.sentence_level_index.client.sentence_query_request import SentenceQueryRequest

#import api key
openai.api_key = OPENAI_API_KEY
debater_api = DebaterApi(DebaterApiKey)

index_searcher_client = debater_api.get_index_searcher_client()
query = SimpleQuery(is_ordered=False, window_size=10)   


app = Flask(__name__)
app.secret_key = 'Arsenal1886'

@app.route('/')
@app.route('/startside')
def startside():
    return render_template('startside.html')

#Side for å velge tema
@app.route('/verktøy',methods=['GET', 'POST'])
def støtteverktøy():
    global tema
    if request.method=='POST':
        print(request.form.get("mycheckBox"))
        tema = request.form.get("mycheckBox")
        return redirect(url_for('setninger'))
    return render_template('verktøy.html')

#Her skal egentlig debater generere setningene inni "sentences"-listen, basert på valgt tema fra forrige side
@app.route('/verktøy/setninger',methods=['GET', 'POST'])
def setninger():

    session['generated_article'] = None

    sentences = ("Doping has caused a lot of controversy in sports, because it is illegal.", 
                     "In competitive sports, doping is the use of banned athletic performance-enhancing drugs by athletes, and it is seen as a way of cheating.",
                     "Lance Armstrong is a well known doping-case, which caused a lot of controversy and uproar",
                     "Some people actually thinks doping should be allowed in sport, because they feel that would make it a level playing-field for everyone")
        
    norske_setninger = [translate_to_norwegian(sentence) for sentence in sentences]
    selected_sentences= []

    if request.method == 'POST':
        selected_sentences = request.form.getlist('sentence')
        
        if selected_sentences:
            session['selected_sentences'] = selected_sentences
            return redirect(url_for('artikkel'))
        
        else:
            selected_sentences = tema
            session['selected_sentences'] = selected_sentences
            return redirect(url_for('artikkel'))
        # Process selected sentences as needed


    return render_template('setninger.html', norske_setninger=norske_setninger, selected_sentences=selected_sentences)

#Artikkel og resultat-side
@app.route('/verktøy/setninger/artikkel', methods=['GET'])
def artikkel():
    selected_sentences = session.get('selected_sentences', [])
    generated_article = session.get('generated_article', None)


    if not generated_article or request.method == 'POST':
        if selected_sentences:
            generated_article = generate_article(selected_sentences)
            session['generated_article'] = generated_article
    
    return render_template('artikkel.html', generated_article=generated_article)




#Debater setninger
# if tema == "Doping i sport":
        #     query.add_concept_element(['Doping','Doping in sport'])   
        #     query.add_normalized_element(['steroids', 'football','testostorone'])   
        #     query.add_type_element(['Sentiment'])   
        #     query_request = SentenceQueryRequest(query=query.get_sentence_query(), size=8, sentenceLength=(7, 60))   
        #     sentences = index_searcher_client.run(query_request)
        #     for sentence in sentences:
        #         print(sentence) 
        # if tema == "Abort":
        #     query.add_concept_element(['Abortion','Abortion debate'])   
        #     query.add_normalized_element(['controversy', 'kids','debate'])   
        #     query.add_type_element(['Sentiment'])   
        #     query_request = SentenceQueryRequest(query=query.get_sentence_query(), size=8, sentenceLength=(7, 60))   
        #     sentences = index_searcher_client.run(query_request)
        #     for sentence in sentences:
        #         print(sentence)


#ChatGPT
#     if request.method == 'POST': 
#         # Retrieve the text from the textarea 
#         text = request.form.get('textarea') 
#         response = ai.chat.completions.create(
#         model='gpt-4',  # Determines the quality, speed, and cost.
#         messages=[{"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": text}
#             ]
        
#         )
#         print(response)
#         result = response.choices[0].message.content
#         print(text) 
#         print(result)
#         return redirect(url_for("støtteverktøy", result=result))

#     result = request.args.get("result")

#     return render_template('verktøy.html',title="Støtteverktøy",result=result)


if __name__ == '__main__':
    app.run(debug=True)





