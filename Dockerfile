FROM python:latest

WORKDIR /usr/src/app/
COPY . . 
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple \
    && chmod +x docker-entrypoint.sh

EXPOSE 8000
CMD ["uwsgi", "-i", "uwsgi.ini"]
