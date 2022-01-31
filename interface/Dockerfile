FROM python:3.9

COPY requirements.txt .

RUN pip install --upgrade --no-cache-dir -r requirements.txt

COPY . /app

WORKDIR /app

CMD ["bash", "-c", "streamlit run app.py"]