# --- Função de Registro de Logs ---
def registrar_log(mensagem: str):
    """Grava as ações e buscas do sistema em um arquivo de texto externo."""
    try:
        with open("historico_pesquisas.txt", "a", encoding="utf-8") as f:
            f.write(f"{mensagem}\n")
    except IOError:
        print("\033[31m Erro ao gravar o arquivo de log.\033[0m")