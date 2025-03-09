import os
import json
import requests
from bs4 import BeautifulSoup
from scholarly import scholarly

def fetch_scholar_data(search_term):
    # Generate dynamic folder name based on search term
    folder_name = f"scholar_results_{search_term.replace(' ', '_').lower()}"
    
    # Create output directory
    os.makedirs(folder_name, exist_ok=True)

    # Search Google Scholar
    search_results = scholarly.search_pubs(search_term)

    journal_data = []
    
    for i, result in enumerate(search_results):
        if i >= 20:  # Limit to 20 results to avoid excessive requests
            break
        
        try:
            title = result.get("bib", {}).get("title", "Unknown Title")
            authors = result.get("bib", {}).get("author", "Unknown Author")
            url = result.get("pub_url", "No URL")
            doi = result.get("pub_id", None)  # DOI might not always be available
            
            # Fetch and save the article's HTML page
            if url != "No URL":
                response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
                if response.status_code == 200:
                    file_path = os.path.join(folder_name, f"article_{i+1}.html")
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write(response.text)
            
            # Store metadata
            journal_data.append({
                "title": title,
                "author_name": authors,
                "doi": doi,
                "journal_url": url
            })

        except Exception as e:
            print(f"Error processing result {i+1}: {e}")
    
    # Save metadata as JSON
    json_file_path = os.path.join(folder_name, "journal_metadata.json")
    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(journal_data, json_file, indent=4)

    print(f"Scraping complete. Results saved in '{folder_name}'.")

from urllib.parse import urljoin

def extract_images_from_articles(search_term):
    # Generate dynamic folder names
    html_folder = f"scholar_results_{search_term.replace(' ', '_').lower()}"
    image_output_folder = f"{html_folder}_images"
    
    # Create folder to save images
    os.makedirs(image_output_folder, exist_ok=True)

    # List all HTML files in the given folder
    html_files = [f for f in os.listdir(html_folder) if f.endswith(".html")]

    for html_file in html_files:
        html_path = os.path.join(html_folder, html_file)

        # Read the HTML content
        with open(html_path, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")

        # Find all image tags
        img_tags = soup.find_all("img")

        for i, img in enumerate(img_tags):
            img_url = img.get("src")

            if img_url:
                # Convert relative URLs to absolute if needed
                img_url = urljoin("https://scholar.google.com/", img_url)

                try:
                    # Request and download the image
                    response = requests.get(img_url, headers={"User-Agent": "Mozilla/5.0"})
                    if response.status_code == 200:
                        img_extension = img_url.split(".")[-1].split("?")[0]  # Get image extension
                        img_extension = img_extension if img_extension.lower() in ["jpg", "jpeg", "png", "gif"] else "jpg"
                        img_filename = f"{html_file.replace('.html', '')}_img{i+1}.{img_extension}"
                        img_path = os.path.join(image_output_folder, img_filename)

                        with open(img_path, "wb") as img_file:
                            img_file.write(response.content)

                        print(f"Saved: {img_filename}")

                except Exception as e:
                    print(f"Error downloading image {img_url}: {e}")

    print(f"Image extraction complete. Images saved in '{image_output_folder}'.")

# Example usage
search_query = "Polymer Protein"
fetch_scholar_data(search_query)
extract_images_from_articles(search_query)


