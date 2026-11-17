# GeoLine

Projeto acadêmico em Python para estudar retas no plano (R²) e no espaço (R³), suas equações e relações geométricas.

## Estado atual

O backend implementa vetores, retas genéricas, retas em R² e R³ e análise de relações entre retas. O `main.py` ainda é apenas um ponto de entrada inicial que imprime o título do projeto. A interface gráfica e a visualização estão reservadas na estrutura, mas ainda não implementadas.

## Requisitos

- Python 3.10 ou superior.
- Nenhuma dependência externa é necessária para o backend ou para os testes automatizados.
- Matplotlib será necessário quando a visualização de gráficos for implementada.
- Tkinter costuma acompanhar a instalação do Python; sua disponibilidade depende da distribuição.

## Executar a suíte automatizada

Na pasta raiz do repositório, execute:

```bash
python -m unittest discover -s tests -v
```

## Executar exemplos interativos

Os scripts com entrada pelo terminal ficam em `scripts/` e não fazem parte da descoberta automática de testes. Para iniciar um deles, a partir da raiz:

```bash
python scripts/interativo_vetor.py
python scripts/interativo_reta_r2.py
python scripts/interativo_reta_r3.py
```

Para exemplos não interativos do analisador, execute `python scripts/exemplos_analisador.py`.

## Estrutura

```text
GeoLine/
├── backend/
│   ├── vetor.py
│   ├── reta.py
│   ├── reta_r2.py
│   ├── reta_r3.py
│   └── analisador.py
├── interface/
│   └── janela.py       # ainda não implementada
├── visualizacao/
│   └── graficos.py     # ainda não implementada
├── tests/
│   ├── test_vetor.py
│   ├── test_reta_r2.py
│   ├── test_reta_r3.py
│   └── test_analisador.py
├── scripts/            # exemplos e menus interativos
├── main.py             # ponto de entrada inicial
├── requirements.txt
└── CONTRATO.md
```

## Interfaces principais

- `Vetor` aceita coordenadas do R² ou R³ e concentra operações vetoriais.
- `Reta` recebe um ponto inicial e um vetor diretor.
- `RetaR2` e `RetaR3` são criadas a partir de dois pontos `Vetor` distintos e herdam as operações comuns de `Reta`.
- `Analisador` recebe objetos `Reta` ou classes derivadas e classifica retas paralelas, coincidentes, concorrentes e, no R³, reversas.

Consulte [CONTRATO.md](CONTRATO.md) para nomes e responsabilidades acordados entre os módulos.

## Colaboração

Desenvolva em uma branch própria, execute os testes e abra um Pull Request para revisão antes da integração à `main`.
