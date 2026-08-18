
# Config do programa internacional (busca vaga remota fora do Brasil que
# aceita/pede português ou inglês). Separado do config.py de propósito —
# ver decisão registrada na conversa: misturar ia forçar o filtro de cidade
# do Nordeste e as keywords em português do JobRadar original a servir dois
# propósitos diferentes ao mesmo tempo, deixando os dois mais frágeis.
#
# Credenciais do Telegram e caminho do banco são os MESMOS do projeto
# principal (reaproveita o bot já configurado, e o dedup por link no mesmo
# jobs.db não tem risco de colisão — o id é hash do link, e vaga
# internacional nunca vai ter o mesmo link de uma vaga brasileira).
from core.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, DB_PATH, CIDADES_EUROPA_IBERICA  # noqa: F401

# Cargos FullStack e adjacentes em inglês e português. O foco é
# desenvolvimento web com prioridade para backend/Node.js, sem perder vagas
# generalistas de software, frontend React e DevOps aderentes ao perfil.
KEYWORDS_INTL = [
    # Inglês
    "Full Stack Developer",
    "Fullstack Developer",
    "Full-Stack Developer",
    "Full Stack Engineer",
    "Fullstack Engineer",
    "Backend Developer",
    "Back-end Developer",
    "Backend Engineer",
    "Node.js Developer",
    "NodeJS Developer",
    "NestJS Developer",
    "TypeScript Developer",
    "Software Developer",
    "Software Engineer",
    "Web Developer",
    "Frontend Developer",
    "Front-end Developer",
    "Frontend Engineer",
    "React Developer",
    "DevOps Engineer",
    # Português
    "Desenvolvedor Full Stack",
    "Desenvolvedora Full Stack",
    "Desenvolvedor Fullstack",
    "Desenvolvedor Backend",
    "Desenvolvedora Backend",
    "Desenvolvedor Node.js",
    "Desenvolvedor NestJS",
    "Desenvolvedor TypeScript",
    "Desenvolvedor de Software",
    "Engenheiro de Software",
    "Desenvolvedor Frontend",
    "Desenvolvedor React",
    "Engenheiro DevOps",
]

# Termos de busca alinhados aos idiomas do usuário: português e inglês.
# Os termos puros no fim são seguros porque LinkedIn e Indeed já os executam
# com país lusófono e modalidade remota; o filtro de mercado faz a checagem
# novamente antes da notificação.
TERMOS_BUSCA_INTL = [
    "full stack developer portuguese speaker",
    "full stack developer english speaking",
    "backend developer portuguese speaker",
    "backend developer english speaking",
    "node.js developer portuguese speaker",
    "node.js developer english speaking",
    "software engineer portuguese speaker",
    "software engineer english speaking",
    "devops engineer portuguese speaker",
    "devops engineer english speaking",
    "desenvolvedor full stack remoto",
    "desenvolvedor backend remoto",
    # Cargos puros, sempre escopados por país + remoto nas fontes.
    "full stack developer",
    "backend developer",
    "node.js developer",
    "nestjs developer",
    "typescript developer",
    "software engineer",
    "react developer",
    "devops engineer",
    # Idioma solto amplia a descoberta, mas o filtro continua exigindo cargo.
    "portuguese speaker",
    "portuguese speaking",
    "english speaker",
    "english speaking",
]

# O filtro de idioma é reconferido depois da busca. Sem isso, uma vaga
# remota genérica de desenvolvimento e sem mercado declarado poderia passar
# apenas porque a descrição indexada pelo site continha o termo pesquisado.
# Usado em Job.combina_com() só quando a
# vaga é remota SEM mercado aceito declarado (ver RegrasFiltro.idiomas_
# exigidos e comentário lá) — quando o escopo já é um país lusófono aceito,
# o país é o sinal, essa lista nem entra em jogo.
IDIOMAS_EXIGIDOS_INTL = [
    "portuguese",
    "português",
    "portugues",
    "english",
    "inglês",
    "ingles",
    "lusofono",
    "lusófono",
]

# Rodízio de termos, mesmo mecanismo do TERMOS_POR_CICLO em config.py (ver
# _proximo_bloco_termos em main.py) — só que com chave de metadados própria
# (sufixo "_internacional"), pra não colidir com o rodízio do perfil BR.
# Esse perfil nunca tinha rodízio antes de virar perfil de verdade (rodava a
# lista de termos INTEIRA todo ciclo, sem custo controlado, e nem chegava a
# rodar de fato — não estava no workflow do GitHub Actions). Os termos x
# mercado por fonte já representam várias consultas; bloco de 10 mantém o
# custo por ciclo parecido com o do perfil BR.
TERMOS_POR_CICLO_INTL = 10

# Mercados pesquisados por rodada de busca no LinkedIn (parâmetro location
# do endpoint). Lista enxuta de propósito — cada país aqui multiplica o
# número de buscas (termos x países), então começa pequeno e dá pra
# expandir depois que confirmar que vale o tempo de execução.
#
# Portugal fica como mercado principal: oferece anúncios em português e em
# inglês sem reabrir o volume de vagas espanholas observado na Argentina e
# nos demais mercados hispanofalantes.
LOCATIONS_INTL = [
    "Portugal",
]

# Sem cidade nenhuma — só remoto, de qualquer país. "Remote" cobre o termo
# em inglês (a maioria dos cards vai estar em inglês), "Remoto" cobre os
# poucos que vierem em português.
#
# PROBLEMA que isso sozinho causava: CIDADES_INTL é uma whitelist — só
# aceita "Remote"/"Remoto" no local. Isso rejeita vaga presencial/híbrida
# em Lisboa ou Porto mesmo quando ela é achada de propósito (via
# LOCATIONS_INTL = Portugal), porque o local não escreve "Remote"
# literalmente. Não é uma regra "excluir Portugal" — é a lógica de
# whitelist só admitir o que está na lista, o que dá no mesmo na prática.
#
CIDADES_INTL = ["Remote", "Remoto"]

# Ver MERCADOS_REMOTO_ACEITOS em config.py e Job.escopo_remoto/
# extrair_escopo_remoto em job.py. Duas listas com propósito DIFERENTE,
# mesma lógica de TERMOS_BUSCA/TERMOS_POR_CICLO vs KEYWORDS: LOCATIONS_INTL
# é ONDE BUSCAR (custo real — cada país multiplica busca × termo, então fica
# enxuto nos mercados que mais contratam); esta lista aqui é O QUE ACEITAR
# (custo zero — só comparação de string), então cobre países lusófonos
# reconhecidos pelo extrator. Precisa ser
# abrangente porque desde que _mercado_correspondente() virou allowlist
# estrita (ver job.py) — escopo declarado que não bate aqui é REJEITADO,
# mesmo vindo de um país que o projeto quer aceitar, então faltar um país
# aqui vira falso negativo (barra vaga boa), não falso positivo.
#
# NÃO inclui "Brasil" porque esse pipeline é justamente o de vaga remota
# FORA do Brasil (main.py/PERFIL_BR já cobre o Brasil). Vaga "Remote — US
# only"/"Remote — India"/"Remote — Vietnam" segue sendo rejeitada, agora
# inclusive quando o país não está no dicionário de job.py (ver
# MEDIDO em _mercado_correspondente).
MERCADOS_REMOTO_ACEITOS_INTL = [
    "Portugal",
    "Angola",
    "Moçambique",
    "Cabo Verde",
]

# Eixo separado pra isso, controlado por ATIVAR_EIXO_IBERICO — dá pra
# desligar sem mexer no resto do pipeline internacional (nem em
# CIDADES_INTL). Quando ativo, vaga presencial/híbrida em Portugal
# passa também, mas marcada como "exploratória" na notificação (ver
# main_intl.py), pra distinguir de vaga remota de verdade.
# CIDADES_EUROPA_IBERICA (hoje restrita a Portugal) fica em config.py — o
# pipeline BR (main.py) passou a ter o mesmo eixo (ver ATIVAR_EIXO_IBERICO_BR
# lá), e as duas listas eram idênticas, então centralizei numa só pra não
# correr risco de uma mudar e a outra ficar pra trás. Esse toggle aqui
# continua LOCAL e independente do ATIVAR_EIXO_IBERICO_BR — são eixos de
# pipelines diferentes, cada um liga/desliga por conta própria.
#
# DESLIGADO: do mercado internacional, só interessa vaga remota — vaga
# presencial/híbrida em Lisboa/Porto não é o que o usuário quer, mesmo
# achada de propósito via LOCATIONS_INTL. Continua fácil de religar depois
# (só o toggle), sem apagar nada da lista/lógica.
ATIVAR_EIXO_IBERICO = False

# Indeed usa subdomínio por país, não parâmetro de location como o
# LinkedIn. O domínio português cobre o mercado que permanece no perfil.
#
# Estados Unidos e Reino Unido continuam fora: falar inglês não torna uma
# vaga restrita a residentes desses países elegível. O perfil aceita inglês
# em vagas mundiais sem escopo geográfico, mas não abre mercados "country only".
#
# Mesmo aviso do Indeed BR original: tem proteção anti-bot que pode
# bloquear acesso automatizado (principalmente de IP de nuvem/datacenter),
# mesmo funcionando em teste manual.
DOMINIOS_INDEED_INTL = {
    "Portugal": "pt.indeed.com",
}
