FROM python:3.10

WORKDIR /code

# to optimize step 3 and 4
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . .
