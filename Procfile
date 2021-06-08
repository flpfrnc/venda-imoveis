release: python3 manage.py migrate
web: gunicorn venda-imoveis.wsgi:application --preload --log-file - 