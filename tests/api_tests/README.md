# Postman API Test Automation

This is my first try to write API automation testing using postman. 

### Steps

- Make sure that newman is installed. If not, follow these steps:
    * open cmd
    * type `node -v`
    * if not installed, download node from *[here](https://nodejs.org/en/download/)*.
    * `npm install -g newman`
    
- start the application 

- cd to this location 
    `cd tests/api_tests`
- type `newman run SuperPosAPIs.postman_collection.json -e SuperPos.postman_environment.json --verbose`