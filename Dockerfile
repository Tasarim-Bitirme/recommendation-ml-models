FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

#RUN pip install uvicorn

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app/app

#run the app in unicorn : uvicorn.run(app, host='127.0.0.1', port=4000)
#CMD ["uvicorn", "--proxy-headers", "app.main:fastAPIApp" "--host", "127.0.0.1", "--port", "80"]