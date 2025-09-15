import datetime

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
# A importação incorreta foi removida daqui

# --- PLANO DE CONTAS (sem alterações) ---
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

# --- LANÇAMENTOS (sem alterações) ---
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


def gerar_pdf(nome_arquivo, titulo, linhas):
    """
    Gera um arquivo PDF formatado a partir de uma lista de linhas de texto.
    """
    try:
        c = canvas.Canvas(nome_arquivo, pagesize=A4)
        largura, altura = A4
        margem = 2 * cm
        y = altura - margem

        # Título
        c.setFont("Courier-Bold", 14)
        c.drawCentredString(largura / 2.0, y, titulo)
        y -= 1.5 * cm
        
        # Conteúdo
        c.setFont("Courier", 10) # Define a fonte para o corpo do texto
        for linha in linhas:
            c.drawString(margem, y, linha)
            y -= 0.7 * cm
            # Adiciona nova página se o conteúdo atingir o final
            if y < margem:
                c.showPage()
                c.setFont("Courier", 10)
                y = altura - margem

        c.save()
        print(f"Arquivo PDF '{nome_arquivo}' gerado com sucesso!\n")

    except Exception as e:
        print(f"Ocorreu um erro ao gerar o PDF '{nome_arquivo}': {e}")


# --- BALANCETE (sem alterações) ---
def balancete(PLANO_DE_CONTAS, LANCAMENTOS, gerar_pdf_flag=False):
    saldos = {c["nome"]: 0 for c in PLANO_DE_CONTAS}

    for lanc in LANCAMENTOS:
        saldos[lanc["debito"]] += lanc["valor"]
        saldos[lanc["credito"]] -= lanc["valor"]

    total_debitos = 0
    total_creditos = 0
    
    linhas = ["Conta".ljust(35) + "Débito".rjust(12) + "Crédito".rjust(12)]
    linhas.append("-" * 60)

    for conta, saldo in sorted(saldos.items()):
        if saldo > 0:
            linhas.append(f"{conta:<35}{saldo:>12.2f}{'':>12}")
            total_debitos += saldo
        elif saldo < 0:
            linhas.append(f"{conta:<35}{'':>12}{-saldo:>12.2f}")
            total_creditos += -saldo

    linhas.append("-" * 60)
    linhas.append(f"{'TOTAL:':<35}{total_debitos:>12.2f}{total_creditos:>12.2f}")

    if gerar_pdf_flag:
        gerar_pdf("balancete.pdf", "BALANCETE - Agosto/2025", linhas)
    else:
        print("\n--- BALANCETE ---")
        for linha in linhas:
            print(linha)

# --- RELATÓRIO DE FOLHA (sem alterações) ---
def relatorio_folha(PLANO_DE_CONTAS, LANCAMENTOS, gerar_pdf_flag=False):
    folha = {}
    contas_folha_despesa = [
        c["nome"] for c in PLANO_DE_CONTAS 
        if c["grupo"] == "Despesa" and c.get("R") and 
           ("Salário" in c["nome"] or "Provisão" in c["nome"] or "FGTS" in c["nome"])
    ]
    
    for lanc in LANCAMENTOS:
        if lanc["debito"] in contas_folha_despesa:
            folha[lanc["debito"]] = folha.get(lanc["debito"], 0) + lanc["valor"]

    total = sum(folha.values())

    linhas = ["Conta de Despesa".ljust(35) + "Valor".rjust(12)]
    linhas.append("-" * 48)
    for conta, valor in sorted(folha.items()):
        linhas.append(f"{conta:<35}{valor:>12.2f}")
    
    linhas.append("-" * 48)
    linhas.append(f"{'TOTAL FOLHA:':<35}{total:>12.2f}")

    if gerar_pdf_flag:
        gerar_pdf("folha_pagamento.pdf", "RELATÓRIO DE DESPESAS DE FOLHA", linhas)
    else:
        print("\n--- RELATÓRIO DE DESPESAS DE FOLHA DE PAGAMENTO ---")
        for linha in linhas:
            print(linha)

# --- RELATÓRIO DE IMPOSTOS (sem alterações) ---
def relatorio_impostos(PLANO_DE_CONTAS, LANCAMENTOS, gerar_pdf_flag=False):
    impostos = {}
    contas_impostos_passivo = [c['nome'] for c in PLANO_DE_CONTAS if "a Recolher" in c['nome']]

    for conta_passivo in contas_impostos_passivo:
        impostos[conta_passivo] = 0

    for lanc in LANCAMENTOS:
        if lanc["credito"] in contas_impostos_passivo:
            impostos[lanc["credito"]] += lanc["valor"]

    total = sum(impostos.values())
    
    linhas = ["Imposto a Recolher".ljust(35) + "Valor".rjust(12)]
    linhas.append("-" * 48)
    for conta, valor in sorted(impostos.items()):
        if valor > 0:
            linhas.append(f"{conta:<35}{valor:>12.2f}")
            
    linhas.append("-" * 48)
    linhas.append(f"{'TOTAL DE IMPOSTOS:':<35}{total:>12.2f}")

    if gerar_pdf_flag:
        gerar_pdf("impostos.pdf", "RELATÓRIO DE IMPOSTOS APURADOS", linhas)
    else:
        print("\n--- RELATÓRIO DE IMPOSTOS APURADOS ---")
        for linha in linhas:
            print(linha)

# --- MENU (sem alterações) ---
def menu():
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1. Balancete")
        print("2. Relatório da Folha de Pagamento")
        print("3. Relatório de Impostos Apurados")
        print("0. Sair")

        opcao = input("Escolha uma opção: ")
        
        gerar_pdf_flag = False
        if opcao in ["1", "2", "3"]:
            while True:
                tipo_saida = input("Deseja visualizar em (1) Tela ou (2) PDF? ")
                if tipo_saida == "1":
                    gerar_pdf_flag = False
                    break
                elif tipo_saida == "2":
                    gerar_pdf_flag = True
                    break
                else:
                    print("Opção de saída inválida! Escolha 1 para Tela ou 2 para PDF.")

        if opcao == "1":
            balancete(PLANO_DE_CONTAS, LANCAMENTOS, gerar_pdf_flag)
        elif opcao == "2":
            relatorio_folha(PLANO_DE_CONTAS, LANCAMENTOS, gerar_pdf_flag)
        elif opcao == "3":
            relatorio_impostos(PLANO_DE_CONTAS, LANCAMENTOS, gerar_pdf_flag)
        elif opcao == "0":
            print("Saindo do sistema...")
            break
        elif opcao not in ["1", "2", "3"]:
            print("Opção inválida!")

# --- EXECUTAR ---
if __name__ == "__main__":
    menu()