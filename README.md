# 🎬 API-CineReserve
Api projetada para gerenciar as complexidades das operações modernas de cinema com foco na integridade dos dados e no controle de concorrência

## 🚀 Tecnologias

- Python 3.12
- Django + Django REST Framework
- PostgreSQL
- Redis
- Celery
- Docker
- JWT Authentication
- Swagger

## ⚙️ Como rodar o projeto

### Pré-requisitos
- Docker
- Docker Compose

### 1. Clone o repositório
```bash
git clone https://github.com/DougVikt/API-CineReserve.git
cd apicine
```

### 2. Configure as variáveis de ambiente
```bash
cp .env.exemple .env
```
Preencha o `.env` com suas configurações. Para gerar a `SECRET_KEY`:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 3. Suba os containers
```bash
docker-compose up --build
```

### 4. Rode as migrações
```bash
docker-compose exec web python manage.py migrate
```

### 5. Crie o superusuário
```bash
docker-compose exec web python manage.py createsuperuser
```

## 📄 Documentação

Acesse a documentação da API em:
```
http://localhost:8000/swagger/
```

## 🧪 Testes
```bash
docker-compose exec web python manage.py test
```

## 📌 Endpoints

| Método | Endpoint | Auth | Descrição |
|---|---|---|---|
| POST | `/apiv1/auth/register/` | ❌ | Cadastro |
| POST | `/apiv1/token/` | ❌ | Login |
| POST | `/apiv1/token/refresh/` | ❌ | Renovar token |
| GET | `/apiv1/movies/` | ❌ | Listar filmes |
| GET | `/apiv1/movies/<id>/sessions/` | ❌ | Listar sessões |
| GET | `/apiv1/sessions/<id>/seats/` | ❌ | Mapa de assentos |
| POST | `/apiv1/sessions/<id>/seats/<id>/reserve/` | ✅ | Reservar assento |
| POST | `/apiv1/sessions/<id>/seats/<id>/purchase/` | ✅ | Comprar ingresso |
| GET | `/apiv1/tickets/` | ✅ | Meus ingressos |