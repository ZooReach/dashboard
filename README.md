# dashboard
For development

cd app

FLASK_APP=app:app FLASK_DEBUG=1 python -m flask run

To run inside docker

cd app

docker build -t test .

docker run --rm -p 80:5000 test
