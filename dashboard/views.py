"""
views.py

Este arquivo contém as views da aplicação, responsáveis por gerenciar a lógica de apresentação e interação com o usuário. As views atuam como intermediárias entre as requisições HTTP feitas pelo cliente e a lógica de negócios implementada em outras partes do sistema, como os serviços de manipulação de dados e acesso ao banco de dados. O objetivo principal do `views.py` é processar as solicitações do usuário, realizar as operações necessárias, e retornar as respostas apropriadas, que podem ser em formato HTML, JSON ou redirecionamentos.

### Importância
A importância do `views.py` reside na sua função crítica de conectar a interface do usuário com a lógica de negócios. Um arquivo de views bem estruturado facilita a manutenção e a extensão do código, permitindo que os desenvolvedores atualizem a interface sem comprometer a lógica subjacente. Além disso, a utilização de tratamento de erros e logging nas views contribui para a robustez da aplicação, tornando mais fácil identificar e resolver problemas em tempo real.

### Principais Funções
Entre as principais funções implementadas neste arquivo, destacam-se:

1. **home(request)**: Renderiza a página inicial da aplicação, apresentando uma mensagem de desenvolvimento.

2. **dashboard_view(request)**: Coleta dados dos robôs e os manipula para exibição em um dashboard, integrando informações essenciais para a visualização do desempenho.

3. **get_timeline_data_view(request)**: Fornece dados para um gráfico de timeline em formato JSON, permitindo que o front-end atualize a interface dinamicamente.

4. **get_bots_funcionando_view(request)**: Retorna a quantidade de bots funcionando em formato JSON, facilitando o acesso a informações críticas de desempenho.

5. **get_bots_meta_view(request)**: Obtém e retorna dados das metas de bots em formato JSON, permitindo que os usuários comparem o desempenho real com as metas estabelecidas.

6. **get_total_minerado_view(request)**: Calcula e retorna o total minerado pelos robôs, oferecendo uma visão clara da produtividade.

Essas funções são fundamentais para a operação da aplicação, pois garantem que as informações sejam apresentadas de forma acessível e organizada aos usuários. A clara documentação e a estrutura lógica do `views.py` ajudam os desenvolvedores a entender rapidamente como a interface do usuário interage com os dados e a lógica de negócios, facilitando futuras manutenções e melhorias.

"""

from django.shortcuts import render

from .services.database_queries import get_bots_meta, get_bots_funcionando, total_minerado, get_robot_data, get_ultima_coleta_data, get_timeline_data

from django.http import JsonResponse

from django.db import connection, DatabaseError

import logging


logger = logging.getLogger(__name__)


def home(request):
    """
    Função que renderiza a página inicial do site.

    Parâmetros:
    - request: objeto HttpRequest que contém informações sobre a solicitação.

    Retorno:
    - Renderiza o template 'index.html'.

    Exceções:
    - `TemplateDoesNotExist`: Se o template 'index.html' não puder ser encontrado.
    
    Notas:
    - Esta função é um ponto de entrada para a página inicial do aplicativo. Qualquer 
      alteração no caminho do template deve ser feita aqui.
    """
    try:
        print('Bem-vindo a gestão de mineradores')
        return render(request, 'index.html')
    except Exception as e:
        logger.error(f"Erro desconhecido na função home: {e}")
        return {}
    

def index(request):
    return render(request, 'index.html')

# def dashboard_view(request):
#     """
#     Função que renderiza o dashboard, exibindo dados de robôs em funcionamento.

#     Parâmetros:
#     - request: objeto HttpRequest que contém informações sobre a solicitação.

#     Retorno:
#     - Renderiza o template 'dashboard.html' com dados de robôs.

#     Exceções:
#     - `DatabaseError`: Pode ocorrer durante a consulta aos robôs funcionando.
#     - `KeyError`: Se os dados manipulados não contiverem as chaves esperadas.
    
#     Notas:
#     - Certifique-se de que as funções chamadas retornam os dados no formato esperado. 
#       Isso é crucial para evitar erros de chave.
#     """
#     try:
#         data = get_robos_funcionando_data()
#         data_manipulation = get_robos_funcionando_data()
#         dados_timeline = arred_time_robos_funcionando(data_manipulation)

#         return render(request, 'dashboard.html', {'dados_timeline': dados_timeline, 'data': data})
    
#     except DatabaseError as e:
#         logger.error(f"Erro na execução da consulta dashboard_view: {e}")
#         return {}
#     except Exception as e:
#         logger.error(f"Erro desconhecido na função dashboard_view: {e}")
#         return {}

    
def get_timeline_data_view(request):
    """
    Função para obter os dados do gráfico de timeline e retornar em formato JSON.

    Parâmetros:
    - request: objeto HttpRequest que contém informações sobre a solicitação.

    Retorno:
    - JsonResponse com os dados da timeline.

    Exceções:
    - `DatabaseError`: Se ocorrer um erro ao obter dados da timeline.
    
    Notas:
    - A função `get_timeline_data` deve estar devidamente implementada e retornar 
      dados no formato correto.
    """
    try:
        data = get_timeline_data()
        return JsonResponse(data)
    except DatabaseError as e:
        logger.error(f"Erro na execução da consulta get_timeline_data_view: {e}")
        return {}
    except Exception as e:
        logger.error(f"Erro desconhecido na função get_timeline_data_view: {e}")
        return {}



def get_bots_funcionando_view(request):
    """
    View que retorna a quantidade de bots funcionando em formato JSON.

    Parâmetros:
    - request: objeto HttpRequest que contém informações sobre a solicitação.

    Retorno:
    - JsonResponse com status e dados dos bots funcionando.

    Exceções:
    - `DatabaseError`: Se houver erro na consulta aos bots funcionando.
    
    Notas:
    - Certifique-se de que a função `get_bots_funcionando` esteja retornando os dados 
      no formato esperado.
    """
    try:
        # Chama a função que busca os dados dos bots funcionando
        bots_data = get_bots_funcionando()

        # Retorna os dados em formato JSON
        return JsonResponse({
            'status': 'success',
            'data': bots_data
        })
    
    except Exception as e:
        # Em caso de erro, retorna uma resposta de erro
        return JsonResponse({
            'status': 'error',
            'message': f'Erro ao obter dados dos bots funcionando: {e}'
        }, status=500)


def calcular_razao_e_cor(robos_funcionando, bots_meta):
    """
    Função que calcula a razão entre robôs funcionando e a meta de robôs,
    e retorna um dicionário com as cores calculadas para cada robô.

    Parâmetros:
    - robos_funcionando: dicionário onde as chaves são nomes dos robôs e os valores são 
      a quantidade de robôs funcionando.
    - bots_meta: dicionário onde as chaves são nomes dos robôs e os valores são as metas.

    Retorno:
    - Dicionário onde as chaves são os nomes dos robôs e os valores são as cores correspondentes.

    Notas:
    - Esta funcao nao esta implementada, foi compreendido que javascript desenvolvia ela melhor
    - A função evita divisão por zero ao usar um valor padrão de 1 para a meta.
    - As cores são determinadas com base nas razões calculadas.
    """
    cores_robos = {}

    try:
        for robo, funcionando in robos_funcionando.items():
            total_meta = bots_meta.get(robo, 1)  # Evita divisão por zero caso não haja meta
            razao = funcionando / total_meta

            # Define a cor com base na razão
            if razao >= 0.7:
                cor = "#00FF00"  # Verde
            elif 0.4 <= razao < 0.7:
                cor = "#FFFF00"  # Amarelo
            else:
                cor = "#FF0000"  # Vermelho

            cores_robos[robo] = cor

        return cores_robos
    
    except Exception as e:
        logger.error(f"Erro desconhecido na função calcular_razao_e_cor: {e}")
        return {}

def exibir_robos(request):
    """
    Função que exibe os robôs e suas respectivas cores com base no funcionamento e metas.

    Parâmetros:
    - request: objeto HttpRequest que contém informações sobre a solicitação.

    Retorno:
    - Renderiza o template 'index.html' com dados das cores dos robôs.

    Exceções:
    - `KeyError`: Se os dicionários de robôs não contiverem as chaves esperadas.
    
    Notas:
    - Esta funcao nao esta implementada, foi compreendido que javascript desenvolvia ela melhor
    - As funções `get_bots_funcionando` e `get_bots_meta` devem retornar dados corretos.
    - Assegure-se de que os dados manipulados são compatíveis.
    """
    # Pega os robôs em funcionamento e as metas de cada robô
    robos_funcionando = get_bots_funcionando()
    bots_meta = get_bots_meta()
    cores_robos = calcular_razao_e_cor(robos_funcionando, bots_meta)

    return render(request, 'index.html', {'cores_robos': cores_robos})


def get_bots_meta_view(request):
    """
    Função para obter a quantidade de bots por robô e retornar em formato JSON.

    Parâmetros:
    - request: objeto HttpRequest que contém informações sobre a solicitação.

    Retorno:
    - JsonResponse com status e dados das metas dos bots.

    Exceções:
    - `DatabaseError`: Se ocorrer um erro na consulta.
    
    Notas:
    - A função `get_bots_meta` deve retornar um dicionário com os dados corretos.
    """
    try:
        bots_meta_data = get_bots_meta()

        return JsonResponse({
            'status': 'success',
            'data': bots_meta_data
        })
    
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Erro ao obter dados das metas dos bots: {e}'
        }, status=500)


def get_total_minerado_view(request):
    """
    Função para obter o total minerado e retornar em formato JSON.

    Parâmetros:
    - request: objeto HttpRequest que contém informações sobre a solicitação.

    Retorno:
    - JsonResponse com status e total minerado.

    Exceções:
    - `DatabaseError`: Se ocorrer um erro na consulta para obter o total minerado.
    
    Notas:
    - A função `total_minerado` deve retornar um valor numérico válido.
    """
    try:
        total_minerado_result = total_minerado()
        logger.info(f'Total minerado: {total_minerado_result}')
        return JsonResponse({
            'status': 'success',
            'total': total_minerado_result
        })
    except Exception as e:
        logger.error(f'Erro ao obter total minerado: {e}')
        return JsonResponse({
            'status': 'error',
            'message': f'Erro ao obter o total minerado: {e}'
        }, status=500)

def get_robot_dashboard_view(request):
    """
    Função para obter dados de robôs e retornar em formato JSON.

    Parâmetros:
    - request: objeto HttpRequest que contém informações sobre a solicitação.

    Retorno:
    - JsonResponse com status e dados dos robôs.

    Exceções:
    - `DatabaseError`: Se ocorrer um erro na consulta para obter dados dos robôs.
    
    Notas:
    - A função `get_robot_data` deve estar implementada corretamente e retornar dados válidos.
    """
    try:
        scroller_result = get_robot_data()
        logger.info(f'Total minerado: {scroller_result}')
        return JsonResponse({
            'status': 'success',
            'total': scroller_result
        })

    except Exception as e:
        logger.error(f'Erro ao obter total minerado: {e}')
        return JsonResponse({
            'status': 'error',
            'message': f'Erro ao obter o total minerado: {e}'
        }, status=500)
    

def ultima_coleta_view(request):
    """
    Função para obter a última coleta registrada e retornar em formato JSON.

    Parâmetros:
    - request: objeto HttpRequest que contém informações sobre a solicitação.

    Retorno:
    - JsonResponse com status e dados da última coleta.

    Exceções:
    - `DatabaseError`: Se ocorrer um erro na consulta para obter a última coleta.
    - `IndexError`: Se a última coleta não puder ser acessada corretamente.
    
    Notas:
    - A função `get_ultima_coleta_data` deve retornar um valor no formato esperado.
    """
    try:
        ultima_coleta_result = get_ultima_coleta_data()
        
        pri_ultima_coleta = ultima_coleta_result[0][0] if ultima_coleta_result else None
        
        return JsonResponse({
            'status': 'success',
            'pri_ultima_coleta': pri_ultima_coleta
        })
    except Exception as e:
        logger.error(f'Erro ao obter última coleta: {e}')
        return JsonResponse({
            'status': 'error',
            'message': f'Erro ao obter a última coleta: {e}'
        }, status=500)


# def my_dashboard_view(request):
#     Funcao para obter o ip do usuario e armazenar no banco
#     Funcao gerou diversos erros durante a implementacao, foi preferido sair sua implementacao
#     ip_address = request.META.get('REMOTE_ADDR')

#     # Armazena no banco de dados
#     AccessLog.objects.create(ip_address=ip_address)

#     # Retorna uma resposta, pode ser um JsonResponse ou renderizar um template
#     return JsonResponse({"message": "Dashboard accessed!", "ip": ip_address})


# def ip_check_view(request):
#     Funcao para obter o ip do usuario e verificar se esta autorizado o acesso a pagina envia ele para uma pagina de erro
#     Funcao gerou diversos erros durante a implementacao, foi preferido sair sua implementacao
#     ip_address = request.META.get('REMOTE_ADDR')
    
#     # Verifica se o IP está registrado
#     if AccessLog.objects.filter(ip_address=ip_address).exists():
#         # IP autorizado, renderiza a página
#         return render(request, 'index.html')
#     else:
#         # IP não autorizado, redireciona ou exibe uma mensagem
#         return render(request, 'my_view.html')

        
# def check_ip(request):
#     Funcao para obter o ip do usuario e verificar se esta autorizado o acesso a pagina e retorna o erro 403
#     Funcao gerou diversos erros durante a implementacao, foi preferido sair sua implementacao
#     user_ip = request.META.get('REMOTE_ADDR')
    
#     # Verifica se o IP do usuário está na tabela
#     if AllowedIP.objects.filter(ip_address=user_ip).exists():
#         # IP permitido, renderiza a página HTML
#         return render(request, 'sua_template.html')
#     else:
#         # IP não permitido, retorna um erro 403
#         return HttpResponseForbidden("Acesso negado: seu IP não está na lista de permitidos.")
   
