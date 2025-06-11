# Arquivo: processador.py
# -*- coding: utf-8 -*-

import pandas as pd
from fpdf import FPDF
import time

# --- Configurações de Validação ---
LISTA_STATUS_SUCESSO = ['aprovado', 'pagos', 'confirmado']

# --- Configurações de Estilo do PDF ---
COR_AZUL_ESCURO = (28, 40, 51); COR_CINZA_TEXTO = (85, 96, 108); COR_CINZA_FUNDO_CABECALHO = (236, 240, 241); COR_LINHA_ZEBRA = (247, 249, 249); COR_BRANCO = (255, 255, 255)

class RelatorioPDF(FPDF):
    def header(self):
        self.set_fill_color(*COR_AZUL_ESCURO); self.rect(10, 8, 12, 12, 'F'); self.set_font('Arial', 'B', 12); self.set_text_color(*COR_BRANCO); self.text(12.5, 17, 'KB'); self.set_font('Arial', 'B', 18); self.set_text_color(*COR_AZUL_ESCURO); self.cell(0, 10, 'Relatório de Vendas', 0, 0, 'C'); self.set_font('Arial', '', 10); self.set_text_color(*COR_CINZA_TEXTO); data_atual = time.strftime("%d/%m/%Y"); self.cell(0, 10, f'Gerado em: {data_atual}', 0, 1, 'R'); self.set_line_width(0.5); self.set_draw_color(*COR_CINZA_FUNDO_CABECALHO); self.line(10, 28, 200, 28); self.ln(25)
    def footer(self):
        self.set_y(-15); self.set_font('Arial', 'I', 8); self.set_text_color(*COR_CINZA_TEXTO); self.cell(0, 10, f'Página {self.page_no()}/{{nb}}', 0, 0, 'C')
    def gerar_secao_resumo(self, dados_processados):
        self.set_font('Arial', 'B', 14); self.set_text_color(*COR_AZUL_ESCURO); self.cell(0, 10, 'Resumo Geral de Performance', 0, 1, 'L'); self.ln(5); faturamento_formatado = f"R$ {dados_processados['faturamento_total']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'); quantidade_formatada = int(dados_processados['quantidade_total_produtos_aprovados']); self.set_font('Arial', '', 12); self.set_text_color(*COR_CINZA_TEXTO); self.cell(0, 8, f"Faturamento Total (todos os status): {faturamento_formatado}", 0, 1, 'L'); self.cell(0, 8, f"Total de Produtos Vendidos (Status de Sucesso): {quantidade_formatada} unidades", 0, 1, 'L'); self.ln(15)
    def gerar_tabela_vendas(self, dataframe_vendas):
        self.set_font('Arial', 'B', 14); self.set_text_color(*COR_AZUL_ESCURO); self.cell(0, 10, 'Detalhes das Vendas Aprovadas', 0, 1, 'L'); self.ln(5); self.set_font('Arial', 'B', 10); self.set_fill_color(*COR_CINZA_FUNDO_CABECALHO); self.set_text_color(*COR_AZUL_ESCURO); self.set_line_width(0.3); larguras = [85, 25, 40, 40]; cabecalho = ['Produto', 'Qtd.', 'Valor Unitário', 'Total Venda'];
        for i, item_cabecalho in enumerate(cabecalho): self.cell(larguras[i], 10, item_cabecalho, 1, 0, 'C', fill=True)
        self.ln(); self.set_font('Arial', '', 10); self.set_text_color(*COR_CINZA_TEXTO); preencher_linha = False
        for _, linha in dataframe_vendas.iterrows():
            self.set_fill_color(*COR_LINHA_ZEBRA) if preencher_linha else self.set_fill_color(*COR_BRANCO); nome_produto = str(linha['Nome_Produto']).encode('latin-1', 'replace').decode('latin-1'); quantidade = str(int(linha['Quantidade_Vendida'])); valor_unitario = f"R$ {linha['Valor_Unitario']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'); total_venda = f"R$ {linha['Total_Venda']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'); self.cell(larguras[0], 10, nome_produto, 'LR', 0, 'L', fill=preencher_linha); self.cell(larguras[1], 10, quantidade, 'LR', 0, 'C', fill=preencher_linha); self.cell(larguras[2], 10, valor_unitario, 'LR', 0, 'R', fill=preencher_linha); self.cell(larguras[3], 10, total_venda, 'LR', 1, 'R', fill=preencher_linha); preencher_linha = not preencher_linha
        self.cell(sum(larguras), 0, '', 'T')

def executar_analise_completa(caminho_arquivo_csv, pasta_saida):
    """
    Função principal que orquestra todo o processo: carregar, limpar, processar e gerar o PDF.
    """
    try:
        # Carregar
        df_bruto = pd.read_csv(caminho_arquivo_csv, encoding='utf-8', sep=',', quotechar='"', skip_blank_lines=True, skipinitialspace=True)
        
        # Limpar
        df_bruto.columns = df_bruto.columns.str.strip()
        df_bruto.drop_duplicates(inplace=True)
        for coluna in df_bruto.select_dtypes(['object']).columns: df_bruto[coluna] = df_bruto[coluna].str.strip()
        df_bruto['Valor_Unitario'] = df_bruto['Valor_Unitario'].astype(str).str.replace('R$', '', regex=False).str.replace('.', '', regex=False).str.replace(',', '.', regex=False).str.strip()
        for coluna in ['Valor_Unitario', 'Quantidade_Vendida']: df_bruto[coluna] = pd.to_numeric(df_bruto[coluna], errors='coerce')
        df_bruto.fillna(0, inplace=True)
        df_bruto['Status_Pagamento'] = df_bruto['Status_Pagamento'].str.lower()

        # Processar
        df_bruto['Total_Venda'] = df_bruto['Quantidade_Vendida'] * df_bruto['Valor_Unitario']
        faturamento_total = df_bruto['Total_Venda'].sum()
        vendas_sucesso = df_bruto[df_bruto['Status_Pagamento'].isin(LISTA_STATUS_SUCESSO)].copy()
        qtd_produtos_sucesso = vendas_sucesso['Quantidade_Vendida'].sum()
        
        dados_processados = {'faturamento_total': faturamento_total, 'vendas_aprovadas': vendas_sucesso, 'quantidade_total_produtos_aprovados': qtd_produtos_sucesso}

        # Gerar PDF
        pdf = RelatorioPDF('P', 'mm', 'A4')
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.gerar_secao_resumo(dados_processados)
        pdf.gerar_tabela_vendas(dados_processados['vendas_aprovadas'])
        
        nome_arquivo_pdf = f"Relatorio_{time.strftime('%Y%m%d_%H%M%S')}.pdf"
        caminho_completo_pdf = f"{pasta_saida}/{nome_arquivo_pdf}"
        pdf.output(caminho_completo_pdf)
        
        # Retornar os resultados para a aplicação web
        return {
            "sucesso": True,
            "resumo": {
                'faturamento_total_fmt': f"R$ {dados_processados['faturamento_total']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
                'quantidade_total_produtos_aprovados': int(dados_processados['quantidade_total_produtos_aprovados'])
            },
            "nome_arquivo_pdf": nome_arquivo_pdf
        }
    except Exception as e:
        return {"sucesso": False, "erro": str(e)}