import json  # Biblioteca para trabalhar com arquivos JSON.
import ollama  # Biblioteca para interagir com o modelo de IA 'llama3.2'.
import logging  # Biblioteca para registro de logs.
from datetime import datetime  # Biblioteca para manipulação de data e hora.

# Configuração de logging para salvar eventos e acontecimentos importantes.
logging.basicConfig(
    filename="chatbot.log",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

# Função para salvar o histórico de conversas em um arquivo JSON.
def salvar_historico(dialogo):
    try:
        with open("historico_conversas.json", "w", encoding="utf-8") as arquivo:
            json.dump(dialogo, arquivo, indent=4, ensure_ascii=False)
        logging.info("Histórico de conversas salvo com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao salvar o histórico: {e}")

# Função para mostrar mensagens de boas-vindas personalizadas.
def mostrar_boas_vindas():
    hora = datetime.now().hour
    if hora < 12:
        print("Bom dia! Seja bem-vindo ao ChatBot. Estou à disposição para você.")
    elif hora < 18:
        print("Boa tarde! Vamos bater um papo?")
    else:
        print("Boa noite! Sobre o que você deseja conversar?")

# Função principal.
def main():
    # Mostra mensagem inicial de boas-vindas.
    mostrar_boas_vindas()
    print("Digite 'sair', 'exit' ou 'quit' para encerrar a conversa.")
    print("Digite '/ajuda' para ver os comandos disponíveis.\n")

    dialogo = []  # Inicializa uma lista vazia para armazenar o histórico de diálogo.

    while True:  # Loop principal para interações com o usuário.
        try:
            user_input = input("Você: ")  # Captura a entrada do usuário.
            
            # Comando para encerrar o chat.
            if user_input.lower() in ['sair', 'exit', 'quit']:
                print("Chat encerrado!")
                salvar_historico(dialogo)  # Salva o histórico ao encerrar.
                break

            # Comando para mostrar as opções de ajuda.
            if user_input.lower() == '/ajuda':
                print("Comandos disponíveis:")
                print("- 'sair', 'exit', 'quit': Encerrar o chat.")
                print("- '/ajuda': Mostrar esta lista de comandos.")
                continue
            
            # Adiciona a entrada do usuário ao histórico.
            dialogo.append({'role': 'system', 'content': user_input})
            
            # Interage com o modelo de IA.
            response = ollama.chat(
                model='llama3.2',
                messages=dialogo
            )
            
            # Obtém e exibe a resposta do modelo.
            reply = response['message']['content']
            print("ChatBot:", reply, "\n")
            
            # Adiciona a resposta do chatbot ao histórico.
            dialogo.append({'role': 'assistant', 'content': reply})
            
            # Registra mensagens no log.
            logging.info(f"Usuário: {user_input}")
            logging.info(f"ChatBot: {reply}")

        except Exception as e:
            # Captura e registra erros durante a execução.
            logging.error(f"Erro durante a execução: {e}")
            print("Erro localizado durante execução. Para mais detalhes, verifique o arquivo 'chatbot.log'.")

# Verifica se o script está sendo executado diretamente e inicia a função principal.
if __name__ == "__main__":
    main()