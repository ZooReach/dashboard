FROM python:3

COPY . /app
RUN chmod 755 /app
RUN git clone https://github.com/ZooReach/visual
RUN mv /visual/app/apis/* /app/apis/
RUN ls /visual/app/static/js
RUN ls /app/static/js/visualization/
RUN mv /visual/app/static/js/* /app/static/js/visualization/
RUN mv /visual/app/helper /app/helper
RUN ls /app/static/js/visualization/
RUN pip install -r /app/requirements.txt
ENTRYPOINT ["gunicorn", "-b","0.0.0.0:5000","app.app:app"]