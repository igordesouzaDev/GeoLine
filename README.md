# GeoLine

Projeto acadêmico em Python para construção e análise de retas no R² e no R³.

## Aplicação

O projeto reúne o backend matemático (`Vetor`, `Reta`, `RetaR2`, `RetaR3` e `Analisador`), uma interface Tkinter e gráficos Matplotlib. A aplicação permite construir retas no R² e R³, analisar a relação entre duas retas e exibir gráficos 2D/3D.

## Instalação e execução

Requer Python 3.10 ou superior. Na raiz do repositório, instale a dependência visual e inicie a aplicação:

```bash
python -m pip install -r requirements.txt
python main.py
```

## Requisitos

- Python 3.10 ou superior.
- Matplotlib para os gráficos e sua incorporação à interface. O backend matemático continua usando apenas a biblioteca padrão.

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
├── interface/             # janela e telas Tkinter
├── visualizacao/           # geração de figuras Matplotlib
├── executar_menu.py       # execução do menu pelo terminal
├── main.py                # inicializa a interface gráfica
├── requirements.txt
├── .gitignore
└── CONTRATO.md
```

Consulte [CONTRATO.md](CONTRATO.md) para o contrato entre as classes.

## Observações

Os testes automatizados do backend continuam independentes da interface. Os gráficos são criados como figuras Matplotlib e exibidos dentro da janela principal.
