from flask import Flask, render_template, redirect, url_for, request, send_file
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField, SelectField, PasswordField
from wtforms.validators import DataRequired, NumberRange,  URL, Email, Length
from flask_ckeditor import CKEditor, CKEditorField
from flask import session
import json
from openai import OpenAI

client = OpenAI()
clave = "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"

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
ckeditor = CKEditor(app)

class Multicarril(FlaskForm):
    seleccion = SelectField("What do you want to do?", choices=[("Grammar check", "Grammar check"),
                                                                ("Translate to spanish","Translate to spanish"),
                                                                ("Translate to english","Translate to english"),
                                                                ("Summarize","Summarize")])
    
    texto = StringField(label="Inserta el texto", validators=[DataRequired()],render_kw={"style": "color:rgb(157, 6, 6); font-weight: bold;"})
    submit = SubmitField("Enviar")


@app.route("/", methods=["GET","POST"])
def home():
    form = Multicarril()
    if form.validate_on_submit():
        selected_option = form.seleccion
        text = form.texto
        
        prompt = ""
        if selected_option == "Grammar check":
            prompt = f"Improve grammar in this text. Give me only the corrected text in the output\n{text} \n"
        elif selected_option == "Translate to spanish":
            prompt = f"Improve grammar in this text and translate the text to Spanish. Give me only the translated text in the output\n{text} \n"
        elif selected_option == "Translate to english":
            prompt = f"Detect the language, translate to english, improve grammar in this text. Give me only the translated text in the output\n{text} \n"
        elif selected_option == "Summarize":
            prompt = f"Improve grammar in this text and summarize the text. Give me only the text in the output\n{text} \n"
        
        if prompt:

            response = client.completions.create(
                model="gpt-3.5-turbo-instruct",
                prompt=prompt,
                max_tokens=2560,
                temperature=0
                )
            response_json = json.dumps(response, default=lambda o: o._dict_, indent=2)
            parsed_response = json.loads(response_json)
            print("Antes")
            text1 = parsed_response['choices'][0]['text']
            print(text1)
            print("despues")
            session['resultado'] = {"texto": text1, "texto2":text1}

        return redirect(url_for('resultado'))
    return render_template ('index.html', form=form)


@app.route("/resultado", methods=["GET","POST"])
def resultado():
    resultado = session.get('resultado', None)
    return render_template('resultado.html', resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)








