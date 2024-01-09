from flask import Flask, render_template, request, redirect, url_for, session
from OpenAiKey import OPENAI_API_KEY
import openai 
from funksjoner import translate_to_norwegian, generate_article, translate_to_english, get_evidence_scores, translate_tuple_norwegian,wiki_sentences
from debater_funksjoner import wiki_term_extractor,index_searcher
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
    if request.method == 'POST':
        tema = request.form.get('textarea') 
        tema = translate_to_english(tema)
        print(tema)
        #setninger = wiki_sentences(tema)
        wiki_terms = wiki_term_extractor([tema])
        print(wiki_terms)
        result = index_searcher(wiki_terms,tema)
        print("Her kommer indeksen:",result)
        result = get_evidence_scores(result, tema)
        result = translate_tuple_norwegian(result)
        for sentence, score in result:
            print(f"Setning: {sentence}, Score: {score}")
        
        session['norske_setninger'] = result

        return redirect(url_for("setninger"))

    return render_template('verktøy.html',title="støtteverktøy")


#Her skal egentlig debater generere setningene inni "sentences"-listen, basert på valgt tema fra forrige side
@app.route('/verktøy/setninger',methods=['GET', 'POST'])
def setninger():

    session['generated_article'] = None

    norske_setninger = session.get('norske_setninger', [])
    norske_setninger_med_score = [(sentence, score) for sentence, score in norske_setninger]
        
    selected_sentences= []

    if request.method == 'POST':
        selected_sentences = request.form.getlist('sentence')
        
        if selected_sentences:
            session['selected_sentences'] = selected_sentences
            return redirect(url_for('parametre'))
        
        else:
            selected_sentences = tema
            session['selected_sentences'] = selected_sentences
            return redirect(url_for('parametre'))
        # Prosesser valgte setninger


    return render_template('setninger.html', norske_setninger_med_score=norske_setninger_med_score, selected_sentences=selected_sentences)

#Parametre (litt flere valg for brukeren)
@app.route('/verktøy/setninger/artikkel/parametre', methods=['GET','POST'])
def parametre():
    global antall_ord
    if request.method == 'POST':
        antall_ord = request.form.get('textarea')
        return redirect(url_for('artikkel'))


    return render_template('parametre.html')

#Artikkel og resultat-side
@app.route('/verktøy/setninger/artikkel', methods=['GET'])
def artikkel():
    selected_sentences = session.get('selected_sentences', [])
    generated_article = session.get('generated_article', None)


    if not generated_article or request.method == 'POST':
        if selected_sentences:
            generated_article = generate_article(selected_sentences,word_count=antall_ord)
            session['generated_article'] = generated_article
    
    return render_template('artikkel.html', generated_article=generated_article)



if __name__ == '__main__':
    app.run(debug=True)





