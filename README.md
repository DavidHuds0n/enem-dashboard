# ENEM 2023 — Dashboard Interativo

Dashboard web interativo para análise dos microdados do ENEM 2023,
construído com Streamlit e Plotly. Permite explorar dados de
**127.574 participantes** através de filtros dinâmicos e múltiplas
visões analíticas.

## 🔗 Demo

> Adicione aqui o link do Streamlit Cloud após o deploy

## 🎯 Funcionalidades

- Filtros simultâneos por região, tipo de escola, acesso à internet e gênero
- Indicadores em tempo real que atualizam conforme os filtros
- 4 abas temáticas de análise:
  - **Desempenho Regional** — comparativo de notas médias por região
  - **Perfil Escolar** — pública vs privada em Matemática e distribuição geral
  - **Fator Socioeconômico** — impacto da renda, internet e gênero
  - **Correlações Analíticas** — matriz de correlação entre áreas e densidade Matemática vs Redação

## 📂 Fonte de Dados

Dataset **Student Performance — ENEM 2023** disponível no Kaggle:  
[Kaggle - Student Performance (ENEM 2023)](https://www.kaggle.com/datasets/jpamcb/student-performance/data)

## 🛠️ Tecnologias

- Python 3.12+
- Streamlit — framework web
- Plotly Express — gráficos interativos
- Pandas — manipulação de dados
- SQLite3 — banco de dados

## ▶️ Como Rodar Localmente

```bash
# 1. Clone o repositório
git clone https://github.com/DavidHuds0n/enem-dashboard.git
cd enem-dashboard

# 2. Crie e ative o ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Adicione o banco de dados
# Coloque o arquivo enem.db dentro da pasta data/
# O banco pode ser gerado pelo projeto: github.com/DavidHuds0n/enem-banco-de-dados

# 5. Rode o dashboard
streamlit run app.py
```

## 📁 Estrutura
```
enem-dashboard/
├── data/
│   └── enem.db        # Banco SQLite (não incluído — ver instruções acima)
├── app.py             # Aplicação principal
├── requirements.txt
└── README.md
```

---
Desenvolvido por [David Hudson](https://github.com/DavidHuds0n)  
Projeto parte do repositório de estudos em Ciência de Dados e Desenvolvimento Web.