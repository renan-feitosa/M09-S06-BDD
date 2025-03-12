# API de Integração de Sistema de Gestão de Tarefas

## Estrutura de Integração

### **1. Camadas**
&emsp;&emsp; A integração da API será composta por três camadas principais:

- **Front-end**: 
    - Responsável pela interface do usuário. O usuário interage com a aplicação (web ou mobile), cria, atualiza ou finaliza tarefas.
- **Camada de Aplicação**:
    - Contém a lógica de negócios que gerencia as regras de manipulação de tarefas.
    - Processa as solicitações do usuário, realiza validações, aciona operações no banco de dados e interage com APIs externas, como Google Calendar e e-mail.
- **Camada de Persistência**:
    - Banco de dados relacional ou NoSQL para armazenar dados de usuários, tarefas e status.
    - Utilizando PostgreSQL, MySQL ou MongoDB, por exemplo.

### **2. Módulos e Componentes**
- **Autenticação de Usuário**:
    - Módulo que gerencia o login e a autorização de usuários.
    - Ferramentas de autenticação como OAuth2, JWT ou Auth0.
- **Gerenciamento de Tarefas**:
    - Componente responsável por criar, atualizar, listar e excluir tarefas.
    - Armazena informações como título, descrição, status, data de vencimento, e usuário responsável.
- **Notificações**:
    - Módulo responsável pelo envio de e-mails, notificações push ou mensagens dentro da aplicação, para alertar o usuário sobre o status das tarefas.
    - Ferramentas comuns incluem SendGrid, AWS SES (para e-mails), Firebase Cloud Messaging (para notificações push).
- **Integração com Calendários**:
    - Componente que se conecta ao Google Calendar ou outros calendários externos para sincronizar tarefas com datas específicas.
   
### **3. Serviços**
- **Serviço de Gerenciamento de Tarefas**:
    - Lida com a lógica de criação, edição e remoção de tarefas no banco de dados.
- **Serviço de Autenticação**:
    - Responsável pela autenticação e gerenciamento de sessões de usuário.
- **Serviço de Notificação**:
    - Envia alertas por e-mail ou push para os usuários em caso de novas tarefas, conclusão de tarefas ou lembretes de vencimento.
- **Serviço de Sincronização de Calendário**:
    - Conecta-se ao Google Calendar ou outras APIs de calendário para criar eventos com base nas datas de vencimento das tarefas.

### **4. Hardware e Software**
- **Hardware**:
    - Servidores para hospedar a API, podendo ser provisionados por provedores de cloud computing como AWS (EC2), Google Cloud (Compute Engine) ou Azure.
- **Software**:
    - **Servidor da API**: Express (Node.js), Flask (Python), Spring Boot (Java).
    - **Banco de Dados**: PostgreSQL, MySQL, MongoDB (NoSQL).
    - **Serviços de e-mail**: SendGrid, AWS SES.
    - **Serviços de Notificação**: Firebase Cloud Messaging, Twilio (para SMS), Push Notifications.

### **5. Processos**
- **Criação de Tarefas**: 
    - O usuário cria uma nova tarefa no front-end.
    - A requisição é enviada para a API.
    - A API valida os dados, armazena a tarefa no banco de dados e envia uma notificação de confirmação para o usuário.
- **Atualização de Tarefas**:
    - O usuário pode alterar o status de uma tarefa (por exemplo, marcar como "concluída").
    - A API atualiza o status no banco de dados e envia uma notificação de conclusão.
- **Integração com Calendário**:
    - Quando uma tarefa é criada ou atualizada com uma data de vencimento, a API sincroniza automaticamente com o Google Calendar ou outro serviço de calendário.

<br>

## Código de Controle de Qualidade de Integração

#### **1. Controle de Qualidade (Tempos)**

&emsp;&emsp; O controle de qualidade deve medir os tempos de resposta para garantir que a API seja eficiente e que as requisições sejam processadas dentro de um tempo aceitável. Abaixo está um exemplo de como você pode implementar e monitorar os tempos de resposta da API.

- **Exemplo de código para medir tempo de execução de um endpoint (em Python com Flask)**:

```python
import time
from flask import Flask, jsonify

app = Flask(__name__)

def medida_tempo(func):
    def wrapper(*args, **kwargs):
        inicio = time.time()
        result = func(*args, **kwargs)
        fim = time.time()
        print(f"Tempo de execução: {fim - inicio:.2f} segundos")
        return result
    return wrapper

@app.route('/criar_tarefa', methods=['POST'])
@medida_tempo
def criar_tarefa():
    # Lógica para criar uma tarefa
    return jsonify({"status": "success", "message": "Tarefa criada com sucesso"})

if __name__ == '__main__':
    app.run(debug=True)
```

- **Objetivo**: Registrar o tempo de execução de cada requisição e garantir que o tempo de resposta fique abaixo de um valor aceitável (ex: 2 segundos).

#### **2. Controle de Qualidade (Protocolos e Versões)**

&emsp;&emsp; O controle de protocolos deve garantir que a comunicação entre o front-end e o back-end siga padrões de comunicação definidos (RESTful APIs, por exemplo). Além disso, a versão da API deve ser documentada para facilitar futuras atualizações sem afetar a compatibilidade com versões anteriores.

   - **Exemplo de Especificação de API**:

```yaml
openapi: 3.0.0
info:
  title: "Task Management API"
  description: "API para gerenciamento de tarefas"
  version: "1.0.0"
paths:
  /tasks:
    get:
      summary: "Lista todas as tarefas"
      responses:
        '200':
          description: "Lista de tarefas"
    post:
      summary: "Cria uma nova tarefa"
      requestBody:
        description: "Informações da tarefa"
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                title:
                  type: string
                description:
                  type: string
      responses:
        '201':
          description: "Tarefa criada"
```

   - **Versão da API**: `"version": "1.0.0"`.

#### **3. Controle de Qualidade (Tratamento de Exceções)**

&emsp;&emsp; O tratamento de exceções é essencial para garantir que erros sejam capturados e tratados de maneira adequada, mantendo a experiência do usuário ininterrupta.

- **Exemplo de código para tratamento de exceções**:

```python
from flask import Flask, jsonify

app = Flask(__name__)

class APIError(Exception):
    pass

@app.errorhandler(APIError)
def handle_api_error(error):
    response = jsonify({"error": str(error)})
    response.status_code = 400
    return response

@app.route('/criar_tarefa', methods=['POST'])
def criar_tarefa():
    try:
        data = request.get_json()
        if not data.get('title'):
            raise APIError("Título da tarefa é obrigatório")
        # Lógica para criar a tarefa
        return jsonify({"status": "success", "message": "Tarefa criada com sucesso"})
    except APIError as e:
        raise e
    except Exception as e:
        raise APIError("Erro interno do servidor")

if __name__ == '__main__':
    app.run(debug=True)
```

- **Objetivo**: Capturar erros como ausência de parâmetros obrigatórios (ex: "title") ou falhas inesperadas e retornar mensagens amigáveis para o usuário.

---