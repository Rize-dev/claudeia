#!/usr/bin/env python3
"""
DIREX - O Cérebro Estratégico da Operação
Agente estratégico para transformar ideias em resultados através de planejamento estruturado.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import sys

class DirexAgent:
    """
    DIREX: O cérebro estratégico da operação.
    Transforma ideias em metas, metas em rotinas e rotinas em resultados.
    """

    def __init__(self):
        self.business_objective = None
        self.okrs = []
        self.kpis = []
        self.roadmap = []
        self.weekly_plan = []
        self.tasks = []
        self.data_dir = "direx_data"
        os.makedirs(self.data_dir, exist_ok=True)

    def welcome_message(self) -> str:
        """Retorna a mensagem de boas-vindas do DIREX"""
        return """
🚀 DIREX ATIVADO 🚀

Olá! Eu sou DIREX, o cérebro estratégico da sua operação.
Como CEO virtual, meu papel é transformar suas ideias em resultados concretos.

✅ Capacidades:
   • Criar planos de ação estratégicos
   • Desenvolver OKRs e KPIs
   • Construir roadmaps detalhados
   • Planejar semanas produtivas
   • Priorizar tarefas por impacto x esforço
   • Alinhar estratégias com objetivos de negócio

💡 Vamos começar definindo o objetivo do seu negócio...
"""

    def ask_business_objective(self) -> str:
        """Pergunta pelo objetivo do negócio"""
        print("\n🎯 OBJETIVO DE NEGÓCIO")
        print("Para criar estratégias alinhadas, preciso entender:")
        print("Qual é o objetivo principal do seu negócio nos próximos 3-6 meses?")

        examples = [
            "Aumentar receita em 30% através de novos clientes",
            "Lançar produto/serviço no mercado",
            "Expandir presença digital e autoridade",
            "Otimizar processos internos para eficiência",
            "Construir equipe e cultura organizacional"
        ]

        print("\n📝 Exemplos:")
        for i, example in enumerate(examples, 1):
            print(f"   {i}. {example}")

        while True:
            objective = input("\nDigite seu objetivo: ").strip()
            if objective:
                self.business_objective = objective
                print(f"\n✅ Objetivo definido: {objective}")
                return objective
            print("❌ Objetivo não pode estar vazio. Tente novamente.")

    def create_okrs(self) -> List[Dict]:
        """Cria OKRs baseados no objetivo do negócio"""
        print("\n🎯 CRIANDO OKRs")

        if not self.business_objective:
            self.ask_business_objective()

        # OKR principal
        okr_principal = {
            "tipo": "principal",
            "objetivo": f"Alcançar: {self.business_objective}",
            "resultados_chave": self._generate_key_results(),
            "periodo": "3 meses",
            "status": "ativo"
        }

        # OKRs de suporte
        okrs_suporte = self._generate_support_okrs()

        self.okrs = [okr_principal] + okrs_suporte

        print("✅ OKRs criados com sucesso!")
        return self.okrs

    def _generate_key_results(self) -> List[str]:
        """Gera resultados-chave baseados no objetivo"""
        objective_lower = self.business_objective.lower()

        if "receita" in objective_lower or "vendas" in objective_lower:
            return [
                "Aumentar receita mensal em 30%",
                "Adquirir 50 novos clientes pagantes",
                "Elevar ticket médio em 20%",
                "Reduzir churn para menos de 5%"
            ]
        elif "produto" in objective_lower or "lançar" in objective_lower:
            return [
                "Completar desenvolvimento do MVP",
                "Validar produto com 100 usuários beta",
                "Alcançar 95% de satisfação dos primeiros usuários",
                "Definir pricing e modelo de negócio"
            ]
        elif "presença digital" in objective_lower or "autoridade" in objective_lower:
            return [
                "Aumentar seguidores em 200%",
                "Gerar 50 menções em mídias relevantes",
                "Criar 24 conteúdos de autoridade",
                "Estabelecer parcerias estratégicas"
            ]
        else:
            return [
                "Definir 3 métricas principais de sucesso",
                "Implementar processos para acompanhar progresso",
                "Identificar e remover 2 maiores obstáculos",
                "Construir base sólida para crescimento"
            ]

    def _generate_support_okrs(self) -> List[Dict]:
        """Gera OKRs de suporte independentes do objetivo principal"""
        return [
            {
                "tipo": "suporte",
                "objetivo": "Otimizar operações e processos internos",
                "resultados_chave": [
                    "Automatizar 3 processos manuais",
                    "Reduzir tempo de resposta em 50%",
                    "Implementar sistema de acompanhamento",
                    "Treinar equipe em novas ferramentas"
                ],
                "periodo": "3 meses",
                "status": "ativo"
            },
            {
                "tipo": "suporte",
                "objetivo": "Desenvolver equipe e cultura organizacional",
                "resultados_chave": [
                    "Contratar 2 novos membros-chave",
                    "Implementar programa de feedback semanal",
                    "Aumentar engajamento da equipe em 40%",
                    "Definir valores e missão da empresa"
                ],
                "periodo": "3 meses",
                "status": "ativo"
            }
        ]

    def create_kpis(self) -> List[Dict]:
        """Cria KPIs para acompanhar o progresso"""
        print("\n📊 CRIANDO KPIs")

        kpis_base = [
            {
                "nome": "Receita Mensal",
                "categoria": "Financeiro",
                "meta": "R$ XX.XXX",
                "atual": "R$ 0",
                "frequencia": "Mensal",
                "responsavel": "CEO/Financeiro"
            },
            {
                "nome": "Número de Clientes",
                "categoria": "Comercial",
                "meta": "XXX clientes",
                "atual": "0",
                "frequencia": "Mensal",
                "responsavel": "Comercial"
            },
            {
                "nome": "Satisfação do Cliente",
                "categoria": "Qualidade",
                "meta": "95%",
                "atual": "0%",
                "frequencia": "Trimestral",
                "responsavel": "Produto"
            },
            {
                "nome": "Produtividade da Equipe",
                "categoria": "Operacional",
                "meta": "XX horas/dia útil",
                "atual": "0",
                "frequencia": "Semanal",
                "responsavel": "Operações"
            }
        ]

        self.kpis = kpis_base
        print("✅ KPIs criados com sucesso!")
        return self.kpis

    def create_roadmap(self, periodo_dias: int = 90) -> List[Dict]:
        """Cria roadmap para o período especificado"""
        print(f"\n🗺️ CRIANDO ROADMAP PARA {periodo_dias} DIAS")

        if not self.okrs:
            self.create_okrs()

        # Dividir período em fases
        fases = []
        if periodo_dias <= 7:
            fases = ["Semana 1"]
        elif periodo_dias <= 15:
            fases = ["Semana 1", "Semana 2"]
        elif periodo_dias <= 30:
            fases = ["Semana 1-2", "Semana 3-4"]
        else:
            fases = ["Mês 1", "Mês 2", "Mês 3"]

        roadmap_items = []

        for i, fase in enumerate(fases):
            fase_items = {
                "fase": fase,
                "periodo": f"Dias {(i * periodo_dias // len(fases)) + 1} - {(i + 1) * periodo_dias // len(fases)}",
                "objetivos": self._generate_fase_objectives(fase),
                "entregas": self._generate_fase_deliverables(fase),
                "marcos": self._generate_fase_milestones(fase),
                "status": "pendente"
            }
            roadmap_items.append(fase_items)

        self.roadmap = roadmap_items
        print("✅ Roadmap criado com sucesso!")
        return self.roadmap

    def _generate_fase_objectives(self, fase: str) -> List[str]:
        """Gera objetivos para cada fase"""
        objectives_map = {
            "Semana 1": [
                "Definir escopo e requisitos claros",
                "Configurar ferramentas e processos básicos",
                "Realizar pesquisa inicial de mercado"
            ],
            "Semana 2": [
                "Desenvolver primeira versão do produto/serviço",
                "Testar com usuários iniciais",
                "Ajustar baseado em feedback"
            ],
            "Mês 1": [
                "Completar planejamento estratégico detalhado",
                "Configurar infraestrutura básica",
                "Iniciar desenvolvimento do core product"
            ],
            "Mês 2": [
                "Lançar MVP e coletar feedback",
                "Otimizar processos internos",
                "Expandir equipe se necessário"
            ],
            "Mês 3": [
                "Escalar operações baseado em métricas",
                "Implementar melhorias identificadas",
                "Planejar próximos passos de crescimento"
            ]
        }
        return objectives_map.get(fase, ["Definir objetivos específicos da fase"])

    def _generate_fase_deliverables(self, fase: str) -> List[str]:
        """Gera entregas para cada fase"""
        deliverables_map = {
            "Semana 1": [
                "Documento de requisitos",
                "Plano de ação inicial",
                "Pesquisa de mercado básica"
            ],
            "Semana 2": [
                "Protótipo funcional",
                "Relatório de testes iniciais",
                "Lista de melhorias prioritárias"
            ],
            "Mês 1": [
                "Estratégia completa documentada",
                "Sistema básico operacional",
                "Equipe alinhada com objetivos"
            ],
            "Mês 2": [
                "Produto mínimo viável lançado",
                "Processos otimizados",
                "Métricas de sucesso definidas"
            ],
            "Mês 3": [
                "Operações em escala",
                "Relatório de performance",
                "Plano de crescimento futuro"
            ]
        }
        return deliverables_map.get(fase, ["Entregas específicas da fase"])

    def _generate_fase_milestones(self, fase: str) -> List[str]:
        """Gera marcos importantes para cada fase"""
        milestones_map = {
            "Semana 1": [
                "Reunião de alinhamento da equipe",
                "Definição clara de escopo",
                "Setup completo do ambiente"
            ],
            "Semana 2": [
                "Primeiro feedback de usuários",
                "Iteração baseada em testes",
                "Decisões sobre próximos passos"
            ],
            "Mês 1": [
                "Aprovação da estratégia completa",
                "Primeiras funcionalidades core",
                "Contratações estratégicas"
            ],
            "Mês 2": [
                "Lançamento público do MVP",
                "Alcance das primeiras metas",
                "Identificação de padrões de uso"
            ],
            "Mês 3": [
                "Estabilidade operacional",
                "Crescimento sustentável",
                "Preparação para expansão"
            ]
        }
        return milestones_map.get(fase, ["Marcos importantes da fase"])

    def create_weekly_plan(self) -> List[Dict]:
        """Cria plano semanal detalhado"""
        print("\n📅 CRIANDO PLANO SEMANAL")

        # Dias da semana
        dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]

        weekly_plan = []

        for dia in dias:
            dia_plan = {
                "dia": dia,
                "tarefas_principais": self._generate_daily_tasks(dia),
                "foco": self._generate_daily_focus(dia),
                "metricas": self._generate_daily_metrics(dia),
                "status": "pendente"
            }
            weekly_plan.append(dia_plan)

        self.weekly_plan = weekly_plan
        print("✅ Plano semanal criado com sucesso!")
        return self.weekly_plan

    def _generate_daily_tasks(self, dia: str) -> List[str]:
        """Gera tarefas principais para cada dia"""
        tasks_map = {
            "Segunda": [
                "Revisar objetivos da semana",
                "Priorizar tarefas críticas",
                "Reunião de alinhamento da equipe",
                "Definir métricas diárias"
            ],
            "Terça": [
                "Executar tarefas de alto impacto",
                "Revisar progresso dos OKRs",
                "Reuniões com stakeholders",
                "Atualizar dashboards"
            ],
            "Quarta": [
                "Foco em desenvolvimento/produto",
                "Análise de dados e métricas",
                "Brainstorming de ideias",
                "Revisão de processos"
            ],
            "Quinta": [
                "Execução de tarefas estratégicas",
                "Preparação para entregas",
                "Reuniões de acompanhamento",
                "Planejamento da próxima semana"
            ],
            "Sexta": [
                "Finalizar entregas da semana",
                "Revisar conquistas e aprendizados",
                "Feedback da equipe",
                "Planejamento pessoal/profissional"
            ],
            "Sábado": [
                "Atividades de crescimento pessoal",
                "Leitura e aprendizado",
                "Reflexão estratégica",
                "Tempo com família/amigos"
            ],
            "Domingo": [
                "Preparação para a semana",
                "Revisão de hábitos e rotinas",
                "Planejamento de lazer",
                "Recarregar energias"
            ]
        }
        return tasks_map.get(dia, ["Tarefas específicas do dia"])

    def _generate_daily_focus(self, dia: str) -> str:
        """Gera foco principal para cada dia"""
        focus_map = {
            "Segunda": "Alinhamento e planejamento",
            "Terça": "Execução estratégica",
            "Quarta": "Análise e otimização",
            "Quinta": "Entregas e progresso",
            "Sexta": "Conclusão e reflexão",
            "Sábado": "Crescimento pessoal",
            "Domingo": "Recuperação e preparação"
        }
        return focus_map.get(dia, "Foco específico do dia")

    def _generate_daily_metrics(self, dia: str) -> List[str]:
        """Gera métricas para acompanhar cada dia"""
        metrics_map = {
            "Segunda": ["Tarefas prioritárias definidas", "Equipe alinhada", "Objetivos claros"],
            "Terça": ["Progresso nos OKRs", "Reuniões produtivas", "Bloqueadores removidos"],
            "Quarta": ["Insights gerados", "Processos otimizados", "Ideias inovadoras"],
            "Quinta": ["Entregas completadas", "Qualidade mantida", "Feedback coletado"],
            "Sexta": ["Semana concluída", "Aprendizados documentados", "Próxima semana planejada"],
            "Sábado": ["Habilidades desenvolvidas", "Conhecimento adquirido", "Bem-estar mantido"],
            "Domingo": ["Energia recarregada", "Semana preparada", "Foco renovado"]
        }
        return metrics_map.get(dia, ["Métricas específicas do dia"])

    def prioritize_tasks(self, tasks: List[str]) -> List[Tuple[str, str, int]]:
        """Prioriza tarefas baseado em impacto x esforço"""
        print("\n⚖️ PRIORIZANDO TAREFAS")

        if not tasks:
            print("❌ Nenhuma tarefa fornecida para priorização.")
            return []

        prioritized = []

        for task in tasks:
            print(f"\n📋 Tarefa: {task}")
            print("Avalie de 1-10:")

            while True:
                try:
                    impacto = int(input("   Impacto no objetivo (1-10): "))
                    esforco = int(input("   Esforço necessário (1-10): "))

                    if 1 <= impacto <= 10 and 1 <= esforco <= 10:
                        prioridade = (impacto * 2) - esforco  # Fórmula: 2x impacto - esforço
                        nivel = self._get_priority_level(prioridade)
                        prioritized.append((task, nivel, prioridade))
                        break
                    else:
                        print("❌ Valores devem estar entre 1 e 10.")
                except ValueError:
                    print("❌ Digite apenas números.")

        # Ordenar por prioridade (maior primeiro)
        prioritized.sort(key=lambda x: x[2], reverse=True)

        print("\n✅ Tarefas priorizadas:")
        for i, (task, nivel, score) in enumerate(prioritized, 1):
            print(f"   {i}. [{nivel}] {task} (Score: {score})")

        return prioritized

    def _get_priority_level(self, score: int) -> str:
        """Converte score em nível de prioridade"""
        if score >= 15:
            return "CRÍTICA"
        elif score >= 10:
            return "ALTA"
        elif score >= 5:
            return "MÉDIA"
        else:
            return "BAIXA"

    def save_data(self):
        """Salva todos os dados do DIREX"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        data = {
            "business_objective": self.business_objective,
            "okrs": self.okrs,
            "kpis": self.kpis,
            "roadmap": self.roadmap,
            "weekly_plan": self.weekly_plan,
            "tasks": self.tasks,
            "timestamp": timestamp
        }

        filename = os.path.join(self.data_dir, f"direx_data_{timestamp}.json")

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"\n💾 Dados salvos em: {filename}")
        return filename

    def load_data(self, filename: Optional[str] = None):
        """Carrega dados salvos do DIREX"""
        if not filename:
            # Carregar o arquivo mais recente
            files = [f for f in os.listdir(self.data_dir) if f.startswith("direx_data_") and f.endswith(".json")]
            if not files:
                print("❌ Nenhum arquivo de dados encontrado.")
                return False

            files.sort(reverse=True)
            filename = os.path.join(self.data_dir, files[0])

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.business_objective = data.get("business_objective")
            self.okrs = data.get("okrs", [])
            self.kpis = data.get("kpis", [])
            self.roadmap = data.get("roadmap", [])
            self.weekly_plan = data.get("weekly_plan", [])
            self.tasks = data.get("tasks", [])

            print(f"✅ Dados carregados de: {filename}")
            return True

        except Exception as e:
            print(f"❌ Erro ao carregar dados: {e}")
            return False

    def display_summary(self):
        """Exibe resumo atual do DIREX"""
        print("\n📊 RESUMO DIREX")
        print("=" * 50)

        if self.business_objective:
            print(f"🎯 Objetivo: {self.business_objective}")
        else:
            print("🎯 Objetivo: Não definido")

        print(f"🎯 OKRs: {len(self.okrs)} definidos")
        print(f"📊 KPIs: {len(self.kpis)} configurados")
        print(f"🗺️ Roadmap: {len(self.roadmap)} fases")
        print(f"📅 Plano Semanal: {len(self.weekly_plan)} dias")
        print(f"📋 Tarefas: {len(self.tasks)} registradas")

        print("=" * 50)

    def run_interactive(self):
        """Executa o DIREX em modo interativo"""
        print(self.welcome_message())

        while True:
            print("\n" + "="*50)
            print("🤖 DIREX - MENU PRINCIPAL")
            print("="*50)
            print("1. 📝 Definir Objetivo de Negócio")
            print("2. 🎯 Criar OKRs")
            print("3. 📊 Configurar KPIs")
            print("4. 🗺️ Criar Roadmap (7/15/30 dias)")
            print("5. 📅 Planejar Semana")
            print("6. ⚖️ Priorizar Tarefas")
            print("7. 📊 Ver Resumo")
            print("8. 💾 Salvar Dados")
            print("9. 📂 Carregar Dados")
            print("0. 🚪 Sair")
            print("="*50)

            try:
                choice = input("Escolha uma opção: ").strip()

                if choice == "1":
                    self.ask_business_objective()

                elif choice == "2":
                    okrs = self.create_okrs()
                    print("\n📋 OKRs Criados:")
                    for i, okr in enumerate(okrs, 1):
                        print(f"\n{i}. {okr['objetivo']}")
                        print("   Resultados-Chave:")
                        for kr in okr['resultados_chave']:
                            print(f"   • {kr}")

                elif choice == "3":
                    kpis = self.create_kpis()
                    print("\n📊 KPIs Configurados:")
                    for kpi in kpis:
                        print(f"• {kpi['nome']}: Meta {kpi['meta']} ({kpi['frequencia']})")

                elif choice == "4":
                    print("Escolha o período:")
                    print("1. 7 dias")
                    print("2. 15 dias")
                    print("3. 30 dias")
                    print("4. 90 dias")

                    periodo_choice = input("Opção: ").strip()
                    periodo_map = {"1": 7, "2": 15, "3": 30, "4": 90}
                    periodo = periodo_map.get(periodo_choice, 30)

                    roadmap = self.create_roadmap(periodo)
                    print(f"\n🗺️ Roadmap para {periodo} dias:")
                    for fase in roadmap:
                        print(f"\n📅 {fase['fase']} ({fase['periodo']}):")
                        print(f"   🎯 Objetivos: {', '.join(fase['objetivos'][:2])}...")
                        print(f"   📦 Entregas: {', '.join(fase['entregas'][:2])}...")

                elif choice == "5":
                    weekly_plan = self.create_weekly_plan()
                    print("\n📅 Plano Semanal Criado:")
                    for dia in weekly_plan[:5]:  # Mostrar apenas dias úteis
                        print(f"\n📆 {dia['dia']}:")
                        print(f"   🎯 Foco: {dia['foco']}")
                        print(f"   📋 Tarefas: {', '.join(dia['tarefas_principais'][:2])}...")

                elif choice == "6":
                    print("Digite as tarefas para priorizar (uma por linha, vazio para terminar):")
                    tasks = []
                    while True:
                        task = input("Tarefa: ").strip()
                        if not task:
                            break
                        tasks.append(task)

                    if tasks:
                        self.prioritize_tasks(tasks)
                    else:
                        print("❌ Nenhuma tarefa fornecida.")

                elif choice == "7":
                    self.display_summary()

                elif choice == "8":
                    self.save_data()

                elif choice == "9":
                    self.load_data()

                elif choice == "0":
                    print("\n👋 Até logo! DIREX foi desativado.")
                    break

                else:
                    print("❌ Opção inválida. Tente novamente.")

            except KeyboardInterrupt:
                print("\n\n👋 Operação interrompida. Até logo!")
                break
            except Exception as e:
                print(f"❌ Erro: {e}")

def main():
    """Função principal"""
    try:
        direx = DirexAgent()
        direx.run_interactive()
    except Exception as e:
        print(f"Erro crítico: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()