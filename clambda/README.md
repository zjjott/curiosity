# cloud lambda
implement lambda function base on cloud,like AWS lambda  
Python lambda core code base on [Celery](http://celery.readthedocs.io/en/latest/)

## feature

* TODO dynamic function loading
* TODO unlimited horzontal expansion
* TODO quasi-realtime task
* TODO router function
* TODO limit function execute time and memory
* TODO schedule task

## process

1. user save code into db
2. set trigger method
3. trigger by: send message
4. worker load task code, ast.literal_eval(How about hot code pre load?)