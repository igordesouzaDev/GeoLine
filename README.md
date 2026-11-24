# GeoLine

GeoLine é um projeto acadêmico em Python para construir, representar e analisar retas no plano (R²) e no espaço (R³). O projeto oferece uma aplicação desktop com Tkinter, gráficos com Matplotlib, um menu de demonstração pelo terminal e um notebook interativo para Google Colab.

## Funcionalidades

- Construir retas no R² e R³ a partir de dois pontos.
- Exibir equações vetoriais, paramétricas e simétricas; no R², também exibir a equação reduzida.
- Verificar se um ponto pertence a uma reta.
- Analisar relações entre duas retas: paralelas, coincidentes, concorrentes e, no R³, reversas.
- Calcular interseções e, para retas no R³, apresentar indicadores geométricos adicionais disponíveis no backend.
- Gerar gráficos 2D e 3D para uma ou duas retas.
- Utilizar as operações matemáticas do backend por meio de uma interface de terminal ou de um notebook Colab.

## Requisitos

- Python 3.10 ou superior.
- Matplotlib, instalado pelo `requirements.txt`.
- Tkinter para executar a interface desktop. Ele costuma acompanhar o Python no Windows; em outras distribuições, pode precisar ser instalado pelo gerenciador de pacotes do sistema.
- Google Colab instala `ipywidgets` durante a execução do notebook; essa dependência não é necessária para a aplicação desktop.

O backend matemático usa a biblioteca padrão do Python. Matplotlib e `ipywidgets` são usados apenas pelas interfaces de visualização.

## Instalação

Abra um terminal na raiz do repositório e instale as dependências:

```bash
python -m pip install -r requirements.txt
```

No Windows, se o comando `python` não apontar para a instalação desejada, use o executável correto ou o lançador `py`:

```powershell
py -m pip install -r requirements.txt
```

## Executar a aplicação desktop

Na raiz do projeto:

```bash
python main.py
```

A janela principal permite navegar pelas telas de construção de retas no R² e R³, análise de duas retas e geração de gráficos 2D/3D. Os gráficos são incorporados à própria janela. A interface coleta os dados e chama os módulos matemáticos; ela não duplica os cálculos do backend.

## Executar o menu pelo terminal

O menu interativo pode ser usado sem iniciar a interface gráfica:

```bash
python executar_menu.py
```

Ele permite testar operações com vetores, construir retas no R² e R³ e analisar relações entre retas nos dois espaços.

## Executar no Google Colab

Abra o notebook pelo link:

[Abrir GeoLine no Google Colab](https://colab.research.google.com/github/igordesouzaDev/GeoLine/blob/main/notebooks/GeoLine_Colab.ipynb)

No Colab, conecte-se a um ambiente de execução e selecione **Ambiente de execução → Executar tudo**. As células clonam a branch `main`, instalam as dependências do projeto e `ipywidgets`, importam as classes originais e exibem a interface interativa. A interface do notebook permite construir retas, analisar duas retas e visualizar gráficos sem Tkinter ou janelas externas.

Para disponibilizar o notebook a outras pessoas, o repositório GitHub precisa estar acessível para elas. O link acima abre a versão do notebook que está na branch `main`.

## Testes automatizados

Execute a suíte a partir da raiz do projeto:

```bash
python -m unittest discover -s tests -v
```

Os testes cobrem as classes `Vetor`, `Reta`, `RetaR2`, `RetaR3` e `Analisador`, além da geração dos gráficos, fluxos da interface e menu do terminal. Os testes automatizados não iniciam menus interativos que aguardam `input()`.

## Exemplos interativos

Além do menu principal, há scripts de demonstração independentes:

```bash
python -m scripts.interativo_vetor
python -m scripts.exemplo_reta_r2
python -m scripts.interativo_analisador_r2
python -m scripts.interativo_analisador_r3
python -m scripts.exemplos_analisador
```

Execute-os a partir da raiz do repositório.

## Organização do projeto

```text
GeoLine/
├── backend/
│   ├── vetor.py             # Operações com vetores no R² e R³
│   ├── reta.py              # Classe-base e operações comuns de retas
│   ├── reta_r2.py           # Retas no plano e equações específicas
│   ├── reta_r3.py           # Retas no espaço e relações geométricas
│   ├── analisador.py        # Classificação e interseção entre retas
│   └── formatacao.py        # Formatação compartilhada de números
├── interface/
│   └── janela.py            # Interface desktop com Tkinter/ttk
├── visualizacao/
│   └── graficos.py          # Figuras Matplotlib 2D e 3D
├── notebooks/
│   └── GeoLine_Colab.ipynb  # Interface interativa para Google Colab
├── scripts/                 # Menu de terminal e exemplos interativos
├── tests/                   # Testes automatizados com unittest
├── main.py                  # Inicialização da aplicação desktop
├── executar_menu.py         # Inicialização do menu pelo terminal
├── requirements.txt         # Dependências Python do projeto
└── CONTRATO.md              # Contrato e responsabilidades das classes
```

## Como os módulos se integram

- `Vetor` valida e representa coordenadas; suas operações são reutilizadas pelas classes de reta e pelo analisador.
- `Reta` guarda o ponto inicial e o vetor diretor, oferecendo operações comuns às retas das duas dimensões.
- `RetaR2` e `RetaR3` herdam de `Reta` e recebem os pontos inicial e final; cada classe acrescenta as representações e operações próprias do seu espaço.
- `Analisador` recebe objetos de reta e retorna a relação identificada, os indicadores e o ponto de interseção quando existe.
- `Graficos` recebe objetos de reta e retorna uma figura e um eixo Matplotlib (`fig, ax`).
- `JanelaPrincipal` conecta as entradas do usuário às classes matemáticas e incorpora as figuras por meio de `FigureCanvasTkAgg`.
- O notebook Colab reutiliza o mesmo backend e o mesmo módulo de gráficos, usando `ipywidgets` como alternativa à interface Tkinter.

Consulte [`CONTRATO.md`](CONTRATO.md) para os nomes, parâmetros e retornos combinados entre as classes.

## Convenções de desenvolvimento

- Classes em `PascalCase`; métodos, atributos e arquivos em `snake_case`.
- Cálculos vetoriais ficam em `Vetor`; operações comuns de retas ficam em `Reta`.
- `RetaR2` e `RetaR3` herdam de `Reta`.
- Testes automatizados ficam em `tests/`; demonstrações que solicitam dados ficam em `scripts/`.
- Novas interfaces devem reutilizar o backend, sem duplicar fórmulas matemáticas.
