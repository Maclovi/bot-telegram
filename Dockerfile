FROM python:3.10.11-slim

WORKDIR /code

COPY requirements.txt ./
# COPY ./__cache__ ../usr/local/bin/pytube/
    
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

CMD ["python", "main"]
