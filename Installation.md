# Installation Guide
## Requirement
* Python 3.11 or higher
* git
* pip

## Installation guide
clone the repository.
    ```bash
    git clone https://github.com/opxz7148/ku-polls.git
    ```

Change to working directory.
```bash
cd ku-polls
```

Create and activate virtual environment
```
python -m venv env
```
```
env\Scripts\activate
```

Install require packages
```bash
pip install -r requirements.txt
```

Migrate database
```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```

Rename sample.env to .env
```bash
move sample.env .env
```