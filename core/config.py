
import os
from dotenv import load_dotenv

load_dotenv()

# Cargos diretamente compatíveis com o perfil FullStack. Estes termos são
# específicos o bastante para aprovar a vaga pelo título, sem depender de
# uma tecnologia também estar escrita nele.
KEYWORDS_CARGO_FORTE = [
    # FullStack — foco principal do perfil
    "Desenvolvedor Full Stack",
    "Desenvolvedora Full Stack",
    "Desenvolvedor Fullstack",
    "Desenvolvedora Fullstack",
    "Full Stack Developer",
    "Fullstack Developer",
    "Full-Stack Developer",
    "Full Stack Engineer",
    "Fullstack Engineer",
    # Backend — maior afinidade técnica
    "Desenvolvedor Backend",
    "Desenvolvedora Backend",
    "Desenvolvedor Back-end",
    "Backend Developer",
    "Back-end Developer",
    "Backend Engineer",
    # Engenharia/desenvolvimento de software em geral
    "Desenvolvedor de Software",
    "Desenvolvedora de Software",
    "Software Developer",
    "Engenheiro de Software",
    "Engenheira de Software",
    "Software Engineer",
    "Desenvolvedor Web",
    "Desenvolvedora Web",
    "Web Developer",
    # Frontend é aderente pela experiência com React
    "Desenvolvedor Frontend",
    "Desenvolvedora Frontend",
    "Desenvolvedor Front-end",
    "Frontend Developer",
    "Front-end Developer",
    "Frontend Engineer",
    # DevOps é um eixo secundário, mas faz parte da experiência prática
    "Engenheiro DevOps",
    "Engenheira DevOps",
    "DevOps Engineer",
    "Analista DevOps",
]

# Cargos que podem representar desenvolvimento ou uma função mais funcional.
# Só aprovam quando o título também contém uma tecnologia ou área da stack.
KEYWORDS_CARGO_AMBIGUO = [
    "Analista de Sistemas",
    "Systems Analyst",
    "System Analyst",
    "Desenvolvedor de Sistemas",
    "Desenvolvedora de Sistemas",
    "Systems Developer",
    "Application Developer",
]

# Termo que confirma aderência à stack quando o cargo é ambíguo.
QUALIFICADORES_STACK = [
    "node",
    "node.js",
    "nodejs",
    "typescript",
    "javascript",
    "nestjs",
    "react",
    "react.js",
    "full stack",
    "fullstack",
    "backend",
    "frontend",
    "web",
    "api",
    "rest",
    "sql",
    "postgresql",
    "redis",
    "docker",
    "aws",
    "devops",
    "cloud",
]

# Tecnologia que aparece como núcleo do título ("Node.js Developer").
# Só conta como match se o título TAMBÉM tiver uma palavra de cargo — é o
# espelho da regra de cargo ambíguo: a tecnologia sozinha não basta.
FERRAMENTAS_TITULO = [
    "Node",
    "Node.js",
    "NodeJS",
    "JavaScript",
    "TypeScript",
    "NestJS",
    "React",
    "React.js",
    "Docker",
    "AWS",
]

# Palavra de cargo que confirma que a tecnologia faz parte do título de uma
# vaga de desenvolvimento, evitando aprovar cursos e funções não técnicas.
QUALIFICADORES_CARGO = [
    "desenvolvedor",
    "desenvolvedora",
    "developer",
    "engenheiro",
    "engenheira",
    "engineer",
    "programador",
    "programadora",
    "programmer",
    "software",
    "full stack",
    "fullstack",
    "backend",
    "frontend",
    "devops",
]

KEYWORDS = KEYWORDS_CARGO_FORTE + KEYWORDS_CARGO_AMBIGUO

# Termos de busca enviados a cada site. Ficam separados das KEYWORDS de
# propósito: TERMOS_BUSCA é a rede ampla (o que é pesquisado em cada site,
# incluindo termos de tecnologia/stack pra achar vaga com título atípico),
# enquanto as regras de cargo são o filtro final e só olham o título da vaga
# já encontrada. Um termo de tecnologia (ex: "redis") só resulta em
# notificação se o TÍTULO também trouxer cargo aderente — isso evita falso
# positivo de vaga que só cita a ferramenta como diferencial.
#
# TERMOS_CARGO é derivado direto de KEYWORDS (em vez de mantido à mão em
# lista separada) — antes as duas listas divergiam: metade das KEYWORDS
# (ex: "Backend Developer" ou "Software Engineer") nunca seria
# buscada de verdade, só existia como filtro, então só pegava essas vagas
# por sorte via outro termo. Com a derivação automática isso não pode mais
# acontecer — toda keyword nova em KEYWORDS já vira busca também.
TERMOS_CARGO_EXTRA = [
    # termos mais amplos que a keyword exata, mantidos por dar rede mais
    # larga na busca (a keyword em si é mais restrita, de propósito, pra
    # não gerar falso positivo no filtro de título).
    "full stack",
    "fullstack",
    "backend node.js",
    "desenvolvedor node.js",
    "desenvolvedor typescript",
    "desenvolvedor nestjs",
    "desenvolvedor react",
]

TERMOS_CARGO = sorted(set(k.lower() for k in KEYWORDS) | set(TERMOS_CARGO_EXTRA))

# Tecnologias centrais do perfil. Elas ampliam a descoberta porque alguns
# portais pesquisam também na descrição; o filtro final continua exigindo um
# cargo aderente no título.
TERMOS_FERRAMENTA = [
    "node.js",
    "javascript",
    "typescript",
    "nestjs",
    "react",
    "postgresql",
    "redis",
    "docker",
    "aws",
    "github actions",
    "ci/cd",
    "api rest",
    "rest api",
    "nx monorepo",
]

TERMOS_BUSCA = TERMOS_CARGO + TERMOS_FERRAMENTA

# Rodar todos os TERMOS_BUSCA em TODO ciclo é o que
# gera as centenas de sessões de navegador por execução — o custo cresce
# linear com o tamanho da lista, e a lista só cresce (mais ainda com a
# expansão internacional puxando mais termos no radar). TERMOS_POR_CICLO é
# o tamanho do BLOCO usado por ciclo, não o total de termos — main.py roda
# um bloco por vez em rodízio (ver _proximo_bloco_termos) e avança pro
# próximo bloco no ciclo seguinte, salvando a posição no jobs.db. Isso
# desacopla custo por ciclo de tamanho da lista: dobrar TERMOS_BUSCA dobra
# quantos ciclos até cobrir tudo de novo, não o custo de cada ciclo.
TERMOS_POR_CICLO = 10

# Onde vaga HIBRIDA ou PRESENCIAL e aceita (mais "Remoto", que nao e
# cidade e sim a porta de entrada da regra de modalidade remota — ver
# _FLAGS_REMOTO em job.py). Vaga hibrida/presencial fora desta lista e
# rejeitada; e uma whitelist, nao uma preferencia de ordenacao.
#
# Nomes canônicos usados tanto no filtro quanto nas buscas específicas do
# LinkedIn. Cada item aqui gera uma busca adicional por termo.
CIDADES_PRESENCIAIS = [
    "Santa Bárbara d'Oeste",
    "Piracicaba",
    "Americana",
    "Campinas",
    "Nova Odessa",
    "Sumaré",
]

# Grafias alternativas aceitas pelo filtro. Ficam fora das buscas do
# LinkedIn para não repetir a mesma consulta várias vezes. A normalização já
# cobre caixa e acentos; estes aliases tratam pontuação, abreviação e a troca
# de "d'Oeste" por "do Oeste".
VARIANTES_CIDADES = [
    "Santa Bárbara do Oeste",
    "Santa Bárbara d Oeste",
    "Santa Bárbara dOeste",
    "Santa Bárbara d’Oeste",
    "Sta. Bárbara d'Oeste",
    "Sta Bárbara d'Oeste",
    "Sta. Bárbara do Oeste",
    "Sta Bárbara do Oeste",
]

CIDADES = ["Remoto", *CIDADES_PRESENCIAIS, *VARIANTES_CIDADES]

# Vagas como "Backend Developer @ Lisboa" reprovam na localização, não no
# cargo — CIDADES acima é whitelist só de cidade brasileira. Esta lista
# separada permite manter um eixo exploratório presencial em Portugal com
# toggle próprio, sem misturar cidades estrangeiras no filtro principal.
# Canônica aqui porque config_intl.py já
# importa de config.py (não o contrário) — o pipeline internacional reusa
# essa mesma lista em vez de manter uma cópia (risco de divergir, mesmo
# motivo da unificação de _contem_termo/_tem_termo).
CIDADES_EUROPA_IBERICA = [
    "Portugal",
    "Lisboa",
    "Porto",
    "Braga",
]

# Toggle independente do ATIVAR_EIXO_IBERICO de config_intl.py — são dois
# eixos diferentes (esse aqui é do pipeline BR/main.py, aquele é do
# pipeline internacional/main_intl.py), cada um com seu próprio liga/
# desliga, mesmo compartilhando a mesma lista de cidades acima.
#
# DESLIGADO: do mercado internacional, só interessa vaga remota — vaga
# presencial/híbrida em Lisboa/Porto (o que esse eixo notifica, marcada
# "exploratória") não é o que o usuário quer. CIDADES_EUROPA_IBERICA
# continua definida (não precisa apagar) pra caso o eixo volte a ser
# ligado depois — só o toggle muda.
ATIVAR_EIXO_IBERICO_BR = False

# LinkedInScraper é a única fonte do pipeline BR que também alcança vaga
# fora do Brasil (as outras são portais brasileiros) — mas até aqui rodava
# só com location=Brasil fixo no código (scrapers/linkedin.py:88), então
# essa "porta pra fora" nunca era usada.
#
# Mercado "casa": busca modalidade completa (presencial/híbrida + remoto),
# porque o usuário mora aqui e vaga local de verdade interessa.
LOCATIONS_LINKEDIN = ["Brasil"]

# Mercado adicional pesquisado apenas como remoto. Países hispanofalantes
# foram removidos porque o usuário fala português e inglês; buscar nesses
# mercados trazia anúncios cuja descrição estava somente em espanhol.
LOCATIONS_LINKEDIN_REMOTO_APENAS = ["Portugal"]

# MEDIDO: a passada nacional acima (location="Brasil") varre o país inteiro
# e só sobra o que bate em CIDADES depois do filtro — pra termo concorrido
# em SP/RJ/MG (a maioria), as 3 páginas (30 resultados) nunca chegam numa
# vaga de cidade menor do Nordeste, porque o volume dos polos maiores
# ocupa tudo antes. Em termos concorridos como "backend developer", a
# Brasil inteiro veio 100% São Paulo/Curitiba/Brasília, nenhuma do
# Nordeste. Busca ESPECÍFICA por cidade não depende de volume nacional —
# o próprio location= do LinkedIn já restringe o resultado à cidade, então
# funciona mesmo quando SP/RJ dominam o termo. "Remoto" (item de CIDADES)
# não é local de busca de verdade — sai da lista, já coberto pela passada
# remoto=True de LOCATIONS_LINKEDIN acima.
LOCATIONS_LINKEDIN_CIDADES_PRESENCIAL = CIDADES_PRESENCIAIS

# Mercado que a vaga remota precisa aceitar pra contar, quando o texto de
# local DECLARA um escopo geográfico ("Remote — US only", "Remote — India").
# Ver Job.escopo_remoto/RegrasFiltro.mercados_remoto_aceitos em job.py — sem
# isso, uma vaga remota só pra outro país passava igual a uma remota de
# verdade pro Brasil. Vaga remota SEM escopo declarado no texto (a grande
# maioria) continua batendo normalmente, isso só filtra quando a fonte
# EXPLICITA um mercado incompatível.
#
# Escopo remoto explícito aceito no perfil Brasil. LATAM e países
# hispanofalantes ficam fora para impedir que uma busca brasileira aprove
# novamente vagas direcionadas ao mercado espanhol.
MERCADOS_REMOTO_ACEITOS = ["Brasil", "Portugal"]

INTERVALO_MINUTOS = int(os.getenv("INTERVALO_MINUTOS", 180))

# Digest ranqueado (item 08): vaga com Job.pontuar_relevancia() >= este
# limiar notifica na hora (como sempre foi); abaixo disso, fica na fila do
# digest diário — ver _enviar_digest_diario em main.py.
#
# Com limiar 7, um cargo forte Júnior/Pleno em mercado confirmado já recebe
# destaque imediato; títulos sem senioridade informada precisam também citar
# uma tecnologia central da stack para chegar nesse grupo.
LIMIAR_DIGEST_IMEDIATO = 7

# Hora UTC em que o digest diário dispara (uma vez por perfil, por dia —
# ver _enviar_digest_diario). 0 = meia-noite UTC = 21h em Brasília (UTC-3).
# O cron do workflow (0 */3 * * *) já passa por essa hora exata todo dia,
# então não precisa de agendamento à parte.
DIGEST_HORA_UTC = 0

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# Caminho ancorado na RAIZ do projeto, não na pasta deste arquivo.
#
# MEDIDO: o commit b8227b0 ("Reorganiza raiz: ... -> core/") moveu este
# config.py da raiz pra core/. Como DB_PATH era relativo a __file__, o
# banco se mudou junto, em silêncio: data/jobs.db virou core/data/jobs.db.
# Efeito real, confirmado em disco e no jobradar.log:
#   - data/jobs.db (1.080 vagas, versionado) ficou órfão;
#   - core/data/jobs.db nasceu vazio, então iniciar_db() passou a abortar
#     por BancoVazioSuspeito em toda execução local;
#   - no GitHub Actions a pasta core/data/ não existe no repositório, então
#     o banco era recriado do zero a cada run — toda vaga virava "nova"
#     (renotificação a cada 3h), o rodízio de termos travava no offset 0
#     (só os 10 primeiros de 44 termos eram buscados), a fila do digest era
#     descartada e o heartbeat saía a cada ciclo em vez de 1x/dia;
#   - o passo "git add data/jobs.db" do workflow não via mudança nenhuma
#     ("Nada novo pra commitar"), então o estado nunca mais persistiu.
#
# _RAIZ_PROJETO sobe um nível a partir de core/, então o caminho deixa de
# depender de onde este arquivo mora — mover config.py de novo não move
# mais o banco junto. Coberto por tests/test_db_path.py, pra uma
# reorganização futura quebrar o teste em vez da produção.
#
# JOBRADAR_DB_PATH existe pra apontar um banco descartável em teste/
# experimento sem risco de escrever no banco real.
_RAIZ_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.getenv("JOBRADAR_DB_PATH") or os.path.join(_RAIZ_PROJETO, "data", "jobs.db")
