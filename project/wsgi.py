"""
wsgi.py

WSGI config for project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/

Este arquivo configura o WSGI (Web Server Gateway Interface) para o projeto Django, permitindo que a aplicação seja executada em servidores compatíveis com a especificação WSGI. A configuração correta do WSGI é essencial para a implantação da aplicação em ambientes de produção, garantindo que as requisições HTTP sejam processadas de forma eficiente.

### Importância
A importância do `wsgi.py` reside na sua função de expor a interface WSGI da aplicação como uma variável de nível de módulo chamada `application`. Isso permite que servidores compatíveis com WSGI, como Gunicorn ou uWSGI, interajam com a aplicação Django. Além disso, a configuração deste arquivo assegura que as variáveis de ambiente necessárias sejam definidas, facilitando a integração com diferentes ambientes de implantação.

### Principais Componentes
Entre os principais componentes implementados neste arquivo, destacam-se:

1. **Importação de Módulos**:
   - O arquivo importa os módulos necessários para a configuração WSGI, incluindo `os` para manipulação de variáveis de ambiente e `get_wsgi_application` do Django.

2. **Configuração de Variáveis de Ambiente**:
   - `os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')`: Define o módulo de configurações do Django que deve ser utilizado pela aplicação. Isso é crucial para que o Django saiba onde encontrar suas configurações específicas.

3. **Exposição da Aplicação WSGI**:
   - `application = get_wsgi_application()`: Chama a função que retorna o objeto WSGI da aplicação, permitindo que o servidor o utilize para processar requisições.

Este arquivo é fundamental para garantir que a sua aplicação Django esteja pronta para ser executada em servidores compatíveis com WSGI, proporcionando robustez e escalabilidade ao sistema.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

application = get_wsgi_application()
