# Todo App

Учебное todo-приложение: backend на FastAPI, PostgreSQL и React frontend.
Backend и база данных запускаются через Docker Compose.

Добавлено кеширование списка задач с помощью Redis.

## Запуск backend

Требуется установленный и запущенный Docker Desktop.

```powershell
Copy-Item .env.example .env
docker compose up --build
```

Перед запуском замените `your_password` в `.env` на локальный пароль.

- API: <http://localhost:8080>
- Swagger UI: <http://localhost:8080/docs>


Остановить контейнеры:

```powershell
docker compose down
```

Удалить контейнеры вместе с данными PostgreSQL:

```powershell
docker compose down -v
```


## Запуск frontend

Frontend подключён как Git submodule и запускается отдельно:

```powershell
git submodule update --init --recursive
cd todo-app-frontend
npm install
npm start
```

Приложение откроется на <http://localhost:3000>.

Frontend основан на репозитории
[makedonsky-it/todo-app-frontend](https://github.com/makedonsky-it/todo-app-frontend).
