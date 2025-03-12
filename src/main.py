import time
from flask import Flask, jsonify, request
from functools import wraps  # Importa o wraps

app = Flask(__name__)

# Função para medir o tempo de execução de cada requisição
def medida_tempo(func):
    @wraps(func)  # Preserva o nome da função original
    def wrapper(*args, **kwargs):
        inicio = time.time()
        result = func(*args, **kwargs)
        fim = time.time()
        print(f"Tempo de execução: {fim - inicio:.2f} segundos")
        return result
    return wrapper

class APIError(Exception):
    pass


@app.errorhandler(APIError)
def handle_api_error(error):
    response = jsonify({"error": str(error)})
    response.status_code = 400
    return response

@app.route('/criar_tarefa', methods=['POST'])
@medida_tempo
def criar_tarefa():
    try:
        data = request.get_json()
        
        if not data.get('title'):
            raise APIError("Título da tarefa é obrigatório")
        
        task = {
            "title": data.get('title'),
            "description": data.get('description', '')
        }
        
        return jsonify({"status": "success", "message": "Tarefa criada com sucesso", "task": task}), 201
    except APIError as e:
        raise e
    except Exception as e:
        raise APIError("Erro interno do servidor")

@app.route('/tarefas', methods=['GET'])
@medida_tempo
def listar_tarefas():
    try:
        tasks = [
            {"title": "Tarefa 1", "description": "Descrição da tarefa 1"},
            {"title": "Tarefa 2", "description": "Descrição da tarefa 2"}
        ]
        return jsonify({"status": "success", "tasks": tasks})
    except Exception as e:
        raise APIError("Erro ao listar tarefas")

if __name__ == '__main__':
    app.run(debug=True)
