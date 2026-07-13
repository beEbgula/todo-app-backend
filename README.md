## 🎨 Frontend

> [!NOTE]
> Frontend-часть проекта основана на репозитории
> [makedonsky-it/todo-app-frontend](https://github.com/makedonsky-it/todo-app-frontend).
>
> Автор оригинального frontend — [makedonsky-it](https://github.com/makedonsky-it).
> В этом проекте мной разработан backend и выполнена его интеграция с frontend.


# Первый запуск:
```bash
python3 -m venv venv
venv/scripts/activate
pip install -r requirements.txt
docker run -e POSTGRES_PASSWORD=<> -p 5432:5432 -d postgres
uvicorn app.main:app --reload --port 8080
```


### 1) Сохранение информации в контейнер

```bash
# Создание и запуск без сохранения данных
docker run -d --name 'container_name' -e POSTGRES_PASSWORD=<> -p 5432:5432 postgres

# Запуск c сохранением данных
docker run 'container_name'

# Посмотреть список всех контейнеров | список активных:
docker ps -a | docker ps
```

При подключении к проекту контейнера мы сохраняем данные в бд, но при его перезагрузке / удалении информация всё равно стирается. 
(Все хранится только в активной сессии)


### 2) Сохранение информации в volume

```bash
# Создание
docker run -d --name 'container_name' -e POSTGRES_PASSWORD=admin -p 5432:5432 -v 'volume_name':/var/lib/postgresql postgres:latest

# Посмотреть список контейнеров
docker ps
```

Так данные сохраняются в отдельном хранилище (Volume) на вашем компьютере.
Volume существует независимо от контейнера (его можно удалить, а затем создать новый и подключить к нему тот же Volume) — все данные будут на месте.
