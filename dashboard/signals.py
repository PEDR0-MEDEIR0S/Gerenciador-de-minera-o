"""
signals.py

Este arquivo contém a definição de sinais que permitem a comunicação entre diferentes partes da aplicação. Os sinais são uma maneira de permitir que um determinado evento ocorra em um local, desencadeando ações em outro, sem a necessidade de acoplamento direto entre os componentes. No contexto deste arquivo, os sinais são usados principalmente para gerenciar eventos relacionados à conexão com o banco de dados.

### Importância
A importância do `signals.py` reside na sua capacidade de implementar lógica de eventos de maneira eficiente e desacoplada. Isso permite que diferentes partes da aplicação respondam a eventos, como a criação de conexões de banco de dados, de forma que o código permaneça modular e organizado. O uso de sinais melhora a manutenção do código e facilita a adição de novos comportamentos sem modificar diretamente o código existente.

### Principais Componentes
Entre os principais componentes implementados neste arquivo, destacam-se:

1. **Função `connection_success(sender, connection, **kwargs)`**: 
   - Esta função é chamada sempre que uma nova conexão com o banco de dados é estabelecida. Ela registra um log informando que a conexão foi criada com sucesso e pode também incluir outras ações, como alertar administradores ou registrar estatísticas.
   - **Parâmetros**:
     - `sender`: O objeto que enviou o sinal.
     - `connection`: A conexão com o banco de dados recém-criada.
     - `**kwargs`: Qualquer outro argumento adicional.

2. **Conexão de Sinais**: 
   - A linha `connection_created.connect(connection_success)` conecta o sinal de criação de conexão com a função `connection_success`, garantindo que esta última seja chamada sempre que um novo evento de conexão ocorrer.

Esse arquivo desempenha um papel fundamental na resposta a eventos do banco de dados, contribuindo para a robustez e a rastreabilidade da aplicação.
"""

import logging

from django.db.backends.signals import connection_created


logger = logging.getLogger(__name__)

# Função que será chamada ao criar a conexão com o banco de dados
def connection_success(sender, connection, **kwargs):
    """
    Função para conectar ao servidor
    """
    print('====================Servidor-em-Uso===================')
    logger.info("Conexão com o banco de dados estabelecida com sucesso!")


# Conecte os sinais às funções
connection_created.connect(connection_success)
