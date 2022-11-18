## Homework 19
This application built based on Flask. There're many interesting functions in the app. There're three base tables in the database like in previous homeworks but some new options was added. First of all - a division on two roles - admin and user. The user have access to the next options:

 - To watch a list of all movies, genres and directors
 - To get an information about movie, genre or director by its id
 - To register in the app
 - To watch his own registration info
 - To update or delete his own account
 
 Unlike the user, the admin has access:
 - To browse, create, update or delete records in the movie, genre or director tables
 - To get full access to users data. Admin can watch info about any user including himself, update or delete any existing user's data

The application built by using: Flask, SQLAlchemy, Marshmallow, Flask-RestX. 

 ---
The project's structure: 
 - dao - DAOs to work with different tables 
 - service - classes provided a business logic
 - views - there are CBVs to work with different routes
 - implemented- there're DAO and Service classes' instances
 - config - configuration class with different settings 
 - constants - a file containing constants like hash algorithms, salt, secrets, required keys to check received data, etc.
 - requirements.txt - file with the project's dependencies
 - app.py - a main file to start the application
 - setup_db - a file with SQLAlchemy instance
 - movies.db - a database with tables described above
 - test_api.http - a file with test requests
 - README.md - this file with app info
 ---
 The project was created in 18 November 2022 by Aleksey Mavrin
