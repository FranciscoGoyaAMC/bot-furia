# Warning control
import warnings
warnings.filterwarnings('ignore')
from crewai import Agent, Task, Crew
import os
from dotenv import load_dotenv
from crewai_tools import SerperDevTool
from datetime import datetime

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()
SERPER = os.getenv("SERPER_API_KEY")
OPENAI = os.getenv("OPENAI_API_KEY")

# Configuração do modelo de linguagem utilizado
gpt = 'gpt-4o-mini'

# Ferramenta de busca Serper
serper_search_tool = SerperDevTool()

# Agente de suporte
support = Agent(
    role="Especialista em Comunicação e Mídias Sociais",
    name="FURIA",
    llm=gpt,
    memory=True,
    temperature=0,
    tools=[serper_search_tool],
    description="Um assistente virtual especializado em comunicação e mídias sociais, "
                "pronto para ajudar os fãs com qualquer dúvida ou questão relacionada à FURIA."
                "Você é simpático, prestativo e sempre busca fornecer informações precisas e úteis."
                "Se não souber a resposta da pergunta, dirá que não sabe e sugerirá que o usuário entre em contato com o suporte.",
    goal="Ajudar os fãs a encontrar informações sobre a FURIA,"
         "responder a pergunta e fornecer suporte em comunicação e mídias sociais da forma mais simpática e precisa possível. ",
    backstory=("Você é um assistente virtual da FURIA (https://www.furia.gg/), "
         "uma organização de eSports. Você tem acesso a informações sobre a equipe, jogadores, jogos, produtos da loja e muito mais. "
         "Sua missão é ajudar os fãs a encontrar o que precisam e responder suas perguntas da melhor maneira possível. "
         "Você deve ser simpático, prestativo e sempre buscar fornecer informações precisas e úteis. "
         "Se não souber a resposta da pergunta, diga que não sabe e sugira que o usuário entre em contato com o suporte."
         ),
    allow_delegation=False,
    verbose=True
)

# Agente de controle de qualidade
quality_assurance = Agent(
    role="Especialista em Controle de Qualidade e Revisão",
    llm=gpt,
    memory=True,
    temperature=0,
    tools=[serper_search_tool],
    goal="Revisar e garantir a qualidade e a precisão das respostas geradas pelo assistente virtual da FURIA. ",
    backstory=("Você é um especialista em controle de qualidade e revisão que trabalha para a FURIA (https://www.furia.gg/), "
               "responsável por garantir que as respostas a perguntas geradas pelo assistente virtual da FURIA sejam precisas, "
               "úteis e estejam de acordo com a identidade da marca. "
               "Você deve revisar as respostas da pergunta do assistente, corrigir erros e garantir que a comunicação seja clara e profissional. "
              f"Para informações sobre notícias, jogos, elencos, produtos e outros tópicos relacionados à FURIA, você deve garantir que elas estejam atualizadas para o ano de {datetime.now().year}."
               "Entretanto, caso o usuário solicite alguma informações específica sobre um ano diferente, você deve garantir que a resposta esteja correta e atualizada para o ano solicitado."
               "Se a resposta da pergunta não estiver correta ou não for útil, você deve corrigi-la e fornecer uma resposta mais adequada, conforme as informações buscadas na Tool."),
    allow_delegation=False,
    verbose=True
)

# Tarefa de suporte
support_task = Task(
    description= "Responder perguntas sobre a FURIA, um time e-Sports, utilizando as ferramentas disponíveis que forem necessárias."
                 "A pergunta deve ser respondida de forma simpática e prestativa, fornecendo informações úteis e precisas sobre o que ele perguntou"
                 "As respostas para o fã devem ter no máximo 4000 caracteres. "
                 "O nome do fã é: {cliente} e ele quer saber sobre: {pergunta}",
    expected_output="Um texto claro e útil, respondendo a pergunta do fã sobre a FURIA. ",
    agent=support,
    temperature=0
)

# Tarefa de controle de qualidade
quality_assurance_task = Task(
    description="Revisar e garantir a qualidade e a precisão das respostas geradas pelo assistente virtual da FURIA para a pergunta. "
                "As respostas da pergunta devem estar corretas, úteis e de acordo com a identidade da marca e principalmente "
                "Além disso, deve verificar se a resposta possui no máximo 4000 caracteres. "
                "com o que foi solicitado a ele pelo fã na pergunta. Garantindo que a comunicação seja clara, precisa e profissional. "
                "Se a resposta não estiver correta ou não for útil, corrija-a e forneça uma resposta mais adequada."
                "O nome do fã é: {cliente} e ele quer saber sobre: {pergunta}",
    expected_output="Uma resposta em texto revisada e corrigida, garantindo a qualidade e a precisão das respostas geradas pelo assistente virtual da FURIA. ",
    agent=quality_assurance,
    temperature=0
)

# Configuração da equipe (Crew)
crew = Crew(
    agents=[support, quality_assurance],
    tasks=[support_task, quality_assurance_task],
    verbose=True,
    memory=True,
)

# Função para responder perguntas utilizando o CrewAI
def responder_com_crewai(pergunta: str, username: str) -> str:
    """
    Gera uma resposta para a pergunta do usuário utilizando os agentes e tarefas configurados no CrewAI.

    Args:
        pergunta (str): A pergunta feita pelo usuário.
        username (str): O nome do usuário que fez a pergunta.

    Returns:
        str: A resposta gerada pelo CrewAI ou uma mensagem de erro caso não seja possível processar a pergunta.
    """
    context = {
        "cliente": username,
        "pergunta": pergunta,
    }
    try:
        resposta = crew.kickoff(inputs=context)
        return str(resposta) if str(resposta) else "Desculpe, não consegui encontrar uma resposta para sua pergunta."
    except Exception as e:
        return f"Erro ao processar a pergunta: {str(e)}"
