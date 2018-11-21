FROM python:3

WORKDIR /app
COPY ./ /app
RUN pip install -r /app/requirements.txt
ENTRYPOINT ["gunicorn", "-b","0.0.0.0:5000","app:app"]