"""Regras de negocio da usuaria, escritas como teste executavel.

Estas regras foram definidas por escrito e sao a especificacao do que o
JobRadar deve ou nao notificar. A lista de cidades presenciais e hibridas
fica coberta aqui para qualquer alteracao futura quebrar o teste em vez de
mudar silenciosamente o comportamento em producao.

Regra, resumida:
  BRASIL   -> remoto de qualquer lugar do pais;
              hibrido/presencial SO nas cidades de CIDADES.
  EXTERIOR -> SO remoto, em mercado lusofono; sem mercado declarado,
              exige portugues ou ingles no titulo. Nunca hibrido/presencial.
"""

import pytest

from core.config import (
    LOCATIONS_LINKEDIN_CIDADES_PRESENCIAL,
    LOCATIONS_LINKEDIN_REMOTO_APENAS,
    MERCADOS_REMOTO_ACEITOS,
)
from core.config_intl import (
    DOMINIOS_INDEED_INTL,
    KEYWORDS_INTL,
    LOCATIONS_INTL,
    MERCADOS_REMOTO_ACEITOS_INTL,
    TERMOS_BUSCA_INTL,
)
from core.job import Job
from core.perfis import PERFIL_BR, PERFIL_INTL


def _vaga(titulo, local, modalidade):
    return Job(
        titulo=titulo, empresa="Empresa Teste", local=local,
        link=f"https://exemplo.com/{abs(hash((titulo, local, modalidade)))}",
        site="Teste", modalidade=modalidade,
    )


# Cidades aceitas para vagas presenciais e híbridas.
CIDADES_ACEITAS = [
    "Santa Bárbara d'Oeste", "Piracicaba", "Americana", "Campinas",
    "Nova Odessa", "Sumaré",
]


# ---------------------------------------------------------------- BRASIL

@pytest.mark.parametrize("modalidade", ["Híbrido", "Presencial"])
@pytest.mark.parametrize("cidade", CIDADES_ACEITAS)
def test_br_hibrido_e_presencial_nas_cidades_aceitas(cidade, modalidade):
    assert _vaga("Desenvolvedor Full Stack", cidade, modalidade).combina_com(PERFIL_BR.regras)


# Variacoes de escrita que as fontes realmente usam -- separador, acento e
# caixa nao podem mudar o resultado.
@pytest.mark.parametrize("local", [
    "Piracicaba - SP", "Americana/SP", "Campinas, SP",
    "Nova Odessa - SP", "Sumaré - SP", "Sumare/SP",
])
def test_br_variacoes_de_escrita_da_cidade(local):
    assert _vaga("Desenvolvedor Full Stack", local, "Híbrido").combina_com(PERFIL_BR.regras)


@pytest.mark.parametrize("local", [
    "Santa Bárbara d'Oeste - SP",
    "Santa Barbara D'Oeste, SP",
    "Santa Bárbara do Oeste/SP",
    "Santa Barbara d Oeste - SP",
    "Santa Bárbara dOeste, SP",
    "Santa Bárbara d’Oeste - SP",
    "Sta. Bárbara d'Oeste - SP",
    "Sta Barbara do Oeste, SP",
])
def test_br_variacoes_de_santa_barbara_doeste(local):
    assert _vaga("Desenvolvedor Full Stack", local, "Presencial").combina_com(PERFIL_BR.regras)


def test_linkedin_busca_so_nomes_canonicos_das_cidades():
    assert "Santa Bárbara d'Oeste" in LOCATIONS_LINKEDIN_CIDADES_PRESENCIAL
    assert "Santa Bárbara do Oeste" not in LOCATIONS_LINKEDIN_CIDADES_PRESENCIAL


@pytest.mark.parametrize("modalidade", ["Híbrido", "Presencial"])
@pytest.mark.parametrize("local", [
    "São Paulo - SP", "Belo Horizonte, MG", "Salvador - BA",
    "Rio de Janeiro, RJ", "Curitiba - PR", "Brasília, DF",
    "Fortaleza - CE", "Porto Alegre - RS",
    # Cidades removidas da whitelist por decisão explícita do usuário.
    "Campina Grande - PB", "João Pessoa - PB", "Recife - PE",
    "Natal - RN", "Caruaru - PE", "Manaus - AM", "Maceió - AL",
    "Aracaju - SE",
    "Jaboatão dos Guararapes - PE", "Teresina - PI",
    "São Luís - MA", "Petrolina - PE",
])
def test_br_hibrido_e_presencial_fora_das_cidades_e_rejeitado(local, modalidade):
    assert not _vaga("Desenvolvedor Full Stack", local, modalidade).combina_com(PERFIL_BR.regras)


@pytest.mark.parametrize("local", [
    "Remoto", "Remoto (São Paulo, SP)", "Remoto (Manaus, AM)",
    "Remoto - Brasil", "Remote, Brazil", "Remoto (Belo Horizonte, MG)",
])
def test_br_remoto_no_brasil_e_aceito_de_qualquer_cidade(local):
    """Remoto nao tem restricao de cidade -- a regra de CIDADES vale so
    pra hibrido/presencial."""
    assert _vaga("Desenvolvedor Full Stack", local, "Remoto").combina_com(PERFIL_BR.regras)


@pytest.mark.parametrize("local", [
    "Remote - US only", "Remote, United States", "Remote (Austin, TX)",
    "Remote - India", "Remote - Argentina", "Remote - Spain",
    "Remote - LATAM",
])
def test_br_remoto_de_mercado_nao_aceito_e_rejeitado(local):
    assert not _vaga("Desenvolvedor Full Stack", local, "Remoto").combina_com(PERFIL_BR.regras)


# --------------------------------------------------------- INTERNACIONAL

@pytest.mark.parametrize("local", [
    "Remote - Portugal", "Remote - Angola", "Remote - Mozambique",
    "Remote - Cape Verde",
])
def test_intl_remoto_em_mercado_aceito_e_aceito(local):
    assert _vaga("Full Stack Developer", local, "Remoto").combina_com(PERFIL_INTL.regras)


@pytest.mark.parametrize("local", [
    "Remote - Spain", "Madrid, Spain", "España (En remoto)",
    "Remote - Mexico", "Ciudad de México, México", "Remote - Colombia",
    "Buenos Aires, Argentina", "Remote - Chile", "Remote - Latin America",
])
def test_intl_remoto_em_mercado_hispanofalante_e_rejeitado(local):
    assert not _vaga("Full Stack Developer", local, "Remoto").combina_com(PERFIL_INTL.regras)


@pytest.mark.parametrize("modalidade", ["Híbrido", "Presencial"])
@pytest.mark.parametrize("local", [
    "Madrid, Spain", "Barcelona, España", "Lisboa, Portugal",
    "Ciudad de México, México", "Buenos Aires, Argentina",
])
def test_intl_hibrido_e_presencial_sempre_rejeitado(local, modalidade):
    """Do exterior so interessa vaga remota -- nem Portugal vale
    presencial/hibrida."""
    assert not _vaga("Full Stack Developer", local, modalidade).combina_com(PERFIL_INTL.regras)


@pytest.mark.parametrize("local", [
    "Remote - US only", "Remote, United States", "Remote (Seattle, WA)",
    "Remote, but candidates must be located in the United States",
    "Remote - India", "Remote - United Kingdom",
])
def test_intl_remoto_de_mercado_de_lingua_inglesa_e_rejeitado(local):
    assert not _vaga("Full Stack Developer", local, "Remoto").combina_com(PERFIL_INTL.regras)


def test_intl_titulo_hibrido_vence_a_classificacao_da_fonte():
    """O filtro nativo do LinkedIn as vezes marca como remota uma vaga que
    o proprio anuncio chama de hibrida -- o titulo vence."""
    vaga = _vaga("Full Stack Developer - Hybrid", "Madrid, Spain", "Remoto")
    assert vaga.modalidade == "Híbrido"
    assert not vaga.combina_com(PERFIL_INTL.regras)


def test_intl_remoto_sem_mercado_declarado_exige_idioma_no_titulo():
    """Sem pais declarado nao da pra saber o mercado -- ai o titulo precisa
    dizer o idioma. Sem nenhum dos dois sinais, a vaga nao entra."""
    assert _vaga("Full Stack Developer (Portuguese speaker)", "Remote - Worldwide", "Remoto").combina_com(PERFIL_INTL.regras)
    assert _vaga("Full Stack Developer (English speaking)", "Remote - Worldwide", "Remoto").combina_com(PERFIL_INTL.regras)
    assert not _vaga("Full Stack Developer (Spanish speaker)", "Remote - Worldwide", "Remoto").combina_com(PERFIL_INTL.regras)
    assert not _vaga("Full Stack Developer", "Remote - Worldwide", "Remoto").combina_com(PERFIL_INTL.regras)


def test_fontes_e_termos_nao_buscam_mercado_espanhol():
    assert LOCATIONS_LINKEDIN_REMOTO_APENAS == ["Portugal"]
    assert MERCADOS_REMOTO_ACEITOS == ["Brasil", "Portugal"]
    assert LOCATIONS_INTL == ["Portugal"]
    assert DOMINIOS_INDEED_INTL == {"Portugal": "pt.indeed.com"}
    assert set(MERCADOS_REMOTO_ACEITOS_INTL) == {"Portugal", "Angola", "Moçambique", "Cabo Verde"}
    assert not any("spanish" in termo or "latam" in termo for termo in TERMOS_BUSCA_INTL)
    assert not any("desarroll" in keyword.lower() for keyword in KEYWORDS_INTL)


# ------------------------------------------------------------------ CARGO

@pytest.mark.parametrize("titulo, esperado", [
    ("Desenvolvedor Full Stack Pleno", True),
    ("Backend Developer", True),
    ("Software Engineer", True),
    ("Frontend Developer React", True),
    ("Engenheiro DevOps", True),
    ("Analista de Sistemas", False),             # ambíguo, sem stack
    ("Analista de Sistemas Node.js", True),      # ambíguo + stack
    ("Desenvolvedor Node.js", True),             # tecnologia + cargo
    ("JavaScript Developer", True),              # tecnologia + cargo
    ("AWS Engineer", True),                      # eixo DevOps/cloud
    ("Especialista React", False),               # tecnologia sem cargo de dev
    ("Vendedor Externo", False),
    ("Analista de Dados", False),                # perfil antigo removido
])
def test_cargo_no_titulo(titulo, esperado):
    assert _vaga(titulo, "Campinas - SP", "Presencial").combina_com(PERFIL_BR.regras) is esperado
