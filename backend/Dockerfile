FROM python:3.9

WORKDIR /app

#pipreqs not generate this depandencies in requirements.txt
RUN pip install uvicorn psycopg2

COPY ./app/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

#COPY ./app /app

CMD ["python", "-m", "uvicorn", "app:app", "--port", "80", "--host", "0.0.0.0", "--reload"]