FROM python:latest

WORKDIR /usr/src/app/
COPY requirements.txt . 
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple
COPY . . 

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "8000"]
