FROM karmaresearch/wdps_assignment

COPY requirements.txt .



RUN /usr/bin/pip3 install -r requirements.txt

