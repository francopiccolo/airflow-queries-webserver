FROM python:3.6

RUN apt-get update

COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD python app.py
#CMD ["gunicorn", "-w", "3", "-b", ":5000", "-t", "360", "--reload", "wsgi:app"]