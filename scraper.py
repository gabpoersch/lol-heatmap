import csv
import os
import requests
from bs4 import BeautifulSoup

url = "https://app.mobalytics.gg/lol/champions"

response = requests.get(url)
html_content = response.text

soup = BeautifulSoup(html_content, "html.parser")

main_divs = soup.find_all("div", class_="m-o0thq4")

champion_info = {}

for main_div in main_divs:
    name_divs = main_div.find_all("div", class_="m-123baga")
    img_divs = main_div.find_all("div", class_="m-mdpkvw")

    for name_div, img_div in zip(name_divs, img_divs):
        name = name_div.text.strip()
        img_tag = img_div.find("img")

        if img_tag and "src" in img_tag.attrs:
            img_url = img_tag["src"]

            # Remove the "?v3" part from the image URL
            img_url = img_url.replace("?v3", "")

            champion_info[name] = img_url

# Create a folder called "dataset/train"
train_folder = "dataset/train"
if not os.path.exists(train_folder):
    os.makedirs(train_folder)

# Iterate through the champion_info dictionary and create subfolders for each champion
for champion_name, img_url in champion_info.items():
    champion_folder = os.path.join(train_folder, champion_name)

    # Create subfolders if they don't exist
    if not os.path.exists(champion_folder):
        os.makedirs(champion_folder)

    # Download the image and save it as ".png"
    img_response = requests.get(img_url)
    img_data = img_response.content
    img_filename = f"{champion_name}.png"  # Add .png extension
    img_path = os.path.join(champion_folder, img_filename)

    with open(img_path, "wb") as img_file:
        img_file.write(img_data)

print("Images downloaded and saved to the 'dataset/train' folder.")

# Define the CSV file path
csv_file_path = os.path.join("model/champion_names.csv")

# Create and write to the CSV file
with open(csv_file_path, "w", newline="", encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file)

    for name_div in name_divs:
        champion_name = name_div.text.strip()
        csv_writer.writerow([champion_name])

print("CSV file created with champion names.")