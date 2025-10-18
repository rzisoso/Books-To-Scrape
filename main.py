# main.py
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm # 引入一个漂亮的进度条库，让等待过程更友好
import time

def scrape_all_books():
    """
    爬取 books.toscrape.com 网站上所有书籍的数据。
    """
    base_url = 'http://books.toscrape.com/catalogue/'
    current_url = base_url + 'page-1.html'
    all_books_data = []

    # 我们知道总共有50页，用tqdm创建一个可视化进度条
    for page_num in tqdm(range(1, 51), desc="正在爬取所有书籍页面..."):
        try:
            response = requests.get(current_url)
            # 检查请求是否成功
            response.raise_for_status() 
        except requests.exceptions.RequestException as e:
            print(f"\n访问 {current_url} 出错: {e}")
            break # 如果出错则停止

        soup = BeautifulSoup(response.content, 'html.parser')

        articles = soup.find_all('article', class_='product_pod')
        for article in articles:
            title = article.h3.a['title']
            
            # 清理价格数据，并转换为浮点数
            price_str = article.find('p', class_='price_color').text
            price = float(price_str.replace('£', ''))
            
            # 获取星级评价并转换为数字
            rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
            # 'star-rating Three' -> class列表的第二个元素是星级
            rating_class = article.find('p', class_='star-rating')['class'][1] 
            rating = rating_map.get(rating_class, 0) # 如果没找到，默认为0星
            
            all_books_data.append({
                '标题': title,
                '价格(£)': price,
                '星级': rating
            })
        
        # 寻找下一页的链接
        next_page_tag = soup.find('li', class_='next')
        if next_page_tag and next_page_tag.a:
            current_url = base_url + next_page_tag.a['href']
            time.sleep(0.1) # 增加一个微小的延时，做一个有礼貌的爬虫
        else:
            print("\n已到达最后一页。")
            break 
            
    return pd.DataFrame(all_books_data)

# --- 主程序 ---
if __name__ == "__main__":
    print("开始爬取 books.toscrape.com ...")
    books_df = scrape_all_books()

    if not books_df.empty:
        # 保存数据到CSV文件，编码设为 'utf-8-sig' 以防止在Excel中打开中文乱码
        output_path = 'books_data.csv'
        books_df.to_csv(output_path, index=False, encoding='utf-8-sig')

        print("\n✅ 任务完成！")
        print(f"总共爬取了 {len(books_df)} 本书的数据。")
        print(f"数据已保存到 {output_path}。")
        print("\n数据预览：")
        print(books_df.head())
    else:
        print("\n❌ 未能爬取到任何数据。")