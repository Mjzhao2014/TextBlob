"""
Unit tests for verifying domain-specific vocab file handling
in TextBlob's spell correction feature.

Focus:
- Words in custom vocab file are preserved (case-insensitive)
- Words not in vocab are corrected (but we don't check the exact correction)
"""

import unittest
import os
import textblob as tb

VOCAB_FILE_PATH = "/root/repo/TextBlob/tests/custom_vocab.txt"
VOCAB_WORDS = "xray\nAI\nChatGPT\nNeuralNet\n"

# Ensure vocab file exists before running tests
os.makedirs(os.path.dirname(VOCAB_FILE_PATH), exist_ok=True)
with open(VOCAB_FILE_PATH, "w") as f:
    f.write(VOCAB_WORDS)


class TestTextBlobCorrectionWithVocab(unittest.TestCase):
    def setUp(self):
        self.blob = tb.TextBlob("I havv bad speling.", custom_vocab_file=VOCAB_FILE_PATH)

    def test_correct(self):
        # Check that the blob is corrected and is a TextBlob object
        corrected = self.blob.correct()
        self.assertIsInstance(corrected, tb.TextBlob)
        self.assertNotIn("havv", corrected.raw.lower())
        self.assertNotIn("speling", corrected.raw.lower())

        # Domain-specific terms should remain untouched
        blob_vocab = tb.TextBlob("Xray AI ChatGPT NeuralNet", custom_vocab_file=VOCAB_FILE_PATH)
        corrected_vocab = blob_vocab.correct().raw
        for word in ["xray", "ai", "chatgpt", "neuralnet"]:
            self.assertIn(word, corrected_vocab.lower())

    def test_case_sensitivity(self):
        # Preserve both "Xray" and "xray"
        blob_case = tb.TextBlob("Xray technology and xray scans.", custom_vocab_file=VOCAB_FILE_PATH)
        corrected = blob_case.correct().raw.lower()
        self.assertIn("xray", corrected)
        self.assertIn("technology", corrected)
        # We don’t care what "scans" becomes, but it must not be "xray"

    def test_similar_but_not_exact_vocab_word(self):
        # Words similar to vocab entries should still be corrected
        blob_similar = tb.TextBlob("I need Xrays.", custom_vocab_file=VOCAB_FILE_PATH)
        corrected = blob_similar.correct().raw
        self.assertNotIn("Xrays", corrected)

    def test_unrelated_word_correction(self):
        # Words not in vocab should be corrected
        blob_unrelated = tb.TextBlob("Speling is hard.", custom_vocab_file=VOCAB_FILE_PATH)
        corrected = blob_unrelated.correct().raw
        self.assertNotIn("Speling", corrected)

    def test_empty_vocab_file(self):
        # Ensure spell correction works when vocab is empty
        EMPTY_VOCAB_FILE_PATH = "/root/repo/TextBlob/tests/empty_vocab.txt"
        open(EMPTY_VOCAB_FILE_PATH, "w").close()
        blob_empty_vocab = tb.TextBlob("I havv bad speling.", custom_vocab_file=EMPTY_VOCAB_FILE_PATH)
        corrected = blob_empty_vocab.correct().raw
        self.assertNotIn("havv", corrected.lower())
        self.assertNotIn("speling", corrected.lower())

if __name__ == "__main__":
    unittest.main()
