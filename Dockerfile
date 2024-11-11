FROM python:3.12 

RUN apt update -y 
RUN apt upgrade -y 

WORKDIR /src 

COPY requirements.txt . 
RUN pip install -r requirements.txt 

COPY . . 
COPY configs-example.py configs.py

CMD ["python3", "main.py"]
