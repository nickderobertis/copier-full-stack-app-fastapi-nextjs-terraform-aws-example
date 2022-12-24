FROM python:3.10

ENV PIPENV_VENV_IN_PROJECT=1

WORKDIR api

RUN pip install pipenv
COPY Pipfile .
COPY Pipfile.lock .
RUN mkdir .venv
RUN pipenv sync
RUN mv .venv/ /venv

COPY . .

CMD ["./start.sh"]