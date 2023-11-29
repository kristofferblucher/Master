from flask import Flask, render_template, request, redirect, url_for
from OpenAiKey import OPENAI_API_KEY
import openai as ai

from debater_python_api.api.debater_api import DebaterApi
from DebaterApi_key import DebaterApiKey
from debater_python_api.api.sentence_level_index.client.sentence_query_base import SimpleQuery
from debater_python_api.api.sentence_level_index.client.sentence_query_request import SentenceQueryRequest

#import api key
ai.api_key = OPENAI_API_KEY
debater_api = DebaterApi(DebaterApiKey)

index_searcher_client = debater_api.get_index_searcher_client()
query = SimpleQuery(is_ordered=False, window_size=10)   


app = Flask(__name__)

@app.route('/')
@app.route('/startside')
def startside():
    return render_template('startside.html')

@app.route('/verktøy',methods=['GET', 'POST'])
def støtteverktøy():
    global tema
    if request.method=='POST':
        print(request.form.get("mycheckBox"))
        tema = request.form.get("mycheckBox")
        return redirect(url_for('setninger'))
    return render_template('verktøy.html')


@app.route('/verktøy/setninger',methods=['GET', 'POST'])
def setninger():
    if request.method == 'GET':
        if tema == "Doping i sport":
            query.add_concept_element(['Doping','Doping in sport'])   
            query.add_normalized_element(['steroids', 'football','testostorone'])   
            query.add_type_element(['Sentiment'])   
            query_request = SentenceQueryRequest(query=query.get_sentence_query(), size=8, sentenceLength=(7, 60))   
            sentences = index_searcher_client.run(query_request)
            for sentence in sentences:
                print(sentence) 
        if tema == "Abort":
            query.add_concept_element(['Abortion','Abortion debate'])   
            query.add_normalized_element(['controversy', 'kids','debate'])   
            query.add_type_element(['Sentiment'])   
            query_request = SentenceQueryRequest(query=query.get_sentence_query(), size=8, sentenceLength=(7, 60))   
            sentences = index_searcher_client.run(query_request)
            for sentence in sentences:
                print(sentence)

    return render_template('setninger.html')


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





