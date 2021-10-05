FROM python:3.9.6

ARG WAREHOUSE_DB
ARG WAREHOUSE_USER
ARG WAREHOUSE_PASSWORD
ARG WAREHOUSE_HOST
ARG WAREHOUSE_PORT

# set up location of code
WORKDIR /code
ENV PYTHONPATH=/code/src
ENV WAREHOUSE_DB=${WAREHOUSE_DB}
ENV WAREHOUSE_USER=${WAREHOUSE_USER}
ENV WAREHOUSE_PASSWORD=${WAREHOUSE_PASSWORD}
ENV WAREHOUSE_HOST=${WAREHOUSE_HOST}
ENV WAREHOUSE_PORT=${WAREHOUSE_PORT}

# install python requirements
ADD ./containers/visualizer/requirements.txt requirements.txt
RUN pip install -r requirements.txt

# copy repo
COPY ./ /code/

CMD ["python", "/code/src/dashboard/stonk_dashboard.py"]
