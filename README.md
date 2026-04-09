# # 📝 automatizateFormularioLaboratorio

Um robô desenvolvido em Python focado em economizar o seu tempo! Este script preenche automaticamente o **Registro de Atividades dos Professores Orientadores** (Google Forms), selecionando sua regional, escola e dados pessoais em segundos, pulando as páginas de forma autônoma.

---

## 🗂️ Estrutura do Projeto

```text
📦 automatizateFormularioMaker
 ┣ 🐍 preenchedor_formulario.py   # O robô em si (Lógica de preenchimento)
 ┣ 📋 requirements.txt            # Arquivo com as bibliotecas necessárias
 ┗ 📖 README.md                   # Documentação do projeto
```

---

## 🚀 Como funciona?

O script se conecta ao seu Google Chrome e assume o controle da aba do Google Forms. Ele possui variáveis globais no topo do código onde você configura os seus dados (Nome, Regional, Escola). Ao rodar, ele clica nos campos exatos, avança as páginas e deixa o formulário pronto para o preenchimento da atividade específica do dia.

---

## 🛠️ Tecnologias

* **Python 3**
* **Selenium WebDriver**

---

## ⚙️ Como instalar e configurar (Do Zero Absoluto)

Se você nunca programou, siga este passo a passo detalhado:

### 1. Preparando o Terreno (Instalações base)
* **Python:** Baixe e instale o [Python 3](https://www.python.org/downloads/). **⚠️ MUITO IMPORTANTE:** Na primeira tela do instalador, marque a caixinha **"Add python.exe to PATH"** antes de clicar em *Install Now*.
* **Editor de Código:** Recomendamos instalar o [Visual Studio Code (VS Code)](https://code.visualstudio.com/) para poder editar seus dados no código facilmente.
* **Git (Opcional):** Você pode usar o [Git](https://git-scm.com/downloads) para clonar o código via terminal, ou simplesmente clicar no botão verde **Code > Download ZIP** no topo desta página e extrair a pasta no seu computador.

### 2. Baixe o projeto
Se estiver usando o terminal:
```bash
git clone [https://github.com/SEU_USUARIO/automatizateFormularioMaker.git](https://github.com/SEU_USUARIO/automatizateFormularioMaker.git)
cd automatizateFormularioMaker
```

### 3. Instale a biblioteca do Robô
Com o terminal aberto na pasta do projeto, instale o Selenium:
```bash
pip install -r requirements.txt
```

### 4. Configure os seus dados no Código!
Abra o arquivo `preenchedor_formulario.py` no seu VS Code (ou bloco de notas). Logo nas primeiras linhas, você verá a seção de variáveis globais. Altere os dados entre aspas para a sua realidade:

```python
MARCAR_RECIBO_EMAIL = True
NOME_PROFESSOR = "Seu Nome Completo"
TIPO_ORIENTADOR = "Tecnologias Educacionais"
REGIONAL = "GRANDE FPOLIS"
ESCOLA = "EEB VICENTE SILVEIRA"
```

### 5. Inicie o Google Chrome em Modo Especial
Para o bot acessar seu navegador, abra uma janela de comunicação. Pressione `Windows + R` e cole:
```cmd
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\ChromeBotProfile"
```

### 6. Execute a Mágica!
Nesta nova janela do Chrome, abra o link do formulário do Estado e faça seu login do Google. Deixe na primeira página do formulário.

Volte ao VS Code e rode o script:
```bash
python preenchedor_formulario.py
```
Veja o robô trabalhar sozinho! Ele vai preencher, clicar em avançar e deixar a tela pronta.

---

✍️ **Autor:** Professor Eduardo Kazenski  
Sinta-se livre para dar um ⭐ *Star*, fazer um *Fork* e automatizar o seu trabalho!
