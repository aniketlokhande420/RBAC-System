# Django RBAC API

This project is a Django-based RESTful API for building a Role Based Authentication System with additional reporting functionalities.

## Features

- **User APIs**: Creates user and lists all users. Note that while are creating the user we are assigning the role to user here itself.
- **Permission Management APIs**: Creates permissions and lists all peremissions. Note only admin and supervisor can create permissions.
- **Role Management APIs**: Retrieves all roles with their assigned permissions. Assigns permissions to a role. Only admin can access this API.
- **Access Validation API**: Checks if a user can perform a particular action on a particular resource. 
- **Get Logs API**: Retrieves logs for last N hours, defaults to 24 Hrs.

## Technology Stack


- **Backend Framework**: Django (Python)
- **Database**: SQLite3

## Setup and Installation

### Prerequisites

- Python 3.x
- `pip` (Python package manager)
- `virtualenv` (optional but recommended)

### Installation Steps

1. **Clone the repository:**

    ```bash
    git clone https://github.com/aniketlokhande420/RBAC-System.git
    cd RBAC-System
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3. **Install dependencies:**

    ```bash
    pip install django
    ```

4. **Apply migrations:**

    ```bash
    python manage.py migrate
    ```

5. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

6. **Access the application:**

    - The application will be available at `http://127.0.0.1:8000/`.


## How to Run the APIs(Postman)

### 1. Import the Postman Collection.

- **Step 1: Create User**

  Make a `POST` request to the `/user` endpoint
  ``` POST http://127.0.0.1:8000/user```
 - Send username, password and role. We are defining the role to user here itself.
 - We have three roles `staff`, `superevisor` and `admin`.
 - It is perferred that you create a user with admin role as it has more acess.


- **Step 2: Create Permission**
Make a `POST` request to the `/permission` endpoint
```bash
POST curl --location 'http://127.0.0.1:8000/permissions/' \
--data '{"permission_name":"gcp-RDBMS",
"resource":"RDBMS",
"action": "CreateDB",
"username": "admin1"}'
```    
-Only Supervisor and admin can access this endpoint.

- **Step 3: Attach Permission to Role**
Make a `POST` request to the `/roles` endpoint
```bash
curl --location 'http://127.0.0.1:8000/roles/' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=CskwKmwagt0cTvWjWaeXDA40beTZ44zt' \
--data '{"username":"admin1",
"permission_name":"gcp-RDBMS",
"role_to_assign_permission":"admin"}'
```
-Only admin users can access this endpoint.

- **Step 4: Access Validation**
Make a `POST` request to the `/access-validation` endpoint
```bash
curl --location 'http://127.0.0.1:8000/access-validation/' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=CskwKmwagt0cTvWjWaeXDA40beTZ44zt' \
--data '{"username":"admin1",
"action":"CreateDB",
"resource":"RDBMS"}'
```
- Any user can check if he has permissions to perform particular action on a particular resource, the combination of action and resource should be exactly same as while defining the permision to get success.

- **Step 4: Access Validation**
Make a `POST` request to the `/logs` endpoint
```bash
curl --location 'http://127.0.0.1:8000/logs?hours=12' \
--header 'Cookie: csrftoken=CskwKmwagt0cTvWjWaeXDA40beTZ44zt'
- Get the logs of last N hours, defauls to 24 hours if hours parameter not set.
```



## Contribution

Feel free to open issues, submit pull requests, or suggest improvements. All contributions are welcome!
