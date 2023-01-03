FROM python:3.10

ENV PIPENV_VENV_IN_PROJECT=1

WORKDIR api

RUN pip install pipenv
COPY Pipfile .
COPY Pipfile.lock .
RUN mkdir .venv
RUN pipenv sync
RUN mv .venv/ /venv

# Use sed to replace VIRTUAL_ENV='/api/.venv' with VIRTUAL_ENV='/venv' in /venv/bin/activate
RUN sed -i 's/\/api\/.venv/\/venv/g' /venv/bin/activate

COPY . .

ENV VIRTUAL_ENV=/venv

CMD ["./start.sh"]