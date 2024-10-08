// Função assíncrona para buscar a última coleta de dados
async function fetchUltimaColeta() {
    try {
        // Faz uma requisição para a URL '/get_ultima_coleta/'
        const response = await fetch('/get_ultima_coleta/');
        const data = await response.json(); // Converte a resposta em JSON

        // Verifica se a resposta foi bem-sucedida
        if (data.status === 'success') {
            // Atualiza o texto do elemento 'ultima-coleta' com o valor recebido ou 'N/A'
            document.getElementById('ultima-coleta').innerText = data.pri_ultima_coleta || 'N/A'; // Exibe 'N/A' se não houver valor
        } else {
            // Loga uma mensagem de erro no console
            console.error(data.message);
        }
    } catch (error) {
        // Loga qualquer erro encontrado durante a requisição
        console.error('Erro ao buscar última coleta:', error);
    }
}

// Chama a função fetchUltimaColeta ao carregar a página
document.addEventListener('DOMContentLoaded', fetchUltimaColeta);

// Define o contexto do gráfico no elemento 'timelineChart'
const ctx = document.getElementById('timelineChart').getContext('2d');
let chart; // Variável para armazenar a instância do gráfico

// Limitar o número de robôs a 6
const maxRobos = 6;
const defaultRobos = ["RFB", "WHATSAPP", "VTCALL", "SEFAZ", "MEU NEGOCIO", "MIDIAS"]; // Robôs padrão
let allRobos = []; // Array para armazenar todos os robôs

// Definição do tipo de interpolação (opções: 'linear', 'monotone', 'step')
const interpolationType = 'linear'; // Escolha entre 'linear', 'monotone', 'step'

// Função para buscar os dados dos robôs
function fetchData(robosSelecionados) {
    // Faz uma requisição para a URL '/get_timeline-data/'
    fetch('/get_timeline-data/')
    .then(response => response.json()) // Converte a resposta em JSON
    .then(data => {
        const datasets = []; // Array para armazenar os conjuntos de dados
        const cores = ['#FF5733', '#33FF57', '#5733FF', '#FF33A1', '#33FFF1', '#F1FF33']; // Cores para os gráficos

        let colorIndex = 0; // Índice para alternar entre as cores
        robosSelecionados.forEach((robo) => {
            if (data[robo]) {
                // Adiciona um conjunto de dados para cada robô selecionado
                datasets.push({
                    label: robo,
                    data: data[robo]['desempenhos'].map((desempenho) => desempenho), // Dados de desempenho
                    borderColor: cores[colorIndex % cores.length], // Cor da borda
                    backgroundColor: cores[colorIndex % cores.length] + '30', // Cor de fundo semi-transparente
                    borderWidth: 2,
                    fill: true, // Preenche a área abaixo da linha
                    tension: getTensionValue(interpolationType), // Define o tipo de interpolação
                    pointRadius: 1 // Torna os pontos visíveis
                });
                colorIndex++; // Incrementa o índice da cor
            }
        });

        const labels = data[Object.keys(data)[0]]['horarios']; // Usar "horarios" para o eixo x
        
        // Processa os rótulos e ordena os dados
        const sortedData = labels.map((label, index) => {
            const [hours, minutes] = label.split(':').map(Number); // Separa horas e minutos
            return { time: new Date(0, 0, 0, hours, minutes), index, label }; // Cria um objeto com o horário
        });

        sortedData.sort((a, b) => a.time - b.time); // Ordena os dados por tempo

        // Extrair os horários ordenados
        const sortedLabels = sortedData.map(item => item.label);
        const sortedDatasets = datasets.map(dataset => ({
            ...dataset,
            data: sortedData.map(item => dataset.data[item.index]) // Usar o índice ordenado
        }));

        // Atualiza ou cria o gráfico
        if (chart) {
            // Atualiza os dados do gráfico existente
            chart.data.labels = sortedLabels;
            chart.data.datasets = sortedDatasets;
            chart.update(); // Atualiza o gráfico
        } else {
            // Cria um novo gráfico
            chart = new Chart(ctx, {
                type: 'line', // Tipo de gráfico
                data: {
                    labels: sortedLabels, // Eixo X
                    datasets: sortedDatasets // Conjuntos de dados
                },
                options: {
                    responsive: true, // Gráfico responsivo
                    maintainAspectRatio: false, // Mantém a proporção ao redimensionar
                    scales: {
                        x: {
                            title: {
                                display: false, // Não exibe título
                                text: 'Última Coleta',
                                color: '#6272a4' // Cor do título do eixo
                            },
                            ticks: {
                                color: '#6272a4', // Cor dos rótulos do eixo X
                                font: {
                                    weight: 'bold' // Define os rótulos do eixo X como negrito
                                }
                            },
                            grid: {
                                color: 'rgba(200, 200, 200, 0.5)' // Cor da grade do eixo X
                            }
                        },
                        y: {
                            title: {
                                display: false, // Não exibe título
                                text: 'Desempenho (%)',
                                color: '#6272a4' // Cor do título do eixo
                            },
                            beginAtZero: true, // Começa o eixo Y em zero
                            ticks: {
                                color: '#6272a4', // Cor dos rótulos do eixo Y
                                font: {
                                    weight: 'bold' // Define os rótulos do eixo Y como negrito
                                },
                                callback: function(value) {
                                    return value + '%'; // Adiciona '%' aos rótulos do eixo Y
                                }
                            },
                            grid: {
                                color: 'rgba(200, 200, 200, 0.5)' // Cor da grade do eixo Y
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: true, // Exibe a legenda
                            position: 'bottom', // Posição da legenda
                            labels: {
                                boxWidth: 10, // Largura da caixa da legenda
                                color: '#6272a4', // Cor da legenda
                                font: {
                                    weight: 'bold' // Define a fonte da legenda como negrito
                                }
                            }
                        }
                    }
                }
            });
        }
    })
    .catch(error => {
        // Loga qualquer erro encontrado durante a requisição
        console.error("Erro ao buscar os dados dos robôs:", error);
    });
}

// Função para obter o valor de tensão com base no tipo de interpolação
function getTensionValue(type) {
    // Retorna o valor de tensão baseado no tipo selecionado
    switch (type) {
        case 'monotone':
            return 0.2; // Suavização
        case 'step':
            return false; // Gráfico de etapas
        default:
            return 0.1; // Linear
    }
}

// Mostrar ou ocultar o filtro
const showFilterButton = document.getElementById('show-filter-button'); // Botão para mostrar/ocultar
const roboSelector = document.getElementById('robo-selector'); // Seletor de robôs
showFilterButton.addEventListener('click', () => {
    // Alterna a visibilidade do seletor
    roboSelector.style.display = roboSelector.style.display === 'none' ? 'block' : 'none';
});

// Carregar robôs e atualizar gráfico inicialmente com os robôs padrão
function loadRobos() {
    // Faz uma requisição para a URL '/get_timeline-data/'
    fetch('/get_timeline-data/')
    .then(response => response.json()) // Converte a resposta em JSON
    .then(data => {
        allRobos = Object.keys(data); // Armazena todos os robôs disponíveis
        const robosSelect = document.getElementById('robos'); // Seleciona o elemento de robôs
        allRobos.forEach((robo) => {
            const option = document.createElement('option'); // Cria uma nova opção
            option.value = robo; // Define o valor da opção
            option.text = robo; // Define o texto da opção
            robosSelect.appendChild(option); // Adiciona a opção ao seletor
        });

        // Selecionar os robôs padrão
        defaultRobos.forEach((robo) => {
            const option = Array.from(robosSelect.options).find(opt => opt.value === robo); // Busca a opção correspondente
            if (option) option.selected = true; // Marca a opção como selecionada
        });

        // Buscar os dados e atualizar o gráfico inicialmente
        fetchData(defaultRobos); // Chama a função para buscar dados com os robôs padrão
    });
}

// Atualizar gráfico ao selecionar robôs
document.getElementById('updateChart').addEventListener('click', () => {
    // Obtém os robôs selecionados
    const robosSelecionados = Array.from(document.getElementById('robos').selectedOptions).map(opt => opt.value);
    if (robosSelecionados.length > maxRobos) {
        alert('Por favor, selecione no máximo 6 robôs.'); // Alerta se ultrapassar o limite
    } else {
        fetchData(robosSelecionados); // Chama a função para buscar dados dos robôs selecionados
    }
});

// Carrega os robôs ao iniciar
loadRobos();

// Atualiza os cartões após adicionar os títulos
document.addEventListener("DOMContentLoaded", function() {
    const containers = document.querySelectorAll('.container'); // Seleciona todos os contêineres

    containers.forEach(container => {
        const roboName = container.id.replace('container-', '').replace(/-/g, ' ').toUpperCase(); // Gera o título
        
        // Verifica se o título já existe para evitar duplicação
        if (!container.querySelector('h3')) {
            const h3 = document.createElement('h3'); // Cria um novo elemento h3
            h3.innerText = roboName; // Define o texto do título
            container.appendChild(h3); // Adiciona o título ao contêiner
        }

        if (!container.querySelector('.card')) {
            const card = document.createElement('div'); // Cria um novo card
            card.className = 'card'; // Define a classe do card
            card.innerText = '0'; // Valor inicial, pode ser atualizado mais tarde
            container.appendChild(card); // Adiciona o card ao contêiner
        }

        if (!container.querySelector('h4')) {
            const h4 = document.createElement('h4'); // Cria um novo elemento h4
            h4.innerText = 'Informações adicionais'; // Define o texto do h4
            container.appendChild(h4); // Adiciona o h4 ao contêiner
        }
    });

    // Atualizar os cartões após adicionar os títulos
    updateCards(); // Chama a função para atualizar os cartões
});

// Função para definir a cor do card com base no desempenho
function definirCorCard(robosFuncionando, robosMeta) {
    // Previne divisão por zero
    let ratio = robosFuncionando / robosMeta; // Calcula a razão

    if (robosMeta === 0 ) {
        return "gray";  // Se não há robôs esperados, cor indefinida
    }
    // Define a cor com base na razão
    if (ratio >= 0.8) {
        return "#00FF00";  // Verde
    } else if (ratio >= 0.5) {
        return "#FFFF00";  // Amarelo
    } else if (ratio > 0) {
        return "#FF0000";  // Vermelho
    } else {
        return "gray";  // cinza
    }            
}

// Chama a função para atualizar os cartões ao carregar a página
updateCards();

// Atualiza os cards a cada 10 segundos
setInterval(updateCards, 10000); // Chama a função 'updateCards' a cada 10 segundos


// Formata o número com separadores de milhar
function formatarNumero(numero) {
    return numero.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
}

// Atualiza as informações adicionais com base nos dados minerados
function updateInformacoesAdicionais(totalMineradoData) {
    // Mapeia as seções dos robôs
    const roboSections = {
        'RFB': 'container-RFB',
        'WHATSAPP': 'container-WHATSAPP',
        'SEFAZ': 'container-SEFAZ',
        'VTCALL': 'container-VTCALL',
        'MEU NEGOCIO': 'container-MEU-NEGOCIO',
        'MIDIAS': 'container-MIDIAS',
        'WHOISBR': 'container-WHOISBR',
        'WHOIS INT': 'container-WHOISINT',
        'SITE': 'container-SITES',
        'EMAIL': 'container-EMAIL',
        'PORTABILIDADE': 'container-PORTABILIDADE',
        'INPI': 'container-INPI-EMPRESA',
        'INPIMARCA': 'container-INPI-MARCA',
        'PROTESTO': 'container-PROTESTO',
        'SMS': 'container-SMS',
        'LINKEDIN': 'container-LINKEDIN',
        'CEP CRUZAMENTO': 'container-CRUZAR-CEP',
        'EMAIL VALIDACAO': 'container-VALIDA-EMAIL',
        'GENERO IDENTIFICACAO': 'container-GENERO-IDENTIFICACAO',
        'GEOLOCALIZACAO': 'container-GEOLOCAL-EMPRESA',
        'RAMO EMPRESA': 'container-EMPRESA-PESQUISA',
        'TELEFONE VALIDACAO': 'container-VALIDA-TELEFONE',
        'FACE IDADE': 'container-FACE-IDADE-GENERO',
        'WHATSAPP LINKEDIN': 'container-WHATSAPP-LINKEDIN',
        'WHATSAPP IMAGEM': 'container-WHATSAPP-IMAGEM',
        'CRFBGOOGLE': 'container-RFB-GOOGLE',
        'OAB': 'container-OAB',
        'GOOGLE CATEGORIA': 'container-GOOGLE-CATEGORIA',
        'INSTAGRAM': 'container-INSTAGRAM',
        'FACEBOOK': 'container-FACEBOOK',
    };

    // Atualiza as informações adicionais
    Object.keys(roboSections).forEach(robo => {
        const section = document.getElementById(roboSections[robo]);
        if (section) {
            const totalMinerado = totalMineradoData[robo.toUpperCase()] !== null ? totalMineradoData[robo.toUpperCase()] : 0; // Pega o total minerado ou 0 se não houver
            const h4 = section.querySelector('h4'); // A tag h4 que contém "Informações adicionais"
            h4.innerText = `${formatarNumero(totalMinerado)}`; // Atualiza o texto
        }
    });
}


// Função para buscar os dados dos robôs e atualizar os cards
function updateCards() {
    Promise.all([
        fetch('/get_bots_meta/'),
        fetch('/get_bots_funcionando/'),
        fetch('/get_total_minerado/')
    ])
    .then(responses => {
        if (!responses[0].ok || !responses[1].ok || !responses[2].ok) {
            throw new Error('Erro ao buscar os dados dos robôs');
        }
        return Promise.all(responses.map(response => response.json()));
    })
    .then(([metaData, funcionandoData, totalMineradoData]) => {
        console.log('Funcionando Data:', funcionandoData);
        if (metaData.status === 'success' && funcionandoData.status === 'success' && totalMineradoData.status === 'success') {
            // Atualize os cards aqui
            const roboSections = {
                'RFB': 'container-RFB',
                'WHATSAPP': 'container-WHATSAPP',
                'SEFAZ': 'container-SEFAZ',
                'VTCALL': 'container-VTCALL',
                'MEU NEGOCIO': 'container-MEU-NEGOCIO',
                'MIDIAS': 'container-MIDIAS',
                'WHOISBR': 'container-WHOISBR',
                'WHOIS INT': 'container-WHOISINT',
                'SITE': 'container-SITES',
                'EMAIL': 'container-EMAIL',
                'PORTABILIDADE': 'container-PORTABILIDADE',
                'INPI': 'container-INPI-EMPRESA',
                'INPIMARCA': 'container-INPI-MARCA',
                'PROTESTO': 'container-PROTESTO',
                'SMS': 'container-SMS',
                'LINKEDIN': 'container-LINKEDIN',
                'CEP CRUZAMENTO': 'container-CRUZAR-CEP',
                'EMAIL VALIDACAO': 'container-VALIDA-EMAIL',
                'GENERO IDENTIFICACAO': 'container-GENERO-IDENTIFICACAO',
                'GEOLOCALIZACAO': 'container-GEOLOCAL-EMPRESA',
                'RAMO EMPRESA': 'container-EMPRESA-PESQUISA',
                'TELEFONE VALIDACAO': 'container-VALIDA-TELEFONE',
                'FACE IDADE': 'container-FACE-IDADE-GENERO',
                'WHATSAPP LINKEDIN': 'container-WHATSAPP-LINKEDIN',
                'WHATSAPP IMAGEM': 'container-WHATSAPP-IMAGEM',
                'CRFBGOOGLE': 'container-RFB-GOOGLE',
                'OAB': 'container-OAB',
                'GOOGLE CATEGORIA': 'container-GOOGLE-CATEGORIA',
                'INSTAGRAM': 'container-INSTAGRAM',
                'FACEBOOK': 'container-FACEBOOK',
                
            };

            Object.keys(roboSections).forEach(robo => {
                const section = document.getElementById(roboSections[robo]);
                if (section) {
                    const card = section.querySelector('.card');
                    const value = funcionandoData.data[robo] || 0; // Valor dos robôs funcionando
                    card.textContent = value; // Atualiza o valor
                    const metaValue = metaData.data[robo] || 0; // Valor da meta
                    card.style.backgroundColor = definirCorCard(value, metaValue); // Defina a cor do card
                    
                    //console.log('Dados do VTCALL:', funcionandoData.data['VTCall']);
                    console.log('Dados do funcionamento:', funcionandoData.data);
                    // Verifique o valor de VTCALL
                    if (robo === 'VTCALL') {
                        console.log('Valor de VTCALL:', value);
                    }
                }
            });
            

            // Atualizar as informações adicionais
            updateInformacoesAdicionais(totalMineradoData.total); // Use total em vez de data
        } else {
            console.error('Erro ao buscar os dados dos robôs:', metaData.message || funcionandoData.message || totalMineradoData.message);
        }
    })
    .catch(error => console.error('Erro ao buscar os dados dos robôs:', error));
}

// Chama a função ao carregar a página
updateCards();

// Atualiza os cards a cada 10 segundos
setInterval(updateCards, 10000);

// Função para buscar dados do scroller
async function fetchScrollerData() {
    try {
        const response = await fetch('/get_scroller/');
        const data = await response.json();
        console.log(data);

        if (data.status === 'success') {
            const scrollerContent = document.getElementById('scroller-content');
            scrollerContent.innerHTML = ''; // Limpa o conteúdo anterior

            const items = []; // Array para armazenar os itens

            for (const [robo, indice] of Object.entries(data.total)) {
                if (indice !== null && !isNaN(indice)) {
                    const item = document.createElement('div'); // Cria um novo elemento

                    // Define a cor do texto
                    item.style.color = indice > 0 ? '#00ff00' : (indice < 0 ? '#ff0000' : '#ffffff'); // Verde, vermelho ou branco

                    // Substitui sinais por setas
                    let arrow = indice > 0 ? '<i class="fa-solid fa-caret-up" style="color: #00ff00;"></i>' :
                                 (indice < 0 ? '<i class="fa-solid fa-caret-down" style="color: #ff0000;"></i>' : '');
                    
                    // Adiciona espaçamento entre o nome do robô e a seta
                    item.innerHTML = `
                        <span>${robo}</span>
                        <span style="margin: 0 5px;">${arrow}</span>
                        <span>${Math.abs(parseFloat(indice)).toFixed(2)}%</span>
                    `;

                    items.push(item); // Adiciona ao array de itens
                } else {
                    console.error(`Valor de índice para ${robo} não é um número:`, indice);
                }
            }

            // Adiciona os itens ao contêiner
            items.forEach(item => scrollerContent.appendChild(item));

            // Inicia a rolagem
            startScrolling(items);
        } else {
            console.error(data.message);
        }
    } catch (error) {
        console.error('Erro ao buscar dados do scroller:', error);
    }
}

// Função para iniciar a rolagem
function startScrolling(items) {
    const scrollerContent = document.getElementById('scroller-content');
    const scroller = document.getElementById('scroller');

    // Limita a quantidade de itens visíveis
    const itemsVisible = 5;
    let currentIndex = 0;

    // Adiciona os itens visíveis ao scroller
    function updateScroller() {
        scrollerContent.innerHTML = ''; // Limpa o conteúdo anterior
        const visibleItems = items.slice(currentIndex, currentIndex + itemsVisible);
        visibleItems.forEach(item => scrollerContent.appendChild(item.cloneNode(true))); // Clona os elementos

        // Atualiza o índice
        currentIndex = (currentIndex + 1) % items.length; // Rola para o próximo item
    }

    // Atualiza o scroller a cada 2 segundo
    updateScroller(); // Atualiza imediatamente
    setInterval(updateScroller, 2000); // Atualiza a cada 1 segundo

    // Inicia a rolagem
    let scrollAmount = 0;
    const scrollSpeed = 10; // Velocidade do scroll

    function scroll() {
        scrollAmount += scrollSpeed;

        if (scrollAmount >= scrollerContent.scrollWidth) {
            scrollAmount = 0; // Reinicia o scroll
        }

        scroller.scrollLeft = scrollAmount;

        requestAnimationFrame(scroll);
    }

    scroll(); // Inicia o scroll
}

// Chama a função ao carregar a página
document.addEventListener('DOMContentLoaded', fetchScrollerData);

let isBlockingEnabled = true; // Variável para controlar o bloqueio

    document.addEventListener("keydown", function(event) {
        // Desabilita o bloqueio se Ctrl + Shift + M for pressionado
        if (event.ctrlKey && event.shiftKey && event.key === "M") {
            isBlockingEnabled = !isBlockingEnabled; // Alterna o estado de bloqueio
            return; // Sai da função
        }

        // Bloqueia F12 e Ctrl+Shift+I se o bloqueio estiver habilitado
        if (isBlockingEnabled) {
            if (event.key === "F12" || (event.ctrlKey && event.shiftKey && event.key === "I") || (event.ctrlKey && event.key === "u")) {
                event.preventDefault(); // Bloqueia a ação
            }
        }
    });

    document.addEventListener("contextmenu", function(event) {
        if (isBlockingEnabled) {
            event.preventDefault(); // Bloqueia o menu de contexto
        }
    });

    // Verifica se está em um ambiente de depuração
    const originalConsole = console.log; // Armazena o console original
    console.log = function(...args) {
        if (isBlockingEnabled) {
            // Não faz nada quando as ferramentas de desenvolvedor estão bloqueadas
        } else {
            originalConsole.apply(console, args); // Chama o console original
        }
    };

