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
        response = ai.chat.completions.create(
        model='gpt-4',  # Determines the quality, speed, and cost.
        messages=[{"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text}
            ]
        
        )
        print(response)

        result = response.choices[0].message.content

        

        print(text) 
        print(result)
        return redirect(url_for("støtteverktøy", result=result))

    result = request.args.get("result")
    return render_template('verktøy.html',title="Støtteverktøy",result=result)


if __name__ == '__main__':
    app.run(debug=True)





