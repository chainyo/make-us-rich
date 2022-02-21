FROM python:3.8

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./main.py /code/app/main.py

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
