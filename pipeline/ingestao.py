"""
pipeline/ingestao.py

Lê respostas do formulário de discovery (JSON, CSV ou entrada manual)
e grava o input estruturado em inputs/{cliente}_{data}_formulario.json.
"""

import json
import csv
import sys
import os
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent.parent
INPUTS_DIR = ROOT / "inputs"

SEGMENTOS_MAP = {
    "varejo": "varejo",
    "e-commerce": "varejo",
    "franquia": "varejo",
    "financeiro": "financeiro",
    "fintech": "financeiro",
    "seguradora": "financeiro",
    "saude": "saude",
    "saúde": "saude",
    "healthtech": "saude",
    "plano de saude": "saude",
    "servicos": "servicos",
    "serviços": "servicos",
    "consultoria": "servicos",
    "industria": "industria",
    "indústria": "industria",
    "manufatura": "industria",
}

PACOTES_MAP = {
    "1": "diagnostico",
    "diagnostico": "diagnostico",
    "diagnóstico": "diagnostico",
    "2": "diagnostico_demo",
    "demo": "diagnostico_demo",
    "diagnostico_demo": "diagnostico_demo",
    "3": "diagnostico_demo_proposta",
    "proposta": "diagnostico_demo_proposta",
    "completo": "diagnostico_demo_proposta",
    "diagnostico_demo_proposta": "diagnostico_demo_proposta",
}

CLOUDS_POR_DOR = {
    "nao sei onde estao minhas oportunidades": "Sales Cloud",
    "time nao registra atividades": "Sales Cloud",
    "perco negocios sem entender o motivo": "Sales Cloud",
    "ciclo de vendas muito longo": "Sales Cloud",
    "previsao de receita": "Sales Cloud",
    "atendimento nao tem historico": "Service Cloud",
    "leads nao sao seguidos": "Marketing Cloud",
    "performance individual": "Sales Cloud",
    "dados duplicados": "Data Cloud",
    "integracao dificil": "Data Cloud",
    "relatorios demoram": "Sales Cloud",
    "falta visibilidade do funil": "Sales Cloud",
}

CLOUDS_POR_SEGMENTO = {
    "varejo": ("Sales Cloud", ["Commerce Cloud", "Marketing Cloud"]),
    "financeiro": ("Financial Services Cloud", ["Sales Cloud", "Service Cloud"]),
    "saude": ("Health Cloud", ["Service Cloud", "Einstein / Agentforce"]),
    "servicos": ("Sales Cloud", ["Service Cloud", "Experience Cloud"]),
    "industria": ("Sales Cloud", ["Service Cloud", "Data Cloud"]),
    "outro": ("Sales Cloud", ["Service Cloud"]),
}

LICENCAD_POR_CLOUD = {
    "Sales Cloud": (150, 300),
    "Service Cloud": (150, 300),
    "Marketing Cloud": (400, 800),
    "Financial Services Cloud": (300, 600),
    "Health Cloud": (300, 600),
    "Commerce Cloud": (500, 1000),
    "Data Cloud": (500, 1200),
    "Experience Cloud": (100, 200),
    "Einstein / Agentforce": (200, 400),
}

IMPL_POR_PORTE = {
    "1-10": (8000, 20000),
    "11-50": (15000, 40000),
    "51-200": (30000, 80000),
    "201-500": (60000, 150000),
    "500+": (120000, 300000),
}


def normalizar_texto(texto: str) -> str:
    return texto.lower().strip()


def normalizar_segmento(resposta: str) -> str:
    resp = normalizar_texto(resposta)
    for chave, valor in SEGMENTOS_MAP.items():
        if chave in resp:
            return valor
    return "outro"


def normalizar_pacote(resposta: str) -> str:
    resp = normalizar_texto(resposta).replace(" ", "_").replace("+", "_")
    for chave, valor in PACOTES_MAP.items():
        if chave in resp:
            return valor
    return "diagnostico"


def detectar_cloud_recomendada(dados: dict) -> dict:
    segmento = dados.get("segmento", "outro")
    dores = [normalizar_texto(d) for d in dados.get("dores", [])]

    votos: dict[str, int] = {}
    for dor in dores:
        for chave, cloud in CLOUDS_POR_DOR.items():
            if any(palavra in dor for palavra in chave.split()):
                votos[cloud] = votos.get(cloud, 0) + 1

    cloud_principal, adicionais = CLOUDS_POR_SEGMENTO.get(segmento, ("Sales Cloud", []))

    if votos:
        cloud_votos = max(votos, key=lambda c: votos[c])
        if votos[cloud_votos] >= 2:
            cloud_principal = cloud_votos

    justificativas = {
        "Sales Cloud": "Alta concentração de dores relacionadas a pipeline e gestão comercial.",
        "Service Cloud": "Dores centradas em atendimento e histórico de clientes.",
        "Marketing Cloud": "Leads não seguidos e baixa conversão indicam gap de nutrição.",
        "Financial Services Cloud": "Segmento financeiro com requisitos regulatórios e de relacionamento.",
        "Health Cloud": "Segmento saúde com necessidades específicas de coordenação de cuidados.",
        "Data Cloud": "Múltiplos sistemas e dados fragmentados exigem unificação.",
        "Commerce Cloud": "Operação de e-commerce ou varejo com gestão de pedidos.",
        "Einstein / Agentforce": "Complexidade e volume que se beneficiam de IA e automação.",
        "Experience Cloud": "Necessidade de portal para clientes ou parceiros.",
    }

    return {
        "cloud": cloud_principal,
        "justificativa": justificativas.get(cloud_principal, "Alinhamento com o perfil do negócio."),
        "adicional": adicionais,
    }


def estimar_investimento(dados: dict) -> dict:
    cloud = dados.get("cloud_recomendada", {}).get("cloud", "Sales Cloud")
    porte = dados.get("porte", "11-50")
    num_usuarios = int(dados.get("num_vendedores", 10))

    porte_key = "11-50"
    for key in IMPL_POR_PORTE:
        if key in porte:
            porte_key = key
            break

    licenca_min_user, licenca_max_user = LICENCAD_POR_CLOUD.get(cloud, (150, 300))
    impl_min, impl_max = IMPL_POR_PORTE.get(porte_key, (15000, 40000))

    licenca_min = licenca_min_user * num_usuarios
    licenca_max = licenca_max_user * num_usuarios
    licenca_ano_min = licenca_min * 12
    licenca_ano_max = licenca_max * 12

    total_min = impl_min + licenca_ano_min
    total_max = impl_max + licenca_ano_max

    receita_map = {
        "ate 1m": 1_000_000,
        "1m-5m": 3_000_000,
        "5m-20m": 12_000_000,
        "20m-100m": 60_000_000,
        "acima de 100m": 150_000_000,
    }
    faturamento_str = normalizar_texto(dados.get("faturamento", "1m-5m")).replace(" ", "")
    faturamento = next(
        (v for k, v in receita_map.items() if k.replace(" ", "") in faturamento_str),
        3_000_000,
    )

    ganho_estimado = faturamento * 0.08
    payback = round((impl_min + licenca_ano_min) / ganho_estimado * 12) if ganho_estimado else 18

    return {
        "licenca_min": licenca_min,
        "licenca_max": licenca_max,
        "impl_min": impl_min,
        "impl_max": impl_max,
        "total_min": total_min,
        "total_max": total_max,
        "roi_estimado": round(ganho_estimado),
        "payback_meses": min(payback, 36),
        "num_usuarios": num_usuarios,
    }


def salvar_input(dados: dict, nome_cliente: str) -> Path:
    INPUTS_DIR.mkdir(exist_ok=True)
    slug = re.sub(r"[^a-z0-9]+", "-", nome_cliente.lower()).strip("-")
    hoje = date.today().isoformat()
    caminho = INPUTS_DIR / f"{slug}_{hoje}_formulario.json"

    if caminho.exists():
        resp = input(f"\nArquivo {caminho.name} já existe. Sobrescrever? (s/N): ").strip().lower()
        if resp != "s":
            print("Operação cancelada.")
            sys.exit(0)

    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    return caminho


def ler_de_json(caminho: str) -> dict:
    with open(caminho, encoding="utf-8") as f:
        raw = json.load(f)

    if isinstance(raw, list):
        raw = raw[0]

    mapeamento = {
        "nome_empresa": ["nome_empresa", "company", "empresa", "nome"],
        "segmento": ["segmento", "industry", "segment"],
        "porte": ["porte", "size", "company_size"],
        "num_vendedores": ["num_vendedores", "vendedores", "sales_reps", "atendentes"],
        "faturamento": ["faturamento", "revenue", "annual_revenue"],
        "cargo": ["cargo", "role", "job_title"],
        "crm_atual": ["crm_atual", "crm", "current_crm"],
        "taxa_adocao": ["taxa_adocao", "adoption", "crm_adoption"],
        "num_ferramentas": ["num_ferramentas", "tools_count"],
        "dores": ["dores", "pain_points", "challenges"],
        "objetivo_90_dias": ["objetivo_90_dias", "goal_90_days", "objetivo"],
        "tentativas_anteriores": ["tentativas_anteriores", "previous_attempts"],
        "resultado_6_meses": ["resultado_6_meses", "goal_6_months"],
        "tem_ti": ["tem_ti", "has_it", "it_team"],
        "prazo_decisao": ["prazo_decisao", "decision_timeline"],
        "budget": ["budget", "orcamento", "orçamento"],
        "pacote": ["pacote", "package", "product"],
        "como_conheceu": ["como_conheceu", "source", "referral"],
        "contexto_adicional": ["contexto_adicional", "additional_context", "notes"],
    }

    dados: dict = {}
    for campo, alternativas in mapeamento.items():
        for alt in alternativas:
            if alt in raw:
                dados[campo] = raw[alt]
                break
        if campo not in dados:
            dados[campo] = ""

    return dados


def ler_de_csv(caminho: str) -> dict:
    dados: dict = {}
    with open(caminho, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            dados = dict(row)
            break
    return dados


def entrada_manual() -> dict:
    print("\n--- Entrada manual do formulário ---\n")

    def perguntar(label: str, obrigatorio: bool = True) -> str:
        while True:
            resp = input(f"{label}: ").strip()
            if resp or not obrigatorio:
                return resp
            print("  Campo obrigatório. Por favor, preencha.")

    def menu(label: str, opcoes: list[str]) -> str:
        print(f"\n{label}")
        for i, op in enumerate(opcoes, 1):
            print(f"  {i}. {op}")
        while True:
            resp = input("Escolha o número: ").strip()
            if resp.isdigit() and 1 <= int(resp) <= len(opcoes):
                return opcoes[int(resp) - 1]
            print("  Opção inválida.")

    def multipla_escolha(label: str, opcoes: list[str]) -> list[str]:
        print(f"\n{label}")
        print("  (Digite os números separados por vírgula, ex: 1,3,5)")
        for i, op in enumerate(opcoes, 1):
            print(f"  {i}. {op}")
        while True:
            resp = input("Escolha: ").strip()
            numeros = [x.strip() for x in resp.split(",") if x.strip().isdigit()]
            selecionados = [opcoes[int(n) - 1] for n in numeros if 1 <= int(n) <= len(opcoes)]
            if selecionados:
                return selecionados
            print("  Selecione ao menos uma opção.")

    dados: dict = {}
    dados["nome_empresa"] = perguntar("Nome da empresa")
    dados["segmento"] = menu("Segmento", [
        "Varejo / E-commerce / Franquias",
        "Financeiro / Fintech / Seguradora",
        "Saúde / Healthtech / Plano de saúde",
        "Serviços profissionais / Consultoria",
        "Indústria / Manufatura",
        "Outro",
    ])
    dados["porte"] = menu("Porte da empresa", [
        "1-10 funcionários", "11-50 funcionários", "51-200 funcionários",
        "201-500 funcionários", "Acima de 500 funcionários",
    ])
    dados["num_vendedores"] = perguntar("Número de vendedores / atendentes")
    dados["faturamento"] = menu("Faturamento anual estimado", [
        "Até R$ 1 milhão", "R$ 1M – R$ 5M", "R$ 5M – R$ 20M",
        "R$ 20M – R$ 100M", "Acima de R$ 100M", "Prefiro não informar",
    ])
    dados["cargo"] = menu("Seu cargo", [
        "CEO / Sócio / Fundador", "VP / Diretor de Vendas",
        "Gerente Comercial / de Operações", "Consultor / Analista",
        "TI / Tecnologia", "Outro",
    ])
    dados["crm_atual"] = menu("Usa CRM hoje?", [
        "Sim, CRM dedicado", "Não, uso planilha", "Não registro nada",
    ])
    dados["num_ferramentas"] = menu("Quantas ferramentas o time usa para vendas/atendimento?", [
        "1 (tudo centralizado)", "2 a 3 ferramentas", "4 a 5 ferramentas", "Mais de 5",
    ])
    dados["dores"] = multipla_escolha("Selecione as dores que mais impactam hoje:", [
        "Não sei onde estão minhas oportunidades em andamento",
        "Meu time não registra as atividades de vendas",
        "Perco negócios sem entender o motivo",
        "Meu ciclo de vendas é muito longo",
        "Não consigo fazer previsão de receita confiável",
        "Meu atendimento não tem histórico do cliente",
        "Leads chegam mas não são seguidos adequadamente",
        "Não sei a performance individual de cada vendedor",
        "Dados duplicados e inconsistentes entre sistemas",
        "Integração difícil entre as ferramentas que uso",
        "Relatórios demoram muito para serem gerados",
        "Falta visibilidade do funil em tempo real",
    ])
    dados["objetivo_90_dias"] = perguntar("O que quer resolver nos próximos 90 dias?")
    dados["tentativas_anteriores"] = perguntar("Já tentou resolver antes? O que aconteceu?", obrigatorio=False)
    dados["resultado_6_meses"] = perguntar("Qual seria o resultado ideal em 6 meses?")
    dados["tem_ti"] = menu("Tem equipe de TI ou parceiro técnico?", [
        "Sim, equipe interna", "Sim, terceirizado", "Não",
    ])
    dados["prazo_decisao"] = menu("Prazo para tomar a decisão?", [
        "Imediato — quero começar este mês", "1 a 3 meses", "3 a 6 meses", "Apenas explorando",
    ])
    dados["budget"] = menu("Orçamento estimado para o projeto?", [
        "Até R$ 10.000", "R$ 10k – R$ 30k", "R$ 30k – R$ 80k",
        "R$ 80k – R$ 200k", "Acima de R$ 200k", "Ainda não definido",
    ])
    dados["pacote"] = menu("Qual pacote tem interesse?", [
        "Diagnóstico (R$ 497)",
        "Diagnóstico + Demo (R$ 997)",
        "Diagnóstico + Demo + Proposta (R$ 1.997)",
    ])
    dados["como_conheceu"] = menu("Como conheceu nosso trabalho?", [
        "LinkedIn", "Indicação", "Google", "Evento", "YouTube / conteúdo", "Outro",
    ])
    dados["contexto_adicional"] = perguntar("Algum contexto adicional?", obrigatorio=False)

    return dados


def enriquecer_dados(dados: dict) -> dict:
    dados["segmento"] = normalizar_segmento(dados.get("segmento", ""))
    dados["pacote"] = normalizar_pacote(dados.get("pacote", "diagnostico"))
    cloud_info = detectar_cloud_recomendada(dados)
    dados["cloud_recomendada"] = cloud_info
    investimento = estimar_investimento(dados)
    dados["investimento"] = investimento
    return dados


def exibir_resumo(dados: dict) -> None:
    inv = dados.get("investimento", {})
    cloud = dados.get("cloud_recomendada", {})
    print("\n" + "=" * 50)
    print(f"  RESUMO — {dados.get('nome_empresa', '').upper()}")
    print("=" * 50)
    print(f"  Segmento:         {dados.get('segmento')}")
    print(f"  Pacote:           {dados.get('pacote')}")
    print(f"  Cloud indicada:   {cloud.get('cloud')}")
    print(f"  Dores mapeadas:   {len(dados.get('dores', []))}")
    print(f"  Invest. estimado: R$ {inv.get('total_min', 0):,.0f} – R$ {inv.get('total_max', 0):,.0f} / ano")
    print(f"  Payback:          {inv.get('payback_meses')} meses")
    print("=" * 50)


def main() -> None:
    print("\n╔══════════════════════════════════════════╗")
    print("║   SF Presales Toolkit — Ingestão         ║")
    print("╚══════════════════════════════════════════╝\n")

    print("Como deseja fornecer os dados do formulário?")
    print("  1. Ler de arquivo JSON")
    print("  2. Ler de arquivo CSV")
    print("  3. Ler JSON colado no terminal (webhook Typeform)")
    print("  4. Entrada manual campo a campo")

    opcao = input("\nOpção (1-4): ").strip()

    if opcao == "1":
        caminho = input("Caminho do arquivo JSON: ").strip()
        dados = ler_de_json(caminho)
    elif opcao == "2":
        caminho = input("Caminho do arquivo CSV: ").strip()
        dados = ler_de_csv(caminho)
    elif opcao == "3":
        print("Cole o JSON abaixo e pressione Enter duas vezes:")
        linhas = []
        while True:
            linha = input()
            if linha == "" and linhas and linhas[-1] == "":
                break
            linhas.append(linha)
        dados = json.loads("\n".join(linhas))
        if isinstance(dados, list):
            dados = dados[0]
    elif opcao == "4":
        dados = entrada_manual()
    else:
        print("Opção inválida.")
        sys.exit(1)

    dados = enriquecer_dados(dados)
    exibir_resumo(dados)

    nome = dados.get("nome_empresa", "cliente")
    caminho_salvo = salvar_input(dados, nome)
    print(f"\n✓ Formulário salvo em: {caminho_salvo}")

    pacote = dados.get("pacote", "diagnostico")
    slug = re.sub(r"[^a-z0-9]+", "-", nome.lower()).strip("-")
    print(f"\nPróximo passo — gerar diagnóstico:")
    print(f"  python pipeline/diagnostico.py {slug}")
    if "demo" in pacote:
        print(f"\nApós o diagnóstico — setup da demo:")
        print(f"  python pipeline/demo_setup.py {slug}")
    if "proposta" in pacote:
        print(f"\nApós a demo — gerar proposta:")
        print(f"  python pipeline/proposta.py {slug}")


if __name__ == "__main__":
    main()
