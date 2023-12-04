#THINGS THAT WORK
# 1. Login/REGISTER
# 2. POST - POST,PUT,GET,GET/1,DELETE
# 3. Category - POST,PUT,GET,GET/1,DELETE
# 3. Courts - POST,PUT,GET,GET/1,DELETE

# POST
# POST
# POST


# 1. Register

{
    "username": "333",
    "password": "333",
    "first_name": "333",
    "last_name": "333",
    "email": "333@email.com",
    "bio": "333",
    "profile_image_url": "http://333.com"
}

# 2. Post

{
    "pickle_user": 1,
    "title": "first post",
    "image_url": "http://first.com",
    "content": "first",
    "court_id": 0
}

# 3. Category

{
    "label": "Delete"
}

# 4. Courts

{
    "title": "1st court",
    "court_image_url": "http://first.com",
    "city": "Nashville",
    "state": "TN",
    "number_of_courts": 10,
    "open_hours": "9am - 6pm"
}

#UPDATE
#UPDATE
#UPDATE

# 1. Post

{
    "id": 1,
    "pickle_user": {
        "user": {
            "id": 3,
            "username": "333",
            "first_name": "333",
            "last_name": "333",
            "email": "333"
        },
        "profile_image_url": "http://333.com",
        "bio": "333"
    },
    "title": "UPDated",
    "publication_date": "2023-12-04",
    "image_url": "http://first.com",
    "content": "first",
    "court_id": 0,
    "categories": [],
    "is_owner": true
}

# 2. Category

{
    "label": "Delete"
}

# 3. Courts

{
    "title": "1st court",
    "court_image_url": "http://first.com",
    "city": "Nashville",
    "state": "TN",
    "number_of_courts": 10,
    "open_hours": "9am - 6pm"
}