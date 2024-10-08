"""
help_project.py

Este arquivo contém um comando personalizado para exibir informações detalhadas sobre o projeto
e listar as dependências de uma pasta. O objetivo principal é fornecer um recurso de ajuda acessível 
ao desenvolvedor, permitindo que ele obtenha informações sobre módulos específicos, como banco de dados, 
autenticação e dashboard, além de consultar detalhes sobre arquivos individuais no projeto.

### Importância
A importância do `help_project.py` reside na sua capacidade de centralizar as informações essenciais 
do projeto, promovendo um entendimento mais profundo da estrutura e das funcionalidades implementadas. 
Esse comando é uma ferramenta útil para desenvolvedores que buscam informações rápidas e organizadas, 
facilitando a manutenção e o desenvolvimento contínuo da aplicação.

### Principais Funcionalidades
Entre as principais funcionalidades implementadas neste arquivo, destacam-se:

1. **Informações do Projeto**: Exibe um resumo dos módulos importantes, como autenticação e dashboard.
2. **Listagem de Dependências**: Permite ao desenvolvedor listar as dependências em um diretório específico.
3. **Informações de Arquivo**: Proporciona um resumo sobre um arquivo específico, buscando sua documentação interna.
4. **Interação com o Usuário**: Facilita a interação através de opções de menu, guiando o desenvolvedor nas informações 
que deseja consultar.
"""

from django.core.management.base import BaseCommand

import os

from dashboard.services.database_queries import get_describe_table


# Comando personalizado para exibir informações sobre o projeto e listar dependências de uma pasta
class Command(BaseCommand):

    help = 'Exibe informações detalhadas sobre o projeto e lista as dependências de uma pasta'


    def add_arguments(self, parser):
        """
        Adiciona argumentos ao comando. Permite passar o caminho da pasta
        cujas dependências devem ser listadas.
        """
        parser.add_argument(
            '--caminho',
            type=str,
            help='Caminho da pasta a ser listada',
            required=False
        )


    def handle(self, *args, **kwargs):
        """
        Método principal que é chamado quando o comando é executado.
        Exibe informações do projeto e, se um caminho for passado,
        lista as dependências da pasta especificada.
        """
        # Exibe informações do projeto
        self.stdout.write("Informações gerais sobre o projeto:\n")
        self.stdout.write("1. Módulo de autenticação: No momento ainda não foi desenvolvido um método de autenticação.\n")
        self.stdout.write("2. Módulo de dashboard: Explica como os gráficos e dados são processados, para saber mais, acesse a opção 2 abaixo.\n")
        self.stdout.write("3. Banco de Dados: Detalhes sobre as tabelas usadas e como as queries são feitas para saber mais, acesse a opção 1 abaixo.\n")
        self.stdout.write("\n\nPara te auxiliar durante o desenvolvimento, iremos listar abaixo todas as dependências do projeto.")

        raiz_projeto = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

        # Lista todas as dependências a partir da raiz do projeto
        self.stdout.write(f"\nListando dependências a partir da raiz do projeto: {raiz_projeto}\n\n")
        self.listar_dependencias(raiz_projeto)

        # Pergunta ao usuário o que ele gostaria de saber
        self.stdout.write("\nSobre o que você gostaria de saber mais?\n")
        self.stdout.write("1. Informações sobre o banco de dados\n")
        self.stdout.write("2. Informações sobre autenticação\n")
        self.stdout.write("3. Informações sobre o dashboard\n")
        self.stdout.write("4. Informações sobre um arquivo específico\n")
        
        # Lê a escolha do usuário
        escolha = input("Escolha uma opção (1-4): ")

        if escolha == '1':
            self.informacoes_banco_dados()
        elif escolha == '2':
            self.informacoes_autenticacao()
        elif escolha == '3':
            self.informacoes_dashboard()
        elif escolha == '4':
            nome_arquivo = input("Digite o nome do arquivo: ")
            self.informacoes_arquivo(nome_arquivo, raiz_projeto)
        else:
            self.stdout.write("Opção inválida. Tente novamente.\n")


    def listar_dependencias(self, caminho):
        """
        Lista todas as dependências dentro do caminho especificado.
        Utiliza a função os.walk para percorrer a estrutura de diretórios.
        """
        if not os.path.exists(caminho):
            self.stdout.write(f"O caminho '{caminho}' não existe.\n")
            return

        for raiz, dirs, arquivos in os.walk(caminho):
            # Ignora o diretório 'venv'
            if 'venv' in dirs:
                dirs.remove('venv')
            
            if '__pycache__' in dirs:
                dirs.remove('__pycache__')

            nivel = raiz.replace(caminho, '').count(os.sep)
            indentacao = ' ' * 4 * (nivel)
            self.stdout.write(f"{indentacao}{os.path.basename(raiz)}/")
            for arquivo in arquivos:
                self.stdout.write(f"{indentacao}    {arquivo}")


    def informacoes_banco_dados(self):
        """
        Exibe informações sobre o banco de dados utilizado no projeto.
        Fornece detalhes sobre as tabelas e as queries realizadas, além
        de listar todas as consultas definidas no arquivo `database_queries.py`.
        """
        tabelas = ['unionall', 'unionalllog', 'meta']

        self.stdout.write("Opção selecionada: Informações sobre o banco de dados:\n")
        self.stdout.write("O banco de dados utilizado durante o projeto foi o MySQL,\n")
        self.stdout.write("contudo não deve haver problemas em se conectar com outros\n")
        self.stdout.write("desde que haja a autenticação requerida no arquivo settings.py.\n")
        self.stdout.write("Uma informação muito importante é que as tabelas não devem\n")
        self.stdout.write("dispor de informações qualitativas sobre a mineração, apenas\n")
        self.stdout.write("quantitativas. Isto indica que as tabelas não precisam de controle\n")
        self.stdout.write("de LGPT ou qualquer outro cuidado sobre os dados, pois aprensenta\n")
        self.stdout.write("apenas as contagens de desempenho sobre a mineração.")

        self.stdout.write("Outra informação importante é que o banco de dados foi projetado\n")
        self.stdout.write("para conter informações do dia atual, isto significa que nunca averá\n")
        self.stdout.write("conflito de informações por causa de data já que não existe informações\n")
        self.stdout.write("de data.\n")

        self.stdout.write("Para se conectar com o banco, o djago querer as seguintes informações:\n")
        self.stdout.write('''# Database\n
                                # https://docs.djangoproject.com/en/5.1/ref/settings/#databases\n
                                DATABASES = {\n
                                    'default': {\n
                                        'ENGINE': 'django.db.backends.mysql',\n
                                        'NAME': 'nome_do_banco',\n
                                        'USER': 'usuario_do_banco',\n
                                        'PASSWORD': 'senha_do_banco',\n
                                        'HOST': 'localhost',\n
                                        'PORT': '3306',\n
                                    }\n
                                }\n
        ''')
        self.stdout.write("\nCom relação ao banco de dados e as respectivas tabelas,\n")
        self.stdout.write(f"foram utilizadas as tabelas denominadas: {tabelas[0]}, {tabelas[1]} e {tabelas[2]}.\n")
        self.stdout.write("\nAgora iremos falar sobre as tabelas e suas especificidades.\n")
        self.stdout.write(f"A tabela {tabelas[0]}, contém informações sobre o desempenho de.\n")
        self.stdout.write("cada um dos bot de cada robo, isto significa que caso existam mais de\n")
        self.stdout.write("um bot por robô, as informações em cada bot não deve ser condensada em\n")
        self.stdout.write("uma única célula. Além disso, é mostrado a informação sem uma ordem\n")
        self.stdout.write("cronologica, pois o que interessa é a última informação de horário\n")
        self.stdout.write("da mineração.\n")
        self.stdout.write("Com relação a {tabelas[1]}, ela consolida todas as informação por robo\n")
        self.stdout.write("conologicamente, ou seja, e consolidado o resultado de todos os bots e\n")
        self.stdout.write("em um determinado minuto, isto significa que não importa a informação por\n")
        self.stdout.write("bot ou segundos.")
        self.stdout.write(f"A tabela {tabelas[2]}, possui apenas indicadores quantitativos sobre\n")
        self.stdout.write("resultados preditivos, como a média de mineração por minuto, o máximo\n")
        self.stdout.write("que foi registrado por minuto, a quantidade de bots por robo, dentr outras.\n")

        for tabela in tabelas:
            estrutura = get_describe_table(tabela)
            self.stdout.write(estrutura + "\n")

        self.stdout.write("Agora falaremos sobre as consultas realizadas ao banco de dados.\n")
        self.stdout.write("As queries são feitas usando o ORM do Django.\n")


        # Exibir as consultas definidas no arquivo database_queries.py
        self.exibir_consultas()

        self.stdout.write("O djago dispõe de um arquivo chamado urls.py dentro da pasta project.\n")
        self.stdout.write("Este arquivo tem por função roteamento da aplicação enquanto cria requisições HTTP .\n")
        self.stdout.write("É possível verificar a consulta obtida no banco e o que esta sendo entregue.\n")
        self.stdout.write("através do acesso ao: http://dominio/funcao/")
                          
        self.stdout.write("Qual quer outra informação sobre o banco de dados deve ser consultado diretamente com o desenvolvedor.\n")

    def exibir_consultas(self):
        """
        Lê e exibe todas as consultas definidas no arquivo database_queries.py.
        As consultas estão separadas por três aspas simples.
        """
        # Caminho fixo para o arquivo database_queries.py
        database_queries_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            'services',
            'database_queries.py'
        )

        # Verifica se o arquivo existe
        if os.path.exists(database_queries_path):
            self.stdout.write(f"\nConsultas encontradas em: {database_queries_path}\n")

            # Lê o conteúdo do arquivo
            try:
                with open(database_queries_path, 'r', encoding='utf-8') as arquivo:
                    conteudo = arquivo.read()
                    
                    # Procura e exibe todas as consultas
                    consultas = conteudo.split("'''")
                    
                    # Verifica se há consultas
                    if len(consultas) < 3:
                        self.stdout.write("Nenhuma consulta válida encontrada no arquivo.\n")
                        return
                    
                    for i in range(1, len(consultas), 2):  # Apenas as partes ímpares são consultas
                        consulta_formatada = consultas[i].strip()
                        if consulta_formatada:
                            self.stdout.write(f"\nConsulta {i//2 + 1}:\n{consulta_formatada}\n\n")
                        else:
                            self.stdout.write(f"\nConsulta {i//2 + 1}: [Consulta vazia ou não válida]\n\n")
                        
            except FileNotFoundError:
                self.stdout.write(f"Arquivo 'database_queries.py' não encontrado em {database_queries_path}.\n\n")
            except Exception as e:
                self.stdout.write(f"Erro ao ler o arquivo: {e}\n\n")
        else:
            self.stdout.write(f"O arquivo 'database_queries.py' não foi encontrado em {database_queries_path}.\n\n")


    def informacoes_autenticacao(self):
        """
        Exibe informações sobre o módulo de autenticação do Django.
        Descreve como a autenticação de usuários é realizada.
        """
        self.stdout.write("Opção selecionada: Informações sobre autenticação:\n")
        self.stdout.write("No momento ainda não foi desenvolvido um método de autenticação.\n")


    def informacoes_dashboard(self):
        """
        Exibe informações sobre o módulo de dashboard.
        Explica como os dados são processados e os gráficos são gerados.
        """
        backend = 'database_queries.py', 'views.py', 'utils.py', 'settings.py', 'models.py', 'signals.py'

        self.stdout.write("Opção selecionada: Informações sobre o dashboard:\n")
        self.stdout.write("O Django possui uma infinidade de funcionalidades para os projetos de desenvolvimento,\n")
        self.stdout.write("cabendo ao desenvolvedor selecionar o que necessita. Para o projeto, foram utilizados\n")
        self.stdout.write("alguns arquivos principais por se tratar de um projeto enxuto.")
        self.stdout.write("Dentre a listagem de arquivos, podemos citar {}. Além destes, podemos encontrar\n".format(backend))
        self.stdout.write("outros arquivos de frontend, sendo eles, index.html, scripts.js e styles.css.\n")
                         
        self.stdout.write("O resumo dos arquivos, estará logo abaixo:\n")

        for arquivo in backend:
            try:
                with open(arquivo, 'r', encoding='utf-8') as f:
                    conteudo = f.read()
                    inicio_comentario = conteudo.find('"""')
                    if inicio_comentario != -1:
                        fim_comentario = conteudo.find('"""', inicio_comentario + 3)
                        if fim_comentario != -1:
                            comentario = conteudo[inicio_comentario + 3: fim_comentario].strip()
                            self.stdout.write(f"\nPrimeiro comentário em '{arquivo}':\n\"\"\"{comentario}\"\"\"\n")
                        else:
                            self.stdout.write(f"\nNão foi encontrado um comentário de fechamento em '{arquivo}'.\n")
                    else:
                        self.stdout.write(f"\nNenhum comentário encontrado em '{arquivo}'.\n")
            except FileNotFoundError:
                self.stdout.write(f"\nO arquivo '{arquivo}' não foi encontrado.\n")

        self.stdout.write("A imagem da logo marca é obtida pelo seu nome: logo, que por sua vez\n")
        self.stdout.write("deve estar contida dentro da pagina static.\n")
                          

        self.stdout.write("O gráfico de scroller é obtido a partir da função: get_robot_dashboard_view.\n")
        self.stdout.write("esta função deve buscar o último registro da tabela unionalllog para que.\n")
        self.stdout.write("seja comparado com o penultimo, a comparação é feita a partir da coluna total\n")
        self.stdout.write("onde a razão da parte pelo todo.\n")
                          
        
    
        self.stdout.write("Os cards de cada robo contido em seções do dashboard são obtidos a\n")
        self.stdout.write("partir da função: get_bots_funcionando_view(). Onde é realizado um filtro\n")
        self.stdout.write("de bots que estão com valores da coluna ultimacoleta com valor menor do que\n")
        self.stdout.write("o horário atual menos 600 segundos. A partir disto é possível realizar a\n")
        self.stdout.write("contagém de que mineraram nos últimos 600 segundos e por robo.\n")
        self.stdout.write("Além disto, a distriuição por cada seção do robo acontece através do nome\n")
        self.stdout.write("descrido na class da div do html e uma correspondencia exata de chave:valor.\n")
        self.stdout.write("que está no próprio script html. Este recurso também serve para filtrar o\n")
        self.stdout.write("título da seção e o total minerado acumulado durante o dia por robo\n")

        
        self.stdout.write("O gráfico de linhas contido no dashboard é obtido a partir da função:\n")
        self.stdout.write("get_timeline_data(). Cada linha representa o desempenho um robo durante\n")
        self.stdout.write("o dia atual. O cálculo para descobrir o desempenho pode ser obtido através\n")
        self.stdout.write("da razão entre o desempenho por minuto e o máximo desempenho já registrado.\n")
        self.stdout.write("Após a obtenção do desempenho é realizada a média de desempenho e consolidada\n")
        self.stdout.write("esta informação a cada 5 minutos, para que tudo fique visual no gráfico.\n")
                         
    def informacoes_arquivo(self, nome_arquivo, caminho):
        """
        Exibe um resumo sobre um arquivo específico, se encontrado.
        Busca o primeiro comentário do tipo docstring no arquivo e exibe seu conteúdo.
        """
        arquivo_encontrado = False
        
        for raiz, dirs, arquivos in os.walk(caminho):
            if nome_arquivo in arquivos:
                arquivo_encontrado = True
                caminho_arquivo = os.path.join(raiz, nome_arquivo)
                self.stdout.write(f"Resumo sobre o arquivo '{nome_arquivo}':\n")
                self.stdout.write(f"Localização: {caminho_arquivo}\n")

                # Lê o conteúdo do arquivo
                with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                    conteudo = arquivo.read()
                    
                    # Procura o primeiro comentário em docstring
                    inicio = conteudo.find('"""')
                    if inicio != -1:
                        fim = conteudo.find('"""', inicio + 3)
                        if fim != -1:
                            resumo = conteudo[inicio + 3:fim].strip()
                            self.stdout.write(f"Conteúdo do arquivo: {resumo}\n")
                        else:
                            self.stdout.write("Docstring não fechada encontrada, não foi possível extrair o resumo.\n")
                    else:
                        self.stdout.write("Nenhuma docstring encontrada no arquivo.\n")
                break

        if not arquivo_encontrado:
            self.stdout.write(f"O arquivo '{nome_arquivo}' não foi encontrado.\n")

