# Gerenciador-de-mineracao
Resumo do Projeto
    Este projeto Django é um sistema de dashboard que exibe dados e gera gráficos baseados 
    em dados provenientes da mineração. O objetivo é fornecer uma interface simples e eficiente 
    para visualização de dados em tempo real, com integração a um banco de dados que processa 
    informações sobre o desempenho de robôs e outros dados do sistema.
    O projeto inclui funcionalidades personalizadas no módulo de dashboard, além de várias 
    funcionalidades padrão do Django, como gerenciamento de usuários e controle de sessões.

Funcionalidades
    O projeto inclui uma série de comandos úteis que podem ser acessados através do comando 
    python manage.py seguido do subcomando desejado. Abaixo está uma lista dos subcomandos 
    disponíveis e suas descrições:
    
Comandos Personalizados do Dashboard ([dashboard])
    help_project: Exibe informações detalhadas sobre o projeto, incluindo descrições de funcionalidades, 
    arquivos e dados utilizados no sistema (altamente recomentadado o acesso prévio a utilização do script.
    
Comandos de Autenticação ([auth])
    changepassword: Permite ao administrador alterar a senha de um usuário registrado. Após 
    executar este comando, você será solicitado a informar o nome de usuário e a nova senha.
    createsuperuser: Cria um novo superusuário no sistema, o que permite ao usuário acessar o 
    painel de administração Django e gerenciar o sistema.

Comandos de Tipos de Conteúdo ([contenttypes])
    remove_stale_contenttypes: Remove tipos de conteúdo obsoletos (ou seja, tipos de conteúdo 
    que não estão mais associados a um modelo) do banco de dados.

Comandos Gerais do Django ([django])
    check: Verifica se há quaisquer problemas de configuração no projeto. Ele é usado para garantir 
    que o sistema esteja corretamente configurado antes de sua execução.
    compilemessages: Compila arquivos de tradução de mensagens para permitir que o projeto suporte 
    internacionalização (i18n).
    createcachetable: Cria uma tabela de cache no banco de dados para armazenar dados temporários 
    que aceleram o desempenho do projeto.
    dbshell: Abre um shell interativo no banco de dados configurado, permitindo ao desenvolvedor 
    executar consultas diretamente.
    diffsettings: Exibe as diferenças entre as configurações padrão do Django e as configurações 
    atuais do projeto.
    dumpdata: Exporta os dados do banco de dados em formato JSON, XML ou YAML, o que é útil para 
    backup ou migração de dados.
    flush: Remove todos os dados do banco de dados, deixando as tabelas intactas. Útil para redefinir 
    o estado do banco de dados durante o desenvolvimento.
    inspectdb: Gera automaticamente os modelos Django a partir de um banco de dados existente. Útil 
    ao integrar um banco de dados legado.
    loaddata: Carrega dados no banco de dados a partir de arquivos de fixture (JSON, XML, YAML).
    makemessages: Gera arquivos de mensagens para internacionalização, buscando strings em todo o 
    código-fonte.
    makemigrations: Cria novos arquivos de migração com base nas mudanças detectadas nos modelos do 
    projeto.
    migrate: Aplica as migrações pendentes no banco de dados, sincronizando a estrutura das tabelas 
    com os modelos do projeto.
    optimizemigration: Otimiza o processo de migração, combinando várias migrações em uma só para 
    melhorar a eficiência.
    sendtestemail: Envia um email de teste para verificar se as configurações de email estão corretas 
    no projeto.
    shell: Abre um shell interativo Python com o contexto do Django carregado, permitindo interação 
    direta com o projeto.
    showmigrations: Lista todas as migrações no projeto e seu status (aplicada ou pendente).
    sqlflush: Gera o SQL necessário para excluir todos os dados das tabelas do banco de dados.
    sqlmigrate: Exibe o SQL equivalente de uma migração específica.
    sqlsequencereset: Gera o SQL necessário para redefinir os contadores de sequência para tabelas 
    com campos de chave primária autoincrementada.
    squashmigrations: Combina várias migrações antigas em uma única, para simplificar a gestão de 
    migrações no projeto.
    startapp: Cria a estrutura de diretórios para um novo aplicativo Django.
    startproject: Cria a estrutura inicial de um projeto Django.
    test: Executa a suíte de testes automatizados definida para o projeto.
    testserver: Executa o servidor de desenvolvimento do Django com dados de fixture pré-carregados, 
    útil para testes em ambiente local.

Comandos de Sessões ([sessions])
    clearsessions: Remove sessões expiradas do banco de dados. Essencial para a manutenção do banco de 
    dados, garantindo que sessões antigas não ocupem espaço.

Comandos de Arquivos Estáticos ([staticfiles])
    collectstatic: Reúne todos os arquivos estáticos do projeto (como imagens, JavaScript, CSS) em um 
    único local para servir em produção.
    findstatic: Localiza o caminho no sistema de arquivos para arquivos estáticos específicos.
    runserver: Inicia o servidor de desenvolvimento do Django, permitindo que você veja o projeto em um 
    navegador local.
