INSTALLATION

Requirements
- python 3
- Amazon S3 access (id, key, and readable bucket)
- RabbitMq running


Local installation:
1) install pipenv
2) run
   $ pipenv install
3) copy .env.example to .env file
   and fill-in the parameters.

Run tests
$ pipenv run python -m unittest tests.RmqTest
$ pipenv run python -m unittest tests.Scan
$ pipenv run python -m unittest tests.S3


RUN IN DOCKER

1) CD into src directory and build Docker image
   docker image build -t avanan-bwt-scans3 .

2) start worker
   docker run -it avanan-bwt-scans3 worker.sh

3) start flask endpoint
   docker run -p 5000:5000 -it avanan-bwt-scans3 flask.sh


RUN IN TERMINALS
Start at least 2 terminal windows.

Variant 1:
In the 1st terminal run worker
  $ pipenv run python worker.py

In the 2nd terminal call scan.py
  $ pipenv run python scan.py <your_bucket_to_scan>

Variant 2:
In the 1st terminal run worker
  $ pipenv run python worker.py

In the 2nd terminal run
  $ pipenv run flask run

  and then open in browser the following URL
  http://localhost:5000/

FILELIST

./data/       - test data
./tests/      - unit tests
.env.example  - configuration example
app.py        - Flask endpoint to place jobs in queue and read worker responses
Dockerfile    - Docker build script
libcore.py    - function to scan S3 bucket
librmq.py     - class to communicate with RabbitMQ
libs3.py      - functions to communicate with Amazon S#
libscan.py    - functions to scan files
Pipfile       - pipenv configuration
Pipfile.lock  - pipenv configuration snapshot
scan.py       - command-line scanner to place jobs in queue and read worker responses
start.sh      - BASH script to start workers and Flask REST endpoint
worker.py     - daemon worker to read jobs from queue, scan file and send report back
