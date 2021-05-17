The authentication mode is basic auth
The solution contains the source and the Postman collection in order to test the api manually. Also y0uo can see the tests in test.py file in api app.

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

* Los usuarios se deben autenticar   DONE
* Las tareas son privadas. Solo las puede administrar su dueño DONE
* Los usuarios pueden agregar, editar, eliminar y marcar como completa/incompleta las tareas DONE
* El listado de tareas debe ser paginado DONE
* Agregar validaciones, como no aceptar tareas sin descripción, etc DONE
* Buscar por descripción DONE
* Escribe test unitarios en el primer commit DONE
