"""
asgi.py
ASGI config for project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
Este arquivo configura o ASGI (Asynchronous Server Gateway Interface) para o projeto Django, permitindo que a aplicação suporte operações assíncronas e conecte-se a servidores que utilizam a especificação ASGI. A configuração adequada do ASGI é essencial para que a aplicação funcione de maneira eficiente em um ambiente de produção, especialmente quando lida com requisições em tempo real e conexões websocket.

### Importância
A importância do `asgi.py` reside na sua função de expor a interface ASGI da aplicação como uma variável de nível de módulo chamada `application`. Isso permite que servidores compatíveis com ASGI, como Daphne ou Uvicorn, interajam com a aplicação Django. Além disso, a configuração deste arquivo garante que as variáveis de ambiente corretas sejam definidas, facilitando a integração com diferentes ambientes de implantação.

### Principais Componentes
Entre os principais componentes implementados neste arquivo, destacam-se:

1. **Importação de Módulos**: 
   - O arquivo importa os módulos necessários para a configuração ASGI, incluindo `os` para manipulação de variáveis de ambiente e `get_asgi_application` do Django.

2. **Configuração de Variáveis de Ambiente**: 
   - `os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')`: Define o módulo de configurações do Django que deve ser utilizado pela aplicação. Isso é crucial para que o Django saiba onde encontrar suas configurações específicas.

3. **Exposição da Aplicação ASGI**: 
   - `application = get_asgi_application()`: Chama a função que retorna o objeto ASGI da aplicação, permitindo que o servidor o utilize para processar requisições.

Este arquivo é fundamental para garantir que a sua aplicação Django esteja preparada para atender a requisições assíncronas, proporcionando melhor desempenho e escalabilidade.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

application = get_asgi_application()
