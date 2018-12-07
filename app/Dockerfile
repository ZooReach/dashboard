FROM python:3

COPY . /app
RUN pip install -r /app/requirements.txt
ENTRYPOINT ["gunicorn", "-b","0.0.0.0:5000","app.app:app"]