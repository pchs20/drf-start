# Introduction to Django Rest Framework
This guide is the second part of the tutorial for [Web Applications and Services](https://www.fib.upc.edu/en/studies/bachelors-degrees/bachelor-degree-informatics-engineering/curriculum/syllabus/ASW)
students, and it focuses on extending a Django-based server-side web application to expose
its functionality through a REST API using Django REST Framework (DRF).

It builds upon the foundational Django project from the first part, introducing students 
to RESTful design and API development.


# What is Django REST Framework (DRF)?

Django REST Framework is a powerful and flexible toolkit built on top of Django for 
building Web APIs. It allows you to serialize your data models, handle API requests and 
responses, and apply authentication and permissions in a structured way.

## Components
- **Models**: Represent the data structure of your application. In Django, models are Python 
classes that map to database tables. They handle the interaction with databases, usually 
using relational databases like PostgreSQL, MySQL, or SQLite.

- **Views and ViewSets**: Define how the API behaves when accessed. DRF supports both 
function-based and class-based views. ViewSets simplify the logic for standard CRUD 
operations by bundling related actions together.

- **Serializers**: Convert complex data types (like Django models) into native Python 
datatypes that can then be rendered into JSON or other content types. They also handle 
data validation and deserialization for incoming requests.

- **URLs** (router): Automatically generate URL patterns for your ViewSets. Instead of manually
mapping each URL, routers make it easier to expose your resources via clean RESTful 
endpoints.

- **Permissions and Authentication**: Define who can access or modify certain resources.
DRF integrates with Django's authentication system and supports token-based auth, sessions,
OAuth, and more.

- **Migrations**: Django's system for managing database changes over time. When you 
modify your models, migrations keep the database schema up-to-date.

- **Admin interface**: Django comes with a built-in admin interface that allows you to 
manage your application's data models without writing additional code. This powerful 
feature lets you add, modify, and delete data directly from a user-friendly interface.



# Let's create an example project!

## Initial configurations
### Install Python and pip (same as Django start)
- Install Python ~3.10 from [here](https://www.python.org/downloads/).
Verify the installation by doing:
  ```shell
  python3 --version  
  ```
- Install pip from [here](https://pip.pypa.io/en/stable/installation/).
Verify the installation by executing:
  ```shell
  pip --version  
  ```

### Python virtual environment (same as Django start)
Virtual environments are isolated spaces where you can install and run specific versions 
of Python and its libraries, without affecting the global or system-wide Python 
installation. For this reason, it is very recommended to use them when developing in 
Python. So we will :)
- Navigate to the directory where you want to create the virtual environment (i.e. the
source root of your project).
- Once there, execute the following command to create a virtualenv named `.env`:
  ```shell
  python3 -m venv .env
  ```
  **Note**: Remember to add `.env` directory to the `.gitignore` file!


- Activate the virtual environment (if macOS or Linux):
  ```shell
  source .env/bin/activate
  ```
- Activate the virtual environment (if Windows):
  ```shell
  .env\Scripts\activate
  ```
From now on, when installing new packages or executing your project, make sure **you have
the virtual environment activated**!

### Install Django REST Framework (new!)
- Execute:
  ```shell
  pip install djangorestframework 
  ```
- Verify the installation with:
  ```shell
  pip show djangorestframework
  ```
- Add DRF to the `INSTALLED_APPS` in `library/settings.py`:
  ```python
  INSTALLED_APPS = [
    ...,
    'rest_framework',
  ]
  ```

### Requirements file (same as Django start)
To manage your project dependencies easily, use a requirements.txt file. This file lists 
all the Python packages your project needs. Therefore, **when installing a new package
or external library** (like we have just done with Django), execute:
```shell
pip freeze > requirements.txt
```
This lists all the dependencies inside the virtual environment into a `requirements.txt`
file. This makes it easy for other developers (such as your teammates) to update their
virtual environment by running:
```shell
pip install -r requirements.txt
```
Which installs all the requirements listed in the file to your activated virtual 
environment.


## New application, first serializer and new view
Let's create a new application named **api**.
### Create the application
Execute the following:
```shell
python manage.py startapp api
```

This command should have created the following package:
```
.
├── api
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py

```

Given the characteristics of the application, we will not need 
`migrations`, `admin.py` and `models.py`. Feel free to delete them.

As always, we have to add the new application to the `INSTALLED_APPS` list in
`library/settings.py`:
```python
INSTALLED_APPS = [
    ...,
    'api',
]
```

### Define a serializer
Serializers should be defined inside a `serializers.py` file.
Let's create a new file `api/serializers.py` and add the following code:
```python
from rest_framework import serializers
from books.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
```

### Define a view
With DRF, views can inherit from different classes depending on the type of view you want to
define. We can start with a simple one, which will allow us to create, update, delete and
list books. This is a `ModelViewSet`, which is a DRF class that provides the basic CRUD:
```python
from api.serializers import BookSerializer
from books.models import Book
from rest_framework import viewsets


class BooksView(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```


### Define the route
- Create a file `api/urls.py` and add the following code to define the URL for the 
books view:
  ```python
  from rest_framework import routers
  from . import views
  
  router = routers.DefaultRouter()
  router.register(r'books', views.BooksView)
  
  urlpatterns = []
  
  urlpatterns += router.urls
  ```
- In the `library/urls.py` include the `api` application's URLs:
  ```python
  from django.contrib import admin
  from django.urls import path, include
  
  
  urlpatterns = [
      path('admin/', admin.site.urls),
      path('books/', include('books.urls')),
      path('api/', include('api.urls')),
  ]
  ```

### Validate everything works
Visit `http://127.0.0.1:8000/api/books/`. You should be able to see a list of books and
also create, update or delete them.


## Add Swagger documentation
To add Swagger documentation to your Django REST Framework project, you can use the
`drf_yasg` package. This package generates OpenAPI 2.0 specifications for your API and provides a
user-friendly interface to explore your API. Let's go!

### Install drf_yasg
Install the package:
  ```shell
  pip install drf-yasg
  ```

### Add drf_yasg to your project
Add `drf_yasg` to the `INSTALLED_APPS` list in `library/settings.py`:
  ```python
  INSTALLED_APPS = [
      ...,
      'drf_yasg',
  ]
  ```

### Define the /docs route
Modify `api/urls.py` to include the Swagger documentation:
```python
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.urls import path
from rest_framework import permissions, routers
from . import views


schema_view = get_schema_view(
   openapi.Info(
      title='Library example project',
      default_version='v1',
      description='API for books as an example',
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

router = routers.DefaultRouter()
router.register(r'books', views.BooksView)

urlpatterns = [
    path(
       'docs/',
       schema_view.with_ui('swagger', cache_timeout=0),
       name='schema-swagger-ui',
    ),
]

urlpatterns += router.urls
```

### Validate everything works
Visit http://127.0.0.1:8000/api/docs/. You should be able to see (and use) the Swagger UI with the API documentation.
Nice, right?

We are done! :)
