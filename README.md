# ♟️ 7Chess - Chess Analysis API

<p align="center">
  <b>API RESTful de alta performance em Python (FastAPI) para validação de partidas de xadrez e análise tática integrada com a engine Stockfish.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.14+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Stockfish-UCI_Engine-8A2BE2?style=for-the-badge&logo=chess&logoColor=white" alt="Stockfish">
  <img src="https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge" alt="License">
</p>

---

## 🚀 Sobre o Projeto

O **7Chess** é o backend de um ecossistema abrangente de análise de xadrez. O projeto foi desenhado seguindo princípios de **Clean Architecture** e separação de responsabilidades, isolando a lógica de negócios da API e desacoplando os binários de motores de xadrez (como o Stockfish) para garantir manutenibilidade, escalabilidade e facilidade de deploy em nuvem (AWS).

---

## 🛠️ Arquitetura do Projeto

A estrutura de diretórios foi organizada para separar a interface web (API) do motor de cálculo de xadrez:

```text
7Chess/
│
├── API/                   # Camada de Apresentação e Regras de Negócio
│   ├── routers/           # Endpoints da API (ex: /partidas/analisar)
│   ├── services/          # Lógica de integração com a engine e validações PGN
│   ├── models/            # Modelos de dados e validação (Pydantic)
│   └── main.py            # Ponto de entrada da aplicação FastAPI
│
├── engine/                # Camada de Binários da Engine
│   └── stockfish.exe      # Executável do Stockfish (suporte UCI)
│
├── venv/                  # Ambiente virtual Python (ignorado pelo Git)
├── .gitignore             # Configuração de exclusão de ficheiros temporários
└── README.md              # Documentação oficial do projeto