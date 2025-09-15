import datetime

# --- PLANO DE CONTAS ---
PLANO_DE_CONTAS = [
    {"nome": "Caixa", "grupo": "Ativo"},
    {"nome": "Clientes a Receber", "grupo": "Ativo"},
    {"nome": "Estoques", "grupo": "Ativo"},
    {"nome": "Fornecedores", "grupo": "Passivo"},
    {"nome": "Salários a Pagar", "grupo": "Passivo"},
    {"nome": "INSS a Recolher", "grupo": "Passivo"},
    {"nome": "FGTS a Recolher", "grupo": "Passivo"},
    {"nome": "Provisão 13º Salário", "grupo": "Passivo"},
    {"nome": "Provisão Férias", "grupo": "Passivo"},
    {"nome": "ICMS a Recolher", "grupo": "Passivo"},
    {"nome": "PIS a Recolher", "grupo": "Passivo"},
    {"nome": "COFINS a Recolher", "grupo": "Passivo"},
    {"nome": "Depreciação Acumulada", "grupo": "Passivo"},
    {"nome": "Receita de Vendas de Mercadorias", "grupo": "Receita"},
    {"nome": "Despesa de Energia", "grupo": "Despesa"},
    {"nome": "Despesa de Honorários", "grupo": "Despesa"},
    {"nome": "Despesa Bancária", "grupo": "Despesa"},
    {"nome": "Despesa de Sistemas", "grupo": "Despesa"},
    {"nome": "Despesa de Combustível", "grupo": "Despesa"},
    {"nome": "Despesa de Depreciação", "grupo": "Despesa"},
    {"nome": "Despesa de Salário João", "grupo": "Despesa", "R": True},
    {"nome": "Despesa de Salário Maria", "grupo": "Despesa", "R": True},
    {"nome": "Despesa Provisão 13º", "grupo": "Despesa", "R": True},
    {"nome": "Despesa Provisão Férias", "grupo": "Despesa", "R": True},
    {"nome": "Despesa FGTS", "grupo": "Despesa", "R": True},
    {"nome": "ICMS sobre Vendas", "grupo": "Despesa", "R": True},
    {"nome": "PIS sobre Vendas", "grupo": "Despesa", "R": True},
    {"nome": "COFINS sobre Vendas", "grupo": "Despesa", "R": True},
]

# --- LANÇAMENTOS (agosto/2025) ---
LANCAMENTOS = [
    {"debito": "Clientes a Receber", "credito": "Receita de Vendas de Mercadorias", "valor": 10000},
    {"debito": "Estoques", "credito": "Fornecedores", "valor": 6000},
    {"debito": "Despesa de Energia", "credito": "Caixa", "valor": 800},
    {"debito": "Despesa de Honorários", "credito": "Caixa", "valor": 1200},
    {"debito": "Despesa Bancária", "credito": "Caixa", "valor": 150},
    {"debito": "Despesa de Sistemas", "credito": "Caixa", "valor": 500},
    {"debito": "Despesa de Combustível", "credito": "Caixa", "valor": 600},
    {"debito": "Despesa de Depreciação", "credito": "Depreciação Acumulada", "valor": 1000},
    {"debito": "Despesa de Salário João", "credito": "Salários a Pagar", "valor": 4500},
    {"debito": "Despesa de Salário João", "credito": "INSS a Recolher", "valor": 500},
    {"debito": "Despesa de Salário Maria", "credito": "Salários a Pagar", "valor": 3600},
    {"debito": "Despesa de Salário Maria", "credito": "INSS a Recolher", "valor": 400},
    {"debito": "Despesa Provisão 13º", "credito": "Provisão 13º Salário", "valor": 1500},
    {"debito": "Despesa Provisão Férias", "credito": "Provisão Férias", "valor": 1200},
    {"debito": "Despesa FGTS", "credito": "FGTS a Recolher", "valor": 880},
    {"debito": "ICMS sobre Vendas", "credito": "ICMS a Recolher", "valor": 1200},
    {"debito": "PIS sobre Vendas", "credito": "PIS a Recolher", "valor": 200},
    {"debito": "COFINS sobre Vendas", "credito": "COFINS a Recolher", "valor": 600},
]

# --- BALANCETE ---
def balancete(PLANO_DE_CONTAS, LANCAMENTOS):
    print("\n📑 BALANCETE - Agosto/2025\n")
    saldos = {c["nome"]: 0 for c in PLANO_DE_CONTAS}

    for lanc in LANCAMENTOS:
        saldos[lanc["debito"]] += lanc["valor"]
        saldos[lanc["credito"]] -= lanc["valor"]

    total_debitos = total_creditos = 0
    print(f"{'Conta':<35}{'Débito':>12}{'Crédito':>12}")
    print("-" * 60)

    for conta, saldo in saldos.items():
        if saldo > 0:
            print(f"{conta:<35}{saldo:>12.2f}{'':>12}")
            total_debitos += saldo
        elif saldo < 0:
            print(f"{conta:<35}{'':>12}{-saldo:>12.2f}")
            total_creditos += -saldo

    print("-" * 60)
    print(f"{'TOTAL:':<35}{total_debitos:>12.2f}{total_creditos:>12.2f}\n")

# --- RELATÓRIO DE FOLHA ---
def relatorio_folha(PLANO_DE_CONTAS, LANCAMENTOS):
    print("\n📊 RELATÓRIO DE DESPESAS DE FOLHA DE PAGAMENTO\n")
    folha = {}
    for lanc in LANCAMENTOS:
        if any(c["nome"] == lanc["debito"] and c.get("R") for c in PLANO_DE_CONTAS if "Salário" in c["nome"] or "Provisão" in c["nome"] or "FGTS" in c["nome"]):
            folha[lanc["debito"]] = folha.get(lanc["debito"], 0) + lanc["valor"]

    total = 0
    for conta, valor in folha.items():
        print(f"{conta:<35}{valor:>12.2f}")
        total += valor
    print("-" * 50)
    print(f"{'TOTAL FOLHA:':<35}{total:>12.2f}\n")

# --- RELATÓRIO DE IMPOSTOS ---
def relatorio_impostos(PLANO_DE_CONTAS, LANCAMENTOS):
    print("\n📊 RELATÓRIO DE IMPOSTOS APURADOS\n")
    impostos = {}

    # Apenas impostos/encargos
    contas_impostos = ["INSS", "FGTS", "ICMS", "PIS", "COFINS"]

    for lanc in LANCAMENTOS:
        conta_debito = lanc["debito"]
        conta_credito = lanc["credito"]
        valor = lanc["valor"]

        # 1) Despesas relacionadas a impostos/encargos
        if any(p in conta_debito for p in contas_impostos):
            impostos[conta_debito] = impostos.get(conta_debito, 0) + valor

        # 2) Passivo correspondente (a Recolher)
        if any(p in conta_credito for p in contas_impostos):
            impostos[conta_credito] = impostos.get(conta_credito, 0) + valor

    total = 0
    for conta, valor in impostos.items():
        print(f"{conta:<35}{valor:>12.2f}")
        total += valor
    print("-" * 50)
    print(f"{'TOTAL DE IMPOSTOS:':<35}{total:>12.2f}\n")

# --- MENU ---
def menu():
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1. Balancete")
        print("2. Relatório da Folha de Pagamento")
        print("3. Relatório de Impostos Apurados")
        print("0. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            balancete(PLANO_DE_CONTAS, LANCAMENTOS)
        elif opcao == "2":
            relatorio_folha(PLANO_DE_CONTAS, LANCAMENTOS)
        elif opcao == "3":
            relatorio_impostos(PLANO_DE_CONTAS, LANCAMENTOS)
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")

# --- EXECUTAR ---
if __name__ == "__main__":
    menu()
