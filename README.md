# oc_epic_events

:books: Made for an [OpenClassrooms](https://openclassrooms.com) studies project.  
`oc_epic_events` is a Django built CRM for an event planning company.

# Features

CRM features 3 different types of users grouped in teams:
1) Management team - CRM admins, use Django admin panel as a frontend to manipulate all DB entries.
2) Sales team - Access to CRM via API, can execute all CRUD operations except on CRM users.
3) Support team - Access to CRM via API, can only interact with assigned events.

PostgreSQL database stores CRM users, clients and related contracts and events.

# Documentation

See full Postman API documentation:  
https://documenter.getpostman.com/view/16341824/TzzBrGTC

# Setup

- First clone this repository and navigate to downloaded folder:
  ``` bash
  git clone https://github.com/PabloLec/oc_epic_events.git
  cd oc_epic_events
  ```

- Then, start a virtual environment:
  ``` bash
  python3 -m venv env
  source env/bin/activate
  ```

- Before running, install the project requirements with:
  ``` bash
  python3 -m pip install -r requirements.txt
  ```

- Make sure to have postgreSQL available on your system.

- In `psql` CLI, type (if you edit below value, also edit `settings.py`):
```sql
CREATE DATABASE epic_events;
CREATE USER epic_events WITH PASSWORD 'epic_events';
ALTER ROLE epic_events SET client_encoding TO 'utf8';
ALTER ROLE epic_events SET default_transaction_isolation TO 'read committed';
ALTER ROLE epic_events SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE epic_events TO epic_events;
\q
```

- Finally, setup DB with:
``` bash
  cd epic_events
  python3 -m manage makemigrations
  python3 -m manage migrate
  python3 -m manage setup
  ```

# Usage

- First, create a superuser with:
  ``` bash
  python3 -m manage createsuperuser
  ```
- Then, run the server:
  ``` bash
  python3 -m manage runserver
  ```
- Website should be served at `127.0.0.1:8000`.
- You can manage your database on `127.0.0.1:8000/admin`  
