# Importo os módulos necessários para as funcionalidades do chatbot.
import json
import ollama
import logging
from datetime import datetime
import requests

# Configuro o sistema de logging para registrar eventos em um arquivo chamado "chatbot.log".
logging.basicConfig(
    filename="chatbot.log",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

# Defino uma função para salvar o histórico das conversas em um arquivo JSON.
def salvar_historico(dialogo):
    try:
        # Abro (ou crio) um arquivo chamado "historico_conversas.json" e escrevo nele o histórico das conversas.
        with open("historico_conversas.json", "w", encoding="utf-8") as arquivo:
            json.dump(dialogo, arquivo, indent=4, ensure_ascii=False)
        # Registro um evento indicando que o histórico foi salvo com sucesso.
        logging.info("Histórico de conversas salvo com sucesso.")
    except Exception as e:
        # Registro um erro caso algo dê errado durante o salvamento do histórico.
        logging.error(f"Erro ao salvar o histórico: {e}")

# Defino uma função para mostrar uma mensagem de boas-vindas com base no horário atual.
def mostrar_boas_vindas():
    # Obtém a hora atual para decidir a saudação apropriada.
    hora = datetime.now().hour
    if hora < 12:
        print("Bom dia! Seja bem-vindo ao ChatBot. Estou à disposição para você.")
    elif hora < 18:
        print("Boa tarde! Vamos bater um papo?")
    else:
        print("Boa noite! Sobre o que você deseja conversar?")

# Defino uma função para obter a cotação atual do dólar americano em relação ao real.
def obter_cotacao_dolar():
    # Configuro a URL da API da AwesomeAPI para obter os dados de câmbio.
    url = "https://economia.awesomeapi.com.br/last/USD-BRL"
    try:
        # Realizo uma requisição GET para a API.
        response = requests.get(url)
        # Verifico se houve algum erro na requisição.
        response.raise_for_status()
        # Converto a resposta da API para formato JSON e extraio os dados necessários.
        data = response.json()
        cotacao = data['USDBRL']['bid']
        timestamp = data['USDBRL']['timestamp']
        data_hora = datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
        # Registro um evento de sucesso contendo a data e hora da cotação.
        logging.info(f"Cotação do dólar obtida com sucesso em {data_hora}.")
        return cotacao, data_hora
    except requests.exceptions.RequestException as e:
        # Registro um erro se algo der errado na requisição.
        logging.error(f"Erro ao fazer a requisição para a API: {e}")
        return None, None
    except (json.JSONDecodeError, KeyError) as e:
        # Registro um erro caso a resposta da API não esteja no formato esperado.
        logging.error(f"Erro ao processar a resposta da API: {e}")
        return None, None
    except Exception as e:
        # Registro qualquer outro erro inesperado.
        logging.error(f"Erro inesperado: {e}")
        return None, None

# Esta é a função principal do chatbot, onde ocorre a interação com o usuário.
def main():
    # Chamo a função para exibir uma mensagem de boas-vindas.
    mostrar_boas_vindas()
    # Exibo instruções para o usuário sobre como usar o chatbot.
    print("Digite 'sair', 'exit' ou 'quit' para encerrar a conversa.")
    print("Digite '/ajuda' para ver os comandos disponíveis.")
    print("Digite '/dolar' para ver a cotação atual do dólar.\n")

    # Inicializo uma lista para armazenar o histórico do diálogo.
    dialogo = []

    # Início do loop principal que mantém o chatbot ativo enquanto o usuário desejar.
    while True:
        try:
            # Solicito uma entrada de texto do usuário.
            user_input = input("Você: ")

            # Verifico se o usuário deseja encerrar a conversa.
            if user_input.lower() in ['sair', 'exit', 'quit']:
                print("Chat encerrado!")
                # Salvo o histórico do diálogo antes de encerrar.
                salvar_historico(dialogo)
                break

            # Verifico se o usuário pediu ajuda com os comandos disponíveis.
            if user_input.lower() == '/ajuda':
                print("Comandos disponíveis:")
                print("- 'sair', 'exit', 'quit': Encerrar o chat.")
                print("- '/ajuda': Mostrar esta lista de comandos.")
                print("- '/dolar': Ver a cotação atual do dólar.")
                continue

            # Verifico se o usuário pediu a cotação do dólar.
            if user_input.lower() == '/dolar':
                cotacao, data_hora = obter_cotacao_dolar()
                if cotacao:
                    reply = f"A cotação atual do dólar (USD) para o real (BRL) é: R$ {cotacao} (Atualizado em: {data_hora})"
                else:
                    reply = "Não foi possível obter a cotação do dólar no momento."
                # Mostro a resposta ao usuário e a adiciono ao histórico do diálogo.
                print("ChatBot:", reply, "\n")
                dialogo.append({'role': 'assistant', 'content': reply})
                logging.info(f"ChatBot: {reply}")
                continue

            # Adiciono a entrada do usuário ao histórico do diálogo.
            dialogo.append({'role': 'system', 'content': user_input})

            # Envio a entrada do usuário para um modelo de linguagem e obtenho uma resposta.
            response = ollama.chat(
                model='llama3.2',
                messages=dialogo
            )

            # Extraio a mensagem de resposta e a exibo ao usuário.
            reply = response['message']['content']
            print("ChatBot:", reply, "\n")

            # Adiciono a resposta do chatbot ao histórico do diálogo.
            dialogo.append({'role': 'assistant', 'content': reply})

            # Registro as interações no log.
            logging.info(f"Usuário: {user_input}")
            logging.info(f"ChatBot: {reply}")

        except Exception as e:
            # Registro um erro caso algo inesperado aconteça no loop principal.
            logging.error(f"Erro durante a execução: {e}")
            print("Erro localizado durante execução. Para mais detalhes, verifique o arquivo 'chatbot.log'.")

# Verifico se este arquivo está sendo executado diretamente, e chamo a função principal.
if __name__ == "__main__":
    main()
