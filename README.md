# ToDobot
docker-compose up
alembic revision --autogenerate -m "create task table"
alembic upgrade head
python main.py