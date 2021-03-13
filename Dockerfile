FROM python:3.9-slim
LABEL maintainer="Sandro Huber <sandrochuber@gmail.com>"
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH="root/.poetry/bin/:${PATH}"
CMD ["/bin/sh", "-c", "poetry install && poetry add pylic --dev && poetry run pylic"]
