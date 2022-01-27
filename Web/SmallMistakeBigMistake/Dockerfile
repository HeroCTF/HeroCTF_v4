FROM python:3.10-alpine

WORKDIR /usr/srv/app

COPY ./src/ .

RUN python3 -m pip install \
	--no-cache-dir -r requirements.txt

EXPOSE 5000
CMD ["python3", "main.py"]