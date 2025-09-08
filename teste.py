import datetime
import os
import platform

# Função para limpar a tela do console para uma melhor experiência
def limpar_tela():
    """Limpa a tela do terminal."""
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

class Conta:
    
    """Representa uma conta contábil. (Sem alterações da versão anterior)"""
    def __init__(self, nome, tipo):
        if tipo not in ['Ativo', 'Passivo', 'Patrimonio Liquido', 'Receita', 'Despesa']:
            raise ValueError("Tipo de conta inválido. Use 'Ativo', 'Passivo', 'Patrimonio Liquido', 'Receita' ou 'Despesa'.")
        
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
            saldo = total_debitos - total_creditos
            return (saldo, 0) if saldo >= 0 else (0, -saldo)
        elif self.tipo in ['Passivo', 'Patrimonio Liquido', 'Receita']:
            saldo = total_creditos - total_debitos
            return (0, saldo) if saldo >= 0 else (-saldo, 0)
        return 0, 0

class Balancete:
    """Gerencia o conjunto de contas e lançamentos contábeis. (Sem alterações da versão anterior)"""
    def __init__(self, nome_empresa):
        self.nome_empresa = nome_empresa
        self.contas = {}
        self.lancamentos = []

    def adicionar_conta(self, nome, tipo):
        if nome in self.contas:
            raise ValueError(f"A conta '{nome}' já existe.")
        nova_conta = Conta(nome, tipo)
        self.contas[nome] = nova_conta

    def fazer_lancamento(self, data, descricao, partidas):
        total_debitos = sum(valor for _, tipo, valor in partidas if tipo.upper() == 'D')
        total_creditos = sum(valor for _, tipo, valor in partidas if tipo.upper() == 'C')

        if round(total_debitos, 2) != round(total_creditos, 2):
            raise ValueError(f"Lançamento desbalanceado! Débitos ({total_debitos:.2f}) != Créditos ({total_creditos:.2f})")

        for nome_conta, _, _ in partidas:
            if nome_conta not in self.contas:
                raise NameError(f"A conta '{nome_conta}' não existe no plano de contas.")

        for nome_conta, tipo, valor in partidas:
            conta = self.contas[nome_conta]
            if tipo.upper() == 'D':
                conta.adicionar_debito(valor)
            elif tipo.upper() == 'C':
                conta.adicionar_credito(valor)
        
        self.lancamentos.append({'data': data, 'descricao': descricao, 'partidas': partidas})

    def gerar_balancete(self):
        limpar_tela()
        print("\n" + "="*60)
        print(f"BALANCETE DE VERIFICAÇÃO - {self.nome_empresa}")
        print(f"Data de Emissão: {datetime.date.today().strftime('%d/%m/%Y')}")
        print("="*60)
        print(f"{'CONTA':<30} | {'SALDO DEVEDOR':>12} | {'SALDO CREDOR':>12}")
        print("-"*60)
        total_devedor, total_credor = 0, 0
        for nome_conta in sorted(self.contas.keys()):
            conta = self.contas[nome_conta]
            saldo_devedor, saldo_credor = conta.get_saldo()
            if saldo_devedor > 0 or saldo_credor > 0:
                print(f"{nome_conta:<30} | {saldo_devedor:12,.2f} | {saldo_credor:12,.2f}")
                total_devedor += saldo_devedor
                total_credor += saldo_credor
        print("-"*60)
        print(f"{'TOTAIS':<30} | {total_devedor:12,.2f} | {total_credor:12,.2f}")
        print("="*60)
        if round(total_devedor, 2) == round(total_credor, 2):
            print("Status: Balancete correto. Totais de débitos e créditos conferem.")
        else:
            print("ERRO: Balancete incorreto! Os totais de débitos e créditos não conferem.")
        input("\nPressione Enter para continuar...")


# --- Funções para Interação com o Usuário ---

def adicionar_conta_manual(balancete):
    """Função para guiar o usuário na adição de uma nova conta."""
    limpar_tela()
    print("--- Adicionar Nova Conta ---")
    try:
        nome = input("Nome da nova conta: ").strip()
        if not nome:
            print("O nome da conta não pode ser vazio.")
            return

        print("\nTipos de conta disponíveis:")
        tipos = ['Ativo', 'Passivo', 'Patrimonio Liquido', 'Receita', 'Despesa']
        for i, tipo in enumerate(tipos, 1):
            print(f"{i}. {tipo}")
        
        while True:
            escolha = input("Escolha o número do tipo da conta: ")
            if escolha.isdigit() and 1 <= int(escolha) <= len(tipos):
                tipo_escolhido = tipos[int(escolha) - 1]
                break
            else:
                print("Escolha inválida. Tente novamente.")
        
        balancete.adicionar_conta(nome, tipo_escolhido)
        print(f"\nConta '{nome}' ({tipo_escolhido}) adicionada com sucesso!")
    except (ValueError, NameError) as e:
        print(f"\nErro: {e}")
    input("\nPressione Enter para continuar...")

def fazer_lancamento_manual(balancete):
    """Função para guiar o usuário na criação de um novo lançamento."""
    limpar_tela()
    print("--- Fazer Novo Lançamento ---")
    data = input(f"Data do lançamento (padrão: {datetime.date.today().strftime('%Y-%m-%d')}): ") or datetime.date.today().strftime('%Y-%m-%d')
    descricao = input("Descrição do lançamento: ").strip()
    
    partidas = []
    while True:
        print("\n--- Partida do Lançamento ---")
        
        print("Contas disponíveis:", ", ".join(balancete.contas.keys()))
        nome_conta = input("Nome da conta para esta partida: ").strip()
        if nome_conta not in balancete.contas:
            print("ERRO: Conta inválida. Por favor, escolha uma da lista ou adicione a conta primeiro.")
            continue
            
        tipo = ''
        while tipo.upper() not in ['D', 'C']:
            tipo = input("Tipo (D para Débito, C para Crédito): ").strip().upper()

        valor = 0.0
        while valor <= 0:
            try:
                valor = float(input("Valor (use ponto para decimais, ex: 1500.50): "))
                if valor <= 0: print("O valor deve ser positivo.")
            except ValueError:
                print("Valor inválido. Por favor, insira um número.")

        partidas.append((nome_conta, tipo, valor))
        
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
    """Mostra o menu principal de opções."""
    limpar_tela()
    print("="*30)
    print("   SISTEMA DE BALANCETE")
    print("="*30)
    print("1. Adicionar Conta")
    print("2. Fazer Lançamento Contábil")
    print("3. Gerar Balancete de Verificação")
    print("4. Sair")
    print("="*30)

# --- Programa Principal ---
if __name__ == "__main__":
    nome_empresa = input("Digite o nome da sua empresa: ")
    balancete = Balancete(nome_empresa)

    # Carga inicial de contas para facilitar
    print("\nCarregando um plano de contas básico...")
    try:
        contas_iniciais = [
            ("Caixa", "Ativo"), ("Contas a Receber", "Ativo"),
            ("Fornecedores", "Passivo"), ("Impostos a Pagar", "Passivo"),
            ("Capital Social", "Patrimonio Liquido"), ("Receita de Serviços", "Receita"),
            ("Despesa com Salários", "Despesa"), ("Despesa de Aluguel", "Despesa")
        ]
        for nome, tipo in contas_iniciais:
            balancete.adicionar_conta(nome, tipo)
    except ValueError:
        pass # Ignora erros se as contas já existirem
    print("Plano de contas básico carregado.")
    input("Pressione Enter para iniciar...")

    while True:
        exibir_menu()
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            adicionar_conta_manual(balancete)
        elif escolha == '2':
            fazer_lancamento_manual(balancete)
        elif escolha == '3':
            balancete.gerar_balancete()
        elif escolha == '4':
            print("Saindo do sistema. Até logo!")
            break
        else:
            input("Opção inválida. Pressione Enter para tentar novamente.")