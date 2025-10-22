# Hindi Probabilistic Spell Checker - Assignment A1 (Roll No: S20230010222)

This project implements a **probabilistic spell checker** for the Hindi language (using the Devanagari script). The methodology is based on **Peter Norvig's well-known approach**, leveraging a statistical language model built from a large text corpus (Hindi Wikipedia Dump).

## Description of Modules

### `build_model.py` (Language Model)

This script creates the statistical language model (word frequency index).

* **Input:** A Hindi Wikipedia XML dump (e.g., `hiwiki-latest-pages-articles-multistream.xml`).

* **Process:** Parses XML, tokenizes content using the Devanagari Unicode range, calculates word frequency.

* **Output:** Saves the frequency map (our "index") to a JSON file on **secondary storage** (`hindi_word_model.json`).

### `spell_checker.py` (Core Logic)

This is the main program containing the `SpellChecker` class and all core logic.

#### Error Model Functions

* **`edits1()` / `edits2()`:** Generate all possible words at an edit distance of 1 and 2, based on four operations: **insertion, deletion, substitution, and transposition** using the Hindi (Devanagari) alphabet.

#### `SpellChecker` Class

* **`__init__():`** Loads the index (`hindi_word_model.json`) from the hard drive into **main memory** upon object creation, fulfilling requirement (d) for index storage.

* **`get_candidates():`** Generates corrections and **ranks these candidates** based on their **frequency** ($P(c)$) in the language model, fulfilling requirement (c) for semantic ranking.

* **`correct_text():`** Processes a document and, as required in (d), stores the **original source document** (as tokenized words) and a dictionary mapping each misspelled word to its set of probable candidates in the **main memory** (`candidate_map`).

## How to Run the Code

### Prerequisites

* Python 3

* A Hindi Wikipedia XML dump (e.g., `hiwiki-latest-pages-articles-multistream.xml`).

### 1. Build the Language Model (One-time setup)

1. Place the Hindi Wikipedia XML file in the same directory as the scripts.

2. Run the model builder from your terminal:

      python build_model.py
   
   
   This will create the index file `hindi_word_model.json`.

### 2. Run the Spell Checker

Once the model is built, run the main spell checker script:

python spell_checker.py


The script will load the index, process a hardcoded sample Hindi text, and print the original text, the corrected version, and the ranked candidates for any misspelled words found.

## Output - 5 Test Cases

| \# | Misspelled Content | Corrected One | 
 | ----- | ----- | ----- | 
| 1 | यह एक महत्वपुर्ण विषय्य है। | यह एक महत्वपूर्ण विषय है। | 
| 2 | आज स्कुल में बऊत मज़ा आया। | आज स्कूल में बहुत मज़ा आया। | 
| 3 | हमें प्रदूशन को कम करना चाहिये। | हमें प्रदूषण को कम करना चाहिए। | 
| 4 | उन्होने कहाकी वह कल आएंगे। | उन्होंने कहा कि वह कल आएंगे। | 
| 5 | भारत् एक देष है। | भारत एक देश है। | 

## Link to Data/Index

The complete Hindi Wikipedia corpus and the generated `hindi_word_model.json` are too large for this submission. The download link will be provided here:

**Link:**

$$
Provide a Google Drive, Dropbox, or GitHub LFS link to your data and model file here
$$