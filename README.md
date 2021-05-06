# Cryptocurrency Exchange Platform

## Description
REST API for cryptocurrency exchange service based on Flask and SQLAlchemy.

First, a user should sign up in the platform. After that, he/she will be given
1000 money units. A user can get buying and selling rate for each currency. 
New currencies can be added at any moment. Any user has a wallet with currencies 
and a balance (in money units). Currency rates change randomly every 10 seconds.

It can happen that at some moment selling rate is higher than buying rate.
As the overall amount of currency and money units is not limited, user abuse it
to become rich :) `bot.py` is just a simple demonstration.


## Documentation
Examples of requests to API can be seen here:
[Postman Documentation](https://documenter.getpostman.com/view/11613270/Tz5tYbRr#8491abf0-d2a7-4f6e-a2e3-83614f8eaeee)

## Usage

### Create database
    make migrate

### Run server
    make up

### Create venv:
    make venv

### Run tests:
    make test
    
### Run linters:
    make lint
    
### Run formatters:
    make format
