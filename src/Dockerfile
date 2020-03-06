# Use the official image as a parent image
FROM python:3

ENV PATH /usr/src/app:$PATH

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8

RUN pip install --upgrade pip && \
    pip install --no-cache-dir flask oletools boto3 python-dotenv pika

# Set the working directory
WORKDIR /usr/src/app

# Copy files
COPY . .

# Run worker
CMD ["./worker.sh"]
