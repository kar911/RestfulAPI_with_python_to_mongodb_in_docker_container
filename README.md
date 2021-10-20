# RestfulAPI_with_python_to_mongodb_in_docker_container

# `How to deploy the docker containers`

---
 * launch the terminal
 * change the dirctory to where the file is unziped.
 * run `docker-compose build` to build containers form docker-compose.yaml file
 * after build run `docker-compose up -d` this activate containers in detached mode
 * check running container `docker ps --all`
 * for any debug use `docker logs <name of container>` to check for error raised while activating
 * now container are `UP` and runing
 * you can use any thing like curl,postman to access the fully operate the API
---


# `How to access APIs on localhost`


---
 * you can access to api at `localhost:5000/` and propagate furter for more function
 * it resourses 
 * `/delete` accept `delete` request delete_one in the collection with try except to catch some common exceptions
 * `/read`  accept `get` request find_one in the collection with try except to catch some common exceptions
 * `/update` accept `put` request update_one in the collection with try except to catch some common exceptions
 * `/create` accept `post` request insert_one in the collection with try except to catch some common exceptions
 * `/create-multi` accept `post` request  insert_many in the collection with try except to catch some common exceptions
 * `/` accept `get` request check if API is `UP`
 * `/count_discounted_products` accept `get` request  
 * `/list_unique_brands` accept `get` request 
 * `/count_high_offer_price` accept `get` request 
 * `/count_high_discount` accept `get` request 
---

---
# `How to use these APIs to list, add, delete or update products`
---

1. List
   - set the json below with change in `data->new->name`
   - and send the request with it to `/read`
   - recive a custom json response.
   - it list all the record having the same name
   - the quaries must not allow duplicate name
   - but the collection may contain duplicate record as they are dumped
2. Add
   - set the json below with change in `data->new` if want to insert only one or insert multiple `data-multi` having array of entries as your data
   - and send the request with it to `/create` or `/create-multi`
   - recive a custom json response.
   - the quarie for single not allow duplicate name
   - where as multiple user must ensure that there is no duplicate value
4. Delete
   - set the json below with change in `data->new->name` 
   - for deleting a entry
   - and send the request with it to `/delete`
6. Update 
   - set the json below with change in `data->set` including what to update and `data->new->name` including where to update with
   - and send the request with it to `/update`

```

{
    "cred": {
        "ID": "main",
        "password": "loopd"
    },
    "data-multi": [
        {
            "name": "pqrs",
            "brand_name": "wab",
            "regular_price_value": "wab",
            "offer_price_value": "wab",
            "currency": "wab",
            "classification_l1": "wab",
            "classification_l2": "wab",
            "classification_l3": "wab",
            "classification_l4": "wab",
            "image_url": "wab"
        },
        {
            "name": "lmno",
            "brand_name": "wab",
            "regular_price_value": "wab",
            "offer_price_value": "wab",
            "currency": "wab",
            "classification_l1": "wab",
            "classification_l2": "wab",
            "classification_l3": "wab",
            "classification_l4": "wab",
            "image_url": "wab"
        }
    ],
    "data": {
        "new": {
            "name": "new entry",
            "brand_name": "wab",
            "regular_price_value": "wab",
            "offer_price_value": "wab",
            "currency": "wab",
            "classification_l1": "wab",
            "classification_l2": "wab",
            "classification_l3": "wab",
            "classification_l4": "wab",
            "image_url": "wab"
        },
        "set": {
            "name": "set this",
            "brand_name": "wab2",
            "regular_price_value": "wab",
            "offer_price_value": "wab",
            "currency": "wab",
            "classification_l1": "wab",
            "classification_l2": "wab",
            "classification_l3": "wab",
            "classification_l4": "wab",
            "image_url": "wab"
        }
    }
}
```


---
# `docker-compose file`
---


---

     version: '3'                     #docker compose version 3

     services:                         #creating two services web and db

        web:                         #specifying metadata for flaskapi

          build: ./web                         #directing to folder web to create the container with flaskapi

          ports:                         #exposing to port 5000 of machine to 5000 of container

            - "5000:5000"

          links:                         #setting link to db container

            - db

         db:                         #specifying metadata for mongodb

          build: ./db                      #directing to folder db to create the container with mongodb image

          hostname: test_mongodb                      #giving host name

          environment:                       #initialyzing database , username and password for mongodb environment

            - MONGO_INITDB_DATABASE=newdb

            - MONGO_INITDB_ROOT_USERNAME=root

            - MONGO_INITDB_ROOT_PASSWORD=pass

---


---
# `Docker file for flaskAPI`
---


~~~
# download python 3 from docker hub or cached

FROM python:3 # download not only python 3, but also ubuntu operating system image layer

# instruct the image(ubuntu OS with python 3 installed), the working directory is /usr/src/app

WORKDIR /usr/src/app

# copy requirements.txt from local machine (the directory include the docker file)

# to current working directory /usr/src/app

COPY requirements.txt .

# install libraries listed in the requirements.txt on the Ubuntu machine

RUN pip install --no-cache-dir -r requirements.txt

# copy all the files from local machine to the ubuntu

COPY . .

# run python app.py to start the flask API

CMD ["python", "app.py"]

~~~


---
# `docker file for mongodb`
---

~~~
#creating container of mongo:3.6.4
FROM mongo:3.6.4
~~~

---
#  `Run the docker compose file`
---

- [x] launch the terminal
- [x] change the dirctory to where the file is unziped.
- [x] sudo docker-compose build
- [X] sudo docker-compose up -d

---
# `MongoDB`
---

MongoDB server > Database > Collections > Documents

Database is a physical container for collections where each database gets its own set of files of the file system.

Collection is a group of Mongo documents and it's equivalent of an RDBMS table. Collections do not enforce schema.

Document is a set of key value pairs and the documents have dynamic schema. Very similar to JSON
