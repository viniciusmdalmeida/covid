# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* Quick summary
* Version
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### How do I get set up? ###

* Summary of set up
* Configuration
* Dependencies
* Database configuration
* How to run tests
* Deployment instructions

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact

### How to start airflow 
1. Set AIRFLOW_HOME
$ export AIRFLOW_HOME=./config/airflow

2. Start database (Optional)
$ airflow initdb 

3. Start scheduler (Optional)
$ airflow scheduler

4. Start webserver 
$ airflow webserver -p 8080

5. Run dag
$  airflow backfill dataops -s 2020-06-12

### How to see mlflow server
1. Go to mlflow path
$cd ./data

2. Start ui
$ mlflow ui

