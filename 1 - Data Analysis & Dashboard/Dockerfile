FROM continuumio/miniconda3

COPY . /app/

RUN apt-get update
RUN apt-get install nano unzip
RUN apt install curl -y
RUN curl -fsSL https://get.deta.dev/cli.sh | sh
RUN python -m pip install --upgrade pip
RUN pip install -r app/requirements.txt


CMD streamlit run --server.port $PORT app/myapp.py
