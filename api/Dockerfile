FROM fedora:latest 

EXPOSE 8000

COPY ./requirements.txt /
COPY ./main.py /

RUN dnf install python3 python3-pip -y
RUN pip3 install -r requirements.txt

ENTRYPOINT [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80" ]

