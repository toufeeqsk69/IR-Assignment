# spell_checker.py

import json
import re
from collections import Counter


# =========================================================
# The Error Model: Generates candidate corrections
# =========================================================
def edits1(word):
    """
    Generates all possible corrections that are one edit away from the word.
    Performs deletion, transposition, substitution, and insertion using the
    Hindi (Devanagari) alphabet.
    """
    # Comprehensive set of Devanagari characters for generating edits
    hindi_alphabet = 'अआइईउऊऋएऐओऔकखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसहळािीुूृेैोौँः'
    
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    
    # Deletion: Remove one character
    deletes = [L + R[1:] for L, R in splits if R]
    
    # Transposition: Swap two adjacent characters
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    
    # Substitution: Replace one character with any Hindi character
    replaces = [L + c + R[1:] for L, R in splits if R for c in hindi_alphabet]
    
    # Insertion: Insert any Hindi character
    inserts = [L + c + R for L, R in splits for c in hindi_alphabet]
    
    return set(deletes + transposes + replaces + inserts)


def edits2(word):
    """
    Generates all possible corrections that are two edits away from the word.
    """
    # This generates words that are two edits away (Deletion, Transposition, Substitution, Insertion)
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))


def tokenize(text):
    """
    Extracts Hindi (Devanagari) words from a given text.
    Uses the Devanagari Unicode range (\u0900 to \u097F).
    """
    if not text:
        return []
    # Tokenizes and converts to lowercase for consistent model lookup
    return [word.lower() for word in re.findall(r'[\u0900-\u097F]+', text)]


# =========================================================
# The Main SpellChecker Class
# =========================================================
class SpellChecker:
    def __init__(self, model_path):
        """
        Loads the language model (index) from secondary memory (disk) into main memory.
        """
        print(f"Loading spell checker index from disk: {model_path}")
        try:
            # Index is loaded from secondary memory into main memory
            with open(model_path, 'r', encoding='utf-8') as f:
                self.word_counts = json.load(f)
        except FileNotFoundError:
            print(f"Error: Model file not found at {model_path}. Please run build_model.py first.")
            exit()
            
        # Total word count for probability calculation
        self.total_words = float(sum(self.word_counts.values()))
        print("Index loaded successfully into main memory.")

    def probability(self, word):
        """
        Calculates the probability P(word) based on its frequency.
        This frequency/probability is used for ranking candidates (semantic ranking).
        """
        return self.word_counts.get(word, 0) / self.total_words

    def known(self, words):
        """
        Returns the subset of words that are present in our language model (corpus).
        """
        return set(w for w in words if w in self.word_counts)

    def get_candidates(self, word):
        """
        Generates a ranked list of probable spelling corrections for a word.
        Ranking is based on word frequency (P(c)) to meet the semantic ranking requirement.
        """
        # Priority 1: The word itself, if it's known
        candidates = self.known([word])
        if candidates:
            return sorted(list(candidates), key=self.probability, reverse=True)

        # Priority 2: Words one edit away (minimum edits = 1)
        candidates = self.known(edits1(word))
        if candidates:
            # Ranking based on frequency (P(c))
            return sorted(list(candidates), key=self.probability, reverse=True)

        # Priority 3: Words two edits away (minimum edits = 2)
        candidates = self.known(edits2(word))
        if candidates:
            # Ranking based on frequency (P(c))
            return sorted(list(candidates), key=self.probability, reverse=True)

        # Priority 4: If no candidates found, return the original word
        return [word]

    def correct_text(self, text):
        """
        Corrects an entire text string.
        Stores the source document and candidate sets in main memory (requirement d).
        """
        # Store source document tokens in main memory
        source_tokens = tokenize(text)
        corrected_tokens = []
        
        # This map holds the probable candidates for each misspelled word (stored in main memory)
        candidate_map = {}

        for word in source_tokens:
            if word in self.word_counts:
                # Word is correct
                corrected_tokens.append(word)
            else:
                # Word is misspelled, find candidates
                candidates = self.get_candidates(word)
                best_correction = candidates[0]
                corrected_tokens.append(best_correction)
                
                # Store the misspelled word and its ranked candidates in main memory
                candidate_map[word] = candidates

        corrected_sentence = " ".join(corrected_tokens)
        
        # The corrected text and the candidate map are returned/stored in main memory
        return corrected_sentence, candidate_map


# =========================================================
# Main execution block for testing
# =========================================================
if __name__ == "__main__":
    MODEL_PATH = 'hindi_word_model.json'

    # The index is loaded from secondary storage into the SpellChecker object in main memory.
    checker = SpellChecker(MODEL_PATH)

    # The source document and candidates will be held in main memory.
    # Test Case: "भारत एक महान देश है। यहाँ हिंदी भाषा बोली जाती है।"
    # Misspelled words: भारत् (भारत), महाना (महान), देष (देश), भाष (भाषा)
    # Note: Punctuation is ignored by the tokenizer.
    text_to_check = "भारत् एक महाना देष है। यहां हिन्दी भाष बोली जाती है"

    # Perform the spell checking
    corrected_text, candidates_for_misspelled = checker.correct_text(text_to_check)

    print("\n" + "=" * 50)
    print("Original Text:  ", text_to_check)
    print("Corrected Text: ", corrected_text)
    print("=" * 50)

    if candidates_for_misspelled:
        print("\nDetails of corrections (misspelled word -> ranked candidates):")
        for misspelled, candidates in candidates_for_misspelled.items():
            # Show the top 5 most probable candidates (ranked by frequency)
            print(f"  '{misspelled}' -> {candidates[:5]}")
    else:
        print("\nNo spelling errors found.")
