# base image  
FROM python:3.8-slim as builder 
ENV DockerHOME=/home/app/webapp  

RUN mkdir -p $DockerHOME  

WORKDIR $DockerHOME  

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  
RUN pip install --upgrade pip  
COPY . $DockerHOME
RUN pip install --no-cache-dir -r requirements.txt 
RUN python manage.py migrate
EXPOSE 8000   

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]