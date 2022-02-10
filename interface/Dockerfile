FROM python:3.9

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt

RUN pip install --upgrade --no-cache-dir -r requirements.txt

COPY ./app /code/app

CMD ["bash", "-c", "streamlit run app/app.py"]
