from tqdm import tqdm
# Importing the necessary module and function
import simple_image_download.simple_image_download as simp

# Creating a response object
response = simp.Downloader()

## Keyword
keyword = ""

with open("bold_text.txt", "r") as f:
    bold_text_list = f.read().splitlines()


# Downloading images
try:
    with tqdm(total=len(bold_text_list), desc="Downloading images", unit="images") as pbar:
        for text in bold_text_list:
            response.download(text, limit=5)
            pbar.update(1)
    print("Images downloaded successfully.")
except Exception as e:
    print("An error occurred:", e)
