"""
utils.py

Este arquivo contém funções utilitárias que servem como ferramentas auxiliares para o restante da aplicação. O objetivo principal do `utils.py` é fornecer funcionalidades que possam ser reutilizadas em diferentes partes do projeto, promovendo a eficiência e a manutenção do código. Ao centralizar funções comuns em um único local, facilita-se a gestão de mudanças e a reutilização de lógica em diversos contextos.

### Importância
A importância do `utils.py` reside na sua capacidade de encapsular lógica que não se encaixa diretamente nas camadas de apresentação ou de acesso a dados, mas que é essencial para o funcionamento da aplicação. Isso contribui para um código mais limpo e modular, permitindo que desenvolvedores e equipes de desenvolvimento mantenham e escalem o projeto de maneira mais eficaz. Funções bem definidas e documentadas em `utils.py` ajudam a reduzir a duplicação de código e a promover melhores práticas de desenvolvimento.

### Principais Funções
Entre as principais funções implementadas neste arquivo, destacam-se:

1. **arredondar_horario(hora, minuto)**: Arredonda um horário para o múltiplo de 5 minutos mais próximo. Essa função é útil para padronizar horários em análises e relatórios.

2. **arred_time_robos_funcionando(dados)**: Processa os dados dos robôs, arredondando horários e organizando informações em uma estrutura de timeline. Isso facilita a visualização e análise do desempenho ao longo do tempo.

Essas funções são fundamentais para a lógica de manipulação de dados na aplicação, pois ajudam a garantir que os dados sejam apresentados de forma consistente e em conformidade com as regras de negócio. A presença de um arquivo `utils.py` bem estruturado não só melhora a qualidade do código, mas também torna o desenvolvimento mais ágil e organizado.
"""

from datetime import datetime, timedelta

import logging


logger = logging.getLogger(__name__)

# def arredondar_horario(hora, minuto):
#     """
#     Função para arredondar o horário para o múltiplo de 5 minutos mais próximo.

#     Exemplo:
#     - 17:38 será arredondado para 17:35
#     - 17:44 será arredondado para 17:40

#     Parâmetros:
#     - hora (int): A hora no formato 24 horas (0-23).
#     - minuto (int): O minuto (0-59).

#     Retorno:
#     - datetime.time: O horário arredondado no formato de objeto time.

#     Exceções:
#     - `ValueError`: Se os parâmetros `hora` ou `minuto` estiverem fora dos limites esperados.
#     - `TypeError`: Se os parâmetros não forem do tipo esperado (int).

#     Notas:
#     - Foi compreendido que o javascript desenvolveria melhor esta função, então ela não esta implementada
#     - A função utiliza `datetime.strptime` para criar um objeto de horário e calcula o arredondamento.
#     - Verifique se os valores de entrada são inteiros e dentro dos intervalos adequados.
#     - O resultado é um objeto `time`, que pode ser utilizado em outras operações de data/hora.

#     Exemplos de Uso:
#     >>> arredondar_horario(17, 38)
#     datetime.time(17, 35)
    
#     >>> arredondar_horario(17, 44)
#     datetime.time(17, 40)
#     """
#     if not (0 <= hora < 24):
#         raise ValueError("A hora deve estar entre 0 e 23.")
#     if not (0 <= minuto < 60):
#         raise ValueError("O minuto deve estar entre 0 e 59.")
    
#     horario = datetime.strptime(f"{hora}:{minuto}", "%H:%M")
    
#     delta = timedelta(minutes=5)
#     arredondado = (horario - datetime.min) // delta * delta + datetime.min

#     return arredondado.time()

# def arred_time_robos_funcionando(dados):
#     """
#     Processa os dados dos robôs, arredondando os horários e criando a timeline.

#     Parâmetros:
#     - dados (list): Lista de dicionários contendo os dados dos robôs. Cada dicionário deve ter:
#         - 'robo_id' (str): Identificador do robô.
#         - 'hora' (int): Hora de operação do robô (0-23).
#         - 'minuto' (int): Minuto de operação do robô (0-59).
#         - 'status' (str): Status do robô.

#     Retorno:
#     - list: Lista de dicionários com os horários arredondados e status dos robôs.

#     Exceções:
#     - `KeyError`: Se algum dos dicionários em `dados` não contiver as chaves esperadas.
#     - `ValueError`: Se a função `arredondar_horario` encontrar um valor de hora ou minuto inválido.
    
#     Notas:
#     - Foi compreendido que o javascript desenvolveria melhor esta função, então ela não esta implementada
#     - A função itera sobre a lista de registros e aplica a função `arredondar_horario` a cada entrada.
#     - É importante garantir que os dados de entrada estejam corretamente estruturados.
    
#     Exemplos de Uso:
#     >>> dados = [
#     ...     {'robo_id': 'R1', 'hora': 17, 'minuto': 38, 'status': 'ativo'},
#     ...     {'robo_id': 'R2', 'hora': 17, 'minuto': 44, 'status': 'inativo'},
#     ... ]
#     >>> arred_time_robos_funcionando(dados)
#     [{'robo_id': 'R1', 'horario_arredondado': datetime.time(17, 35), 'status': 'ativo'},
#      {'robo_id': 'R2', 'horario_arredondado': datetime.time(17, 40), 'status': 'inativo'}]
#     """
#     timetable_timeline = []
    
#     for registro in dados:
#         try:
#             hora, minuto = registro['hora'], registro['minuto']
#             horario_arredondado = arredondar_horario(hora, minuto)
            
#             timetable_timeline.append({
#                 'robo_id': registro['robo_id'],
#                 'horario_arredondado': horario_arredondado,
#                 'status': registro['status'],
#             })
#         except KeyError as e:
#             logger.error(f'Chave ausente no registro: {registro}. Erro: {e}')
#             raise KeyError(f'Registro deve conter as chaves: "robo_id", "hora", "minuto", "status". Erro: {e}')
#         except ValueError as e:
#             logger.error(f'Valor inválido para hora ou minuto no registro: {registro}. Erro: {e}')
#             raise ValueError(f'Hora ou minuto inválidos: {e}')

#     return timetable_timeline

