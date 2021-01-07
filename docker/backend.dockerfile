FROM python:3.7

ENV DOCKER_HOST_SRC=.
ENV DOCKER_CONTAINER_SRC=/async_service

RUN echo deb [check-valid-until=no] http://archive.debian.org/debian jessie-backports main >> /etc/apt/sources.list && \
    apt-get -y update && \
    apt-get -y install \
      nginx \
      && apt-get -y clean

WORKDIR $DOCKER_CONTAINER_SRC
ADD . $DOCKER_CONTAINER_SRC

# Install Python dependencies
COPY ${DOCKER_HOST_SRC}/requirements ${DOCKER_CONTAINER_SRC}/requirements
RUN pip install -r requirements/base.txt

# Copy source
COPY $DOCKER_HOST_SRC .

# Prepare entrypoint
RUN mv ${DOCKER_HOST_SRC}/docker/scripts/backend.entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Port to expose
EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]