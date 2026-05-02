"""
pipeline/demo_setup.py

Orquestra o setup automático da demo na Developer Edition.
Executado para Pacotes 2 e 3 (diagnostico_demo / diagnostico_demo_proposta).
"""

import json
import sys
import re
import subprocess
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent.parent
INPUTS_DIR = ROOT / "inputs"
OUTPUTS_DIR = ROOT / "outputs"
SCRIPTS_DIR = ROOT / "scripts"

CENARIOS_POR_SEGMENTO = {
    "varejo": {
        "cloud": "Sales Cloud",
        "casos_uso": ["pipeline de vendas B2B", "gestão de franqueados", "atendimento pós-venda"],
        "dados_dir": "data/varejo/",
        "foco_demo": "Visibilidade de pipeline, gestão de contas e automação de follow-up",
    },
    "financeiro": {
        "cloud": "Financial Services Cloud",
        "casos_uso": ["visão 360° do cliente", "gestão de portfólio", "pipeline de produtos"],
        "dados_dir": "data/financeiro/",
        "foco_demo": "Relacionamento com cliente financeiro, portfólio e cross-sell",
    },
    "saude": {
        "cloud": "Health Cloud",
        "casos_uso": ["coordenação de cuidados", "gestão de beneficiários", "credenciamento"],
        "dados_dir": "data/saude/",
        "foco_demo": "Jornada do paciente, coordenação e visão 360° do beneficiário",
    },
    "servicos": {
        "cloud": "Sales Cloud",
        "casos_uso": ["pipeline consultivo", "gestão de projetos", "renovações de contrato"],
        "dados_dir": "data/varejo/",
        "foco_demo": "Pipeline complexo, múltiplos stakeholders e gestão de renovações",
    },
    "industria": {
        "cloud": "Sales Cloud",
        "casos_uso": ["gestão de distribuidores", "field service", "pipeline de grandes contas"],
        "dados_dir": "data/varejo/",
        "foco_demo": "Canal de distribuição, performance de revendas e grandes contas",
    },
    "outro": {
        "cloud": "Sales Cloud",
        "casos_uso": ["pipeline comercial", "automação de follow-up", "dashboards executivos"],
        "dados_dir": "data/varejo/",
        "foco_demo": "Centralização do pipeline e visibilidade em tempo real",
    },
}

PERSONAS_POR_CARGO = {
    "ceo": "Decisor de negócio — foco em ROI, payback e casos de referência",
    "vp": "Liderança executiva — foco em forecast, dashboards e metas",
    "diretor": "Gestão comercial — foco em pipeline, performance do time e relatórios",
    "gerente": "Operacional — foco em processos, automação e facilidade de uso",
    "ti": "Técnico — foco em integrações, segurança e arquitetura",
    "consultor": "Influenciador técnico — foco em capacidades e comparativos",
    "analista": "Usuário final — foco em UX, mobile e produtividade",
}

OBJECOES_POR_SEGMENTO = {
    "varejo": [
        ("O volume de SKUs/transações é muito alto para um CRM",
         "O Salesforce foi construído para escala — temos clientes com bilhões de registros. "
         "Com o Data Cloud, unificamos dados de PDV, e-commerce e fidelidade em tempo real.",
         "Qual é o volume médio de pedidos por dia hoje?"),
        ("Já temos um ERP que faz isso",
         "ERP e CRM resolvem problemas diferentes. O ERP cuida do back-office; o CRM cuida "
         "do relacionamento. Seu ERP te diz qual cliente está prestes a churnar antes que ele vá embora?",
         "O que acontece com um cliente que comprou uma vez e sumiu?"),
    ],
    "financeiro": [
        ("LGPD e regulamentação do Banco Central são um risco",
         "O Financial Services Cloud foi construído com esses requisitos em mente. "
         "Shield oferece criptografia em nível de campo e trilha de auditoria auditável para o Bacen.",
         "Quais são os dados específicos que mais preocupam o compliance de vocês?"),
        ("Dados sensíveis não podem sair do nosso ambiente",
         "O Salesforce tem opções de residência de dados no Brasil e configurações de soberania. "
         "Mas antes dos detalhes técnicos: que tipo de dados específicos preocupam mais?",
         "Posso conectar você com nosso time de segurança para uma sessão técnica?"),
    ],
    "saude": [
        ("LGPD com dados de pacientes é intransponível",
         "O Health Cloud tem suporte nativo a LGPD com controles de consentimento, "
         "anonimização e acesso granular — temos operadoras de saúde operando com esses controles.",
         "Quais dados específicos preocupam mais do ponto de vista de compliance?"),
        ("Os médicos nunca vão usar um novo sistema",
         "Adoção de médicos é um desafio real — e por isso o Health Cloud tem interface "
         "construída para o fluxo clínico. A chave é envolver 2–3 médicos no design antes de implementar.",
         "Você tem algum early adopter na equipe que poderia ser o champion?"),
    ],
    "servicos": [
        ("Nosso processo de vendas é muito complexo para um CRM padrão",
         "O Salesforce é altamente configurável — não é um CRM de prateleira. "
         "Podemos modelar exatamente o seu processo consultivo com múltiplos decisores.",
         "Quais são as etapas do processo que mais variam de negociação para negociação?"),
    ],
    "industria": [
        ("Nossos distribuidores não vão usar uma ferramenta nova",
         "O Experience Cloud cria um portal de parceiro que os distribuidores acessam pelo browser, "
         "sem precisar instalar nada. Funciona como um extranet moderno.",
         "Como distribuidores se comunicam com vocês hoje?"),
    ],
    "outro": [
        ("É muito caro para nosso porte",
         "O investimento é real — e por isso mapeamos o retorno esperado antes de qualquer contrato. "
         "Clientes do porte de vocês tipicamente recuperam o investimento em 12–18 meses.",
         "Se o custo ficasse dentro do budget, o que mais precisaria estar claro para avançar?"),
        ("Já tentamos um CRM antes e não funcionou",
         "Isso é mais comum do que parece. Na maioria dos casos, o problema não foi o sistema, "
         "mas a implementação: sem treinar, sem adaptar processos, sem champion interno.",
         "O que especificamente não funcionou da última vez?"),
    ],
}


def verificar_org() -> bool:
    script = SCRIPTS_DIR / "check-org.sh"
    if not script.exists():
        print(f"[ERRO] Script não encontrado: {script}")
        return False
    result = subprocess.run(["bash", str(script)], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        return False
    return True


def deploy_metadados(segmento: str) -> bool:
    segmentos_validos = {"varejo", "financeiro", "saude"}
    seg_deploy = segmento if segmento in segmentos_validos else "varejo"

    script = SCRIPTS_DIR / "deploy-demo.sh"
    if not script.exists():
        print(f"[ERRO] Script não encontrado: {script}")
        return False

    print(f"      Executando deploy para segmento '{seg_deploy}'...")
    result = subprocess.run(["bash", str(script), seg_deploy], capture_output=True, text=True, cwd=ROOT)
    if result.stdout:
        for linha in result.stdout.strip().split("\n"):
            print(f"      {linha}")
    if result.returncode != 0:
        print(f"[ERRO] Deploy falhou:\n{result.stderr}")
        return False
    return True


def carregar_dados(segmento: str) -> bool:
    segmentos_validos = {"varejo", "financeiro", "saude"}
    seg_data = segmento if segmento in segmentos_validos else "varejo"

    script = SCRIPTS_DIR / "load-data.sh"
    if not script.exists():
        print(f"[ERRO] Script não encontrado: {script}")
        return False

    print(f"      Carregando dados do segmento '{seg_data}'...")
    result = subprocess.run(["bash", str(script), seg_data], capture_output=True, text=True, cwd=ROOT)
    if result.stdout:
        for linha in result.stdout.strip().split("\n"):
            print(f"      {linha}")
    if result.returncode != 0:
        print(f"[AVISO] Load de dados retornou erro:\n{result.stderr}")
        return False
    return True


def gerar_roteiro(dados: dict, cenario: dict) -> str:
    nome = dados.get("nome_empresa", "Cliente")
    segmento = dados.get("segmento", "outro")
    cargo = dados.get("cargo", "").lower()
    dores = dados.get("dores", [])
    cloud = cenario.get("cloud", "Sales Cloud")
    casos = cenario.get("casos_uso", [])
    foco = cenario.get("foco_demo", "")
    hoje = date.today().strftime("%d/%m/%Y")

    persona_descricao = "Executivo de negócio — foco em ROI e resultados"
    for chave, descricao in PERSONAS_POR_CARGO.items():
        if chave in cargo:
            persona_descricao = descricao
            break

    dores_top3 = dores[:3]
    blocos_md = ""
    for i, (caso, dor_ref) in enumerate(zip(casos, dores_top3 + ["visibilidade geral"]), 1):
        blocos_md += f"""
### Bloco {i}: {caso.capitalize()}
**Duração:** 8–10 min
**Dor que resolve:** {dor_ref}
**Persona principal:** {persona_descricao}

**Narrativa:**
> "Vocês mencionaram que hoje {dor_ref.lower()}. Deixa eu mostrar como isso muda com o Salesforce."

**Passos no sistema:**
1. Navegar para o App Launcher → {cloud}
2. Abrir a tela principal de {caso}
3. Demonstrar a funcionalidade central
4. Destacar o diferencial (automação / IA / dashboard)

**Frase de impacto:** "Isso que levava horas agora acontece automaticamente — sem intervenção manual."

**Ponto de pausa:** Isso representa a realidade de vocês hoje?

---
"""

    return f"""# Roteiro de Demo — {nome}
**Data da demo:** A agendar
**Duração total estimada:** 45–50 minutos
**Org de demo:** demo-org
**Segmento:** {segmento}
**Preparado em:** {hoje}

---

## 1. Objetivo da Demo

Demonstrar que o {cloud} resolve os desafios específicos de {nome}, com foco em:
{chr(10).join(f"- {d}" for d in dores_top3)}

**Critério de sucesso:** o grupo sair com clareza de como o Salesforce resolve os problemas que trouxeram para a reunião.

---

## 2. Personas Esperadas e o que Cada Uma Quer Ver

| Persona | Preocupação principal | O que vai impressionar |
|---|---|---|
| {dados.get("cargo", "Decisor")} | {persona_descricao.split("—")[0].strip()} | Dashboard executivo, ROI, casos de referência |
| Usuário final (vendedor/atendente) | Facilidade de uso, mobile | UX simples, automação que poupa tempo |

---

## 3. Mensagem Central

> "Com o Salesforce, {nome} vai parar de tomar decisões no escuro e começar a crescer com previsibilidade — sem aumentar o time."

Repita essa mensagem no início, no meio e no fechamento.

---

## 4. Roteiro de Telas e Flows

### Bloco 0: Abertura (5 min)
**Sem abrir o sistema ainda.**

Narrativa:
> "Antes de entrar no sistema, deixa eu confirmar: vocês me disseram que hoje {dores_top3[0].lower() if dores_top3 else 'o processo comercial tem gargalos importantes'}. É isso? [pausa] Perfeito. O que vou mostrar nas próximas meia hora resolve exatamente isso."

---
{blocos_md}
### Bloco Final: Visão de Futuro e ROI (5–8 min)
**Dashboard executivo / relatório de forecast.**

Narrativa:
> "O que vocês viram hoje é a fase 1. Em 90 dias, o time já estaria operando assim. Em 6 meses, {nome} teria {foco}."

**Pergunta de fechamento:** "O que vocês viram hoje responde às perguntas que tinham antes de entrar aqui?"

---

## 5. Checklist de Preparação Técnica

- [ ] `./scripts/check-org.sh` — confirmar autenticação
- [ ] `./scripts/deploy-demo.sh {segmento}` — metadados deployados
- [ ] `./scripts/load-data.sh {segmento}` — dados carregados
- [ ] Navegar pelos blocos ao menos uma vez antes da reunião
- [ ] App Launcher com os apps na ordem certa
- [ ] Org aberta no browser antes do cliente entrar
- [ ] Screenshots de backup dos momentos-chave

---

## 6. Gestão de Tempo

| Bloco | Duração |
|---|---|
| Abertura | 5 min |
{chr(10).join(f"| {caso.capitalize()} | 8–10 min |" for caso in casos)}
| Visão de futuro e ROI | 8 min |
| Q&A e próximos passos | 10 min |
| **Total** | **~50 min** |

---

## 7. Próximos Passos a Propor ao Final

1. Enviar diagnóstico completo por email (se ainda não enviado)
2. Alinhar proposta técnica com escopo e cronograma
3. Definir data de kickoff
"""


def gerar_objecoes(dados: dict) -> str:
    nome = dados.get("nome_empresa", "Cliente")
    segmento = dados.get("segmento", "outro")
    crm_atual = dados.get("crm_atual", "")
    hoje = date.today().strftime("%d/%m/%Y")

    objecoes_seg = OBJECOES_POR_SEGMENTO.get(segmento, OBJECOES_POR_SEGMENTO["outro"])
    objecoes_universais = OBJECOES_POR_SEGMENTO["outro"]

    todas = objecoes_seg + [o for o in objecoes_universais if o not in objecoes_seg]

    objecoes_md = ""
    for i, (objecao, resposta, pergunta_retorno) in enumerate(todas, 1):
        objecoes_md += f"""
### O{i:02d}. "{objecao}"

**Resposta:**
> "{resposta}"

**Pergunta de retorno:** {pergunta_retorno}

---
"""

    migracao_md = ""
    if crm_atual and "sim" in crm_atual.lower():
        migracao_md = f"""
## Objeção específica: migração do CRM atual

### "Já investimos muito no sistema atual, trocar vai custar caro"

**Resposta:**
> "Entendo — e por isso faço essa pergunta: o que vocês têm hoje está gerando o ROI esperado?
> Se o sistema atual estivesse funcionando bem, vocês não estariam aqui. O custo real não é
> a migração — é continuar com um sistema que o time não usa."

**Pergunta de retorno:** "Qual seria o custo de não mudar nos próximos 12 meses?"

---
"""

    return f"""# Preparação de Objeções — {nome}
**Data:** {hoje}
**Segmento:** {segmento}

---

## Como usar

Para cada objeção: (1) ouça completamente, (2) valide — "faz sentido essa preocupação",
(3) responda com a estrutura abaixo, (4) verifique — "isso responde sua dúvida?"

---

## Objeções prováveis para este perfil
{objecoes_md}
{migracao_md}
## Sinais de compra a observar

- Perguntas sobre prazo de implementação
- Perguntas sobre integrações com sistemas específicos
- Pedido para ver mais uma funcionalidade específica
- Menção de budget ou ciclo orçamentário
- Solicitação de referências do setor

**Quando identificar esses sinais:** proponha próximo passo concreto imediatamente.
"""


def carregar_input(slug_cliente: str) -> dict:
    arquivos = sorted(INPUTS_DIR.glob(f"{slug_cliente}*_formulario.json"), reverse=True)
    if not arquivos:
        print(f"[ERRO] Formulário não encontrado para '{slug_cliente}' em {INPUTS_DIR}/")
        sys.exit(1)
    with open(arquivos[0], encoding="utf-8") as f:
        return json.load(f)


def salvar_output(conteudo: str, nome_cliente: str, tipo: str) -> Path:
    OUTPUTS_DIR.mkdir(exist_ok=True)
    slug = re.sub(r"[^a-z0-9]+", "-", nome_cliente.lower()).strip("-")
    hoje = date.today().isoformat()
    caminho = OUTPUTS_DIR / f"{slug}_{hoje}_{tipo}.md"

    if caminho.exists():
        resp = input(f"\nArquivo {caminho.name} já existe. Sobrescrever? (s/N): ").strip().lower()
        if resp != "s":
            return caminho

    with open(caminho, "w", encoding="utf-8") as f:
        f.write(conteudo)
    return caminho


def imprimir_checklist(itens: list[tuple[str, bool]]) -> None:
    for label, ok in itens:
        marca = "✓" if ok else "✗"
        print(f"  [{marca}] {label}")


def main() -> None:
    print("\n╔══════════════════════════════════════════╗")
    print("║   SF Presales Toolkit — Demo Setup       ║")
    print("╚══════════════════════════════════════════╝\n")

    if len(sys.argv) > 1:
        slug = sys.argv[1]
    else:
        slug = input("Nome do cliente (slug, ex: banco-meridian): ").strip()

    print(f"Carregando dados para '{slug}'...")
    dados = carregar_input(slug)
    nome = dados.get("nome_empresa", slug)
    segmento = dados.get("segmento", "outro")
    pacote = dados.get("pacote", "")
    cenario = CENARIOS_POR_SEGMENTO.get(segmento, CENARIOS_POR_SEGMENTO["outro"])

    if "demo" not in pacote:
        print(f"[AVISO] Pacote '{pacote}' não inclui demo.")
        continuar = input("Continuar mesmo assim? (s/N): ").strip().lower()
        if continuar != "s":
            sys.exit(0)

    print(f"\nCliente: {nome} | Segmento: {segmento} | Cloud: {cenario['cloud']}\n")

    checklist: list[tuple[str, bool]] = []

    print("[1/5] Verificando org demo-org...")
    org_ok = verificar_org()
    checklist.append(("Org demo-org autenticada", org_ok))
    if not org_ok:
        print("\n[ERRO] Org não autenticada. Execute:")
        print("  sf org login web --alias demo-org --set-default")
        sys.exit(1)

    print("\n[2/5] Fazendo deploy dos metadados...")
    deploy_ok = deploy_metadados(segmento)
    checklist.append(("Metadados deployados", deploy_ok))

    print("\n[3/5] Carregando dados de demo...")
    data_ok = carregar_dados(segmento)
    checklist.append(("Dados de demo carregados", data_ok))

    print("\n[4/5] Gerando roteiro de demo...")
    roteiro = gerar_roteiro(dados, cenario)
    caminho_roteiro = salvar_output(roteiro, nome, "roteiro")
    checklist.append(("Roteiro de demo gerado", True))
    print(f"      ✓ {caminho_roteiro}")

    print("\n[5/5] Preparando antecipação de objeções...")
    objecoes = gerar_objecoes(dados)
    caminho_objecoes = salvar_output(objecoes, nome, "objecoes")
    checklist.append(("Objeções preparadas", True))
    print(f"      ✓ {caminho_objecoes}")

    print(f"\n{'═' * 50}")
    print("  CHECKLIST FINAL")
    print(f"{'═' * 50}")
    imprimir_checklist(checklist)
    print(f"{'═' * 50}")
    print(f"\n  Abrir a org:")
    print(f"  sf org open --target-org demo-org")
    print(f"\n  Roteiro:   outputs/{caminho_roteiro.name}")
    print(f"  Objeções:  outputs/{caminho_objecoes.name}")
    print()


if __name__ == "__main__":
    main()
