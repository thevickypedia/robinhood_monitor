FROM python:3.7-slim

MAINTAINER vignesh rao <svignesh1793@gmail.com>

# DOCKER env var is to indicate the script to fetch creds from AWS
ENV DOCKER="True" \
    graph_min=100 \
    graph_max=500

RUN mkdir /opt/robinhood_monitor
COPY . /opt/robinhood_monitor

# # Bad option: Use venv within docker to solve root pip installation problem
# RUN /bin/bash -c "source /opt/robinhood_monitor/venv/bin/activate"
# RUN python3 -m pip install --user --no-cache-dir --no-warn-script-location --upgrade pip

RUN /usr/local/bin/python3 -m pip install --upgrade pip
RUN cd /opt/robinhood_monitor/lib && pip3 install --user -r requirements.txt

WORKDIR /opt/robinhood_monitor

ENTRYPOINT ["/usr/local/bin/python", "./robinhood.py"]