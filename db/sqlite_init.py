import sqlite3
from urllib.parse import urlparse

def create_database(db_path: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create table for product links
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS product_links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            link TEXT NOT NULL UNIQUE,
            status TEXT DEFAULT 'not_processed',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create table for shop links
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS shop_links (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                        link TEXT NOT NULL UNIQUE,
                        status TEXT DEFAULT 'not_processed',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                     )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def insert_product_link(db_path: str, link: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        parsed = urlparse(link)
        shop_path = parsed.scheme + "://" + parsed.netloc + parsed.path.split("/product/")[0]
        cursor.execute("SELECT 1 FROM shop_links WHERE link = ?", (shop_path,))
        if cursor.fetchone():
            print(f"{shop_path} already exists in shop_links, skipping insert for {link}.")
            conn.close()
            return

        cursor.execute('INSERT INTO product_links (link) VALUES (?)', (link,))
        conn.commit()

    except sqlite3.IntegrityError:
        print(f"Link already exists: {link}")
    
    conn.close()

def insert_shop_link(db_path: str, link: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute('INSERT INTO shop_links (link) VALUES (?)', (link,))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Link already exists: {link}")
    
    conn.close()

def get_product_links(db_path: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('SELECT link FROM product_links WHERE status = "not_processed"')
    links = cursor.fetchall()
    
    conn.close()
    return [link[0] for link in links]

def product_link_processed(db_path: str, link: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('UPDATE product_links SET status = "processed" WHERE link = ?', (link,))
    conn.commit()
    
    conn.close()