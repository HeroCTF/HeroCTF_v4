FROM python:latest
WORKDIR /app
COPY requirements.txt .
COPY serv.py .
RUN pip3 install -r requirements.txt
RUN rm requirements.txt
CMD ["python3","serv.py"]