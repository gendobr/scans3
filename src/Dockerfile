# Use the official image as a parent image
FROM python:3

# ensure local python is preferred over distribution python
ENV PATH /usr/local/bin:$PATH

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8

# Set the working directory
WORKDIR /usr/src/app

# Copy files
COPY . .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir flask oletools boto3 python-dotenv pika

# Inform Docker that the container is listening on the specified port at runtime.
EXPOSE 5000

# Run the specified command within the container.
CMD ["/usr/src/app/start.sh"]
