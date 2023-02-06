FROM python:3.11
RUN pip install --upgrade pip
ADD ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt
COPY ./epl343 /epl343
# ADD entrypoint.sh /entrypoint.sh
WORKDIR /epl343
ENTRYPOINT [ "python3", "manage.py" , "runserver", "0.0.0.0:80"]