
# 🏨 Hotel API – Backend em Flask + PostgreSQL (Deploy na Vercel)

Este projeto consiste numa API REST para gestão de um hotel, desenvolvida com Flask (Python) e PostgreSQL. A aplicação está preparada para autenticação JWT, permissões por tipo de utilizador (admin, rececionista, cliente) e está implementada na Vercel.

---

## 📌 Funcionalidades

- 🔐 Autenticação JWT
- 👥 Gestão de utilizadores com diferentes permissões
- 🏨 Gestão de quartos e reservas
- ⚙️ Ligação dinâmica à base de dados conforme o tipo de utilizador
- 🚀 Deploy automático via Vercel

---

## ⚙️ Instalação Local

### 1. Pré-requisitos

- Python 3.9+
- PostgreSQL ativo
- Git
- Conta na Vercel (opcional para deploy)

### 2. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 3. Criar ambiente virtual e instalar dependências

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Criar o ficheiro `.env`

Cria um ficheiro `.env` na raiz com as tuas variáveis de ambiente:

```env
FLASK_ENV=development
JWT_SECRET_KEY=sua_chave_super_segura

DB_NAME=nome_da_base
DB_HOST=localhost
DB_PORT=5432

ADMIN_USER=admin
ADMIN_PASSWORD=admin123

RECECIONISTA_USER=rececionista
RECECIONISTA_PASSWORD=recep123

CLIENTE_USER=cliente
CLIENTE_PASSWORD=cliente123
```

### 5. Executar a aplicação

```bash
cd api
python index.py
```

---

## 🚀 Deploy na Vercel

1. Cria um repositório GitHub com este projeto.
2. Acede a [https://vercel.com](https://vercel.com), liga a tua conta GitHub.
3. Cria um novo projeto com o repositório.
4. No menu **Environment Variables**, adiciona todas as variáveis do `.env`.
5. Define como comando de build: `pip install -r requirements.txt`
6. Define como ficheiro de entrada: `api/index.py`

> A Vercel irá fazer o deploy automaticamente e disponibilizar um domínio como:
> `https://teu-projeto.vercel.app`

---

## 📡 Endpoints da API

| Método | Endpoint                  | Descrição                                      | Autenticação |
|--------|---------------------------|------------------------------------------------|--------------|
| POST   | `/auth/login`             | Autenticar utilizador e receber token JWT      | ❌           |
| GET    | `/user/get_all`           | Obter todos os utilizadores (admin)            | ✅ admin      |
| GET    | `/quartos/get_all`        | Listar todos os quartos                        | ✅ admin/rececionista |
| GET    | `/reserva/get_all`        | Listar todas as reservas                       | ✅            |
| POST   | `/reserva/create`         | Criar nova reserva                             | ✅            |
| GET    | `/test_db`                | Testar conexão à base de dados                 | ❌           |

> Para rotas autenticadas, enviar no cabeçalho:
> `Authorization: Bearer <TOKEN_JWT>`

---

## 🧪 Testar com Postman

1. Autentica com o endpoint `POST /auth/login` e guarda o token JWT.
2. Para as chamadas seguintes, inclui no cabeçalho:
```
Authorization: Bearer <teu_token>
```

---

## 📁 Estrutura do Projeto

```
/
├── api/
│   ├── index.py
│   ├── routes/
│   ├── controllers/
│   ├── models/
│   ├── database/
│   └── utils/
├── requirements.txt
├── vercel.json
├── .env
└── README.md
```

---

## 🛠 Tecnologias Utilizadas

- Python 3.9+
- Flask
- PostgreSQL
- psycopg2-binary
- flask-jwt-extended
- python-dotenv
- Vercel (deploy backend)

---

## 👤 Manual de Utilizador

### Como utilizar:

1. Autenticar-se via `/auth/login`.
2. Guardar o token JWT retornado.
3. Aceder às rotas apropriadas ao seu tipo de utilizador.
4. Enviar sempre o token no cabeçalho `Authorization`.

Tipos de utilizador disponíveis:
- `admin`: acesso total
- `rececionista`: acesso parcial (ex: gestão de quartos)
- `cliente`: acesso restrito (reservas)

---

## 🖥️ Manual de Instalação

1. Instalar dependências com `pip install -r requirements.txt`
2. Configurar o `.env` com credenciais da base de dados
3. Executar o ficheiro `index.py`
4. Testar a aplicação via `localhost` ou com ferramentas como Postman
5. Para produção, usar Vercel conforme descrito acima

---

## 📬 Contacto

Desenvolvido por [O Teu Nome]  
📧 Email: teuemail@exemplo.com

---
