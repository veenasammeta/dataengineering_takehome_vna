# Fetch Rewards #
## Data Engineering Take Home: ETL off a SQS Qeueue ##

## About Code

1. create_and_write_to_queue.py 
        This script will unzip the gz file and read the contents and push the message to sqs queue.

2. retreive_messages_and_write_to_db.py
        This script will read the message from sqs queue and create a pandas dataframe. Then it will mask the device_id and ip and then this dataframe will be written to postgres table 'user_logins'
3. main.py
        This script is the main script which will run the above 2 scripts, it will send the messages to the sqs and read the messages from the queue and then mask the data and then push to the table 'user_logins' in postgres database.

## Project Setup
1. Fork this repository to a personal Github, GitLab, Bitbucket, etc... account.
2. You will need the following installed on your local machine
    * make
        * Ubuntu -- `apt-get -y install make`
        * Windows -- `choco install make`
        * Mac -- `brew install make`
    * python3 -- [python install guide](https://www.python.org/downloads/)
    * pip3 -- `python -m ensurepip --upgrade` or run `make pip-install` in the project root
    * awslocal -- `pip install awscli-local`  or run `make pip install` in the project root
    * docker -- [docker install guide](https://docs.docker.com/get-docker/)
    * docker-compose -- [docker-compose install guide]()
3. Run `make start` to execute the docker-compose file in the the project (see scripts/ and data/ directories to see what's going on, if you're curious)
    * An AWS SQS Queue is created
    * A script is run to write 100 JSON records to the queue
    * A Postgres database will be stood up
    * A user_logins table will be created in the public schema
4. Test local access
    * Read a message from the queue using awslocal, `awslocal sqs receive-message --queue-url http://localhost:4566/000000000000/login-queue`
    * Connect to the Postgres database, verify the table is created
    * username = `postgres`
    * database = `postgres`
    * password = `postgres`

```bash
# password: postgres

psql -d postgres -U postgres  -p 5432 -h localhost -W
Password: 

postgres=# select * from user_logins;
 user_id | device_type | hashed_ip | hashed_device_id | locale | app_version | create_date 
---------+-------------+-----------+------------------+--------+-------------+-------------
(0 rows)
```
5. Run `make stop` to terminate the docker containers and optionally run `make clean` to clean up docker resources.


## Execution:

### Option1: 

Installation and running python script.

```
pip3 install -r requirements.txt
python3 scripts/main.py

```

OR

### Option2: 

Just run the below shell script , then it will install libraries and execute the scripts.

```
sh execution.sh
```
