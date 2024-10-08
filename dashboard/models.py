"""
models.py

Este arquivo contém a definição dos modelos de dados para a aplicação de dashboard. Os modelos são representações das tabelas no banco de dados e definem a estrutura dos dados que a aplicação manipula. Cada classe definida neste arquivo corresponde a uma tabela e cada atributo da classe corresponde a uma coluna dessa tabela.

### Importância
A importância do `models.py` reside na sua capacidade de abstrair a lógica de manipulação de dados, permitindo que os desenvolvedores interajam com o banco de dados usando objetos Python em vez de SQL direto. Isso não apenas simplifica o desenvolvimento, mas também melhora a legibilidade do código e a manutenção futura. A definição clara dos modelos facilita a aplicação de migrações e a implementação de relações entre diferentes entidades de dados.

### Principais Modelos
Entre os principais modelos implementados neste arquivo, destacam-se:

1. **AccessLog**: 
   - **Campos**:
     - `ip_address`: Armazena o endereço IP que acessou a aplicação. Este campo utiliza `GenericIPAddressField`, permitindo tanto endereços IPv4 quanto IPv6.
     - `accessed_at`: Armazena a data e hora em que o acesso ocorreu, com o valor sendo automaticamente adicionado na criação do registro.
   - **Método `__str__`**: Retorna uma representação em string do registro, mostrando o endereço IP e a data/hora do acesso.

2. **AllowedIP**: 
   - **Campos**:
     - `ip_address`: Armazena endereços IP permitidos, garantindo que cada endereço seja único no sistema.
   - **Método `__str__`**: Retorna a representação em string do endereço IP armazenado.

Esses modelos fornecem a base para a lógica de negócios da aplicação, permitindo a manipulação eficiente de dados e a criação de registros que são essenciais para o funcionamento do dashboard.
"""

from django.db import models

"""
class AccessLog(models.Model):
    ip_address = models.GenericIPAddressField()
    accessed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip_address} - {self.accessed_at}"
    
class AllowedIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)

    def __str__(self):
        return self.ip_address"""