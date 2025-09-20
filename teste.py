import tkinter as tk
from tkinter import ttk, messagebox, Toplevel, Text, Scrollbar
import json
import os
import datetime
import locale

# --- CONFIGURAÇÃO DE LOCALIDADE PARA FORMATO DE MOEDA BRASILEIRO ---
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')
    except locale.Error:
        print("Aviso: Localidade pt_BR não encontrada. A formatação de moeda pode não funcionar como esperado.")


# ==============================================================================
# --- LÓGICA DE NEGÓCIO E DADOS ---
# ==============================================================================

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
    {"nome": "Despesa de Salário", "grupo": "Despesa", "R": True},
    {"nome": "Despesa Provisão 13º", "grupo": "Despesa", "R": True},
    {"nome": "Despesa Provisão Férias", "grupo": "Despesa", "R": True},
    {"nome": "Despesa FGTS", "grupo": "Despesa", "R": True},
    {"nome": "ICMS sobre Vendas", "grupo": "Despesa", "R": True},
    {"nome": "PIS sobre Vendas", "grupo": "Despesa", "R": True},
    {"nome": "COFINS sobre Vendas", "grupo": "Despesa", "R": True},
]

def gerar_pdf(nome_arquivo, titulo, linhas):
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import cm
    
    c = canvas.Canvas(nome_arquivo, pagesize=A4)
    largura, altura = A4
    margem = 2 * cm
    y = altura - margem
    
    data_geracao = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    c.setFont("Courier-Bold", 14)
    c.drawCentredString(largura / 2.0, y, titulo)
    c.setFont("Courier", 8)
    c.drawCentredString(largura / 2.0, y - 20, f"Gerado em: {data_geracao}")
    y -= 1.5 * cm
    
    c.setFont("Courier", 10)
    for linha in linhas:
        c.drawString(margem, y, linha)
        y -= 0.7 * cm
        if y < margem:
            c.showPage()
            c.setFont("Courier", 10)
            y = altura - margem
    c.save()

def get_balancete(plano_de_contas, lancamentos):
    saldos = {c["nome"]: 0 for c in plano_de_contas}
    for lanc in lancamentos:
        saldos[lanc["debito"]] += lanc["valor"]
        saldos[lanc["credito"]] -= lanc["valor"]
    total_debitos = total_creditos = 0
    linhas = ["Conta".ljust(35) + "Débito".rjust(12) + "Crédito".rjust(12), "-" * 60]
    for conta, saldo in sorted(saldos.items()):
        if saldo > 0:
            linhas.append(f"{conta:<35}{saldo:>12.2f}{'' :>12}")
            total_debitos += saldo
        elif saldo < 0:
            linhas.append(f"{conta:<35}{'' :>12}{-saldo:>12.2f}")
            total_creditos += -saldo
    linhas.extend(["-" * 60, f"{'TOTAL:':<35}{total_debitos:>12.2f}{total_creditos:>12.2f}"])
    return linhas

def get_relatorio_folha(plano_de_contas, lancamentos):
    folha = {}
    contas_folha_despesa = [
        c["nome"] for c in plano_de_contas
        if c["grupo"] == "Despesa" and c.get("R") and
           ("Salário" in c["nome"] or "Provisão" in c["nome"] or "FGTS" in c["nome"])
    ]
    for lanc in lancamentos:
        if lanc["debito"] in contas_folha_despesa:
            folha[lanc["debito"]] = folha.get(lanc["debito"], 0) + lanc["valor"]
    total = sum(folha.values())
    linhas = ["Conta de Despesa".ljust(35) + "Valor".rjust(12), "-" * 48]
    for conta, valor in sorted(folha.items()):
        linhas.append(f"{conta:<35}{valor:>12.2f}")
    linhas.extend(["-" * 48, f"{'TOTAL FOLHA:':<35}{total:>12.2f}"])
    return linhas

def get_relatorio_impostos(plano_de_contas, lancamentos):
    impostos = {}
    contas_impostos_passivo = [c['nome'] for c in plano_de_contas if "a Recolher" in c['nome']]
    for conta_passivo in contas_impostos_passivo:
        impostos[conta_passivo] = 0
    for lanc in lancamentos:
        if lanc["credito"] in contas_impostos_passivo:
            impostos[lanc["credito"]] += lanc["valor"]
    total = sum(impostos.values())
    linhas = ["Imposto a Recolher".ljust(35) + "Valor".rjust(12), "-" * 48]
    for conta, valor in sorted(impostos.items()):
        if valor > 0:
            linhas.append(f"{conta:<35}{valor:>12.2f}")
    linhas.extend(["-" * 48, f"{'TOTAL DE IMPOSTOS:':<35}{total:>12.2f}"])
    return linhas

# ==============================================================================
# --- CAMADA DE INTERFACE GRÁFICA (Tkinter) APRIMORADA ---
# ==============================================================================

class ContabilidadeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Contábil Simplificado")
        self.root.geometry("900x600")
        
        # --- APLICAÇÃO DE ESTILO E TEMA ---
        self.style = ttk.Style(self.root)
        self.available_themes = self.style.theme_names()
        self.style.theme_use(self.available_themes[0] if self.available_themes else "default")

        self.ARQUIVO_DADOS = "dados_contabeis.json"
        self.plano_de_contas = PLANO_DE_CONTAS
        self.nomes_contas = sorted([c['nome'] for c in self.plano_de_contas])
        self.lancamentos = self.carregar_dados()

        # --- Layout da Janela Principal ---
        frame_superior = ttk.Frame(self.root, padding="10")
        frame_superior.pack(side="top", fill="x")
        
        # Botões de Ação
        ttk.Button(frame_superior, text="Adicionar Lançamento", command=self.abrir_janela_lancamento).pack(side="left", padx=5)
        ttk.Button(frame_superior, text="Deletar Selecionado", command=self.deletar_lancamento).pack(side="left", padx=5)
        
        # Menu de Temas
        ttk.Label(frame_superior, text="Tema:").pack(side="left", padx=(20, 5))
        self.theme_combobox = ttk.Combobox(frame_superior, values=self.available_themes, state="readonly")
        self.theme_combobox.set(self.style.theme_use())
        self.theme_combobox.bind("<<ComboboxSelected>>", self.mudar_tema)
        self.theme_combobox.pack(side="left")

        # Frame para os botões de relatório
        frame_relatorios = ttk.Frame(self.root, padding="10")
        frame_relatorios.pack(side="top", fill="x")
        ttk.Button(frame_relatorios, text="Gerar Balancete", command=self.gerar_relatorio_balancete).pack(side="left", padx=5)
        ttk.Button(frame_relatorios, text="Gerar Rel. Folha", command=self.gerar_relatorio_folha).pack(side="left", padx=5)
        ttk.Button(frame_relatorios, text="Gerar Rel. Impostos", command=self.gerar_relatorio_impostos).pack(side="left", padx=5)

        # Frame para a lista de lançamentos (Treeview)
        frame_lista = ttk.Frame(self.root, padding="10")
        frame_lista.pack(expand=True, fill="both")
        ttk.Label(frame_lista, text="Lançamentos Contábeis (Duplo-clique para editar)", font=("Helvetica", 12, "bold")).pack(anchor="w")
        
        cols = ("Data", "Débito", "Crédito", "Valor")
        self.tree = ttk.Treeview(frame_lista, columns=cols, show='headings', selectmode="browse")
        
        for col in cols:
            self.tree.heading(col, text=col)
        self.tree.column('Data', width=100, anchor='center')
        self.tree.column('Valor', width=150, anchor='e') # Alinhamento à direita
        
        self.tree.pack(side="left", expand=True, fill="both")

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
        self.tree.bind("<Double-1>", self.editar_lancamento_selecionado)

        self.atualizar_lista_lancamentos()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def mudar_tema(self, event=None):
        selected_theme = self.theme_combobox.get()
        self.style.theme_use(selected_theme)

    def carregar_dados(self):
        if os.path.exists(self.ARQUIVO_DADOS):
            try:
                with open(self.ARQUIVO_DADOS, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if not content: return []
                    return json.loads(content)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        else:
            return []

    def salvar_dados(self):
        try:
            with open(self.ARQUIVO_DADOS, 'w', encoding='utf-8') as f:
                json.dump(self.lancamentos, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Erro ao Salvar", f"Não foi possível salvar os dados.\nErro: {e}")

    def on_closing(self):
        if messagebox.askokcancel("Sair", "Deseja salvar os lançamentos e sair do sistema?"):
            self.salvar_dados()
            self.root.destroy()
    
    def atualizar_lista_lancamentos(self):
        # Ordena os lançamentos por data antes de exibir
        self.lancamentos.sort(key=lambda x: datetime.datetime.strptime(x['data'], '%d/%m/%Y'))
        for i in self.tree.get_children():
            self.tree.delete(i)
        for i, lanc in enumerate(self.lancamentos):
            valor_formatado = locale.currency(lanc['valor'], grouping=True)
            # Usando o índice (i) como ID do item no Treeview
            self.tree.insert("", "end", iid=i, values=(lanc['data'], lanc['debito'], lanc['credito'], valor_formatado))

    def abrir_janela_lancamento(self, lancamento_existente=None, index=None):
        janela_lancamento = Toplevel(self.root)
        janela_lancamento.title("Editar Lançamento" if lancamento_existente else "Novo Lançamento")

        frame = ttk.Frame(janela_lancamento, padding="20")
        frame.pack(expand=True, fill="both")
        
        # Data
        ttk.Label(frame, text="Data (DD/MM/AAAA):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        entry_data = ttk.Entry(frame)
        entry_data.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Débito
        ttk.Label(frame, text="Conta a Debitar:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        combo_debito = ttk.Combobox(frame, values=self.nomes_contas, state="readonly")
        combo_debito.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Crédito
        ttk.Label(frame, text="Conta a Creditar:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        combo_credito = ttk.Combobox(frame, values=self.nomes_contas, state="readonly")
        combo_credito.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Valor
        ttk.Label(frame, text="Valor (R$):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        entry_valor = ttk.Entry(frame)
        entry_valor.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Preenche os campos se estiver editando
        if lancamento_existente:
            entry_data.insert(0, lancamento_existente['data'])
            combo_debito.set(lancamento_existente['debito'])
            combo_credito.set(lancamento_existente['credito'])
            entry_valor.insert(0, str(lancamento_existente['valor']).replace('.', ','))

        # Função de salvamento (aninhada para ter acesso aos widgets da janela)
        def salvar():
            data_str = entry_data.get()
            debito = combo_debito.get()
            credito = combo_credito.get()
            valor_str = entry_valor.get()

            # Validações
            if not all([data_str, debito, credito, valor_str]):
                messagebox.showwarning("Campos Vazios", "Todos os campos devem ser preenchidos.", parent=janela_lancamento)
                return
            try:
                datetime.datetime.strptime(data_str, '%d/%m/%Y')
            except ValueError:
                messagebox.showwarning("Data Inválida", "Formato de data inválido. Use DD/MM/AAAA.", parent=janela_lancamento)
                return
            if debito == credito:
                messagebox.showwarning("Contas Iguais", "A conta de débito não pode ser igual à de crédito.", parent=janela_lancamento)
                return
            try:
                valor = float(valor_str.replace(",", "."))
                if valor <= 0: raise ValueError
            except ValueError:
                messagebox.showwarning("Valor Inválido", "O valor deve ser um número positivo.", parent=janela_lancamento)
                return

            novo_lancamento = {"data": data_str, "debito": debito, "credito": credito, "valor": valor}
            
            if index is not None: # Se é uma edição
                self.lancamentos[index] = novo_lancamento
            else: # Se é um novo lançamento
                self.lancamentos.append(novo_lancamento)
            
            self.atualizar_lista_lancamentos()
            messagebox.showinfo("Sucesso", "Lançamento salvo com sucesso!", parent=janela_lancamento)
            janela_lancamento.destroy()

        ttk.Button(frame, text="Salvar", command=salvar).grid(row=4, column=0, columnspan=2, pady=10)
        frame.columnconfigure(1, weight=1)

    def editar_lancamento_selecionado(self, event):
        selected_item = self.tree.focus()
        if not selected_item:
            return
        
        index = int(selected_item) # O ID do item é o seu índice na lista
        lancamento = self.lancamentos[index]
        self.abrir_janela_lancamento(lancamento, index)

    def deletar_lancamento(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Nenhum Lançamento", "Por favor, selecione um lançamento na lista para deletar.")
            return

        if messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja deletar o lançamento selecionado?"):
            index = int(selected_item)
            del self.lancamentos[index]
            self.atualizar_lista_lancamentos()
            messagebox.showinfo("Sucesso", "Lançamento deletado com sucesso.")

    # Funções de gerar relatório
    def _gerar_relatorio(self, get_linhas_func, titulo, nome_arquivo):
        if not self.lancamentos:
            messagebox.showwarning("Sem Dados", "Não há lançamentos para gerar o relatório.")
            return
        if messagebox.askyesno("Formato de Saída", f"Deseja gerar o relatório '{titulo}' em PDF?"):
            linhas = get_linhas_func(self.plano_de_contas, self.lancamentos)
            try:
                gerar_pdf(nome_arquivo, titulo, linhas)
                messagebox.showinfo("PDF Gerado", f"O arquivo '{nome_arquivo}' foi gerado com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro ao Gerar PDF", f"Não foi possível gerar o arquivo.\nErro: {e}")
        else:
            linhas = get_linhas_func(self.plano_de_contas, self.lancamentos)
            self.exibir_relatorio_em_janela(titulo, linhas)

    def gerar_relatorio_balancete(self): self._gerar_relatorio(get_balancete, "BALANCETE", "balancete.pdf")
    def gerar_relatorio_folha(self): self._gerar_relatorio(get_relatorio_folha, "RELATÓRIO DE DESPESAS DE FOLHA", "folha_pagamento.pdf")
    def gerar_relatorio_impostos(self): self._gerar_relatorio(get_relatorio_impostos, "RELATÓRIO DE IMPOSTOS APURADOS", "impostos.pdf")

    def exibir_relatorio_em_janela(self, titulo, linhas):
        janela_relatorio = Toplevel(self.root)
        janela_relatorio.title(titulo)
        text_area = Text(janela_relatorio, wrap="none", font=("Courier", 10))
        scrollbar_y = Scrollbar(janela_relatorio, orient="vertical", command=text_area.yview)
        scrollbar_x = Scrollbar(janela_relatorio, orient="horizontal", command=text_area.xview)
        text_area.config(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        text_area.pack(expand=True, fill="both")
        conteudo = "\n".join(linhas)
        text_area.insert("1.0", conteudo)
        text_area.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = ContabilidadeApp(root)
    root.mainloop()