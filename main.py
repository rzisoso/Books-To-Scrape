# main.py
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm # Import a nice progress bar library
import time

def scrape_all_books():
    """
    Scrapes all book data from the books.toscrape.com.
    """
    base_url = 'http://books.toscrape.com/catalogue/'
    current_url = base_url + 'page-1.html'
    all_books_data = []

    # There are 50 pages total, so create a progress bar with tqdm
    for page_num in tqdm(range(1, 51), desc="Scraping all pages..."):
        try:
            response = requests.get(current_url)
            # Check if the request was successful
            response.raise_for_status() 
        except requests.exceptions.RequestException as e:
            print(f"\nError occurred while accessing {current_url}: {e}")
            break # Stop if there's an error

        soup = BeautifulSoup(response.content, 'html.parser')

        articles = soup.find_all('article', class_='product_pod')
        for article in articles:
            title = article.h3.a['title']
            
            # Clean the price data and convert to float
            price_str = article.find('p', class_='price_color').text
            price = float(price_str.replace('£', ''))
            
            # Get the star rating and convert it to number
            rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
            # e.g.,'star-rating Three' -> the second class is the rating
            rating_class = article.find('p', class_='star-rating')['class'][1] 
            rating = rating_map.get(rating_class, 0) # Default to 0 if not found
            
            all_books_data.append({
                'Title': title,
                'Price(£)': price,
                'Rating': rating
            })
        
        # Find the link for the next page
        next_page_tag = soup.find('li', class_='next')
        if next_page_tag and next_page_tag.a:
            current_url = base_url + next_page_tag.a['href']
            time.sleep(0.1) # Add a small delay to be a polite scraper
        else:
            print("\nReached the last page.")
            break 
            
    return pd.DataFrame(all_books_data)

# --- Main Execution ---
if __name__ == "__main__":
    print("Starting to scrape books.toscrape.com ...")
    books_df = scrape_all_books()

    if not books_df.empty:
        # Save data to CSV file, with encoding set to 'utf-8-sig' to prevent garbled Chinese characters in Excel
        output_path = 'books_data.csv'
        books_df.to_csv(output_path, index=False, encoding='utf-8-sig')

        print("\n Task Completed!")
        print(f"Successfully scraped books: {len(books_df)}")
        print(f"Data saved to {output_path}.")
        print("\nPreview of the data:")
        print(books_df.head())
    else:
        print("\n Failed to scrape any book data.")