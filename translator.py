import os
from google.cloud import translate_v2 as translate
from bs4 import BeautifulSoup
from bs4 import NavigableString
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

# Create an argument parser
parser = argparse.ArgumentParser(description='Translate HTML files')

# Add the options
parser.add_argument('-m', nargs='+', help='translate multiple files')
parser.add_argument('-f', help='translate a single file')
parser.add_argument('-r', help='translate all HTML files recursively in a directory')
parser.add_argument('-s', '--google-credentials', type=str, required=True, help='Path to the Google credentials JSON file')
parser.add_argument('-l', '--language', type=str, default='en', help='Language code to check for translation')
parser.add_argument('-t', '--tags', nargs='+', default=['title', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'a', 'span', 'strong', 'header', 'div', 'button', 'li', 'td', 'th', 'label', 'small', 'em', 'blockquote', 'pre', 'alt', 'img', 'value', 'i', 'input', 'time', 'figcaption', 'figure', 'del', 'option', 'select'], help='List of HTML tags to be translated')

# Parse the arguments
args = parser.parse_args()

# Set the environment variable for your Google Cloud API key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = args.google_credentials

# Instantiates a client
translate_client = translate.Client()


def write_translated_html(file_path, soup):
    with open(file_path, 'w') as f:
        f.write(soup.prettify())

def translate_file(file_path, tags):
    # Load the HTML file
    with open(file_path, 'r') as f:
        html = f.read()

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    for tag in soup.find_all(tags):
        text = (tag.string)
        if tag.name == 'input':
            if 'placeholder' in tag.attrs:
                translation = translate_client.translate(tag['placeholder'], target_language=args.language)
                translated_text = translation['translatedText']
                tag['placeholder'] = translated_text
            elif 'value' in tag.attrs:
                translation = translate_client.translate(tag['value'], target_language=args.language)
                translated_text = translation['translatedText']
                tag['value'] = translated_text
            write_translated_html(file_path, soup)
        elif text is not None:
            # Translate the text using the Google Cloud Translation API
            translation = translate_client.translate(text, target_language=args.language)
            translated_text = translation['translatedText']
            text.replace_with(translated_text)
            write_translated_html(file_path, soup)
            print(f"{text} >> {translated_text}")
        else:
            for child in tag.children:
                if isinstance(child, NavigableString):
                    # Translate the text node
                    translation = translate_client.translate(child.string, target_language=args.language)
                    child.string.replace_with(translation['translatedText'])
                    write_translated_html(file_path, soup)

if args.f:
    # Translate a single file
    translate_file(args.f, args.tags)
elif args.m:
    # Use ThreadPoolExecutor to translate multiple files in parallel
    with ThreadPoolExecutor() as executor:
        futures = []
        for file_path in args.m:
            futures.append(executor.submit(translate_file, file_path, args.tags))
    
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Translation error: {e}")
elif args.r:
    # Use ThreadPoolExecutor to translate multiple files in parallel
    with ThreadPoolExecutor() as executor:
        futures = []
        # Translate all HTML files recursively in a directory
        for root, dirs, files in os.walk(args.r):
            for file in files:
                if file.endswith('.html'):
                    futures.append(executor.submit(translate_file, os.path.join(root, file), args.tags))
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Translation error: {e}")
else:
    parser.print_help()