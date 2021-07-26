# unnax-be-test
This is just a code challenge.

To setup the project follow the next steps:

## Installation

1 - Create a postgres database for the project

2 - Edit env_variables file and set the next values using your database credentials
~~~
    export DATABASE_NAME=<database_name>
    export DATABASE_USER=<database_user>
    export DATABASE_PASSWORD=<database_password>
    export DATABASE_HOST=localhost
    export DATABASE_PORT=<database_port> // 5432
~~~

3 - Build the docker containers
```bash
$ docker-compose build
```

4 - Run the docker containers
```bash
$ docker-compose up
```

5 - Open a new terminal and launch the shell of the web container
```bash
$ docker-compose exec web sh
```

6 - In the shell of the web container, execute the next commands to create a superuser and run the tests.
```bash
$ source env_variables
$ python manage.py createsuperuser
```

7 - Keep open the shell of the web container.

## Usage

### Point 1
To run the script of the point 1 and print the extracted data in the required format, execute in the shell of the web container the next command.
```bash
$ python read.py --username Y3216434F --password pperez2018
```

### Point 2 and 3
Access to the django admin with your superuser credentials.
[http://localhost:8000/admin/](http://localhost:8000/admin/)


Access to the celery flower dashboard to see the status of each task.
[http://localhost:5555](http://localhost:5555) 

If you're using Postman import the collection of the file unnax_be_test.postman_collection.json

Call the read endpoint with the methods GET, POST, DELETE

Check the stored data using the django admin module and check the status of the scheduled tasks in the queue.

Check the log files in project/logs/

To run the tests execute the next command in the shell of the web container.
```bash
$ pytest -v
```
If you get an error related to the environment variables, execute the next command before run the tests.
```bash
$ source env_variables
```

### Point 4
This point is already covered following the installation steps.