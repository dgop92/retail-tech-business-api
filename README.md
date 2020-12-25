# Simple Retail Businnes API

Simple Retail Bussines is an API that allows you to control exits and entries while collecting useful data to create insights for your business

## Project setup

If you use anaconda replicate the environment using my-retail-env.yml otherwise use requirements.txt to download the dependencies with pip

### Duplicate environment using conda

```
conda env create -f my-retail-env.yml
```

### Download the dependencies with pip

```
pip install -r requirements.txt
```

### Before running the project apply the respective migrations

```
python manage.py migrate
```

### Run the API in the localhost

```
python manage.py runserver
```

## API reference

The API reference was created using postman, click in the following link to open it [Docs](https://documenter.getpostman.com/view/12352026/TVsxB6Z3)
