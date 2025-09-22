from flask import Flask, request
from rag import client, first_agent, generar_prompt


respuesta = ""

def text_to_html(text):
    # Dividir el texto en secciones
    sections = text.strip().split('\n\n')

    # Iniciar el contenido HTML
    html_content =""""""

    # Procesar cada sección
    section_title = sections[0]
    html_content += f"<h2>{section_title}</h2>\n"
    for section in sections[1:-1]:
        lines = section.strip("#*").split('\n')
        if lines:
            html_content += "<ul>\n"
            for line in lines:
                if line.strip("#*"):
                    html_content += f"<li><h3>{line.strip("#*")}</h3></li>\n"
            html_content += f"        </ul>\n"
    html_content += F"<h2 class='fin'>{sections[-1]}</h2>"

    # Cerrar el contenido HTML

    return html_content

def plantilla(respuesta=""):
    html = f"""
        
    <!DOCTYPE html>
        <html lang="es">
        <head>
        <meta charset="utf-8">
        <title>HTML</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 20px;
            }}
            h1 {{
                color: #333;
            }}
            h2 {{
                color: #444;
                border-bottom: 1px solid #ccc;
                padding-bottom: 5px;
            }}
            ul{{
                margin-bottom: 20px;
            }}
            .form-container {{
            background: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 400px;
            }}

            .form-container h2 {{
                margin-top: 0;
                color: #333;
                text-align: center;
            }}

            .form-group {{
                margin-bottom: 20px;
            }}

            .form-group label {{
                display: block;
                margin-bottom: 5px;
                color: #555;
                font-weight: bold;
            }}

            .form-group input {{
                width: 100%;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 4px;
                box-sizing: border-box;
                font-size: 16px;
            }}

            .form-group input:focus {{
                border-color: #007BFF;
                outline: none;
                box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
            }}

            .form-container button {{
                width: 100%;
                padding: 10px;
                background-color: #007BFF;
                color: #fff;
                border: none;
                border-radius: 4px;
                font-size: 16px;
                cursor: pointer;
            }}

            .form-container button:hover {{
                background-color: #0056b3;
            }}
            .fin{{
                color: #444;
                border-top: 1px solid #ccc;
            }}
        </style>
        </head>
        <body>
        <h1>Libro de Relevos</h1>
        <div class="form-container">
        <h2>Hola, ¿que te gustaria saber?</h2>
        <form action="\chat" method=POST>
            <div class="form-group">
                <label for="input-field"></label>
                <input type="text" name="query">
            </div>
            <button type="submit">Enviar</button>
        </form>
        </div>
        {respuesta}
        </body>
        </html>
    """

    return html

app = Flask(__name__)

@app.route('/chat', methods=['GET'])
def queryRelevos():
    return plantilla()

@app.route('/chat', methods=['POST'])
def leerQuery():
    query = request.form['query']
    respuesta = client.beta.conversations.start(
    agent_id=first_agent.id, inputs=generar_prompt(query) 
    )
    
    return plantilla(respuesta = text_to_html(respuesta.outputs[0].content))

if __name__ == "__main__":
    app.run(debug=True, port=8080)