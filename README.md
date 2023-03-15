# Inventory Management System

A website for Inventory mangement - using Django, SQLite3
## Installation

To installation this project run
### Step 1

```bash
  git clone https://github.com/gavinleehau/Django_InventoryManagementSystem.git
```

### Step 2
Create virtual environment
```bash
  python -m venv <name_of_virtualenv>
  <name_of_virtualenv>\Scripts\activate
```

### Step 3
Install dependencies using
```bash
  pip install requirements.txt
```

### Step 4
After the first time, the following can be run to migrate model changes in any app
```bash
  python manage.py makemigrations
  python manage.py migrate
```

### Step 5
Use the following command to create an admin user
```bash
  python manage.py createsuperuser
```

### Step 5
Use the following command to run the server
```bash
  python manage.py runserver
```

### Thank you
