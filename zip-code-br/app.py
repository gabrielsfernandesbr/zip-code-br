from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Consulta de CEP</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #00c6ff, #ffff99);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }

        .container {
            background-color: #ffffffcc;
            padding: 30px 40px;
            border-radius: 12px;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
            max-width: 500px;
            width: 90%;
        }

        h2 {
            text-align: center;
            margin-bottom: 20px;
            color: #333;
        }

        form {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        label {
            font-weight: bold;
        }

        input[type="text"] {
            padding: 10px;
            font-size: 1rem;
            border: 1px solid #ccc;
            border-radius: 6px;
        }

        button {
            padding: 10px;
            background-color: #00aaff;
            color: white;
            font-weight: bold;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        button:hover {
            background-color: #008ecc;
        }

        .resultado, .erro {
            margin-top: 20px;
        }

        .resultado ul {
            list-style: none;
            padding: 0;
        }

        .resultado li {
            margin-bottom: 8px;
            color: #333;
        }

        .erro {
            color: red;
            text-align: center;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Consulta de CEP</h2>
        <form method="post">
            <label for="cep">Digite o CEP:</label>
            <input type="text" name="cep" placeholder="Ex: 01001-000" required>
            <button type="submit">Buscar</button>
        </form>

        {% if data %}
        <div class="resultado">
            <h3>Resultado:</h3>
            <ul>
                <li><strong>CEP:</strong> {{ data['cep'] }}</li>
                <li><strong>Logradouro:</strong> {{ data['logradouro'] }}</li>
                <li><strong>Complemento:</strong> {{ data['complemento'] }}</li>
                <li><strong>Bairro:</strong> {{ data['bairro'] }}</li>
                <li><strong>Cidade:</strong> {{ data['localidade'] }}</li>
                <li><strong>Estado:</strong> {{ data['uf'] }}</li>
            </ul>
        </div>
        {% elif error %}
        <p class="erro">{{ error }}</p>
        {% endif %}
    </div>
</body>
</html>
"""

def buscar_cep(cep):
    url = f'https://viacep.com.br/ws/{cep}/json/'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.json()
            if 'erro' not in json_data:
                return json_data, None
            else:
                return None, f"CEP {cep} não encontrado."
        else:
            return None, "Erro ao consultar o serviço ViaCEP."
    except Exception as e:
        return None, f"Ocorreu um erro: {e}"

@app.route('/', methods=['GET', 'POST'])
def index():
    data = None
    error = None

    if request.method == 'POST':
        cep = request.form.get('cep', '').strip().replace('-', '')

        if not cep.isdigit() or len(cep) != 8:
            error = "CEP inválido. Deve conter exatamente 8 números."
        else:
            data, error = buscar_cep(cep)

    return render_template_string(HTML_TEMPLATE, data=data, error=error)

if __name__ == '__main__':
    app.run(debug=True)
