FROM python:3.7


COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip3 install google-cloud-storage
RUN pip3 install gsutil

EXPOSE 8501

COPY . /app
WORKDIR /app

CMD streamlit run extract_main.py --server.port=8501

