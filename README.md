# REST API Data Fetcher & Visualizer CLI

A Python Command Line Interface (CLI) application that fetches live JSON data from the public GitHub API. It parses repository data for a specified user, calculates core metrics (totals, averages, maximums), formats date-time strings, and outputs a clean analytical summary directly to the terminal.

## Features
* **Live API Integration:** Uses the `requests` module to fetch real-time data from the GitHub Users API.
* **JSON Parsing:** Extracts relevant data points (stars, sizes, timestamps) from complex nested dictionaries and lists.
* **Data Metrics Calculation:** Computes total counts, averages, and maximum values algorithmically.
* **Datetime Handling:** Converts ISO 8601 timestamp strings from the API into human-readable Python `datetime` objects.
* **Interactive CLI:** Prompts the user for dynamic input and displays formatted, readable data tables in the console.

## Technologies Used
* Python 3.x
* `requests`
* Built-in `json` parsing logic
* Built-in `datetime` module

## Prerequisites
To run this application, you need Python installed on your machine along with the `requests` library.

Install the required dependency using pip:
```bash
pip install requests