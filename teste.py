import datetime
import os
import platform
# --- COMANDO PARA INICIAR, CD para entrar na pasta onde está o arquivo.py e depois: python .\teste.py
# --- ESTRUTURA DE DADOS CENTRAL ---


PLANO_DE_CONTAS = [
    # --- ATIVOS ---
    ('1.1.01', 'Caixa', 'Ativo'),
    ('1.1.02', 'Bancos Conta Movimento', 'Ativo'),
    ('1.1.03', 'Clientes a Receber', 'Ativo'),
    ('1.1.04', 'Estoques', 'Ativo'),
    ('1.2.01', 'Imobilizado', 'Ativo'),
    ('1.2.02', 'Veículos', 'Ativo'),
    ('1.2.03', 'Depreciação Acumulada', 'Ativo'), # Natureza credora, mas fica no grupo do Ativo
    # --- PASSIVOS E PL ---
    ('2.1.01', 'Fornecedores', 'Passivo'),
    ('2.1.02', 'Salários a Pagar', 'Passivo'),
    ('2.1.03', 'INSS a Recolher', 'Passivo'),
    ('2.1.04', 'FGTS a Recolher', 'Passivo'),
    ('2.1.05', 'ICMS a Recolher', 'Passivo'),
    ('2.1.06', 'PIS a Recolher', 'Passivo'),
    ('2.1.07', 'COFINS a Recolher', 'Passivo'),
    ('2.1.08', 'Provisão 13º Salário', 'Passivo'),
    ('2.1.09', 'Provisão Férias', 'Passivo'),
    ('2.3.01', 'Capital Social', 'Patrimonio Liquido'),
    ('2.3.02', 'Lucros ou Prejuízos Acumulados', 'Patrimonio Liquido'),
    # --- RECEITAS ---
    ('3.1.01', 'Receita de Vendas de Mercadorias', 'Receita'),
    ('3.1.02', 'Receita de Serviços', 'Receita'),
    # --- CUSTOS E DESPESAS (DEDUÇÕES) ---
    ('4.1.01', 'ICMS sobre Vendas', 'Despesa'),
    ('4.1.02', 'PIS sobre Vendas', 'Despesa'),
    ('4.1.03', 'COFINS sobre Vendas', 'Despesa'),
    # --- DESPESAS OPERACIONAIS ---
    ('4.2.01', 'Despesa com Salários', 'Despesa'),
    ('4.2.02', 'Despesa com INSS', 'Despesa'),
    ('4.2.03', 'Despesa com FGTS', 'Despesa'),
    ('4.2.04', 'Despesa Provisão 13º', 'Despesa'),
    ('4.2.05', 'Despesa Provisão Férias', 'Despesa'),
    ('4.2.06', 'Despesa de Energia', 'Despesa'),
    ('4.2.07', 'Despesa de Honorários', 'Despesa'),
    ('4.2.08', 'Despesa Bancária', 'Despesa'),
    ('4.2.09', 'Despesa de Sistemas', 'Despesa'),
    ('4.2.10', 'Despesa de Combustível', 'Despesa'),
    ('4.2.11', 'Despesa de Depreciação', 'Despesa'),
    ('4.2.12', 'Despesa com Aluguel', 'Despesa'),
]

LANCAMENTOS_INICIAIS = [
    {'data': '2025-08-03', 'descricao': 'Venda de Mercadorias a prazo', 'partidas': [('Clientes a Receber', 'D', 10000.00), ('Receita de Vendas de Mercadorias', 'C', 10000.00)]},
    {'data': '2025-08-05', 'descricao': 'Compra de Estoque a Prazo', 'partidas': [('Estoques', 'D', 6000.00), ('Fornecedores', 'C', 6000.00)]},
    {'data': '2025-08-07', 'descricao': 'Pagamento de conta de energia', 'partidas': [('Despesa de Energia', 'D', 800.00), ('Caixa', 'C', 800.00)]},
    {'data': '2025-08-10', 'descricao': 'Pagamento de honorários contábeis', 'partidas': [('Despesa de Honorários', 'D', 1200.00), ('Caixa', 'C', 1200.00)]},
    {'data': '2025-08-12', 'descricao': 'Tarifas bancárias', 'partidas': [('Despesa Bancária', 'D', 150.00), ('Caixa', 'C', 150.00)]},
    {'data': '2025-08-14', 'descricao': 'Mensalidade de sistema de gestão', 'partidas': [('Despesa de Sistemas', 'D', 500.00), ('Caixa', 'C', 500.00)]},
    {'data': '2025-08-15', 'descricao': 'Abastecimento de veículo da empresa', 'partidas': [('Despesa de Combustível', 'D', 600.00), ('Caixa', 'C', 600.00)]},
    {'data': '2025-08-20', 'descricao': 'Depreciação de imobilizado do período', 'partidas': [('Despesa de Depreciação', 'D', 1000.00), ('Depreciação Acumulada', 'C', 1000.00)]},
    {'data': '2025-08-25', 'descricao': 'Folha de Pagamento João', 'partidas': [('Despesa com Salários', 'D', 5000.00), ('Salários a Pagar', 'C', 4500.00), ('INSS a Recolher', 'C', 500.00)]},
    {'data': '2025-08-25', 'descricao': 'Folha de Pagamento Maria', 'partidas': [('Despesa com Salários', 'D', 4000.00), ('Salários a Pagar', 'C', 3600.00), ('INSS a Recolher', 'C', 400.00)]},
    {'data': '2025-08-28', 'descricao': 'Provisão de 13º Salário', 'partidas': [('Despesa Provisão 13º', 'D', 1500.00), ('Provisão 13º Salário', 'C', 1500.00)]},
    {'data': '2025-08-28', 'descricao': 'Provisão de Férias', 'partidas': [('Despesa Provisão Férias', 'D', 1200.00), ('Provisão Férias', 'C', 1200.00)]},
    {'data': '2025-08-28', 'descricao': 'Apuração FGTS sobre folha', 'partidas': [('Despesa com FGTS', 'D', 880.00), ('FGTS a Recolher', 'C', 880.00)]},
    {'data': '2025-08-30', 'descricao': 'Apuração ICMS sobre Vendas', 'partidas': [('ICMS sobre Vendas', 'D', 1200.00), ('ICMS a Recolher', 'C', 1200.00)]},
    {'data': '2025-08-30', 'descricao': 'Apuração PIS sobre Vendas', 'partidas': [('PIS sobre Vendas', 'D', 200.00), ('PIS a Recolher', 'C', 200.00)]},
    {'data': '2025-08-30', 'descricao': 'Apuração COFINS sobre Vendas', 'partidas': [('COFINS sobre Vendas', 'D', 600.00), ('COFINS a Recolher', 'C', 600.00)]},
    {'data': '2025-08-01', 'descricao': 'Integralização de Capital Social Inicial', 'partidas': [('Caixa', 'D', 50000.00), ('Capital Social', 'C', 50000.00)]},
]

# Função para limpar a tela
def limpar_tela():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

class Conta:
    def __init__(self, codigo, nome, tipo):
        if tipo not in ['Ativo', 'Passivo', 'Patrimonio Liquido', 'Receita', 'Despesa']:
            raise ValueError("Tipo de conta inválido.")
        self.codigo = codigo
        self.nome = nome
        self.tipo = tipo
        self.debitos = []
        self.creditos = []

    def adicionar_debito(self, valor):
        if valor > 0: self.debitos.append(valor)

    def adicionar_credito(self, valor):
        if valor > 0: self.creditos.append(valor)

    def get_saldo(self):
        total_debitos = sum(self.debitos)
        total_creditos = sum(self.creditos)
        if self.tipo in ['Ativo', 'Despesa']:
            # Caso especial: Depreciação Acumulada tem natureza credora, mas está no ativo
            if "depreciação acumulada" in self.nome.lower():
                 saldo = total_creditos - total_debitos
                 return (0, saldo) if saldo >= 0 else (-saldo, 0)
            saldo = total_debitos - total_creditos
            return (saldo, 0) if saldo >= 0 else (0, -saldo)
        elif self.tipo in ['Passivo', 'Patrimonio Liquido', 'Receita']:
            saldo = total_creditos - total_debitos
            return (0, saldo) if saldo >= 0 else (-saldo, 0)
        return 0, 0

class Balancete:
    def __init__(self, nome_empresa):
        self.nome_empresa = nome_empresa
        self.contas = {}
        self.lancamentos = []
        self.nome_para_codigo = {}

    def adicionar_conta(self, codigo, nome, tipo):
        if codigo in self.contas:
            raise ValueError(f"O código de conta '{codigo}' já existe.")
        nova_conta = Conta(codigo, nome, tipo)
        self.contas[codigo] = nova_conta
        self.nome_para_codigo[nome] = codigo

    def fazer_lancamento(self, data, descricao, partidas):
        total_debitos = sum(valor for _, tipo, valor in partidas if tipo.upper() == 'D')
        total_creditos = sum(valor for _, tipo, valor in partidas if tipo.upper() == 'C')

        if round(total_debitos, 2) != round(total_creditos, 2):
            raise ValueError(f"Lançamento desbalanceado! Débitos ({total_debitos:.2f}) != Créditos ({total_creditos:.2f})")

        for codigo_conta, _, _ in partidas:
            if codigo_conta not in self.contas:
                raise NameError(f"O código de conta '{codigo_conta}' não existe no plano de contas.")

        for codigo_conta, tipo, valor in partidas:
            conta = self.contas[codigo_conta]
            if tipo.upper() == 'D':
                conta.adicionar_debito(valor)
            elif tipo.upper() == 'C':
                conta.adicionar_credito(valor)
        
        self.lancamentos.append({'data': data, 'descricao': descricao, 'partidas': partidas})

    def gerar_balancete(self):
        limpar_tela()
        print("\n" + "="*80)
        print(f"BALANCETE DE VERIFICAÇÃO - {self.nome_empresa}")
        print(f"Data de Emissão: {datetime.date.today().strftime('%d/%m/%Y')}")
        print("="*80)
        print(f"{'CÓDIGO':<10} | {'CONTA':<40} | {'SALDO DEVEDOR':>12} | {'SALDO CREDOR':>12}")
        print("-"*80)
        total_devedor, total_credor = 0, 0
        
        for codigo_conta in sorted(self.contas.keys()):
            conta = self.contas[codigo_conta]
            saldo_devedor, saldo_credor = conta.get_saldo()
            if saldo_devedor > 0 or saldo_credor > 0:
                print(f"{conta.codigo:<10} | {conta.nome:<40} | {saldo_devedor:12,.2f} | {saldo_credor:12,.2f}")
                total_devedor += saldo_devedor
                total_credor += saldo_credor
        print("-"*80)
        print(f"{'TOTAIS':<53} | {total_devedor:12,.2f} | {total_credor:12,.2f}")
        print("="*80)
        if round(total_devedor, 2) == round(total_credor, 2):
            print("Status: Balancete correto. Totais de débitos e créditos conferem.")
        else:
            print(f"ERRO: Balancete incorreto! Diferença de {(total_devedor - total_credor):.2f}")
        input("\nPressione Enter para continuar...")

# --- FUNÇÕES DE CARGA INICIAL ---

def carregar_plano_de_contas(balancete):
    for codigo, nome, tipo in PLANO_DE_CONTAS:
        balancete.adicionar_conta(codigo, nome, tipo)
    print("Plano de contas carregado com sucesso.")

def realizar_lancamentos_iniciais(balancete):
    try:
        for lancamento in LANCAMENTOS_INICIAIS:
            partidas_com_codigo = []
            for nome_conta, tipo, valor in lancamento['partidas']:
                codigo = balancete.nome_para_codigo.get(nome_conta)
                if not codigo:
                    raise NameError(f"Erro no lançamento inicial: A conta '{nome_conta}' não foi encontrada.")
                partidas_com_codigo.append((codigo, tipo, valor))
            
            balancete.fazer_lancamento(lancamento['data'], lancamento['descricao'], partidas_com_codigo)
        print("Lançamentos iniciais realizados com sucesso.")
    except (ValueError, NameError) as e:
        print(f"\nERRO CRÍTICO AO FAZER LANÇAMENTOS INICIAIS: {e}")
        exit()

# --- FUNÇÕES DE RELATÓRIO (REINTEGRADAS) ---

def gerar_relatorio_folha(balancete):
    limpar_tela()
    print("\n" + "="*60)
    print(f"RELATÓRIO DE DESPESAS DE FOLHA - {balancete.nome_empresa}")
    print(f"Data de Emissão: {datetime.date.today().strftime('%d/%m/%Y')}")
    print("="*60)
    print(f"{'CONTA DE DESPESA':<45} | {'VALOR (R$)'}")
    print("-"*60)
    total_despesas_folha = 0
    PALAVRAS_CHAVE = ['salários', 'inss', 'fgts', 'provisão 13', 'provisão férias']
    
    contas_folha = []
    for conta in balancete.contas.values():
        if conta.tipo == 'Despesa' and any(kw in conta.nome.lower() for kw in PALAVRAS_CHAVE):
            contas_folha.append(conta)

    if not contas_folha:
        print("Nenhuma despesa de folha de pagamento encontrada.")
    else:
        for conta in sorted(contas_folha, key=lambda c: c.codigo):
            saldo_devedor, _ = conta.get_saldo()
            if saldo_devedor > 0:
                print(f"{conta.nome:<45} | {saldo_devedor:10,.2f}")
                total_despesas_folha += saldo_devedor
    
    print("-"*60)
    print(f"{'TOTAL DE DESPESAS COM FOLHA':<45} | {total_despesas_folha:10,.2f}")
    print("="*60)
    input("\nPressione Enter para continuar...")

def gerar_relatorio_impostos(balancete):
    limpar_tela()
    print("\n" + "="*60)
    print(f"RELATÓRIO DE IMPOSTOS APURADOS - {balancete.nome_empresa}")
    print("="*60)
    print(f"{'CONTA DE IMPOSTO (PASSIVO)':<45} | {'VALOR A PAGAR (R$)'}")
    print("-"*60)
    total_impostos = 0
    PALAVRAS_CHAVE = ['a recolher', 'a pagar']

    contas_impostos = []
    for conta in balancete.contas.values():
        if conta.tipo == 'Passivo' and any(kw in conta.nome.lower() for kw in PALAVRAS_CHAVE):
            contas_impostos.append(conta)
    
    if not contas_impostos:
        print("Nenhuma conta de imposto a pagar (Passivo) encontrada.")
    else:
        for conta in sorted(contas_impostos, key=lambda c: c.codigo):
            _, saldo_credor = conta.get_saldo()
            if saldo_credor > 0:
                print(f"{conta.nome:<45} | {saldo_credor:10,.2f}")
                total_impostos += saldo_credor

    print("-"*60)
    print(f"{'TOTAL DE IMPOSTOS A PAGAR':<45} | {total_impostos:10,.2f}")
    print("="*60)
    input("\nPressione Enter para continuar...")


# --- FUNÇÕES DE INTERAÇÃO COM O USUÁRIO ---

def exibir_plano_de_contas(balancete):
    limpar_tela()
    print("\n" + "="*70)
    print("PLANO DE CONTAS")
    print("="*70)
    print(f"{'CÓDIGO':<10} | {'CONTA':<40} | {'CATEGORIA'}")
    print("-"*70)
    for codigo in sorted(balancete.contas.keys()):
        conta = balancete.contas[codigo]
        print(f"{conta.codigo:<10} | {conta.nome:<40} | {conta.tipo}")
    print("="*70)
    input("\nPressione Enter para continuar...")

def fazer_lancamento_manual(balancete):
    limpar_tela()
    print("--- Fazer Novo Lançamento ---")
    data = input(f"Data (padrão: hoje): ") or datetime.date.today().strftime('%Y-%m-%d')
    descricao = input("Descrição do lançamento: ").strip()
    
    partidas = []
    while True:
        print("\n--- Partida do Lançamento ---")
        codigo_conta = input("Código da conta (ou 'listar' para ver o plano): ").strip()
        
        if codigo_conta.lower() == 'listar':
            exibir_plano_de_contas(balancete)
            continue

        if codigo_conta not in balancete.contas:
            print(f"ERRO: Código '{codigo_conta}' inválido. Digite 'listar' para ver as opções.")
            continue
        
        print(f"Conta selecionada: {balancete.contas[codigo_conta].nome}")
        tipo = ''
        while tipo.upper() not in ['D', 'C']:
            tipo = input("Tipo (D para Débito, C para Crédito): ").strip().upper()

        valor = 0.0
        while valor <= 0:
            try:
                valor_str = input("Valor (ex: 1500.50): ").replace(',', '.')
                valor = float(valor_str)
                if valor <= 0: print("O valor deve ser positivo.")
            except ValueError:
                print("Valor inválido.")

        partidas.append((codigo_conta, tipo, valor))
        
        continuar = input("Adicionar outra partida a este lançamento? (s/n): ").strip().lower()
        if continuar != 's':
            break
    try:
        balancete.fazer_lancamento(data, descricao, partidas)
        print("\nLançamento realizado com sucesso!")
    except (ValueError, NameError) as e:
        print(f"\nERRO AO REGISTRAR LANÇAMENTO: {e}")
    input("\nPressione Enter para continuar...")

def exibir_menu():
    limpar_tela()
    print("="*42)
    print("      SISTEMA CONTÁBIL SIMPLIFICADO")
    print("="*42)
    print("1. Fazer Lançamento Manual")
    print("2. Gerar Balancete de Verificação")
    print("3. Visualizar Plano de Contas")
    print("4. Relatório de Despesas de Folha")
    print("5. Relatório de Impostos Apurados")
    print("6. Sair")
    print("="*42)

# --- PROGRAMA PRINCIPAL ---
if __name__ == "__main__":
    nome_empresa = input("Digite o nome da sua empresa: ")
    balancete = Balancete(nome_empresa)

    print("\nInicializando sistema...")
    carregar_plano_de_contas(balancete)
    realizar_lancamentos_iniciais(balancete)
    
    input("\nSistema pronto! Pressione Enter para ir ao menu principal...")

    while True:
        exibir_menu()
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            fazer_lancamento_manual(balancete)
        elif escolha == '2':
            balancete.gerar_balancete()
        elif escolha == '3':
            exibir_plano_de_contas(balancete)
        elif escolha == '4':
            gerar_relatorio_folha(balancete) # Reintegrado
        elif escolha == '5':
            gerar_relatorio_impostos(balancete) # Reintegrado
        elif escolha == '6':
            print("Saindo do sistema. Até logo!")
            break
        else:
            input("Opção inválida. Pressione Enter para tentar novamente.")
