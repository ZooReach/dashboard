# Dashboard
## For development

***Run outside docker***

python3 -m venv localenv
source localenv/bin/activate

cd app

pip install -r requirements.txt

FLASK_APP=app:app FLASK_DEBUG=1 python -m flask run

***Run inside docker***

cd app

docker build -t test .

docker run --rm -p 80:5000 test
