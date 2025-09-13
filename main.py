from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import pandas as pd
from keep_alive import keep_alive

# Mantém o bot online 24h
keep_alive()

# Token do BotFather
TOKEN = "8340156867:AAEOt-raNJNZvz6BOwdCqcgkhJFn5PBz4w4"

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Olá! Envie o nome do produto e eu te retorno o código."
    )

# Busca inteligente com leitura do Excel
async def buscar_codigo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    produto = update.message.text.lower().strip()
    
    try:
        # Ler Excel a cada mensagem
        df = pd.read_excel("produtos.xlsx")
        
        # Garantir que todas as células sejam string e sem NaN
        df['Produtos'] = df['Produtos'].fillna('').astype(str)
        df['Codigos'] = df['Codigos'].fillna('').astype(str)
        
        codigos = dict(zip(df['Produtos'].str.lower(), df['Codigos']))
        
        resultados = []
        for nome, codigo in codigos.items():
            if produto == nome:        # match exato
                resultados = [(nome, codigo)]
                break
            elif produto in nome:      # match parcial
                resultados.append((nome, codigo))

        if resultados:
            resposta = "Encontrei os seguintes produtos:\n"
            for nome, codigo in resultados:
                resposta += f"• {nome} → {codigo}\n"
            await update.message.reply_text(resposta)
        else:
            await update.message.reply_text(f"Não encontrei nenhum produto relacionado a '{produto}'.")
    
    except FileNotFoundError:
        await update.message.reply_text("Erro: não consegui encontrar o arquivo produtos.xlsx.")
    except Exception as e:
        await update.message.reply_text(f"Ocorreu um erro: {e}")

# Configuração do bot
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, buscar_codigo))
    
    print("Bot rodando...")
    app.run_polling()

if __name__ == "__main__":
    main()
