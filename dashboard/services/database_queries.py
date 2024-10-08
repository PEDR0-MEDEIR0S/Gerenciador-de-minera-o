"""
database_queries.py

Este arquivo contém uma coleção de funções responsáveis por interagir com o banco de dados da aplicação. Seu objetivo principal é encapsular as consultas SQL necessárias para extrair e manipular dados relacionados aos robôs e suas operações. A estrutura modular deste script permite uma fácil manutenção e reutilização das funções, promovendo uma abordagem organizada para lidar com as operações de banco de dados.

### Importância
A importância do `database_queries.py` reside na sua capacidade de centralizar a lógica de acesso aos dados, o que não apenas simplifica o desenvolvimento, mas também melhora a segurança e a eficiência do sistema. Ao usar funções dedicadas para consultas, é possível aplicar facilmente alterações na lógica de acesso ao banco de dados sem impactar outras partes do código. Além disso, a inclusão de tratamento de erros e logs proporciona maior robustez e rastreabilidade, facilitando a identificação de problemas em produção.

### Principais Funções
Entre as principais funções implementadas neste arquivo, destacam-se:

1. **get_data(query, params=None, function_name='N/A', create_objects=False)**: Função genérica para executar consultas SQL e retornar resultados, com suporte para parametrização e tratamento de erros.

2. **get_robos(robo_name=None)**: Recupera uma lista de robôs disponíveis no sistema, permitindo a opção de filtrar por nome.

3. **get_timeline_data()**: Coleta dados de desempenho e horários dos robôs, formatando as informações para visualização em gráficos.

4. **get_robos_funcionando()**: Conta e retorna a quantidade de robôs que estão operando dentro de parâmetros específicos.

5. **get_bots_meta()**: Obtém a quantidade de bots por robô, permitindo a análise do desempenho esperado em relação ao real.

6. **describe_table(table_name)**: Descreve a estrutura de uma tabela específica.

Essas funções, juntamente com outras presentes no script, constituem a base para a lógica de negócios da aplicação, permitindo que as partes front-end e de visualização acessem dados precisos e relevantes de forma eficiente.

"""

import logging

from django.db import connection, DatabaseError


logger = logging.getLogger(__name__)

def get_data(query, params=None, function_name='N/A', create_objects=False):
    """
    Função pai que executa as consultas no banco de dados e captura erros.
    
    Parâmetros:
    - query: string com a query SQL que será executada.
    - params: parâmetros opcionais para passar para a query (default: None).
    - function_name: nome da função que chamou 'get_data', permite identificar onde o erro ocorreu.
    - create_objects: se True, permite criar objetos a partir dos resultados da consulta.
    
    Retorno:
    - Retorna os resultados da consulta como uma lista de tuplas ou cria objetos, dependendo do parâmetro `create_objects`.
    
    Exceções:
    - `DatabaseError`: Loga erros relacionados ao banco de dados.
    - `ValueError`: Se os parâmetros de consulta estiverem mal formatados.
    
    Notas:
    - Ao editar a query, certifique-se de que os parâmetros estão corretamente configurados.
    - Verifique a necessidade de `create_objects` se o retorno precisa ser mapeado para objetos.
    """
    try:
        with connection.cursor() as cursor:
            # Executa a query com ou sem parâmetros
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # Busca os resultados
            result = cursor.fetchall()

            # Log de sucesso
            logger.info(f'Consulta realizada com sucesso: {function_name}')
            
            if create_objects:
                return [create_object_from_row(row) for row in result]
            
            return result
    except DatabaseError as e:
        logger.error(f'Erro ao realizar a consulta "{function_name}": {e}')
        return None
    except ValueError as ve:
        logger.error(f'Erro de valor na função "{function_name}": {ve}')
        return None


def create_object_from_row(row):
    """
    Função para criar um objeto a partir de uma linha de resultado.
    
    Parâmetros:
    - row: uma tupla representando uma linha de dados retornada da consulta.
    
    Retorno:
    - Um objeto que representa a linha de dados.
    
    Notas:
    - A implementação dessa função deve ser feita de acordo com a estrutura do objeto desejado.
    - Verifique se todos os elementos da tupla são necessários para a criação do objeto.
    """
    # Implementação necessária para criar o objeto a partir da linha
    pass



def get_robos(robo_name=None):
    """
    Função para obter os nomes dos robôs disponíveis no banco de dados.
    
    Parâmetros:
    - robo_name: (opcional) Nome do robô para filtrar a consulta.
    
    Retorno:
    - Retorna uma lista de nomes de robôs.
    
    Exceções:
    - Lança uma exceção personalizada em caso de erro na consulta.
    
    Notas:
    - Assegure-se de que o banco de dados contém dados na tabela `_name_table`.
    """
    query = '''
        SELECT 
            robo 
        FROM 
            unionall 
        GROUP BY 
            robo;
    '''
    try:
        result = get_data(query, function_name="Obter nome dos robos")
        return result
    except Exception as e:
        logger.error(f'Erro na função "Obter nome dos robos": {e}')
        raise Exception(f'Erro ao obter os robôs: {str(e)}')



def get_timeline_data():
    """
    Função para obter os dados do gráfico de timeline, processando os horários e desempenho dos robôs.
    
    Retorno:
    - Retorna um dicionário onde cada chave é o nome do robô e o valor é outro dicionário com
      as chaves 'horarios' e 'desempenhos', contendo listas dos dados correspondentes.
    
    Exceções:
    - Captura e loga erros ao executar a consulta, retornando um dicionário vazio em caso de erro.
    
    Notas:
    - Certifique-se de que os dados estão na tabela `_name_table` e que a coluna `desempenho` 
      não possui valores nulos ou negativos.
    """
    query = '''
        SELECT 
            UPPER(u.robo) AS robo,
            CONCAT(u.hora, ':', 
                CASE 
                    WHEN u.minuto <= 4 THEN '00'
                    WHEN u.minuto <= 9 THEN '05'
                    WHEN u.minuto <= 14 THEN '10'
                    WHEN u.minuto <= 19 THEN '15'
                    WHEN u.minuto <= 24 THEN '20'
                    WHEN u.minuto <= 29 THEN '25'
                    WHEN u.minuto <= 34 THEN '30'
                    WHEN u.minuto <= 39 THEN '35'
                    WHEN u.minuto <= 44 THEN '40'
                    WHEN u.minuto <= 49 THEN '45'
                    WHEN u.minuto <= 54 THEN '50'
                    WHEN u.minuto <= 59 THEN '55'
                    ELSE '00' 
                END) AS ultima_coleta,
            FORMAT(AVG(u.desempenho), 2) AS media_desempenho
        FROM  
            unionalllog u
        WHERE 
            u.desempenho IS NOT NULL AND u.desempenho > 0
        GROUP BY 
            robo, ultima_coleta
        ORDER BY 
            ultima_coleta
        LIMIT 0, 20000;
    '''
    
    data = {}
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                robo = row[0]
                desempenho = float(row[2]) * 100  # Certificando-se que é um float
                ultima_coleta = row[1] 
                
                logger.debug(f"Processando linha: robo={robo}, desempenho={desempenho}, ultima_coleta={ultima_coleta}")
                
                if robo not in data:
                    data[robo] = {'horarios': [], 'desempenhos': []}
                data[robo]['horarios'].append(ultima_coleta)
                data[robo]['desempenhos'].append(desempenho)

        return data
    except DatabaseError as e:
        logger.error(f"Erro na execução da consulta get_timeline_data: {e}")
        return {}
    except Exception as e:
        logger.error(f"Erro desconhecido na função get_timeline_data: {e}")
        return {}
    

def get_robos_funcionando():
    """
    Função para contar robôs que estão funcionando (paradosegundos > 0 e <= 600).
    
    Retorno:
    - Retorna o número de robôs em funcionamento.
    
    Exceções:
    - Lança uma exceção personalizada em caso de erro na consulta.
    
    Notas:
    - A lógica da contagem depende da coluna `paradosegundos`, que deve estar presente e 
      devidamente preenchida na tabela `_name_table`.
    """
    query = '''
        SELECT 
            COUNT(*) AS robosfuncionando
        FROM 
            unionall
        WHERE 
            paradosegundos > 0 
            AND paradosegundos <= 600;
    '''
    
    try:
        result = get_data(query, function_name="Obter robos funcionando")
        return result[0][0] if result else 0
    except Exception as e:
        logger.error(f'Erro na função "Obter robos funcionando": {e}')
        raise Exception(f'Erro ao contar robôs funcionando: {str(e)}')


def get_robos_funcionando_data():
    """
    Função que busca os dados de desempenho e horários dos robôs no dia atual.
    
    Retorno:
    - Retorna os dados de desempenho e horários dos robôs.
    
    Exceções:
    - Captura e loga erros na execução da consulta.
    
    Notas:
    - A consulta deve ser monitorada para verificar se os dados estão sendo retornados conforme o esperado.
    """
    query = '''
        SELECT
            UPPER(robo),
            desempenho,
            hora,
            minuto
        FROM
            unionalllog
        WHERE
            desempenho IS NOT NULL
        ORDER BY
            hora, minuto;
    '''
    try:
        return get_data(query, function_name="Obter dados de desempenho dos robos")
    except Exception as e:
        logger.error(f'Erro na função "Obter dados de desempenho dos robos": {e}')
        return []


def get_bots_funcionando():
    """
    Função para obter a quantidade de bots que estão funcionando,
    baseado na diferença entre a hora atual e a última coleta.
    
    Retorno:
    - Retorna um dicionário onde a chave é o nome do robô e o valor é a contagem de bots funcionando.
    
    Exceções:
    - Captura e loga erros ao executar a consulta, retornando um dicionário vazio em caso de erro.
    
    Notas:
    - Assegure-se de que a tabela `_name_table` contém a coluna `ultimacoleta` corretamente formatada.
    - O desempenho da consulta pode ser afetado se houver muitos dados na tabela.
    """
    query = '''
        SELECT
            UPPER(robo),
            COUNT(CASE 
                    WHEN TIME_TO_SEC(TIMEDIFF(CURTIME(), STR_TO_DATE(ultimacoleta, '%H:%i:%s'))) > 0
                        AND TIME_TO_SEC(TIMEDIFF(CURTIME(), STR_TO_DATE(ultimacoleta, '%H:%i:%s'))) <= 600 
                    THEN 1 
                    ELSE NULL 
                END) AS count_between_0_and_600
        FROM
            unionall
        GROUP BY
            robo
        LIMIT 1000;
    '''
    bots_data = {}

    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()

            # Preencher o dicionário com o nome do robô e os segundos
            for row in result:
                bots_data[row[0]] = row[1]  # row[0] = nome_robo, row[1] = segundos

    except DatabaseError as e:
        logger.error(f"Erro na função get_bots_funcionando: {e}")
    
    return bots_data


def get_bots_meta():
    """
    Função para obter a quantidade de bots por robô.
    
    Retorno:
    - Retorna um dicionário onde a chave é o nome do robô e o valor é a quantidade de bots.
    
    Exceções:
    - Captura e loga erros ao executar a consulta, retornando um dicionário vazio em caso de erro.
    
    Notas:
    - Verifique a integridade da tabela `_name_table` e se as colunas estão devidamente preenchidas.
    - A estrutura da consulta depende da tabela `_name_table`, alterações na estrutura podem afetar os resultados.
    """
    query = '''
        SELECT 
            UPPER(robo),
            bot
        FROM 
            meta;
    '''
    bots_data = {}

    try:
        result = get_data(query, function_name="Obter quantidade de bots por robô")
        return {row[0]: row[1] for row in result} if result else {}
    except Exception as e:
        raise Exception(f'Erro na função "get_bots_meta": {str(e)}')

    except DatabaseError as e:
        logger.error(f"Erro na função get_bots_meta: {e}")
    
    return bots_data


def total_minerado():
    """
    Função para obter o total minerado por robô.
    
    Retorno:
    - Retorna um dicionário onde a chave é o nome do robô e o valor é o total minerado.
    
    Exceções:
    - Captura e loga erros ao executar a consulta, lançando uma exceção personalizada em caso de erro.
    
    Notas:
    - Assegure-se de que a tabela `_name_table` possui a coluna `total` e que os dados estão devidamente preenchidos.
    """
    query = '''
        SELECT
            UPPER(robo),
            SUM(total) AS total_minerado
        FROM
            unionall
        GROUP BY
            robo;
        '''
    try:
        result = get_data(query, function_name="Obter total minerado")
        return {row[0]: row[1] for row in result} if result else {}
    except Exception as e:
        logger.error(f'Erro na função "Obter total minerado": {e}')
        raise Exception(f'Erro ao obter total minerado: {str(e)}')
    

def get_robot_data():
    """
    Função para obter dados de desempenho dos robôs, calculando índices com base nas últimas coletas.
    
    Retorno:
    - Retorna um dicionário onde a chave é o nome do robô e o valor é o índice calculado.
    
    Exceções:
    - Captura e loga erros ao executar a consulta, lançando uma exceção personalizada em caso de erro.
    
    Notas:
    - A consulta utiliza CTEs e requer suporte a SQL avançado no banco de dados.
    - Verifique se as colunas `robo`, `hora`, e `minuto` estão presentes na tabela `_name_table`.
    """
    query = '''
        WITH UltimasColetas AS (
            SELECT  
                robo AS robo,  -- Verifique se 'robo' existe na tabela 'unionalllog'
                CONCAT(LPAD(hora, 2, '0'), ':', LPAD(minuto, 2, '0')) AS ultima_coleta,
                total
            FROM  
                unionalllog
        ),
        RankedColetas AS (
            SELECT  
                robo,
                ultima_coleta,
                total,
                ROW_NUMBER() OVER (PARTITION BY robo ORDER BY ultima_coleta DESC) AS coleta_rank
            FROM  
                UltimasColetas
        )
        SELECT  
            UPPER(robo),
            ((NULLIF(MAX(CASE WHEN coleta_rank = 1 THEN total END), 0) - 
            MAX(CASE WHEN coleta_rank = 2 THEN total END)) / 
            NULLIF(MAX(CASE WHEN coleta_rank = 1 THEN total END), 0)) * 100 AS indice
        FROM  
            RankedColetas
        GROUP BY  
            robo
        HAVING 
            ((NULLIF(MAX(CASE WHEN coleta_rank = 1 THEN total END), 0) - 
            MAX(CASE WHEN coleta_rank = 2 THEN total END)) / 
            NULLIF(MAX(CASE WHEN coleta_rank = 1 THEN total END), 0)) * 100 IS NOT NULL;
        '''    
    try:
        results = get_data(query, function_name="Obter scroller por robô")
        for row in results:
            logger.info(f'Robô: {row[0]}, Índice: {row[1]}')
        return {row[0]: row[1] for row in results} if results else {}
    except Exception as e:
        logger.error(f'Erro na função "get_robot_data": {str(e)}')  # Log detalhado
        raise Exception(f'Erro na função "total_minerado": {str(e)}')
    

def get_ultima_coleta_data():
    """
    Função para obter o horário da última coleta registrada.
    
    Retorno:
    - Retorna a data e hora da última coleta.
    
    Exceções:
    - Captura e loga erros ao executar a consulta, lançando uma exceção personalizada em caso de erro.
    
    Notas:
    - Certifique-se de que a tabela `_name_table` possui a coluna `ultimacoleta`.
    - O resultado deve ser tratado conforme o formato esperado.
    """
    query = '''
        SELECT 
            MAX(ultimacoleta) AS pri_ultima_coleta
        FROM 
            unionall;
        '''
    try:
        results = get_data(query, function_name="Obter ultima coleta")
        return results
    except Exception as e:
        logger.error(f'Erro na função "get_robot_data": {str(e)}')
        raise Exception(f'Erro na função "total_minerado": {str(e)}')


def get_describe_table(table_name):
    """
    Retorna a estrutura da tabela especificada no banco de dados.

    :param table_name: Nome da tabela a ser descrita.
    :return: Uma string com a descrição das colunas e seus tipos.
    """
    query = f"DESCRIBE {table_name};"  # Consulta para descrever a tabela
    try:
        result = get_data(query, function_name=f"Descrever tabela {table_name}")
        
        if result is None:
            return f"Erro ao obter a descrição da tabela '{table_name}'."
        
        estrutura = f"Estrutura da tabela '{table_name}':\n"
        for col in result:
            estrutura += f"Nome: {col[0]}, Tipo: {col[1]}, Nulo: {'Sim' if col[2] == 'YES' else 'Não'}, Default: {col[4]}\n"
        
        return estrutura
    
    except Exception as e:
        return f"Erro ao descrever a tabela '{table_name}': {str(e)}"
    
