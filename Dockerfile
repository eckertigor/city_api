FROM python:3.11-slim
## Create default user:group for this container
RUN groupadd testgroup;
RUN useradd -g testgroup -ms /bin/bash testuser;

USER testuser


WORKDIR /home/testuser/app
ENV PATH /home/testuser/.local/bin:${PATH}

COPY --chown=testuser:testgroup requirements.txt /home/testuser/requirements.txt

RUN pip3 install -r /home/testuser/requirements.txt

ENV PYTHONPATH /home/testuser/app/

COPY --chown=testuser:testgroup . /home/testuser/app

