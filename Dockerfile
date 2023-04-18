FROM python:3.8

WORKDIR .

RUN apt-get update && apt-get install -y git

COPY . .

RUN pip install numpy

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
