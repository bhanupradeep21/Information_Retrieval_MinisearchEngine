import requests
from urllib.parse import quote

def get_wikipedia_category_pages(category_name):
    base_url = "https://en.wikipedia.org/w/api.php"
    params = {
        'action': 'query',
        'format': 'json',
        'list': 'categorymembers',
        'cmtitle': f'Category:{category_name}',
        'cmlimit': 500  # You can adjust the limit based on your needs
    }

    response = requests.get(url=base_url, params=params)
    data = response.json()

    if 'query' in data and 'categorymembers' in data['query']:
        pages = data['query']['categorymembers']
        page_urls = []
    
        for page in pages:
            title = page['title']
            if 'Category:' not in title:
                formatted_title = title.replace(' ', '_')
                encoded_title = quote(formatted_title)
                url = f"https://en.wikipedia.org/wiki/{encoded_title}"
                page_urls.append(url)

        return page_urls
    else:
        print("Error retrieving data from Wikipedia API.")
        return None

def save_urls_to_file(urls, filename):
    with open(filename, 'a') as file:
        for url in urls:
            file.write(url + '\n')

categories_file_path = 'unique.txt'

def read_categories_from_file(file_path):
    with open(file_path, 'r') as file:
        categories = [line.strip() for line in file.readlines()]
    return categories

# Read categories from file
categories = read_categories_from_file(categories_file_path)

# Now 'categories' is a list containing all the categories
# print(categories)

for category_name in categories:
    print(category_name+'......................')
    output_filename = 'links.txt'
    urls = get_wikipedia_category_pages(category_name)

    if urls:
        # Save URLs to a text file
        save_urls_to_file(urls, output_filename)
        print(f"URLs saved to {output_filename}")
    else:
        print("No URLs to save.")

