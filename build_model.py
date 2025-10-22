# build_model.py

import re
from collections import Counter
import json
import xml.etree.ElementTree as ET
import os

WIKI_XML_PATH = 'hiwiki-latest-pages-articles.xml'
MODEL_OUTPUT_PATH = 'hindi_word_model.json'

def tokenize(text):
    """
    Extracts Hindi (Devanagari) words from a given text.
    The regex uses the Devanagari Unicode range (\u0900 to \u097F).
    """
    if not text:
        return []
    return [word.lower() for word in re.findall(r'[\u0900-\u097F]+', text)]


def build_model(xml_path, output_path):
    """
    Parses a Wikipedia XML dump using a memory-efficient iterative parser,
    tokenizes the text, counts word frequencies, and saves the model.
    """
    if not os.path.exists(xml_path):
        print("=" * 60)
        print(f"ERROR: XML file not found at path: {os.path.abspath(xml_path)}")
        print("Please ensure the Hindi Wikipedia dump is in the same folder.")
        print("=" * 60)
        return
        
    word_counts = Counter()
    print(f"Parsing XML file from: {xml_path} using an iterative parser.")

    context = ET.iterparse(xml_path, events=("start", "end"))

    try:
        event, root = next(context)
    except StopIteration:
        print("Error: XML file is empty or invalid.")
        return

    namespace = root.tag.split('}')[0].strip('{')
    
    text_path = f'./{{{namespace}}}revision/{{{namespace}}}text'

    page_count = 0
    for event, elem in context:
        if event == 'end' and elem.tag == f'{{{namespace}}}page':
            text_element = elem.find(text_path)
            if text_element is not None and text_element.text:
                words = tokenize(text_element.text)
                word_counts.update(words)

            page_count += 1
            if page_count % 1000 == 0:
                print(f"Processed {page_count} pages...")

            elem.clear()

    print(f"\nProcessing complete. Processed a total of {page_count} pages.")
    
    del root 

    if not word_counts:
        print("Warning: No words were extracted. Check your XML file content and tokenization regex.")
        return
        
    print(f"Model created with {len(word_counts)} unique words.")

    print(f"Saving model to secondary memory: {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(word_counts, f, ensure_ascii=False, indent=4)
    print("Model building complete.")


if __name__ == '__main__':
    if not os.path.exists(WIKI_XML_PATH):
        print(f"\nFATAL ERROR: The required data file '{WIKI_XML_PATH}' was not found.")
        print("Please download the Hindi Wikipedia XML dump and save it in the directory.")
        print("Run the script again once the file is in place.")
    else:
        build_model(WIKI_XML_PATH, MODEL_OUTPUT_PATH)
