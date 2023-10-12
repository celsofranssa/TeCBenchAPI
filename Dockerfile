FROM python:3.10.12-buster

WORKDIR /Optimus-API
COPY . /Optimus-API
RUN pip install --no-cache-dir --upgrade -r /Optimus-API/requirements.txt

EXPOSE 8000

CMD ["python", "main.py"]
