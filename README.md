# Interactive Bookstore Dashboard

An end-to-end data project that scrapes book market data using Python and presents it in an interactive, filterable web dashboard built with Streamlit and Plotly.

![Books Dashboard Screenshot](Books3.gif)

---

## Project Overview

This project demonstrates a complete data workflow: from data acquisition (web scraping) to data analysis (Pandas) and finally to data visualization in a custom-themed, interactive web application (Streamlit).

The final product is a "Market Intelligence Dashboard" for the `books.toscrape.com` website, allowing users to dynamically filter and analyze the bookstore's inventory by price and star rating.

## Live Demo
**[ -> View the Live Dashboard Here <- ](https://books-to-scrape-dashboard.streamlit.app/)**

## Key Features

* **Web Scraper (`main.py`):** A robust Python script using `Requests`, `BeautifulSoup`, and `tqdm` to scrape all 1,000 book entries across 50 pages, saving the data to a clean `books_data.csv`.
* **Interactive Dashboard (`app.py`):** A beautiful web app built with Streamlit.
* **Dynamic Filtering:** Users can filter data in real-time using sidebar controls for price range and star rating.
* **Data-Driven KPIs:** The dashboard displays key metrics (Total Books, Avg. Price, Avg. Rating) that update instantly with filters.
* **Rich Visualizations:** Uses `Plotly Express` to create interactive histograms and bar charts with custom styling.
