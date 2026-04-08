# 📌 Projeto: Buscador de Emails (Streamlit)

Aplicação web simples desenvolvida com Streamlit para buscar emails a partir do nome do usuário em uma planilha Excel.

---

# 🚀 Tecnologias utilizadas

* Python
* Streamlit
* Pandas
* OpenPyXL

---

# 📂 Estrutura do projeto

```
buscador_usuario/
│
├── venv/                # Ambiente virtual (não subir pro Git)
├── app.py              # Aplicação principal
├── requirements.txt    # Dependências do projeto
├── dados.xlsx          # Planilha com nome e email
```

---

# ⚙️ Instalação do projeto (PASSO A PASSO)

## 🟢 1. Instalar o Python

Baixar em:
https://www.python.org/downloads/

⚠️ Durante a instalação, marcar:
✔️ Add Python to PATH

---

## 🟢 2. Criar pasta do projeto

Exemplo:

```
C:\Users\brunna\Documents\buscador_usuario
```

Abrir no VS Code.

---

## 🟢 3. Criar ambiente virtual

No terminal:

```bash
python -m venv venv
```

Caso não funcione:

```bash
py -m venv venv
```

---

## 🟢 4. Ativar ambiente virtual

### ✔️ No PowerShell:

```bash
venv\Scripts\activate
```

### ✔️ No CMD (alternativa):

```bash
venv\Scripts\activate.bat
```

---

## 🟢 5. Criar arquivo requirements.txt

Conteúdo:

```
streamlit
pandas
openpyxl
```

---

## 🟢 6. Instalar dependências

Com ambiente ativo:

```bash
pip install -r requirements.txt
```
---

# 💡 Importante
✔️ Usar o comando: Se você fechar o VS Code, da próxima vez:
👉 Sempre ative o ambiente antes:
```bash
venv\Scripts\activate
```
✔️ Não subir pasta `venv` para o Git
✔️ Usar `pip freeze > requirements.txt` para produção

---

## 🟢 7. Rodar aplicação

```bash
streamlit run app.py
```

---

# ❌ Problemas comuns e soluções

---

## 🔴 ERRO 1: Execution Policy bloqueada (PowerShell)

### ❌ Erro:

```
execution of scripts was disabled
```

### 📌 Causa:

PowerShell bloqueia execução de scripts por segurança

---

### ✅ Solução 1 (recomendada):

Abrir PowerShell como administrador:

```bash
Set-ExecutionPolicy RemoteSigned
```

Confirmar com:

```
Y
```

---

### ✅ Solução 2 (mais rápida):

Rodar no CMD:

```bash
venv\Scripts\activate.bat
```

---

## 🔴 ERRO 3: Comando não reconhecido

### ❌ Erro:

```
'Set-ExecutionPolicy' não é reconhecido
```

### 📌 Causa:

Comando executado no CMD (Prompt de Comando)

---

### ✅ Solução:

Executar no **PowerShell**, não no CMD

---

## 🔴 ERRO 4: Python não reconhecido

### ❌ Erro:

```
'python' não é reconhecido
```

### 📌 Causa:

Python não foi adicionado ao PATH

---

### ✅ Solução:

Reinstalar Python marcando:
✔️ Add Python to PATH


---

# ✨ Autor

Projeto desenvolvido para automação de busca de emails institucionais.
