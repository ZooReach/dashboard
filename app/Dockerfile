FROM python:3

COPY . /app
RUN chmod 755 /app
RUN git clone https://github.com/ZooReach/visual && \
    mv /visual/app/apis/* /app/apis/ && \
    mv /visual/app/static/js/* /app/static/js/visualization/ && \
    mv /visual/app/helper /app/helper
RUN pip install -r /app/requirements.txt
ENTRYPOINT ["gunicorn", "-b","0.0.0.0:5000","app.app:app"]