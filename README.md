# Translate-My-Site

Translate-My-Site is a Python script that uses the Google Cloud Translation API to translate the text in HTML files. The script can translate a single file, multiple files, or all HTML files in a directory recursively. The user can specify the target language and the HTML tags to be translated.

## Requirements

- Python 3
- `google-cloud-translate` package
- `beautifulsoup4` package

## Installation

1. Install the required packages:

```
pip install google-cloud-translate beautifulsoup4
```

2. Clone the repository:

```
git clone https://github.com/yu3ufe/Translate-My-Site.git
```

3. Obtain a Google Cloud API key and download the credentials JSON file.

## Usage

```
usage: translate.py [-h] [-m [M [M …]]] [-f F] [-r R] -s GOOGLE_CREDENTIALS [-l LANGUAGE] [-t [TAGS [TAGS …]]]
```

Translate HTML files

```
optional arguments: -h, --help show this help message and exit -m [M [M …]], --multiple [M [M …]] translate multiple files -f F translate a single file -r R translate all HTML files recursively in a directory -s GOOGLE_CREDENTIALS, --google-credentials GOOGLE_CREDENTIALS Path to the Google credentials JSON file -l LANGUAGE, --language LANGUAGE Language code to check for translation (default: en) -t [TAGS [TAGS …]], --tags [TAGS [TAGS …]] List of HTML tags to be translated (default: [‘title’, ‘h1’, ‘h2’, ‘h3’, ‘h4’, ‘h5’, ‘h6’, ‘p’, ‘a’, ‘span’, ‘strong’, ‘header’, ‘div’, ‘button’, ‘li’, ‘td’, ‘th’, ‘label’, ‘small’, ‘em’, ‘blockquote’, ‘pre’, ‘alt’, ‘img’, ‘value’, ‘i’, ‘input’, ‘time’, ‘figcaption’, ‘figure’, ‘del’, ‘option’, ‘select’])
```

To translate a single file:

```
python translate.py -f example.html -s path/to/google/credentials.json
```

To translate multiple files:

```
python translate.py -m example1.html example2.html -s path/to/google/credentials.json
```

To translate all HTML files in a directory recursively:

```
python translate.py -r path/to/directory -s path/to/google/credentials.json
```

To specify the target language:

```
python translate.py -f example.html -s path/to/google/credentials.json -l es
```

To specify the HTML tags to be translated:

```
python translate.py -f example.html -s path/to/google/credentials.json -t title h1 h2 p
```

## Customization

The script can be easily customized to meet specific needs. For example, you can add support for additional command-line arguments or modify the `translate_file` function to change how the translation is performed.

## Contributions

Contributions are welcome! If you find any bugs or have suggestions for improving the script, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
