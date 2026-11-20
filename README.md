# GeoLine

Projeto acadêmico em Python para construção e análise de retas no R² e no R³.

## Etapa atual

Esta etapa integra o backend matemático: `Vetor`, `Reta`, `RetaR2`, `RetaR3` e `Analisador`. O backend usa somente a biblioteca padrão do Python.

A interface Tkinter e o módulo de gráficos estão sendo desenvolvidos independentemente e **ainda não foram integrados** ao backend. O arquivo `main.py` é apenas um ponto de entrada inicial e imprime o nome do projeto; ele ainda não inicia uma aplicação completa.

## Requisitos

- Python 3.10 ou superior.
- Nenhuma dependência externa para executar o backend e seus testes.

## Testes automatizados

Na raiz do repositório, execute:

```bash
python -m unittest discover -s tests -v
```

## Exemplos interativos

Menus e exemplos manuais ficam fora de `tests/`, para não serem confundidos com a suíte automatizada. Execute a partir da raiz:

```bash
python executar_menu.py
python -m scripts.interativo_vetor
python -m scripts.exemplo_reta_r2
python -m scripts.interativo_analisador_r2
python -m scripts.interativo_analisador_r3
python -m scripts.exemplos_analisador
```

## Estrutura

```text
GeoLine/
├── backend/
│   ├── vetor.py
│   ├── reta.py
│   ├── reta_r2.py
│   ├── reta_r3.py
│   └── analisador.py
├── tests/                 # testes automatizados do backend
├── scripts/               # exemplos e menus interativos
│   └── menu_terminal.py   # menu integrado para testar o backend
├── interface/             # em desenvolvimento independente
├── visualizacao/          # gráficos em desenvolvimento independente
├── executar_menu.py       # execução do menu pelo terminal
├── main.py                # ponto de entrada inicial
├── requirements.txt
├── .gitignore
└── CONTRATO.md
```

Consulte [CONTRATO.md](CONTRATO.md) para o contrato entre as classes.

## Próximas etapas

Depois que os responsáveis concluírem as telas e os gráficos, esses módulos poderão ser integrados ao backend e ao fluxo principal da aplicação.
