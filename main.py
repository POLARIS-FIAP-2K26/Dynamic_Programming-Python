import requests
import os
import logger  # Importa a funcionalidade do arquivo separado

# --- Definição de Cores ---
cor_reset = "\033[0m"
cor_verde = "\033[32m"
cor_vermelho = "\033[31m"
cor_amarelo = "\033[33m"
cor_ciano = "\033[36m"

# --- Função para limpar o terminal ---
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

# --- Pilha ---
def criar_pilha(): return []
def empilhar(pilha, elemento): pilha.append(elemento)
def esta_vazia(pilha): return len(pilha) == 0
def desempilhar(pilha): return pilha.pop()

# --- API ---
def carregar_dados():
    print(f"{cor_amarelo}Baixando dados da SpaceX...{cor_reset}\n")
    resposta = requests.get("https://api.spacexdata.com/v4/launches")
    if resposta.status_code == 200:
        return resposta.json()
    print(f"{cor_vermelho}Erro ao baixar dados.{cor_reset}")
    return []

# --- Busca Binária Recursiva ---
def busca_binaria(lista, alvo_id, inicio, fim):
    if inicio > fim: 
        return None
    
    meio = (inicio + fim) // 2
    
    if lista[meio]["flight_number"] == alvo_id:
        return lista[meio]
    if alvo_id < lista[meio]["flight_number"]:
        return busca_binaria(lista, alvo_id, inicio, meio - 1)
        
    return busca_binaria(lista, alvo_id, meio + 1, fim)

# --- Função Nova: Formatação Simples dos Detalhes ---
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
        
        if opcao == '1':
            brutos = carregar_dados()
            if brutos:
                pilha = criar_pilha()
                for voo in brutos[:50]:
                    empilhar(pilha, {
                        "flight_number": voo.get("flight_number"),
                        "missao": voo.get("name"),
                        "sucesso": voo.get("success")
                    })
                    
                dados_processados.clear()
                while not esta_vazia(pilha):
                    dados_processados.append(desempilhar(pilha))
                    
                dados_processados.sort(key=lambda x: x["flight_number"])
                print(f"✓ Dados carregados e ordenados com sucesso!")
                
        elif opcao == '2' and dados_processados:
            print(f"{cor_ciano}--- 5 ÚLTIMOS LANÇAMENTOS ---{cor_reset}\n")
            for voo in dados_processados[-5:]:
                status_cor = cor_verde if voo['sucesso'] else cor_vermelho
                status_texto = "Sucesso" if voo['sucesso'] else "Falha"
                print(f"Voo {voo['flight_number']}: {voo['missao']} (Status: {status_cor}{status_texto}{cor_reset})")
                
        elif opcao == '3' and dados_processados:
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
                
        elif opcao == '4':
            print(f"{cor_amarelo}Agradecemos a sua atenção... Até a próxima, professor!{cor_reset}")
            break
            
        else:
            print(f"{cor_vermelho}Opção inválida ou dados ainda não carregados (Execute a opção 1 primeiro).{cor_reset}")
            
        input(f"\n{cor_ciano}Pressione Enter para continuar...{cor_reset}")

if __name__ == "__main__":
    main()