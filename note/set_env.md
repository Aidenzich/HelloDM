## Start with Pipenv in Mac
- Use below command to setup pipenv.
    ```
    brew install pipenv
    pipenv --python 3.9
    pipenv shell
    ```
  - Use `pipenv install -r requirements.txt` to install necessary packages.
  - Use `pip freeze > requirements.txt` to create new requirements file.
- Select python interpreter.
  - *⌘ + ⇧ + P* in mac.
  - Choose Python interpreter with `pipenv`.