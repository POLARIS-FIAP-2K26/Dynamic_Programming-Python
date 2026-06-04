import requests
import os
import logger  

# --- Definição de Cores ---
cor_reset = "\033[0m"
cor_verde = "\033[32m"
cor_vermelho = "\033[31m"
cor_amarelo = "\033[33m"
cor_ciano = "\033[36m"

# --- Função para limpar o terminal ---
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

# --- Pilha (LIFO) ---
def criar_pilha(): 
    return []

def push(stack, item): 
    stack.append(item)

def is_empty(stack): 
    return len(stack) == 0

def pop(stack): 
    return stack.pop()

# --- API ---
def carregar_dados():
    print(f"{cor_amarelo}Baixando dados da SpaceX...{cor_reset}\n")
    resposta = requests.get("https://api.spacexdata.com/v4/launches")
    
    if resposta.status_code == 200:
        return resposta.json()
        
    print(f"{cor_vermelho}Erro ao baixar dados.{cor_reset}")
    return []

# --- Busca Binária Recursiva ---
def busca_binaria(stack, alvo_id, inicio, fim):
    if inicio > fim: 
        return None
    
    meio = (inicio + fim) // 2
    
    if stack[meio]["flight_number"] == alvo_id:
        return stack[meio]
        
    if alvo_id < stack[meio]["flight_number"]:
        return busca_binaria(stack, alvo_id, inicio, meio - 1)
        
    return busca_binaria(stack, alvo_id, meio + 1, fim)

# --- Formatação dos Detalhes ---
def formatar_detalhes(resultado):
    status = f"{cor_verde}Sucesso{cor_reset}" if resultado['sucesso'] else f"{cor_vermelho}Falha{cor_reset}"
    print(f"{cor_ciano}--- DETALHES DA MISSÃO ---{cor_reset}")
    print(f" Número do Voo : {resultado['flight_number']}")
    print(f" Nome da Missão: {resultado['missao']}")
    print(f" Status        : {status}")
    print(f"{cor_ciano}--------------------------{cor_reset}")

# --- Execução Principal ---
def main():
    dados_processados = []
    primeira_execucao = True
    
    while True:
        limpar_tela() 
        
        if primeira_execucao:
            print(f"{cor_ciano}--- Seja bem vindo ao projeto Polaris ---{cor_reset}\n")
            primeira_execucao = False 
            
        print(f"{cor_ciano}-{cor_reset}" * 25)
        print(" [1] Baixar Dados")
        print(" [2] Ver 5 Últimos")
        print(" [3] Buscar Voo")
        print(" [4] Sair")
        print(f"{cor_ciano}-{cor_reset}" * 25)
        opcao = input(f"\n {cor_amarelo}❯ Digite sua escolha:{cor_reset} ")
        
        limpar_tela() 
        
        match opcao:
            case '1':
                brutos = carregar_dados()
                if brutos:
                    pilha = criar_pilha()
                    
                    # Empilha os primeiros 50 registros da API
                    for voo in brutos[:50]:
                        push(pilha, {
                            "flight_number": voo.get("flight_number"),
                            "missao": voo.get("name"),
                            "sucesso": voo.get("success")
                        })
                        
                    dados_processados.clear()
                    
                    # Desempilha pra a lista de processados
                    while not is_empty(pilha):
                        dados_processados.append(pop(pilha))
                        
                    # Ordenação obrigatória pra funcionar direitinho a busca binária
                    dados_processados.sort(key=lambda x: x["flight_number"])
                    print(f"✓ Dados carregados e ordenados com sucesso!")
                    
            case '2' if dados_processados:
                print(f"{cor_ciano}--- 5 ÚLTIMOS LANÇAMENTOS ---{cor_reset}\n")
                for voo in dados_processados[-5:]:
                    status_cor = cor_verde if voo['sucesso'] else cor_vermelho
                    status_texto = "Sucesso" if voo['sucesso'] else "Falha"
                    print(f"Voo {voo['flight_number']}: {voo['missao']} (Status: {status_cor}{status_texto}{cor_reset})")
                    
            case '3' if dados_processados:
                try:
                    alvo = int(input(f"{cor_amarelo}Digite o número do voo:{cor_reset} "))
                    print() 
                    
                    resultado = busca_binaria(dados_processados, alvo, 0, len(dados_processados) - 1)
                    
                    if resultado:
                        formatar_detalhes(resultado)
                        logger.registrar_log(f"Busca efetuada - Voo {alvo}: Encontrado (Missao: {resultado['missao']})")
                    else:
                        print(f"{cor_vermelho}❌ O voo número {alvo} não foi encontrado.{cor_reset}")
                        logger.registrar_log(f"Busca efetuada - Voo {alvo}: Nao encontrado na base")
                        
                except ValueError:
                    print(f"{cor_vermelho}⚠️ Erro: Digite apenas números inteiros.{cor_reset}")
                    
            case '4':
                print(f"{cor_amarelo}Agradecemos a sua atenção... Até a próxima!{cor_reset}")
                break
                
            case _:
                print(f"{cor_vermelho}Opção inválida ou dados ainda não carregados (Execute a opção 1 primeiro).{cor_reset}")
            
        input(f"\n{cor_ciano}Pressione Enter para continuar...{cor_reset}")

if __name__ == "__main__":
    main()