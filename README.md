# Book Recapper
For when you need to get back into a book you abandoned partway.

## How to Run the Application

1. [Install Poetry](https://python-poetry.org/docs/#installation)
2. Install the required dependencies using Poetry:

       poetry install

3. Run the Streamlit App

      streamlit run bookrecapper/book_recapper.py

## Setting Up the Development Environment
1. [Install Poetry](https://python-poetry.org/docs/#installation)
2. Install the required dependencies using Poetry:

       poetry install

3. Install the pre-commit hooks:

       poetry run pre-commit install


## Python Dev Stuff

1. Dependency Management
2. Pre-commit hooks
3. Linting
4. Testing

## Todos

1. Parallelize API calls while being mindful of rate limits.
2. PaLM seems to be pretty bad at following instructions, try GPT-3.5-turbo
3. Implement BM25
