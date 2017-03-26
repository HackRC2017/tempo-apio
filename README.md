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
docker run --name tempo-mongo -d mongo

# run api
docker run -d \
    -p 5001:5001 \
    --name tempo-apio \
    --link tempo-mongo:mongo \
    -e 'MONGODB_HOST=mongo' \
    tempo-apio
```
