FROM python:3

COPY . /app
RUN git clone https://github.com/ZooReach/visual
RUN mv /visual/apis/* /app/apis/
RUN mv /visual/flaskr/static/js/* /app/static/js/visualization/
RUN pip install -r /app/requirements.txt
ENTRYPOINT ["gunicorn", "-b","0.0.0.0:5000","app.app:app"]