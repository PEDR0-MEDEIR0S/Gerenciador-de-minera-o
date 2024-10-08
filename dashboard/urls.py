"""
urls.py

Este arquivo é responsável por definir as rotas de URL para a aplicação de dashboard. Nele, você encontrará as definições de caminhos que permitem que os usuários acessem diferentes partes da aplicação através de URLs. A estrutura das URLs é fundamental para a navegação do usuário e para a interação com os diferentes componentes da aplicação.

### Importância
A importância do `urls.py` reside na sua capacidade de gerenciar a navegação da aplicação de forma organizada e modular. Cada rota definida neste arquivo mapeia uma URL específica para uma função de visualização correspondente, garantindo que as requisições dos usuários sejam processadas de forma adequada. Uma configuração clara e bem documentada das URLs facilita a manutenção do código e permite uma fácil adição de novas funcionalidades no futuro.

### Principais Rotas
Entre as principais rotas implementadas neste arquivo, destacam-se:

1. **path('', index, name='home')**: Define a URL raiz da aplicação, que redireciona para a função de visualização `index`. Esta é a página inicial do dashboard, onde os usuários podem visualizar informações gerais e dados relevantes.

Esse arquivo é fundamental para a estrutura da aplicação, e quaisquer modificações nas rotas devem ser feitas com cuidado para garantir que a navegação da aplicação permaneça intuitiva e funcional.
"""
# dashboard/urls.py
from django.urls import path
from .views import index  # Assegure-se de que a função 'index' está definida em views.py

urlpatterns = [
    path('', index, name='home'),  # Define a URL raiz
]
