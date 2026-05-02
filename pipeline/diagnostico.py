"""
pipeline/diagnostico.py

Lê o formulário processado por ingestao.py e gera o documento
de diagnóstico completo em outputs/{cliente}_{data}_diagnostico.md.
"""

import json
import sys
import re
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).parent.parent
INPUTS_DIR = ROOT / "inputs"
OUTPUTS_DIR = ROOT / "outputs"

NARRATIVAS_DORES = {
    "nao sei onde estao minhas oportunidades": {
        "titulo": "Falta de visibilidade do pipeline comercial",
        "impacto": "Decisões de contratação, metas e forecast são tomadas sem dados confiáveis, "
                   "aumentando o risco de erros operacionais e perda de oportunidades.",
        "solucao": "O Sales Cloud centraliza todas as oportunidades em um pipeline visual "
                   "em tempo real, com estágios, valores e probabilidades de fechamento.",
    },
    "time nao registra atividades": {
        "titulo": "Baixo registro de atividades de vendas",
        "impacto": "Histórico de negociações se perde quando vendedores saíem ou mudam de conta, "
                   "e gestores não conseguem identificar gargalos no processo.",
        "solucao": "O Salesforce captura atividades automaticamente via integração com email e "
                   "calendário, reduzindo a dependência de registro manual.",
    },
    "perco negocios sem entender o motivo": {
        "titulo": "Ausência de análise de perdas",
        "impacto": "Sem dados estruturados de motivo de perda, o time repete os mesmos erros "
                   "e não consegue ajustar o pitch ou a proposta comercial.",
        "solucao": "Campos obrigatórios de motivo de perda e relatórios de win/loss analysis "
                   "revelam padrões e permitem ação corretiva rápida.",
    },
    "ciclo de vendas muito longo": {
        "titulo": "Ciclo de vendas excessivamente longo",
        "impacto": "Cada semana a mais no ciclo representa custo de venda mais alto e capital "
                   "imobilizado em oportunidades que poderiam estar fechadas.",
        "solucao": "Automações de follow-up, alertas de oportunidades paradas e playbooks "
                   "digitais no Salesforce reduzem o ciclo médio em 20–35%.",
    },
    "previsao de receita": {
        "titulo": "Previsão de receita imprecisa",
        "impacto": "Forecast manual ou em planilha gera variância alta entre projetado e realizado, "
                   "comprometendo planejamento financeiro e de capacidade.",
        "solucao": "O módulo de Forecast do Sales Cloud combina dados reais do pipeline com "
                   "IA preditiva para gerar previsões com variância inferior a 5%.",
    },
    "atendimento nao tem historico": {
        "titulo": "Atendimento sem histórico unificado do cliente",
        "impacto": "Clientes precisam repetir informações a cada contato, gerando frustração e "
                   "aumentando o tempo médio de atendimento (AHT).",
        "solucao": "O Service Cloud consolida todo o histórico de interações, compras e casos "
                   "em uma única tela para o atendente.",
    },
    "leads nao sao seguidos": {
        "titulo": "Leads sem nurturing estruturado",
        "impacto": "Leads qualificados esfriam por falta de follow-up sistemático, reduzindo "
                   "a taxa de conversão e desperdiçando investimento em marketing.",
        "solucao": "Jornadas automatizadas no Marketing Cloud ou fluxos de nurturing no Sales Cloud "
                   "garantem que nenhum lead fique sem resposta.",
    },
    "performance individual": {
        "titulo": "Falta de visibilidade de performance individual",
        "impacto": "Sem dados por vendedor, gestores não conseguem identificar quem treinar, "
                   "quem promover ou ajustar metas de forma justa.",
        "solucao": "Dashboards individuais e relatórios de atividades no Sales Cloud mostram "
                   "métricas de cada vendedor em tempo real.",
    },
    "dados duplicados": {
        "titulo": "Dados duplicados e inconsistentes entre sistemas",
        "impacto": "Decisões baseadas em dados errados ou duplicados geram retrabalho, "
                   "relatórios inconsistentes e perda de confiança nas métricas.",
        "solucao": "O Data Cloud (CDP) unifica dados de múltiplas fontes com deduplicação "
                   "automática e cria um perfil único de cliente.",
    },
    "integracao dificil": {
        "titulo": "Integração difícil entre ferramentas",
        "impacto": "Dados ficam em silos, forçando exportações manuais e aumentando o "
                   "risco de inconsistências entre sistemas.",
        "solucao": "A plataforma Salesforce conta com mais de 3.000 conectores nativos no "
                   "AppExchange e APIs abertas para integração com qualquer sistema.",
    },
    "relatorios demoram": {
        "titulo": "Relatórios lentos e manuais",
        "impacto": "Tempo gasto gerando relatórios é tempo que não está sendo usado em vendas "
                   "ou atendimento — além de relatórios prontos sempre estarem desatualizados.",
        "solucao": "Dashboards em tempo real no Salesforce eliminam a necessidade de relatórios "
                   "manuais e entregam insights na palma da mão, inclusive pelo mobile.",
    },
    "falta visibilidade do funil": {
        "titulo": "Falta de visibilidade do funil em tempo real",
        "impacto": "Reuniões de pipeline demoram horas porque os dados precisam ser coletados "
                   "manualmente antes de cada encontro.",
        "solucao": "O Kanban de pipeline do Sales Cloud exibe todas as oportunidades em estágios "
                   "visuais, com filtros por vendedor, produto, região e período.",
    },
}

CASOS_USO_POR_SEGMENTO = {
    "varejo": [
        ("Gestão de relacionamento com franqueados",
         "Centralizar comunicação, metas e suporte para toda a rede de franquias.",
         "Redução de 40% no tempo de resposta para franqueados."),
        ("Pipeline de vendas B2B",
         "Controlar negociações com grandes varejistas ou distribuidores.",
         "Aumento de visibilidade e previsibilidade de receita."),
        ("Atendimento pós-venda",
         "Gestão de trocas, devoluções e reclamações em um único sistema.",
         "Redução do tempo médio de resolução de casos."),
    ],
    "financeiro": [
        ("Gestão de relacionamento com clientes de alta renda",
         "Visão 360° do cliente com portfólio, histórico e próximas oportunidades.",
         "Aumento da receita por cliente (cross-sell e up-sell)."),
        ("Onboarding digital de clientes",
         "Fluxo automatizado de aprovação e documentação para novos produtos.",
         "Redução do tempo de onboarding de semanas para dias."),
        ("Gestão de pipeline de crédito / seguros",
         "Acompanhamento de propostas, renovações e sinistros.",
         "Melhora na taxa de renovação e redução de churn."),
    ],
    "saude": [
        ("Coordenação de cuidados",
         "Visão unificada do paciente com histórico clínico e jornada de tratamento.",
         "Redução de readmissões e melhora na adesão ao tratamento."),
        ("Gestão de beneficiários",
         "Centralizar dados de planos, coberturas e histórico de utilizações.",
         "Aumento da satisfação e redução de ligações repetidas."),
        ("Pipeline de credenciamento de prestadores",
         "Controle de documentação, validade e performance de médicos e clínicas.",
         "Redução de 60% no tempo de credenciamento."),
    ],
    "servicos": [
        ("Pipeline de vendas consultivas",
         "Gestão de oportunidades complexas com múltiplos stakeholders.",
         "Aumento da taxa de conversão e redução do ciclo."),
        ("Gestão de projetos e renovações",
         "Acompanhar entregas, marcos e renovações de contratos.",
         "Redução de churn e aumento de expansão de receita."),
        ("Portal do cliente",
         "Autoatendimento para solicitações, documentos e acompanhamento.",
         "Redução de 30% no volume de chamados."),
    ],
    "industria": [
        ("Gestão de distribuidores e revendas",
         "Visibilidade de sell-out, estoque e performance de canal.",
         "Melhora no planejamento de produção e logística."),
        ("Field Service",
         "Despacho e acompanhamento de técnicos de campo em tempo real.",
         "Redução do tempo médio de reparo (MTTR)."),
        ("Pipeline de grandes contas",
         "Gestão de oportunidades longas com múltiplos decisores.",
         "Aumento do win rate em contas estratégicas."),
    ],
    "outro": [
        ("Centralização do pipeline comercial",
         "Visão única de todas as oportunidades com estágio e valor.",
         "Mais previsibilidade e controle sobre a receita."),
        ("Automação de follow-up",
         "Alertas e tarefas automáticas para nunca deixar um lead esfriar.",
         "Aumento da taxa de conversão sem aumentar o time."),
        ("Dashboards executivos",
         "KPIs de vendas e atendimento em tempo real para a liderança.",
         "Decisões mais rápidas e baseadas em dados."),
    ],
}

PLANO_90_DIAS = {
    "fase1": {
        "pequeno": [
            ("Configurar org e perfis de usuário", "Kliente-360", "Ambiente pronto para uso"),
            ("Migrar dados do sistema atual", "Compartilhado", "Base de dados limpa no Salesforce"),
            ("Configurar pipeline e estágios de vendas", "Kliente-360", "Processo comercial mapeado"),
        ],
        "medio": [
            ("Configurar org, perfis e regras de negócio", "Kliente-360", "Ambiente configurado"),
            ("Migrar contas, contatos e histórico", "Compartilhado", "Dados migrados e validados"),
            ("Configurar objetos e campos customizados", "Kliente-360", "Modelo de dados finalizado"),
        ],
        "grande": [
            ("Arquitetura e configuração do ambiente", "Kliente-360", "Blueprint aprovado"),
            ("Migração e limpeza de dados legados", "Compartilhado", "Dados auditados"),
            ("Configuração de segurança e perfis", "Kliente-360", "Governança estabelecida"),
        ],
    },
    "fase2": {
        "pequeno": [
            ("Criar automações de follow-up", "Kliente-360", "Zero leads sem resposta"),
            ("Configurar relatórios e dashboard", "Kliente-360", "Visibilidade em tempo real"),
            ("Treinamento do time (4h)", "Kliente-360", "Adoção >70% em 30 dias"),
        ],
        "medio": [
            ("Implementar Flows de automação", "Kliente-360", "Processos automatizados"),
            ("Configurar integrações (e-mail, calendário)", "Kliente-360", "Captura automática de atividades"),
            ("Dashboards por perfil (vendedor/gestor)", "Kliente-360", "Insights diferenciados"),
        ],
        "grande": [
            ("Flows e automações complexas", "Kliente-360", "Processos críticos automatizados"),
            ("Integrações com sistemas legados", "Compartilhado", "Dados fluindo em tempo real"),
            ("Relatórios e dashboards executivos", "Kliente-360", "BI operacional ativo"),
        ],
    },
    "fase3": {
        "pequeno": [
            ("Ajustes pós-treinamento", "Kliente-360", "Sistema alinhado ao uso real"),
            ("Go-live e suporte intensivo (2 semanas)", "Kliente-360", "Time operando de forma autônoma"),
            ("Revisão de adoção e próximos passos", "Compartilhado", "Roadmap de evolução definido"),
        ],
        "medio": [
            ("UAT com usuários-chave", "Compartilhado", "Validação funcional completa"),
            ("Treinamento por perfil (8h total)", "Kliente-360", "Adoção >80%"),
            ("Go-live e suporte pós-implantação (30 dias)", "Kliente-360", "Operação estável"),
        ],
        "grande": [
            ("UAT e homologação formal", "Compartilhado", "Aprovação para go-live"),
            ("Treinamento em ondas (16h total)", "Kliente-360", "Adoção medida por perfil"),
            ("Go-live faseado + hypercare 60 dias", "Kliente-360", "Transição controlada"),
        ],
    },
}


def carregar_input(slug_cliente: str) -> tuple[dict, Path]:
    arquivos = sorted(INPUTS_DIR.glob(f"{slug_cliente}*_formulario.json"), reverse=True)
    if not arquivos:
        print(f"[ERRO] Nenhum formulário encontrado para '{slug_cliente}' em {INPUTS_DIR}/")
        sys.exit(1)
    if len(arquivos) > 1:
        print("Múltiplos formulários encontrados:")
        for i, a in enumerate(arquivos, 1):
            print(f"  {i}. {a.name}")
        escolha = input("Qual usar? (número): ").strip()
        caminho = arquivos[int(escolha) - 1]
    else:
        caminho = arquivos[0]
    with open(caminho, encoding="utf-8") as f:
        return json.load(f), caminho


def _porte_key(porte: str) -> str:
    porte = porte.lower()
    if any(x in porte for x in ["1-10", "até 10", "ate 10", "micro"]):
        return "pequeno"
    if any(x in porte for x in ["11-50", "51-200", "pequena", "media", "média"]):
        return "medio"
    return "grande"


def formatar_real(valor: int) -> str:
    return f"{valor:,.0f}".replace(",", ".")


def gerar_secao_dores(dores: list[str]) -> str:
    linhas = []
    for dor in dores:
        dor_norm = re.sub(r"[^a-z0-9 ]", "", dor.lower())
        narrativa = None
        for chave, dados in NARRATIVAS_DORES.items():
            if any(palavra in dor_norm for palavra in chave.split()):
                narrativa = dados
                break
        if not narrativa:
            narrativa = {
                "titulo": dor.strip(),
                "impacto": "Impacto direto na eficiência operacional e resultados comerciais.",
                "solucao": "O Salesforce oferece ferramentas específicas para endereçar esse desafio.",
            }
        linhas.append(f"### {narrativa['titulo']}\n")
        linhas.append(f"**Situação:** {dor.strip()}\n\n")
        linhas.append(f"**Impacto no negócio:** {narrativa['impacto']}\n\n")
        linhas.append(f"**Como o Salesforce resolve:** {narrativa['solucao']}\n\n---\n")
    return "\n".join(linhas)


def gerar_casos_uso(segmento: str, cloud: str) -> str:
    casos = CASOS_USO_POR_SEGMENTO.get(segmento, CASOS_USO_POR_SEGMENTO["outro"])
    linhas = []
    for titulo, descricao, resultado in casos[:4]:
        linhas.append(f"#### {titulo}\n{descricao}\n\n**Resultado esperado:** {resultado}\n\n---\n")
    return "\n".join(linhas)


def gerar_plano_90_dias(porte: str) -> str:
    key = _porte_key(porte)
    linhas = []
    for fase_key, fase_label in [("fase1", "Fundação (Dias 1–30)"),
                                   ("fase2", "Automação (Dias 31–60)"),
                                   ("fase3", "Otimização (Dias 61–90)")]:
        atividades = PLANO_90_DIAS[fase_key][key]
        linhas.append(f"### Fase — {fase_label}\n")
        linhas.append("| Atividade | Responsável | Resultado esperado |")
        linhas.append("|---|---|---|")
        for atv, resp, res in atividades:
            linhas.append(f"| {atv} | {resp} | {res} |")
        linhas.append("")
    return "\n".join(linhas)


def gerar_diagnostico(dados: dict) -> str:
    hoje = date.today()
    validade = hoje + timedelta(days=30)
    inv = dados.get("investimento", {})
    cloud_info = dados.get("cloud_recomendada", {})
    cloud = cloud_info.get("cloud", "Sales Cloud")
    segmento = dados.get("segmento", "outro")
    porte = dados.get("porte", "11-50 funcionários")
    nome = dados.get("nome_empresa", "Cliente")
    dores = dados.get("dores", [])

    pacotes_labels = {
        "diagnostico": "Diagnóstico (R$ 497)",
        "diagnostico_demo": "Diagnóstico + Demo (R$ 997)",
        "diagnostico_demo_proposta": "Diagnóstico + Demo + Proposta (R$ 1.997)",
    }
    proximo_passo_map = {
        "diagnostico": "Agende uma call de 30 minutos para apresentarmos os achados ao seu time.",
        "diagnostico_demo": "Confirme o horário da sua demo personalizada de 45 minutos.",
        "diagnostico_demo_proposta": "A proposta técnica completa está sendo preparada — aguarde em até 48 horas.",
    }
    sumario = (
        f"{nome} é uma empresa do segmento {segmento} que enfrenta desafios relevantes "
        f"na gestão comercial e operacional. Com base nas informações compartilhadas, "
        f"identificamos {len(dores)} pontos críticos que impactam diretamente a capacidade "
        f"de crescimento e previsibilidade do negócio.\n\n"
        f"O principal desafio identificado é a ausência de uma plataforma centralizada que "
        f"conecte dados, processos e equipes — gerando retrabalho, perda de oportunidades e "
        f"decisões baseadas em informações incompletas.\n\n"
        f"A solução recomendada é o {cloud}, que resolve diretamente as dores mapeadas com "
        f"implementação em 8 a 16 semanas. O investimento se paga em {inv.get('payback_meses', 12)} meses "
        f"com base nos benchmarks do segmento {segmento}.\n\n"
        f"Este documento detalha o diagnóstico completo, a solução recomendada com casos de uso "
        f"específicos, o plano de ação em 90 dias e a estimativa de investimento e ROI."
    )
    adicional_str = ", ".join(cloud_info.get("adicional", [])) or "—"
    plano = gerar_plano_90_dias(porte)
    secao_dores = gerar_secao_dores(dores)
    casos_uso = gerar_casos_uso(segmento, cloud)
    receita_atual = inv.get("roi_estimado", 0) * 10
    receita_sf = int(receita_atual * 1.08)

    return f"""# Diagnóstico Salesforce — {nome}

**Preparado por:** Kliente-360
**Data:** {hoje.strftime("%d/%m/%Y")}
**Pacote contratado:** {pacotes_labels.get(dados.get("pacote", "diagnostico"), "Diagnóstico")}
**Válido até:** {validade.strftime("%d/%m/%Y")}
**Confidencial — uso exclusivo de {nome}**

---

## Sumário Executivo

{sumario}

---

## Situação Atual

| Campo | Dado |
|---|---|
| **Empresa** | {nome} |
| **Segmento** | {segmento.capitalize()} |
| **Porte** | {porte} |
| **Vendedores / Atendentes** | {dados.get("num_vendedores", "—")} |
| **CRM atual** | {dados.get("crm_atual", "—")} |
| **Budget estimado** | {dados.get("budget", "—")} |
| **Prazo de decisão** | {dados.get("prazo_decisao", "—")} |

**O que quer resolver em 90 dias:**
> {dados.get("objetivo_90_dias", "—")}

**Resultado ideal em 6 meses:**
> {dados.get("resultado_6_meses", "—")}

---

## Dores Identificadas e Análise de Impacto

{secao_dores}

---

## Solução Salesforce Recomendada

**Produto principal:** {cloud}

**Por que essa solução para {nome}:**
{cloud_info.get("justificativa", "")} O {cloud} é o produto Salesforce com maior aderência ao perfil de {nome}, considerando segmento ({segmento}), porte e as dores mapeadas.

**Produtos complementares a considerar:** {adicional_str}

### Casos de Uso Prioritários

{casos_uso}

---

## Plano de Ação — 90 Dias

{plano}

---

## Estimativa de Investimento

| Item | Faixa estimada |
|---|---|
| Licenças Salesforce ({inv.get("num_usuarios", "—")} usuários) | R$ {formatar_real(inv.get("licenca_min", 0))} – R$ {formatar_real(inv.get("licenca_max", 0))} / mês |
| Implementação e configuração | R$ {formatar_real(inv.get("impl_min", 0))} – R$ {formatar_real(inv.get("impl_max", 0))} |
| Treinamento do time | Incluso |
| **Total no primeiro ano** | **R$ {formatar_real(inv.get("total_min", 0))} – R$ {formatar_real(inv.get("total_max", 0))}** |

**Impacto financeiro estimado:** R$ {formatar_real(inv.get("roi_estimado", 0))} / ano
**Payback estimado:** {inv.get("payback_meses", 12)} meses

---

## Próximos Passos

{proximo_passo_map.get(dados.get("pacote", "diagnostico"), "")}

---

*Diagnóstico preparado com base nas informações fornecidas em {hoje.strftime("%d/%m/%Y")}.*
*Válido por 30 dias. Kliente-360 — Consultoria Salesforce Certificada.*
"""


def salvar_output(conteudo: str, nome_cliente: str) -> Path:
    OUTPUTS_DIR.mkdir(exist_ok=True)
    slug = re.sub(r"[^a-z0-9]+", "-", nome_cliente.lower()).strip("-")
    hoje = date.today().isoformat()
    caminho = OUTPUTS_DIR / f"{slug}_{hoje}_diagnostico.md"
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
    print("║   SF Presales Toolkit — Diagnóstico      ║")
    print("╚══════════════════════════════════════════╝\n")
    slug = sys.argv[1] if len(sys.argv) > 1 else input("Nome do cliente (slug): ").strip()
    print(f"\n[1/5] Carregando formulário para '{slug}'...")
    dados, caminho_input = carregar_input(slug)
    print(f"      ✓ {caminho_input.name}")
    print("[2/5] Analisando dores e segmento...")
    nome = dados.get("nome_empresa", slug)
    segmento = dados.get("segmento", "outro")
    cloud = dados.get("cloud_recomendada", {}).get("cloud", "Sales Cloud")
    dores = dados.get("dores", [])
    print(f"      ✓ Segmento: {segmento} | Cloud: {cloud} | Dores: {len(dores)}")
    print("[3/5] Gerando diagnóstico...")
    conteudo = gerar_diagnostico(dados)
    print("      ✓ Documento gerado")
    print("[4/5] Estimando investimento e ROI...")
    inv = dados.get("investimento", {})
    print(f"      ✓ R$ {inv.get('total_min', 0):,.0f} – R$ {inv.get('total_max', 0):,.0f} / ano")
    print("[5/5] Finalizando e salvando documento...")
    caminho_output = salvar_output(conteudo, nome)
    print(f"      ✓ Diagnóstico salvo em {caminho_output}")
    pacote = dados.get("pacote", "diagnostico")
    print("─" * 50)
    if "demo" in pacote:
        slug_out = re.sub(r"[^a-z0-9]+", "-", nome.lower()).strip("-")
        print(f"Próximo passo: python pipeline/demo_setup.py {slug_out}")
    if "proposta" in pacote:
        slug_out = re.sub(r"[^a-z0-9]+", "-", nome.lower()).strip("-")
        print(f"Após a demo: python pipeline/proposta.py {slug_out}")
    print()


if __name__ == "__main__":
    main()
