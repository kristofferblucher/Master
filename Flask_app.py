from flask import Flask, render_template, request, redirect, url_for
from OpenAiKey import OPENAI_API_KEY
import openai as ai

#import api key
ai.api_key = OPENAI_API_KEY


app = Flask(__name__)

@app.route('/')
@app.route('/startside')
def startside():
    return render_template('startside.html')

@app.route('/verktøy',methods=['GET', 'POST'])
def støtteverktøy():
    if request.method == 'POST': 
        # Retrieve the text from the textarea 
        text = request.form.get('textarea') 
        response = ai.Completion.create(
        engine='text-davinci-003',  # Determines the quality, speed, and cost.
        temperature=0.5,            # Level of creativity in the response
        prompt=text,                # What the user typed in
        max_tokens=100,              # Maximum tokens in the prompt AND response
        n=1,                        # The number of completions to generate
        stop=None,                  # An optional setting to control response generation
        )

        result = response.choices[0].text
        print(text) 
        print(result)
        return redirect(url_for("støtteverktøy", result=result))

    result = request.args.get("result")
    return render_template('verktøy.html',title="Støtteverktøy",result=result)

if __name__ == '__main__':
    app.run(debug=True)
    
    


