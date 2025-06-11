# 📦 web_csv_relatorio

**Web CSV Relatório** é um script em Python que coleta dados via web scraping (por exemplo, preços ou informações de produtos de um site) e gera automaticamente um arquivo `.csv` contendo essas informações. Ideal para monitoramento, extração de dados e geração rápida de relatórios.

---

## 🛠️ Tecnologias

- Python 3.x  
- Bibliotecas utilizadas:
  - `requests`
  - `beautifulsoup4`
  - `selenium` *(opcional, se usar lógica com navegador)*
  - `pandas`

---

## 📁 Estrutura

```
web_csv_relatorio/
├── coletor_de_precos.py       # Script principal para coleta e exportação CSV
├── produtos_kabum.csv         # Exemplo de resultado gerado após execução
├── requirements.txt           # Dependências do projeto
└── README.md                  # Documentação do projeto
```

---

## 🚀 Como usar

1. Clone o repositório:

```bash
git clone https://github.com/eukevinbruno/web_csv_relatorio.git
cd web_csv_relatorio
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Execute o script:

```bash
python coletor_de_precos.py
```

4. O script criará automaticamente o arquivo `produtos_kabum.csv`.

---

## 📊 Funcionalidades

- Configuração de cabeçalhos (User-Agent) para evitar bloqueios HTTP 403.
- Extração de dados via `BeautifulSoup` ou `Selenium`.
- Organização dos dados em um arquivo CSV.
- Tratamento básico de dados ausentes.

---

## 🔄 Melhorias futuras

- Implementar paginação automática para captar todas as páginas do site.
- Adicionar dados como link do produto, disponibilidade, avaliação, etc.
- Suporte a múltiplos sites além do Kabum.
- Exportação opcional para `.xlsx` ou banco de dados.

---

## ✍️ Autor

**Kevin Bruno** ([@eukevinbruno](https://github.com/eukevinbruno))  
Feito com excelência e foco na clareza de código e documentação.

---

## ⚠️ Legal

Projetado para fins educativos. Verifique os Termos de Uso do site alvo antes de coletar dados.
