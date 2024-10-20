from flask import Flask,render_template,request
from dotenv import load_dotenv
import os
from openai import OpenAI
import json

# Cargar las variables del archivo .env
load_dotenv()
# Obtener la clave de OpenAI
openai_api_key = os.getenv("OPENAI_API_KEY")
# Verifica que la clave se ha cargado correctamente
if openai_api_key:
    print("La clave de OpenAI se ha cargado correctamente.")
else:
    print("Error al cargar la clave de OpenAI.")

client=OpenAI(api_key=openai_api_key)
MODEL='gpt-4-turbo'

def generate_colors(prompt):
    print(f"prompt {prompt}")
    prompt_system="""
    Eres un asistente generador de paletas de colores que responde a indicaciones de texto para paletas de colores. 
    Debes generar paletas de colores que se ajusten al tema, estado de ánimo o instrucciones dadas en la indicación. 
    Las paletas deben tener entre 2 y 8 colores. Los colores deben estar ordenados por tonalidad.

    Formato deseado: un JSON Array con los códigos hexadecimales, solamente los codigos, nada más.

    """

    messages=[
        {'role':'system','content':prompt_system},
        {'role':'user','content':prompt},
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=1,
        max_tokens=200,
        n=1,
        stop=None
    )

    color_list = json.loads(response.choices[0].message.content)
    return color_list

app=Flask(__name__,
          template_folder='templates'
          )

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/paleta", methods=['POST'])
def prompt_to_palette():
    prompt=request.form.get("prompt")
    paleta=generate_colors(prompt)
    return {"colors":paleta}



if __name__ == "__main__":
    app.run(debug=True)