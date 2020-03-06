INSTALLATION

Requirements
- python 3
- RabbitMq directory
- Amazon S3 access (id, key, and readable bucket)


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


RUN
Start at least 2 terminal windows.

Variant 1:
In the 1st terminal run worker
  $ pipenv run python worker.py

In the 2nd terminal run
  $ pipenv run python scan.py <your_bucket_to_scan>

Variant 2:
In the 1st terminal run worker
  $ pipenv run python worker.py

In the 2nd terminal run
  $ pipenv run flask run

  and then open in browser the following URL
  http://localhost:5000/

