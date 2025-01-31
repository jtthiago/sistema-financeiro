# Sistema de Controle Financeiro

Este projeto é um sistema de controle financeiro desenvolvido com **Django** e **Bootstrap**. Ele permite gerenciar transações financeiras (receitas e despesas), categorizá-las e organizá-las por data.

## 🚀 Funcionalidades
- Criar, visualizar, editar e excluir transações
- Classificar transações como **receita** ou **despesa**
- Interface amigável com **Bootstrap**

## 📦 Tecnologias Utilizadas
- **Django** (Framework web)
- **SQLite** (Banco de dados padrão)
- **Bootstrap** (Estilização do frontend)

## 📂 Estrutura do Projeto
```
sistema-financeiro/
│-- finance/              # Aplicação principal
│   │-- migrations/       # Migrações do banco de dados
│   │-- templates/        # Templates HTML
│   │-- views.py          # Lógica das views
│   │-- models.py         # Modelos do banco de dados
│   │-- urls.py           # Rotas da aplicação
│-- sistema_financeiro/   # Configuração do Django
│-- db.sqlite3            # Banco de dados SQLite
│-- manage.py             # Gerenciador do Django
│-- README.md             # Documentação
```

## 🛠️ Instalação e Configuração
### 1️⃣ Clonar o repositório
```sh
git clone https://github.com/seu-usuario/sistema-financeiro.git
cd sistema-financeiro
```

### 2️⃣ Criar e ativar o ambiente virtual
```sh
python -m venv env
# No Windows
env\Scripts\activate
# No Linux/Mac
source env/bin/activate
```

### 3️⃣ Instalar as dependências
```sh
pip install -r requirements.txt
```

### 4️⃣ Aplicar migrações e iniciar o servidor
```sh
python manage.py migrate
python manage.py runserver
```

O sistema estará disponível em **http://127.0.0.1:8000/finance/**

## 🔗 Rotas Principais
| Rota                 | Descrição |
|----------------------|--------------------------------|
| `/finance/`         | Lista todas as transações |
| `/finance/create/`  | Criar uma nova transação |
| `/finance/<pk>/update/` | Editar uma transação |
| `/finance/<pk>/delete/` | Excluir uma transação |

## 📝 Licença
Este projeto é de código aberto e pode ser usado e modificado livremente.

---
Feito com ❤️ usando Django!

