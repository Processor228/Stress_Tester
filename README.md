# Stress Tester

This repository contains the backend part of the implementation
of a competitive programming stress testing platform.

What exactly is stress testing in Competitive Programming? Let me explain...

Suppose you have a solution to some problem A that you are very sure of (a bruteforce, for instance). And you have a solution B for that problem that (maybe more optimal) you are not sure of. So, you 
may wanna run some tests to figure out, whether their output coincide or, more importantly,
differ. This application (with some good UI) may come in handy for such problems. (This will be useful only in case there is just
one correct output for an input)

# Local Deployment procedure:

#### 1) Make sure you have docker installed

#### 2) Clone the repository (or pull the changes)

#### 3) Build the testing sandbox image:
```
docker build -t sandbox_container testing_env/
```

#### 4) Build the application image:
```
docker build -t containerized_stress_backend .
```

#### 5) Prepare a .env file
```
POSTGRES_PSW=Password
POSTGRES_USR=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB_NAME=Stress
OAUTH_SECRET_KEY=2d34fdsd345ggermfkwlm-efg2t-gfwerg-24
```

#### 6) Run the container
```
docker run \ 
    --network host \ 
    --env-file ./.env \
    -v /var/run/docker.sock:/var/run/docker.sock \
     containerized_stress_backend
```
Why specifying ``-v /var/run/docker.sock:...`` ? <br>
``TL; DR``: to solve docker-in-docker situation. <br>
Because now, the isolation of the tested solutions is carried out using docker containers. 
So, the application launches a number of docker sandboxes and, 
if necessary, puts code in them, runs a testing procedure, etc. In
order not to install docker inside the container with the application, we
simply specify the path to the socket of the external docker daemon. Thus, we have
there is only one dockerd in the entire system, and it runs both
the server application and the test sandboxes, and the application sends commands
to it when needed.


# Project structure:
We have a monolith here, the logic is separated between multiple modules: one handles `room management` 
(just code files user wish to test) and `stress-testing` logic, where the most important
stuff is. Also there are `user management`, and `OAuth` modules. <br>
Each module has:
- `schemas.py` - for types used in the module
- file with helping procedures (e.g. crud or like testing implementation)
- `router` - for endpoints
- `models` - possibly db models

`main.py` contains the FastApi class instance and there all the modules endpoints are binded to it.<br>
`db_connection` - connects to db.

---
There also is directory `testing_env`. It has `Dockerfile` for lightweight alpineOS-based container, which is used as testing sandbox. It has "testing_pipeline.py" code that drives the testing procedure.


Seems to be easy and structured... let's see what I and others will say after a while...

