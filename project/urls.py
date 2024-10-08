"""
urls.py

URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
### Importância
A importância do `urls.py` reside na sua função como o ponto central de roteamento da aplicação. Ele mapeia URLs para views, possibilitando que as requisições HTTP sejam direcionadas corretamente. Uma boa configuração de URLs é crucial para garantir uma navegação intuitiva e eficiente, além de ser fundamental para a segurança e manutenção da aplicação. Ao organizar rotas de maneira clara e concisa, o arquivo `urls.py` contribui para a escalabilidade e a legibilidade do projeto.

### Principais Funções
Entre as principais rotas configuradas neste arquivo, destacam-se:

1. **`admin/`**: URL padrão para acessar o painel de administração do Django, onde os administradores podem gerenciar modelos e usuários.

2. **`''` (home)**: URL raiz que leva à função `home`, que geralmente serve como ponto de entrada principal da aplicação.

3. **`get_timeline-data/`**: URL que invoca a função `get_timeline_data_view`, retornando dados para a visualização de timelines.

4. **`get_bots_funcionando/`**: URL que chama a função `get_bots_funcionando_view`, que fornece informações sobre os bots que estão em funcionamento.

5. **`get_bots_meta/`**: URL associada à função `get_bots_meta_view`, que retorna dados sobre as metas dos bots.

6. **`get_total_minerado/`**: URL que ativa a função `get_total_minerado_view`, fornecendo o total minerado pela aplicação.

7. **`get_scroller/`**: URL que leva à função `get_robot_dashboard_view`, que retorna dados específicos para a visualização do dashboard dos robôs.

8. **`get_ultima_coleta/`**: URL que invoca a função `ultima_coleta_view`, que fornece informações sobre a última coleta realizada.

Essas rotas são essenciais para a interatividade da aplicação, permitindo que os usuários acessem e manipulem dados de forma eficiente. Um `urls.py` bem estruturado é vital para garantir que a aplicação funcione de maneira fluida e que as interações do usuário sejam processadas corretamente.
"""

from django.contrib import admin

from django.urls import include, path

from django.http import HttpResponse

from dashboard.views import index

from dashboard.views import home, get_timeline_data_view, get_bots_funcionando_view, get_bots_meta_view, get_total_minerado_view, get_robot_dashboard_view, ultima_coleta_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('', include('dashboard.urls')),
    path('get_timeline-data/', get_timeline_data_view, name='get_timeline_data'),
    path('get_bots_funcionando/', get_bots_funcionando_view, name='get_bots_funcionando'),
    path('get_bots_meta/', get_bots_meta_view, name='get_bots_meta'),
    path('get_total_minerado/', get_total_minerado_view, name='get_total_minerado'),
    path('get_scroller/', get_robot_dashboard_view, name='get_scroller'),
    path('get_ultima_coleta/', ultima_coleta_view, name='get_ultima_coleta'),
]
