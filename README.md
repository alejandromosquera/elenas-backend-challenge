The authentication mode is basic auth
The solution contains the source and the Postman collection in order to test the api manually. Also yuo can see the test in test.py file in api app.

The next are the info required:

Admin Panel: 
    http://127.0.0.1:8000/admin/

    Use the any of these users:

    email: admin@example.com
    username: admin
    password: admin

    username: user1
    password: abcdario123

    username: user2
    password: abcdario123


run app:
    python manage.py runserver

run tests:
    python manage.py test