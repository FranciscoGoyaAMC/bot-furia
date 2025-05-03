from dotenv import load_dotenv
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, ContextTypes
import asyncio
from crewai_client import responder_com_crewai
from datetime import datetime

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
USERNAME = os.getenv("BOT_USERNAME")

# COMANDOS

# Comando /start
async def start(update: Update, context: CallbackContext) -> None:
    # Verificar se a mensagem e o usuário existem
    if update.message and update.message.from_user:
        user = update.message.from_user
        first_name = user.first_name if user.first_name else "usuário"
        username = user.username if user.username else ""

        # Montando a mensagem de boas-vindas
        welcome_message = f"🎮 Olá, {first_name}! Seja bem-vindo ao chatbot oficial da FURIA! 🔥\n\n"
        welcome_message += (
            "Aqui estão os comandos que você pode usar:\n"
            "/start - Iniciar o bot e ver a mensagem de boas-vindas\n"
            "/help - Ver todos os comandos disponíveis\n"
            "/noticias - Obter as últimas notícias sobre a FURIA\n"
            "/jogos - Consultar os próximos jogos do time\n"
            "/elenco - Conhecer o elenco da FURIA\n"
            "/loja - Ver produtos exclusivos da FURIA\n"
            "/pergunta - Fazer uma pergunta ao bot"
        )
        
        # Se o usuário tem nome de usuário, adicionar na mensagem
        if username:
            welcome_message += f"\n\nSeu nome de usuário é @{username}? \n 🔥FURIOSO!🔥"
        
        # Enviando a mensagem personalizada
        await update.message.reply_text(welcome_message)
    else:
        # Caso a mensagem ou o usuário não existam
        await update.message.reply_text("Não foi possível identificar o usuário. Tente novamente.")

# Comando /help
async def help(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Aqui estão os comandos disponíveis:\n"
                                    "/start - Iniciar o bot\n"
                                    "/help - Ver ajuda\n"
                                    f"/noticias - Últimas notícias em {datetime.now().year}\n"
                                    f"/jogos - Próximos jogos em {datetime.now().year}\n"
                                    "/elenco - Informações do elenco atual\n"
                                    "/loja - Ver lançamentos recentes dos produtos\n"
                                    "/pergunta - Fazer uma pergunta ao bot\n"
    )
# Comando /noticias
async def noticias(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    query = f"notícias sobre a FURIA em {datetime.now().year}. {user_message}"
    username = update.message.from_user.first_name if update.message and update.message.from_user else "usuário"
    await update.message.reply_text("🔍 Buscando as últimas notícias sobre a FURIA, um momento...")
    resposta = await asyncio.to_thread(responder_com_crewai, query, username)
    resposta = resposta[:4000]  # Limitar a resposta a 4000 caracteres
    await update.message.reply_text(resposta)

# Comando /jogos
async def jogos(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    query = f"próximos jogos da FURIA a partir de {datetime.now().year}. {user_message}"
    username = update.message.from_user.first_name if update.message and update.message.from_user else "usuário"
    await update.message.reply_text("🔍 Buscando informações sobre os próximos jogos da FURIA, um momento...")
    resposta = await asyncio.to_thread(responder_com_crewai, query, username)
    resposta = resposta[:4000]  # Limitar a resposta a 4000 caracteres
    await update.message.reply_text(resposta)

# Comando /elenco
async def elenco(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    query = f"elenco atual da FURIA no ano de {datetime.now().year}. {user_message}"
    await update.message.reply_text("🔍 Buscando informações sobre o elenco da FURIA, um momento...")
    username = update.message.from_user.first_name if update.message and update.message.from_user else "usuário"
    resposta = await asyncio.to_thread(responder_com_crewai, query, username)
    resposta = resposta[:4000]  # Limitar a resposta a 4000 caracteres
    await update.message.reply_text(resposta)

# Comando /loja
async def loja(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    query = f"produtos exclusivos da loja FURIA em {datetime.now().year}. {user_message}"
    await update.message.reply_text("🔍 Buscando informações sobre os produtos da loja FURIA, um momento...")
    username = update.message.from_user.first_name if update.message and update.message.from_user else "usuário"
    resposta = await asyncio.to_thread(responder_com_crewai, query, username)
    resposta = resposta[:4000]  # Limitar a resposta a 4000 caracteres
    await update.message.reply_text(resposta)

# Comando /pergunta
async def pergunta(update: Update, context: CallbackContext) -> None:
    if update.message and update.message.text:
        query = " ".join(context.args)  # pega o texto após o comando
        username = update.message.from_user.first_name if update.message and update.message.from_user else "usuário"
        if query:
            await update.message.reply_text("🔍 Estou buscando essa informação, um momento...")
            resposta = await asyncio.to_thread(responder_com_crewai, query, username)
            resposta = resposta[:4000]  # Limitar a resposta a 4000 caracteres
            await update.message.reply_text(resposta)
        else:
            await update.message.reply_text("Por favor, envie uma pergunta após o comando /pergunta.")

# Função de erro
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log de erro com traceback"""
    print(f"Update {update} causou erro {context.error}")

# Função principal
async def main():
    print("Aplicação iniciada com sucesso!")

    # Criação do Application com o token
    application = Application.builder().token(TOKEN).build()

    # Handlers para os comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("noticias", noticias))
    application.add_handler(CommandHandler("jogos", jogos))
    application.add_handler(CommandHandler("elenco", elenco))
    application.add_handler(CommandHandler("loja", loja))
    application.add_handler(CommandHandler("pergunta", pergunta))
    # Handler de erros
    application.add_error_handler(error)

    # Inicializa e executa o bot
    await application.initialize()  # Inicializa a aplicação
    await application.start()       # Inicia o bot
    await application.updater.start_polling()  # Começa o polling

    # Aguarda até que o programa seja interrompido manualmente
    await asyncio.Event().wait()


# Se o script for executado diretamente, garantir que a execução é feita no loop correto
if __name__ == "__main__":
    asyncio.run(main())  # Executa a função main no loop de eventos
    