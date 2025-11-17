# 📊 Understat Data Explorer – Streamlit App

Este projeto é uma aplicação **Streamlit** que utiliza a biblioteca **understatapi** para explorar dados avançados de futebol (xG, chutes, estatísticas de jogadores, partidas e standings) das ligas disponíveis no **Understat**, cobrindo as temporadas **2014–2024**.

A ferramenta permite visualizar **tabelas, rankings, jogos**, além de **mapas de chutes (shotmaps)** desenhados com o **mplsoccer**.

---

## 🚀 Funcionalidades

### ✔️ Seleção de Liga e Temporada

* O usuário escolhe uma **liga** disponível no Understat.
* Depois escolhe uma **temporada** entre **2014/15 e 2024/25**.
* A temporada selecionada é convertida automaticamente para o formato aceito pela API.

---

### ✔️ Standings da Liga

Após selecionar liga + temporada, o app:

* Consulta os dados de todos os times via API.
* Calcula:

  * Pontos
  * Vitórias, empates e derrotas
  * Gols marcados e sofridos
  * Total de jogos
* Exibe uma tabela ordenada pelo critério:

  > PTS → Jogos → GA (menor)

---

### ✔️ Top Jogadores da Liga

Também são exibidos os **10 jogadores com melhores números**, incluindo:

* Nome
* Partidas, minutos
* Gols, assistências
* Finalizações
* Key passes
* Cartões
* Time

---

### ✔️ Seleção de um Time

O usuário pode selecionar qualquer time da liga, e o app mostra:

* **Todos os jogos disputados** na temporada (casa/fora)
* Data e horário
* Gols marcados e sofridos

---

### ✔️ Seleção de Jogador

Ao escolher um jogador do time:

* O app exibe sua **tabela completa de estatísticas**.
* Busca todos os **chutes do jogador na temporada**, incluindo xG e resultado.

---

### ✔️ Shotmap Interativo

Usando **mplsoccer**, o app constrói um mapa visual de chutes:

* Tamanho do ponto = **xG do chute**
* Cor:

  * 🟢 **Verde** = Gol
  * ⚪ **Branco** = Não foi gol
* Transparência e ordem de desenho destacam os gols
* Campo renderizado no estilo **StatsBomb (metade do campo)**

---

## 🧠 Principais Dependências

* `understatapi` – acesso aos dados do Understat
* `streamlit` – interface interativa
* `pandas` – manipulação dos dados
* `mplsoccer` – visualização do campo e chutes

---

## 📌 Estrutura Principal do Código

### 🔹 `plot_shots(df, ax, pitch)`

Desenha todos os chutes de um jogador, com tamanho proporcional ao xG e coloração conforme o resultado.

### 🔹 `build_standings(data)`

Calcula a classificação da liga a partir do histórico de partidas de cada time.

### 🔹 Fluxo geral do app

1. Usuário seleciona liga
2. Seleciona temporada
3. App exibe standings + top players
4. Usuário escolhe time
5. App mostra partidas
6. Usuário escolhe jogador
7. App exibe shotmap

---

## 📷 Exemplo de Saída

* Tabela da liga
* Tabela dos 10 principais jogadores
* Lista de partidas do time selecionado
* Shotmap com todos os chutes do jogador

---
