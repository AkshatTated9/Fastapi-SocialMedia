FROM python:3.10.11
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
# Make sure Alembic and Uvicorn are installed
RUN pip install alembic uvicorn

# Copy and set Alembic configuration
COPY alembic.ini alembic.ini
COPY alembic alembic

# Run Alembic migrations before starting the server
ENTRYPOINT ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]
# CMD [ "alembic","upgrade","head","&&","uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]

