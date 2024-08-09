import os
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import time

# Create a folder named "ALL_TEXTS" if it doesn't exist
output_folder = "ALL_TEXTS"
os.makedirs(output_folder, exist_ok=True)

# Function to extract text from <p> tags
async def extract_text_from_url(url, session):
    try:
        # Specify multiple user agents to rotate
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.37",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 YaBrowser/21.6.2.855 Yowser/2.5 Safari/537.36",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.37",
        ]

        headers = {"User-Agent": user_agents[hash(url) % len(user_agents)]}

        async with session.get(url, headers=headers, timeout=10) as response:
            response.raise_for_status()

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(await response.text(), 'html.parser')

            # Extract text from all <p> tags
            paragraphs = soup.find_all('p')
            text = "\n".join([p.get_text() for p in paragraphs])

            return text
    except aiohttp.ClientError as e:
        print(f"Aiohttp error processing URL {url}: {e}")
    except Exception as e:
        print(f"Error processing URL {url}: {e}")
    return None

# Function to process a batch of links and save text to files
async def process_batch(file_path, session):
    with open(file_path, "r", encoding="utf-8") as file:
        wiki_links = file.readlines()

    for i, wiki_link in enumerate(wiki_links, start=1):
        wiki_link = wiki_link.strip()
        text = await extract_text_from_url(wiki_link, session)

        if text is not None:
            # Save the text to a file in the "ALL_TEXTS" folder
            filename = os.path.join(output_folder, f"{i}.txt")
            with open(filename, "w", encoding="utf-8") as output_file:
                output_file.write(text + "\n" + wiki_link)

            print(f"Processed Document {i}: {wiki_link} and saved to {filename}")
        else:
            print(f"Skipping Document {i}: {wiki_link} due to an error")

# Asynchronous main function
async def main():
    # Folder containing files with links
    link_folder = "split_links"

    # List all files in the link folder
    link_files = [os.path.join(link_folder, file) for file in os.listdir(link_folder) if file.endswith(".txt")]

    # Create an aiohttp session for asynchronous requests
    async with aiohttp.ClientSession() as session:
        start_time = time.time()

        for link_file in link_files:
            await process_batch(link_file, session)

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"All documents processed and saved. Elapsed time: {elapsed_time:.2f} seconds")

# Run the event loop
asyncio.run(main())
