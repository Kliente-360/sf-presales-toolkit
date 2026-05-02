"""
pipeline/proposta.py

Gera a proposta técnica completa de implementação.
Executado apenas para Pacote 3 (diagnostico_demo_proposta).
"""

import json
import sys
import re
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).parent.parent
INPUTS_DIR = ROOT / "inputs"
OUTPUTS_DIR = ROOT / "outputs"
TEMPLATE_PATH = ROOT / "outputs" / "templates" / "proposta_template.md"

ESCOPO_POR_CLOUD = {
    "Sales Cloud": {
        "incluidos": [
            "Configuração de perfis, papéis e regras de compartilhamento",
            "Customização de Contas, Contatos e Oportunidades",
            "Configuração de estágios do pipeline e probabilidades",
            "Até 5 Flows de automação (follow-up, alertas, atribuição)",
            "Integração com e-mail e calendário (Gmail ou Outlook)",
            "10 relatórios e 3 dashboards (vendedor, gestor, executivo)",
            "Migração de dados do sistema atual (até 50.000 registros)",
            "Treinamento do time: 8h total (4h usuários + 4h administrador)",
        ],
        "excluidos": [
            "Desenvolvimento de código Apex ou Lightning Web Components",
            "Integrações além das listadas no escopo",
            "Migração de mais de 50.000 registros (cotação adicional)",
            "Licenças Salesforce (faturadas diretamente pela Salesforce)",
            "Suporte técnico após o período de go-live (cotado separadamente)",
        ],
    },
    "Service Cloud": {
        "incluidos": [
            "Configuração de filas, roteamento e SLAs de atendimento",
            "Customização de Casos e fluxo de escalada",
            "Base de conhecimento (Knowledge) com até 50 artigos iniciais",
            "Configuração de canais: e-mail e web-to-case",
            "Até 4 Flows de automação (escalada, fechamento, pesquisa)",
            "8 relatórios e 2 dashboards de atendimento",
            "Migração de histórico de casos (até 20.000 registros)",
            "Treinamento: 8h total (4h agentes + 4h supervisores)",
        ],
        "excluidos": [
            "Implementação de chat ao vivo ou redes sociais",
            "Integração com telefonia (CTI) — cotação separada",
            "Field Service Lightning — produto adicional",
            "Licenças e suporte pós go-live",
        ],
    },
    "Financial Services Cloud": {
        "incluidos": [
            "Configuração de Grupos Familiares e Portfólios financeiros",
            "Customização de Contas, Contatos e Oportunidades financeiras",
            "Configuração de Referral Management",
            "Trilha de auditoria e controles de segurança (LGPD/Bacen)",
            "Até 4 Flows de automação (revisão de portfólio, alertas)",
            "10 relatórios e 3 dashboards por perfil (assessor, gerente)",
            "Migração de dados de clientes e produtos (até 30.000 registros)",
            "Treinamento: 10h total (assessores, gerentes, compliance)",
        ],
        "excluidos": [
            "Integração com core bancário — cotação específica",
            "Desenvolvimento de aplicativos customizados",
            "Einstein Analytics avançado — produto adicional",
            "Licenças e suporte pós go-live",
        ],
    },
    "Health Cloud": {
        "incluidos": [
            "Configuração de perfis de Paciente e Plano de Cuidados",
            "Fluxo de Coordenação de Cuidados e encaminhamentos",
            "Configuração de Times de Cuidado e papéis clínicos",
            "Controles de consentimento e privacidade (LGPD)",
            "Até 4 Flows de automação (triagem, follow-up, alertas)",
            "8 relatórios e 2 dashboards clínicos e operacionais",
            "Migração de dados de pacientes e histórico (até 20.000 registros)",
            "Treinamento: 10h total (clínicos, gestores, administrativo)",
        ],
        "excluidos": [
            "Integração com prontuário eletrônico (PEP) — cotação específica",
            "Telemedicina e agendamento online — produtos adicionais",
            "Certificações regulatórias específicas do cliente",
            "Licenças e suporte pós go-live",
        ],
    },
}

CRONOGRAMA_BASE = {
    "pequeno": {"f1": 3, "f2": 3, "f3": 2},
    "medio": {"f1": 4, "f2": 5, "f3": 3},
    "grande": {"f1": 6, "f2": 7, "f3": 4},
}

RISCOS_BASE = [
    ("Baixa adoção do time de vendas", "Média", "Alto",
     "Treinamento estruturado + champion interno + quick wins visíveis na semana 1"),
    ("Qualidade dos dados legados abaixo do esperado", "Média", "Médio",
     "Auditoria de dados na Fase 1 com plano de limpeza e normalização"),
    ("Escopo expandindo durante o projeto", "Baixa", "Médio",
     "Processo formal de change request — qualquer adição é cotada separadamente"),
    ("Atrasos nas aprovações internas do cliente", "Média", "Médio",
     "SLA de resposta de 3 dias úteis acordado no kickoff"),
]


def formatar_real(valor: int) -> str:
    return f"{valor:,.0f}".replace(",", ".")


def _porte_key(porte: str) -> str:
    porte = porte.lower()
    if any(x in porte for x in ["1-10", "até 10", "micro"]):
        return "pequeno"
    if any(x in porte for x in ["11-50", "51-200"]):
        return "medio"
    return "grande"


def calcular_cronograma(dados: dict) -> dict:
    porte = dados.get("porte", "11-50 funcionários")
    key = _porte_key(porte)
    semanas = CRONOGRAMA_BASE.get(key, CRONOGRAMA_BASE["medio"])
    total = sum(semanas.values())
    inicio = date.today() + timedelta(days=7)
    golive = inicio + timedelta(weeks=total)
    return {
        "f1": semanas["f1"],
        "f2": semanas["f2"],
        "f3": semanas["f3"],
        "total": total,
        "data_inicio": inicio.strftime("%d/%m/%Y"),
        "data_golive": golive.strftime("%d/%m/%Y"),
    }


def carregar_diagnostico(slug_cliente: str) -> str:
    arquivos = sorted(OUTPUTS_DIR.glob(f"{slug_cliente}*_diagnostico.md"), reverse=True)
    if not arquivos:
        return ""
    with open(arquivos[0], encoding="utf-8") as f:
        return f.read()


def carregar_input(slug_cliente: str) -> dict:
    arquivos = sorted(INPUTS_DIR.glob(f"{slug_cliente}*_formulario.json"), reverse=True)
    if not arquivos:
        print(f"[ERRO] Formulário não encontrado para '{slug_cliente}' em {INPUTS_DIR}/")
        sys.exit(1)
    with open(arquivos[0], encoding="utf-8") as f:
        return json.load(f)


def gerar_proposta(dados: dict, diagnostico: str) -> str:
    hoje = date.today()
    validade = hoje + timedelta(days=30)
    inv = dados.get("investimento", {})
    cloud_info = dados.get("cloud_recomendada", {})
    cloud = cloud_info.get("cloud", "Sales Cloud")
    nome = dados.get("nome_empresa", "Cliente")
    segmento = dados.get("segmento", "outro")
    porte = dados.get("porte", "11-50 funcionários")
    num_usuarios = int(dados.get("num_vendedores", 10))
    dores = dados.get("dores", [])

    crono = calcular_cronograma(dados)
    escopo = ESCOPO_POR_CLOUD.get(cloud, ESCOPO_POR_CLOUD["Sales Cloud"])

    incluidos_md = "\n".join(f"- [ ] {item}" for item in escopo["incluidos"])
    excluidos_md = "\n".join(f"- {item}" for item in escopo["excluidos"])

    riscos_md = "\n".join(
        f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} |"
        for r in RISCOS_BASE
    )

    impl_min = inv.get("impl_min", 15000)
    impl_max = inv.get("impl_max", 40000)
    impl_medio = (impl_min + impl_max) // 2

    licenca_min = inv.get("licenca_min", 150 * num_usuarios)
    licenca_max = inv.get("licenca_max", 300 * num_usuarios)
    licenca_medio = (licenca_min + licenca_max) // 2

    suporte = impl_medio * 2 // 10

    total = impl_medio + suporte
    v40 = int(total * 0.4)
    v30_f1 = int(total * 0.3)
    v30_f3 = total - v40 - v30_f1

    objetivo = (
        f"Este projeto tem como objetivo implementar o {cloud} em {nome}, "
        f"resolvendo os desafios críticos identificados no diagnóstico realizado em {hoje.strftime('%d/%m/%Y')}.\n\n"
        f"Os principais problemas a resolver são:\n"
        + "\n".join(f"- {d}" for d in dores[:4])
        + f"\n\nAo final da implementação, {nome} terá uma plataforma centralizada que conecta "
        f"dados, processos e equipes — eliminando silos de informação e dando previsibilidade "
        f"ao crescimento do negócio."
    )

    return f"""# Proposta Técnica de Implementação
## {cloud} para {nome}

**Versão:** 1.0
**Data:** {hoje.strftime("%d/%m/%Y")}
**Validade:** 30 dias ({validade.strftime("%d/%m/%Y")})
**Preparada por:** Kliente-360
**Confidencial**

---

## Objetivo do Projeto

{objetivo}

---

## Escopo da Implementação

### O que está incluído

{incluidos_md}

### O que não está incluído

{excluidos_md}

---

## Arquitetura Técnica

**Objetos principais configurados:**

```
{nome}
│
├── Conta (Account) ─── Empresas clientes e prospects
│   ├── Contato (Contact) ─── Pessoas de relacionamento
│   └── Oportunidade (Opportunity) ─── Pipeline comercial
│       ├── Produtos / Serviços ─── Catálogo de oferta
│       └── Atividades (Tasks / Events) ─── Histórico de interações
│
└── Relatórios e Dashboards ─── Visibilidade executiva e operacional
```

**Integrações previstas:**

| Sistema | Direção | Frequência | Método |
|---|---|---|---|
| E-mail (Gmail / Outlook) | Bidirecional | Tempo real | Einstein Activity Capture |
| Calendário | Sincronização | Tempo real | Einstein Activity Capture |

---

## Cronograma

| Fase | Atividades principais | Duração | Responsável |
|---|---|---|---|
| **Fase 1 — Fundação** | Configuração, perfis, migração de dados | {crono["f1"]} semanas | Kliente-360 |
| **Fase 2 — Automação** | Flows, integrações, relatórios | {crono["f2"]} semanas | Kliente-360 |
| **Fase 3 — Go-live** | Treinamento, UAT, go-live | {crono["f3"]} semanas | Compartilhado |

**Prazo total estimado:** {crono["total"]} semanas
**Data de início prevista:** {crono["data_inicio"]}
**Go-live previsto:** {crono["data_golive"]}

---

## Premissas e Responsabilidades do Cliente

Para entrega dentro do prazo e orçamento, o cliente se compromete a:

- [ ] Designar um **champion interno** com disponibilidade de 4h/semana
- [ ] Fornecer acesso ao sistema de origem em até 5 dias úteis após assinatura
- [ ] Exportar dados para migração em formato CSV ou XLS
- [ ] Disponibilizar usuários para testes de aceitação (UAT) na Fase 3
- [ ] Aprovar ou solicitar ajustes em cada entregável em até 3 dias úteis
- [ ] Garantir participação nas sessões de treinamento

---

## Investimento

| Item | Valor |
|---|---|
| Implementação e configuração | R$ {formatar_real(impl_medio)} |
| Suporte pós go-live (2 meses) | R$ {formatar_real(suporte)} |
| Treinamento ({8}h) | Incluso |
| **Total de implementação** | **R$ {formatar_real(total)}** |

**Licenças Salesforce** (faturadas pela Salesforce, não inclusas acima):

| Licença | Usuários | Estimativa |
|---|---|---|
| {cloud} | {num_usuarios} | R$ {formatar_real(licenca_min)} – R$ {formatar_real(licenca_max)} / mês |

**Condições de pagamento:**
- 40% na assinatura do contrato — R$ {formatar_real(v40)}
- 30% no go-live da Fase 1 — R$ {formatar_real(v30_f1)}
- 30% no go-live final — R$ {formatar_real(v30_f3)}

---

## Riscos e Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
{riscos_md}

---

## Por que a Kliente-360

- **Especialização em {segmento}:** conhecimento do negócio, não apenas da ferramenta
- **Implementações em PT-BR:** time 100% brasileiro, sem intermediários
- **Metodologia testada:** go-lives dentro do prazo com adoção acima de 80%
- **Suporte pós go-live:** não desaparecemos após o go-live

---

## Próximos Passos para Aprovação

1. **Revisar** a proposta com o time interno (prazo sugerido: 5 dias úteis)
2. **Call de alinhamento** — 30 minutos para esclarecer dúvidas
3. **Ajustes no escopo** se necessário (1 rodada incluída sem custo)
4. **Assinatura** e pagamento da primeira parcela (R$ {formatar_real(v40)})
5. **Kickoff** em até 5 dias úteis após assinatura — **início: {crono["data_inicio"]}**

---

*Proposta válida por 30 dias a partir de {hoje.strftime("%d/%m/%Y")}.*
*Kliente-360 — Consultoria Salesforce Certificada.*
"""


def salvar_output(conteudo: str, nome_cliente: str) -> Path:
    OUTPUTS_DIR.mkdir(exist_ok=True)
    slug = re.sub(r"[^a-z0-9]+", "-", nome_cliente.lower()).strip("-")
    hoje = date.today().isoformat()
    caminho = OUTPUTS_DIR / f"{slug}_{hoje}_proposta.md"

    if caminho.exists():
        resp = input(f"\nArquivo {caminho.name} já existe. Sobrescrever? (s/N): ").strip().lower()
        if resp != "s":
            print("Operação cancelada.")
            sys.exit(0)

    with open(caminho, "w", encoding="utf-8") as f:
        f.write(conteudo)
    return caminho


def main() -> None:
    print("\n╔══════════════════════════════════════════╗")
    print("║   SF Presales Toolkit — Proposta         ║")
    print("╚══════════════════════════════════════════╝\n")

    if len(sys.argv) > 1:
        slug = sys.argv[1]
    else:
        slug = input("Nome do cliente (slug, ex: banco-meridian): ").strip()

    print(f"[1/4] Carregando formulário para '{slug}'...")
    dados = carregar_input(slug)
    nome = dados.get("nome_empresa", slug)
    print(f"      ✓ {nome}")

    pacote = dados.get("pacote", "")
    if "proposta" not in pacote:
        print(f"[AVISO] Pacote contratado é '{pacote}' — proposta não está incluída.")
        continuar = input("Continuar mesmo assim? (s/N): ").strip().lower()
        if continuar != "s":
            sys.exit(0)

    print("[2/4] Carregando diagnóstico gerado...")
    diagnostico = carregar_diagnostico(slug)
    if diagnostico:
        print("      ✓ Diagnóstico encontrado")
    else:
        print("      [AVISO] Diagnóstico não encontrado — gerando proposta sem ele")

    print("[3/4] Calculando cronograma e escopo...")
    crono = calcular_cronograma(dados)
    print(f"      ✓ {crono['total']} semanas | Go-live: {crono['data_golive']}")

    print("[4/4] Gerando proposta técnica...")
    conteudo = gerar_proposta(dados, diagnostico)
    caminho = salvar_output(conteudo, nome)
    print(f"      ✓ Proposta salva em {caminho}")

    inv = dados.get("investimento", {})
    impl = (inv.get("impl_min", 0) + inv.get("impl_max", 0)) // 2
    print(f"\n{'─' * 50}")
    print(f"  Cloud:       {dados.get('cloud_recomendada', {}).get('cloud', '—')}")
    print(f"  Valor impl.: R$ {formatar_real(impl)}")
    print(f"  Prazo:       {crono['total']} semanas")
    print(f"  Go-live:     {crono['data_golive']}")
    print(f"  Arquivo:     outputs/{caminho.name}")
    print(f"{'─' * 50}\n")


if __name__ == "__main__":
    main()
