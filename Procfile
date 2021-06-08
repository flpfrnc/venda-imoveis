release: python3 manage.py migrate
web: gunicorn venda_imoveis.wsgi:application --preload --log-file - 