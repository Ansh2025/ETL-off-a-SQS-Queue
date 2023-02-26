# ETL-off-a-SQS-Queue

In order to run this project, please run the following commands in the following order below:
(Assuming these commands are running in Windows)

Step 1: Clone the repository into a local folder in your system using the following command:

```
git clone https://github.com/Ansh2025/ETL-off-a-SQS-Queue.git
```

Step 2: Install all requirements for this project.
Open a command prompt and run the following command:

```
make install
```

Step 3: Create a table in postgres
Run the following command and the password is **postgres**:
```
make create
```

Step 4: Run the docker containers.
To run the localstack and postgres containers for setting up the environment for this application, run:
```
make start
```

Step 5: Run the python ETL application for reading the data from an AWS SQS Queue, masking the 'ip' and 'device_id' columns and writing it into a postgres database:
```
make run
```

Once you are done with these steps, you should be able to run the following command in a separate terminal to check the added records.
Password for postgres is **postgres**
```
psql -d postgres -U postgres -p 5432 -h localhost -W
```
```
select * from user_logins;
```

In case you want to get the encrypted string back, please run the following command:
```
python decode.py -e "<YOUR ENCRYPTED STRING>"
```


