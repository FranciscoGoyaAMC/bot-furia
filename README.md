# 🤖 Chatbot Oficial da FURIA eSports

Bem-vindo ao projeto do **Chatbot Oficial da FURIA**, um assistente virtual que utiliza **CrewAI** e **Python Telegram Bot** para responder perguntas sobre o time de eSports FURIA. Ele oferece informações atualizadas sobre jogos, elenco, produtos da loja e muito mais — tudo de forma simpática e interativa pelo Telegram!

## 🚀 Funcionalidades

* Comandos automatizados para:

  * `/start` – Boas-vindas ao usuário
  * `/help` – Lista de comandos disponíveis
  * `/noticias` – Últimas notícias sobre a FURIA
  * `/jogos` – Próximos jogos da equipe
  * `/elenco` – Elenco atual da FURIA
  * `/loja` – Produtos e lançamentos da loja oficial
  * `/pergunta` – Pergunta personalizada ao assistente virtual

* Respostas geradas por **CrewAI**, com dois agentes:

  * `FURIA`: Agente simpático e informativo que responde às perguntas
  * `Quality Assurance`: Garante que as respostas estejam claras, corretas e alinhadas com a identidade da marca

* Integração com **Serper** para realizar buscas e recuperar informações em tempo real.

## 📁 Estrutura do Projeto

```
.
├── crewai_client.py       # Lógica dos agentes e tarefas CrewAI
├── telegram_bot.py        # Bot Telegram com comandos integrados ao CrewAI
├── requirements.txt       # Dependências do projeto
├── .env                   # Chaves de API (não incluído no repositório)
└── README.md              # Documentação do projeto
```

## 🔧 Instalação e Execução

### 1. Clone o repositório

```bash
git clone https://github.com/FranciscoGoyaAMC/bot-furia
cd bot-furia
```

### 2. Crie e ative um ambiente virtual (opcional, mas recomendado)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o arquivo `.env`

Crie um arquivo `.env` com as seguintes variáveis:

```env
TELEGRAM_TOKEN=seu_token_do_telegram
BOT_USERNAME=seu_nome_do_bot
SERPER_API_KEY=sua_chave_serper
OPENAI_API_KEY=sua_chave_openai
```

### 5. Execute o bot

```bash
python telegram_bot.py
```

## 🧠 Tecnologias Utilizadas

* [Python 3.10+](https://www.python.org/)
* [CrewAI](https://docs.crewai.com/) – Framework de agentes colaborativos
* [Python Telegram Bot 20.3](https://docs.python-telegram-bot.org/)
* [Serper.dev](https://serper.dev/) – Ferramenta de busca com IA
* [OpenAI GPT-4o-mini](https://openai.com)

## 🤝 Contribuições

Pull requests são bem-vindos! Sinta-se livre para sugerir melhorias, novas funcionalidades ou corrigir bugs.

---

🔥 **FURIA eSports** – "Nada como ser FURIOSO!"
