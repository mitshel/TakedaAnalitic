## Для Windows 10
celery -A TakedaAnalitic  worker --loglevel=info -P eventlet

## Для Linux
celery -A TakedaAnalitic  worker --loglevel=info

## Для Linux c Демонизацией
celery multi start -A TakedaAnalitic  worker --loglevel=info