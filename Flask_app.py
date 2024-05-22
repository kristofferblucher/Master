from flask import Flask, render_template, request, redirect, url_for, session, flash
import openai
import os
from funksjoner import generate_article, translate_to_english, translate_tuple_norwegian, translate_to_norwegian, split_sentences, translate_list_to_english, finn_bakgrunnsinfo,legg_til_chatgpt
from debater_funksjoner import wiki_term_extractor,index_searcher, get_argument_scores
from debater_python_api.api.debater_api import DebaterApi
from debater_python_api.api.sentence_level_index.client.sentence_query_base import SimpleQuery

#import api keys for debater and openai
open_ai_key = os.environ.get('OPENAI_API_KEY')
debater_key = os.environ.get('DEBATER_API_KEY')
openai.api_key = open_ai_key
debater_api = DebaterApi(debater_key)



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
        tekst = request.form.get('textarea') 
        tema = translate_to_english(tekst)
        print(tema)
        #setninger = wiki_sentences(tema)
        wiki_terms = wiki_term_extractor([tema])
        print(wiki_terms)
        try:
            result = index_searcher(wiki_terms,tema,query_size=20)
        except: 
            flash(f'Feil ved henting av setninger til temaet: "{tekst}".Prøv å omformulere ordet eller setningen litt.', 'error')
            return redirect(url_for('støtteverktøy'))
        
        print("Her kommer indeksen:",result)

        #Legg til Chatgpt på setningene
        result = legg_til_chatgpt(result)

        #Legg til argument-score på setningene
        result = get_argument_scores(result, tema)
        result = translate_tuple_norwegian(result)
        session.clear()
        for sentence, score in result:
            print(f"Setning: {sentence}, Score: {score}")
        session['norske_setninger'] = result
        session['topic'] = tema
        return redirect(url_for("bakgrunnsinfo"))

    return render_template('verktøy.html',title="støtteverktøy")

#Bakgrunnsinfo
@app.route('/bakgrunnsinfo', methods=['GET','POST'])
def bakgrunnsinfo():
    antall_ord = 300
    tema = session['topic']

    if 'bakgrunnsinfo_en' not in session or request.method == 'POST':
        try: 
            print(tema)
            bakgrunnsinfo = finn_bakgrunnsinfo(tema,word_count=antall_ord)
            session['bakgrunnsinfo_en'] = bakgrunnsinfo
            session['bakgrunnsinfo_no'] = translate_to_norwegian(bakgrunnsinfo)

        except: 
            tema= "Ingen tema"
            bakgrunnsinfo = finn_bakgrunnsinfo(tema,word_count=antall_ord)
            session['bakgrunnsinfo_en'] = bakgrunnsinfo
            session['bakgrunnsinfo_no'] = translate_to_norwegian(bakgrunnsinfo)
    
    return render_template('bakgrunnsinfo.html', bakgrunnsinfo=session['bakgrunnsinfo_no'], bakgrunnsinfo_en=session['bakgrunnsinfo_en'])


#Setninger fra Debater
@app.route('/setninger',methods=['GET', 'POST'])
def setninger():

    #Clear ut setninger i tilfelle det ligger noe her fra før
    session['selected_sentences'] = None

    #Hent setningene og sorter de fra høyest til lavest score
    norske_setninger = session.get('norske_setninger', [])
    print("her er norske setningene:", norske_setninger)
    norske_setninger_med_score = [(sentence, score) for sentence, score in norske_setninger]
    setninger_sortert = sorted(norske_setninger_med_score, key=lambda x: x[1], reverse=True)
    

    selected_sentences= []

    if request.method == 'POST':
        selected_sentences = request.form.getlist('sentence')
        print('VALGTE SETNINGER:', selected_sentences)
        
        if selected_sentences:
            session['selected_sentences'] = selected_sentences
            return redirect(url_for('sekvens'))
        
        else:
            selected_sentences = tema
            session['selected_sentences'] = selected_sentences
            return redirect(url_for('sekvens'))
        # Prosesser valgte setninger

    return render_template('setninger.html', norske_setninger_med_score=setninger_sortert, selected_sentences=selected_sentences)

@app.route('/sekvens', methods=['GET','POST'])
def sekvens():
    
    selected_sentences = session.get('selected_sentences',[])
    tema = session.get('topic',[])

    print(selected_sentences)

    engelske_setninger = translate_list_to_english(selected_sentences)

    print("ALLE SETNINGENE:",engelske_setninger)
    valgte_setninger = get_argument_scores(engelske_setninger,tema)
    valgte_setninger = translate_tuple_norwegian(valgte_setninger)
    

    sekvens_med_score = [(sentence, score) for sentence, score in valgte_setninger]
    print(sekvens_med_score)

    if request.method == 'POST':
        selected_sentences = request.form.getlist('sentence')
        print("HER ER DE VALGTE 1:", selected_sentences)
        session['selected_sentences'] = selected_sentences

        if selected_sentences:
            session['selected_sentences'] = selected_sentences
            return redirect(url_for('likte_setninger'))
        
        else:
            selected_sentences = tema
            session['selected_sentences'] = selected_sentences
            return redirect(url_for('likte_setninger'))
        # Prosesser valgte setninger

    return render_template('sekvens.html',title="sekvens", sekvens_med_score=sekvens_med_score)

#Artikkel og resultat-side
@app.route('/likte_setninger', methods=['GET'])
def likte_setninger():
    "Dette er de setningene du likte:"
    
    return render_template('artikkel.html')



if __name__ == '__main__':
    app.run(debug=True)





