# 🚀 Projeto Polaris: Sistema de Rastreamento Espacial (SpaceX)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![FIAP](https://img.shields.io/badge/FIAP-Global_Solution-ed145b?style=for-the-badge)
![API](https://img.shields.io/badge/API-SpaceX-black?style=for-the-badge)

Projeto desenvolvido como parte da avaliação **Global Solution** da disciplina de **Dynamic Programming (2ESPY)**, ministrada pelo Prof. Paulo Viníccius Vieira, na **FIAP**.

---

## 👨‍🚀 Integrantes do Grupo

* **Arthur Berlofa Bosi** – RM: 564438
* **Levi de Jesus** – RM: 563279
* **Luigi Borghi** – RM: 563096
* **Ulisses Ribeiro** – RM: 562230

---

## 🌌 Contexto: A Nova Economia Espacial

O espaço sempre foi visto como a última fronteira, mas hoje representa um dos maiores territórios de inovação e negócios. A economia espacial moderna utiliza tecnologias e dados para monitorar o clima, evitar desastres, conectar regiões remotas e realizar missões de exploração e transporte.

Neste cenário de rápida expansão, empresas como a SpaceX lançam foguetes e satélites com uma frequência sem precedentes, gerando um volume massivo de dados de telemetria e status de missão. 

### 🎯 Definição do Problema Escolhido
Para gerir essa vasta quantidade de dados na Indústria Espacial, é necessário um sistema rápido e confiável que consiga processar pacotes de informações contínuas e permita buscas instantâneas sobre o status de qualquer missão. O **Projeto Polaris** resolve este problema ao consumir dados reais da API pública da SpaceX, utilizando estruturas de dados adequadas para processamento de streaming (Pilhas) e algoritmos de alta performance (Busca Binária) para rastreamento.

---

## 🛠️ Lógica de Resolução e Estruturas de Dados

Para cumprir os requisitos técnicos e simular um ambiente real de controle de missão, adotamos as seguintes estratégias:

1. **Consumo de API:** Os dados são obtidos diretamente da `SpaceX API (v4)`, garantindo o processamento de mais de 30 registros reais e contínuos de lançamentos.
2. **Uso de Pilha (LIFO):** Em sistemas de telemetria espacial, os pacotes de dados mais recentes gerados (últimos a entrar) costumam ser os mais críticos para análise imediata em caso de falha. Por isso, os dados da API são armazenados e processados utilizando o conceito *Last In, First Out*.
3. **Busca Binária Recursiva:** Para localizar uma missão específica em uma grande base de dados sem perda de performance, utilizamos a Busca Binária (com complexidade $O(\log n)$). A recursividade foi aplicada para dividir a lista pela metade a cada iteração, tornando a busca extremamente eficiente.
4. **Persistência em Logs:** Implementação de um módulo separado (`logger.py`) para registrar todas as buscas efetuadas pelos operadores do sistema, garantindo a rastreabilidade das ações.

---

## ⚙️ Detalhamento das Funções do Sistema

O código foi rigorosamente modularizado para facilitar a manutenção e escalabilidade.

### Módulo Principal (`main.py`)
* `limpar_tela()`: Responsável por limpar o terminal adaptando-se automaticamente ao sistema operacional (Windows/Linux/Mac), mantendo a interface de linha de comando (CLI) limpa e focada.
* `criar_pilha()`, `empilhar()`, `esta_vazia()`, `desempilhar()`: Conjunto de funções clássicas para manipulação da estrutura de dados Pilha.
* `carregar_dados()`: Realiza a requisição HTTP GET para a API da SpaceX e faz o tratamento (parse) do JSON retornado.
* `busca_binaria(lista, alvo_id, inicio, fim)`: Algoritmo central do sistema. Recebe a lista ordenada de voos e utiliza a técnica de divisão e conquista (recursiva) para localizar um `flight_number` específico.
* `formatar_detalhes(resultado)`: Função de interface que exibe os dados da missão encontrada formatados em um painel visual utilizando caracteres ASCII e códigos de cores ANSI.
* `main()`: Função que concentra o fluxo de execução principal, o loop do menu interativo e o tratamento de erros e exceções (como `ValueError`).

### Módulo de Registro (`logger.py`)
* `registrar_log(mensagem)`: Abre o arquivo `log_sistema.txt` em modo de adição (*append*) e salva as buscas efetuadas, de forma isolada da lógica principal do sistema.

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
Certifique-se de ter o Python 3.8 ou superior instalado em sua máquina. O projeto utiliza a biblioteca `requests` para o consumo da API.

### Passo a Passo

1. Clone este repositório para a sua máquina local:
   ```bash
   git clone [https://github.com/SeuUsuario/Projeto-Polaris.git](https://github.com/SeuUsuario/Projeto-Polaris.git)
