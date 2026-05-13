# Sprint Data Science

Projeto desenvolvido para realizar um tratamento inicial em um arquivo CSV utilizando Python e Pandas.

## Objetivo

O objetivo deste projeto é ler um arquivo CSV bruto, aplicar algumas etapas básicas de limpeza e salvar uma nova versão tratada do arquivo.

O arquivo original fica na pasta `data/raw` e o arquivo tratado é salvo na pasta `data/processed`.

## O que o código faz

- Lê um arquivo CSV utilizando a biblioteca Pandas.
- Usa `latin-1` para conseguir ler caracteres especiais que podem não funcionar em UTF-8.
- Considera a vírgula como separador das colunas.
- Usa um leitor mais flexível do Pandas para lidar melhor com textos grandes no CSV.
- Ignora linhas com quantidade incorreta de colunas.
- Padroniza os nomes das colunas:
  - remove espaços;
  - transforma tudo em letras minúsculas;
  - troca espaços por underline.
- Remove linhas duplicadas.
- Remove espaços extras no início e no fim de campos de texto.
- Substitui valores vazios ou inválidos por `NA`.
- Salva o CSV tratado na pasta `data/processed`.

## Estrutura do projeto

```text
Sprint-Data_Science/
├── data/
│   ├── raw/
│   │   └── ANON_nome_transcricao.csv
│   └── processed/
│       └── csv_tratado.csv
├── csv_preprocessor.py
└── README.md