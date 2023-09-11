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


## Todos

1. Allow user to select the correct chunk before summarizing.
2. Divide chunks more sensibly (sentences, chapter breaks, etc.).
3. Parallelize API calls while being mindful of rate limits.
4. PaLM seems to be pretty bad at following instructions and GPT-3.5-turbo seems to be much better. The API for the latter is paid and heavily rate-limited, however. Simply taking the final prompt text from this application and pasting it in ChatGPT gives a much better result.
