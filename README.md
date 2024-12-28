# WIKIMEDIA WORDCLOUD GENERATOR

Dataset consists of 10859 gathered from Wikimedia.

## Project Overview
The **Wikimedia Wordcloud Generator** is a Python-based web application that allows users to generate word clouds and bar plots from a dataset collected from Wikimedia. The application uses the power of Natural Language Processing (NLP) to clean, process, and visualize textual data from Wikipedia articles.

The dataset consists of 10,859 entries gathered from Wikimedia, and it allows users to explore various text mining techniques like title generation, word cloud creation, and bar plot visualization based on term frequency.

---

## Features

- **Generate Title**: Generate a title based on the provided parameters.
- **Gather Page**: Gather the page from the dataset.
- **Data Cleaning**: Demonstrates the cleaning process.
- **Bar Plot Generation**: Create a bar plot for term frequency data.
- **Word Cloud Generation**: Generate a word cloud of terms from the dataset.

---

## Installation

### Requirements

- Python 3.7 or higher
- Flask
- Other Python dependencies listed in `requirements.txt`

### Steps to Run the Project Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/giraydorukyurt7/WikiMedia-WordCloud-Generator.git
   cd WikiMedia-WordCloud-Generator
   ```
2. Set up a virtual environment:
    ```bash
    python -m venv venv
    ```
3. Activate the virtual environment:
    On Windows:
    ```bash
    venv\\Scripts\\activate
    ```
    On Mac/Linux:
    ```bash
    source venv/bin/activate
    ```
4. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5. Run the Flask application:
    ```bash
    python WikiMedia_Text_Mining_NLP/wikimedia_text_mining_nlp.py
    ```
6. Open a browser and navigate to http://127.0.0.1:5000/ to view the app.


-----

## Usage
Once the app is running, you can interact with the following sections:

### Generate Title
* Page No: Select the page number to use for title generation.
* Use All: Check this option to use the entire dataset.
* Title Size: Specify the size of the generated title.

### Get Page
* Page No: Specify the page number you want to extract text from.
* Clean Page: Clean the extracted page text.

### Get Bar Plot
* Page No: Specify the page number for which you want to generate a bar plot.
* Use All: Use the entire dataset.
* Minimum Term Frequency: Set the minimum frequency of terms to be displayed.

### Get Word Cloud
* Page No: Specify the page number for word cloud generation.
* Use All: Generate a word cloud using the entire dataset.