# tempo-apio

## setup

```shell
python3 -m venv .env && source .env/bin/activate
pip install -r requirements.txt
```

## development

```shell
FLASK_APP=tempo_apio.py FLASK_DEBUG=1 flask run
```

## docker

```shell
# building
docker build -t tempo-apio .

# start mongo
docker run --name some-mongo -d mongo

# run api
docker run -d \
    -p 5001:5001 \
    --link some-mongo:mongo \
    --name tempo-apio \
    tempo-apio
```
