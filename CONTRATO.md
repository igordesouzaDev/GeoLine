# Padrão de desenvolvimento — GeoLine

## 1. Convenção de nomenclatura

Todos devem seguir o mesmo padrão:

| Elemento   | Padrão     | Exemplo         |
| ---------- | ---------- | --------------- |
| Classes    | PascalCase | `RetaR2`        |
| Métodos    | snake_case | `obter_ponto()` |
| Variáveis  | snake_case | `vetor_diretor` |
| Atributos  | snake_case | `ponto_inicial` |
| Constantes | MAIÚSCULAS | `TOLERANCIA`    |
| Arquivos   | snake_case | `reta_r2.py`    |
| Parâmetros | snake_case | `ponto_final`   |

Regra: todo o código deve utilizar nomes em português, seguindo os nomes definidos no contrato.

## 2. Contrato entre as classes

Esta é a parte mais importante. Os nomes abaixo devem ser respeitados por todos, pois uma classe depende da outra.

### Classe `Vetor` — Igor

Arquivo: `backend/vetor.py`

Atributos:

- `coordenadas`
- `dimensao`

Métodos:

| Método                       | Retorno |
| ---------------------------- | ------- |
| `somar(outro)`               | `Vetor` |
| `subtrair(outro)`            | `Vetor` |
| `multiplicar_escalar(valor)` | `Vetor` |
| `modulo()`                   | `float` |
| `produto_escalar(outro)`     | `float` |
| `produto_vetorial(outro)`    | `Vetor` |
| `sao_proporcionais(outro)`   | `bool`  |

### Classe `Reta` — Igor

Arquivo: `backend/reta.py`

Atributos:

- `ponto_inicial`
- `vetor_diretor`
- `dimensao`

Métodos:

| Método                  | Retorno |
| ----------------------- | ------- |
| `obter_ponto(t)`        | `Vetor` |
| `ponto_pertence(ponto)` | `bool`  |
| `equacao_vetorial()`    | `str`   |
| `equacao_parametrica()` | `str`   |

Construtor obrigatório:

```
Reta(ponto_inicial, vetor_diretor)
```

### Classe `RetaR2` — Ian

Arquivo: `backend/reta_r2.py`

Herda de `Reta`.

Construtor combinado:

```
RetaR2(ponto_inicial, ponto_final)
```

O vetor diretor deve ser calculado internamente:

```
vetor_diretor = ponto_final.subtrair(ponto_inicial)
```

Métodos adicionais:

- `equacao_simetrica()`
- `equacao_reduzida()`

Também deve disponibilizar os métodos herdados de `Reta`.

### Classe `RetaR3` — Dominique

Arquivo: `backend/reta_r3.py`

Herda de `Reta`.

Construtor combinado:

```
RetaR3(ponto_inicial, ponto_final)
```

Calcula internamente o vetor diretor da mesma maneira que `RetaR2`.

Método adicional:

\- `equacao_simetrica()`

Também deve disponibilizar os métodos herdados de `Reta`.

### Classe `Analisador` — Aloísio

Arquivo: `backend/analisador.py`

Métodos:

| Método                                 | Responsabilidade                       |
| -------------------------------------- | -------------------------------------- |
| `analisar(reta1, reta2)`               | Classificar a relação entre duas retas |
| `verificar_paralelismo(reta1, reta2)`  | Verificar se são paralelas             |
| `verificar_coincidencia(reta1, reta2)` | Verificar se são coincidentes          |
| `calcular_intersecao(reta1, reta2)`    | Calcular o ponto de interseção         |
| `verificar_reversas(reta1, reta2)`     | Verificar se são reversas no R³        |

Padrão de retorno do método `analisar()`:

Todos devem respeitar esta estrutura:

```
{    "relacao": "concorrentes",    "ponto_intersecao": Vetor([2, 3]),    "sao_paralelas": False,    "sao_coincidentes": False,    "sao_reversas": False,    "mensagem": "As retas se intersectam no ponto (2, 3)."}
```

Os valores devem ser ajustados conforme a relação encontrada. Quando não houver interseção única, `ponto_intersecao` deve ser `None`.

### Classe `Graficos` — Esdras

Arquivo: `visualizacao/graficos.py`

Métodos:

- `plotar_reta_r2(reta)`
- `plotar_reta_r3(reta)`
- `plotar_duas_retas_r2(reta1, reta2)`
- `plotar_duas_retas_r3(reta1, reta2)`

Padrão de retorno: `(fig, ax)`, para permitir que a interface incorpore os gráficos.

### Classe `JanelaPrincipal` — Esdras

Arquivo: `interface/janela.py`

Métodos combinados:

- `criar_menu()`
- `criar_campos_entrada()`
- `obter_dados()`
- `calcular_reta()`
- `analisar_retas()`
- `exibir_resultados()`
- `exibir_grafico()`
- `iniciar()`

A interface deve utilizar as classes do backend, sem implementar os cálculos matemáticos diretamente nela.

## 3. Regras obrigatórias de integração

Estas são as regras que eu estabeleceria para todos os integrantes:

1\. Não alterar nomes combinados

Não renomear atributos ou métodos do contrato sem comunicar o grupo e atualizar as classes dependentes.

2\. Respeitar os tipos de retorno

Se um método foi definido para retornar `Vetor`, não deve retornar uma lista ou uma string no lugar dele.

3\. Respeitar a herança

`RetaR2` e `RetaR3` devem herdar de `Reta`, aproveitando seus atributos e métodos.

4\. Não duplicar funcionalidades

Operações de vetores devem ficar em `Vetor`; cálculos genéricos de retas devem ficar em `Reta`.

5\. Validar entradas

Verificar dimensões, tipos de dados, parâmetros e situações matemáticas inválidas.

6\. Testar antes do Pull Request

Cada integrante deve testar sua implementação e verificar se não quebrou funcionalidades existentes.

7\. Respeitar a estrutura de pastas

Não criar arquivos aleatórios na raiz ou dentro de outras pastas. Testes ficam em `tests/`.

## 4. Exemplo prático de por que isso é importante

Imagine que o Ian desenvolva a classe `RetaR2` usando:

```
self.ponto_aself.ponto_bself.direcao
```

Mas o Aloísio desenvolva o `Analisador` esperando:

```
reta.ponto_inicialreta.vetor_diretor
```

O resultado será um erro de atributo (`AttributeError`), mesmo que os dois códigos funcionem individualmente.

Por isso, todos precisam respeitar os mesmos nomes.

## 5. Fluxo de desenvolvimento que o grupo deve seguir

1. Consultar o contrato antes de implementar.
2. Desenvolver somente o módulo de sua responsabilidade.
3. Não modificar arquivos de outros integrantes sem comunicar.
4. Executar os testes individuais.
5. Conferir a compatibilidade com as classes dependentes.
6. Abrir Pull Request para `main`.
7. Outro integrante revisar e aprovar.