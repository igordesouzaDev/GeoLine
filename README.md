# GeoLine

Sistema desenvolvido em Python para construção, análise e visualização de equações de retas no espaço bidimensional (R²) e tridimensional (R³).

O GeoLine tem como objetivo auxiliar no estudo de Geometria Analítica e Álgebra Linear, permitindo realizar cálculos matemáticos envolvendo retas, identificar relações entre elas e visualizar suas representações gráficas.

## Funcionalidades

- Construção de retas no R² e R³ a partir de pontos.
- Cálculo e representação de equações vetoriais.
- Cálculo e representação de equações paramétricas.
- Determinação de equações simétricas.
- Determinação da equação reduzida no R², quando aplicável.
- Análise das relações entre duas retas:
  - Paralelas;
  - Coincidentes;
  - Concorrentes;
  - Reversas (no R³).
- Identificação do ponto de interseção, quando existente.
- Visualização gráfica de retas em 2D e 3D.
- Interface gráfica para interação com o sistema.

## Tecnologias utilizadas

- **Python:** linguagem principal de desenvolvimento.
- **Matplotlib:** geração e visualização de gráficos 2D e 3D.
- **Tkinter:** desenvolvimento da interface gráfica.
- **Git e GitHub:** controle de versão e colaboração entre os integrantes.

## Pré-requisitos

Antes de executar o projeto, é necessário ter instalado:

- Python 3.10 ou superior.
- Git (opcional, caso o projeto seja baixado diretamente pelo GitHub).

O Tkinter geralmente já acompanha as instalações padrão do Python. Em algumas distribuições Linux, pode ser necessário instalá-lo separadamente.

## Instalação

### 1. Clonar o repositório

Abra o terminal e execute:

```bash
git clone https://github.com/igordesouzaDev/GeoLine.git
```

### 2. Acessar a pasta do projeto

```bash
cd GeoLine
```

### 3. Criar um ambiente virtual (recomendado)

```bash
python -m venv .venv
```

Ative o ambiente virtual:

**Windows (PowerShell):**

```powershell
.venv\Scripts\Activate.ps1
```

**Windows (Prompt de Comando):**

```cmd
.venv\Scripts\activate.bat
```

**Linux/macOS:**

```bash
source .venv/bin/activate
```

### 4. Instalar as dependências

```bash
pip install -r requirements.txt
```

## Como executar

Com as dependências instaladas e o ambiente virtual ativado, execute o arquivo principal:

```bash
python main.py
```

A interface gráfica do GeoLine será iniciada.

## Executar os testes

O projeto possui testes automatizados para verificar o funcionamento das classes e operações matemáticas.

Para executar todos os testes, utilize:

```bash
python -m unittest discover -s tests -v
```

## Estrutura do projeto

```text
GeoLine/
│
├── backend/
│   ├── vetor.py
│   ├── reta.py
│   ├── reta_r2.py
│   ├── reta_r3.py
│   └── analisador.py
│
├── visualizacao/
│   └── graficos.py
│
├── interface/
│   └── janela.py
│
├── tests/
│   ├── test_vetor.py
│   ├── test_reta_r2.py
│   ├── test_reta_r3.py
│   └── test_analisador.py
│
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

### Organização dos módulos

| Módulo | Responsabilidade |
|---|---|
| `backend/` | Implementação das classes e operações matemáticas. |
| `visualizacao/` | Construção dos gráficos 2D e 3D. |
| `interface/` | Desenvolvimento da interface gráfica. |
| `tests/` | Testes automatizados das funcionalidades. |
| `main.py` | Ponto de entrada e inicialização do sistema. |

## Desenvolvimento e colaboração

O GeoLine é desenvolvido de forma colaborativa, utilizando Git e GitHub para controle de versão.

As alterações devem ser realizadas em branches específicas, evitando commits diretamente na branch principal (`main`).

Fluxo de contribuição:

1. Atualizar a branch `main`.
2. Criar uma branch para a funcionalidade que será desenvolvida.
3. Implementar e testar as alterações.
4. Realizar commits com mensagens descritivas.
5. Enviar a branch para o GitHub.
6. Abrir um Pull Request para revisão e integração à `main`.

## Projeto acadêmico

Desenvolvido como projeto acadêmico no curso de Bacharelado em Sistemas de Informação da Universidade do Estado de Santa Catarina (UDESC).

O projeto integra conceitos de programação orientada a objetos, matemática aplicada, desenvolvimento de interfaces gráficas e visualização de dados.
