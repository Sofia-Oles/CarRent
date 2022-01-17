[![CodeFactor](https://www.codefactor.io/repository/github/sofia-oles/epam_final_project/badge)](https://www.codefactor.io/repository/github/sofia-oles/epam_final_project)
[![buddy pipeline](https://app.buddy.works/epam/epam-final-project/pipelines/pipeline/369262/badge.svg?token=bd35b849fb1efc1a72d3acb47e2e043f49486cb88f011285b0b4678f72cff4d4 "buddy pipeline")](https://app.buddy.works/epam/epam-final-project/pipelines/pipeline/369262)

# EPAM final project
Author: Oleskevych Sofiia

# CarRent is real commercial project for family business.
This project represents the REST-API car rental service, where user can:

1. Register and log in

2. Check the lists of all cars with name, model, price etc.

3. Make an order with time slots. Then user can see list of all his orders.

4. Can retrieve his balance and all operations with profile too.


Admin

1. Perform operations with cars such as adding, editing, deleting

2. Check all clients and orders statistic (in future it`ll be improved by adding filters, search, sorting)


## Install virtual environment

```sh
python -m venv .VENV
.VENV\Scripts\activate
pip install -r requirements.txt
```

## Install project requirements:

```sh
pip install -r requirements.txt
```

## Run the migration scripts to create database schema:

```sh
flask db migrate
flask db update
```

Essential links:
   1) http://192.168.0.107:5000/
   2) http://192.168.0.107:5000/admin/cars

### API operations

* ###### /api/cars

    * GET - get all cars in json format
    * POST - create a new car:
    
    `{"name":"Land Cruiser", "model":"Prado", "year":2017, "price_per_day":80, "people_count":5}`

* ###### /api/car/<id>

    * GET - get the car by id in json format
    * PUT - (work as patch) update the department with a given id
      
      `{"name":"UPDATED Land Cruiser", "model":"UPDATED"}`
  
    * DELETE - delete the car by id
  
* ###### /api/users

    * GET - get all users in json format with their data
    * POST - create a new user:
    
    `{"login": "userIvan1@gmail.com", "name": "Ivan", "surname": "Ivanov", "passport_id":7, "password": "12345", "repeat_password": "12345"}`

* ###### /api/user/<id>

    * GET - get the user by id in json format
    * PUT - (work as patch) update the user with a given id
      
      `{"password":"99999", "password2":"99999"}`
  
    * DELETE - delete the user by id
  
  
* ###### /api/passport

    * POST - create a new passport:
    
    `{"series": "KC", "number": 21899239, "published_by": 4927, "date_of_birth": "2001-12-22"}`

* ###### /api/passport/<id>

    * GET - get the passport by id in json format
    * PUT - (work as patch) update the passport with a given id
      
      `{"series":"KK", "published_by":"7777"}`
 
 * ###### /api/orders

    * GET - get all orders in json format with their data
    * POST - create a new order:
    
    `{"user_id": 1, "car_id":1, "start_date":"2024-01-28", "end_date":"2024-01-29", "price":100}`

* ###### /api/order/<id>

    * GET - get the user by id in json format
    * PUT - (work as patch) update the order with a given id
      
      `{"start_date": "2025-09-09", "end_date":"2025-09-29"}`
  
    * DELETE - delete the order by id
