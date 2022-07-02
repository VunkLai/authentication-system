FROM python:3.8-slim
WORKDIR /app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY server ./server
RUN python server/manage.py makemigrations
RUN python server/manage.py migrate

# Initialize
# RUN python server/manage.py initialize

ENTRYPOINT [ "python", "/app/server/manage.py" ]
CMD [  "runserver", "0.0.0.0:8000" ]
EXPOSE 8000
