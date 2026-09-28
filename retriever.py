"""
CSC-128 Assignment 6 starter: retrieval
Michelle Salgado
"""
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from knowledge import DOCUMENTS

STOP_WORDS = {
    "a", "an", "and", "are", "at", "be", "can",
    "do", "does", "for", "from", "have", "i",
    "if", "in", "is", "it", "my", "of", "on",
    "the", "there", "to", "what", "when", "with",
    "you", "your"
}

# TODO 5: set this from the evidence your tests print
DEFAULT_THRESHOLD = 0.23
DEFAULT_TOP_K = 3


def stem(word):
    """
    TODO 1: strip common suffixes so that reserve, reserved, and
    reservation collapse to the same token. It does not have to be a real
    Porter stemmer.
    """
    suffixes = ["ation", "ing", "ed", "es", "s"]

    for suffix in suffixes:
        if word.endswith(suffix) and len(word) > len(suffix) + 2:
            return word[:-len(suffix)]

    return word

def analyze(text):
    """TODO 2: normalize, tokenize, stem, and add bigrams."""

    # Convert text to lowercase and keep only words
    words = re.findall(r"[a-z0-9]+", text.lower())

    # Remove stop words and stem each word
    tokens = [stem(word) for word in words if word not in STOP_WORDS]

    # Create bigrams from neighboring words
    bigrams = [
        tokens[i] + "_" + tokens[i + 1]
        for i in range(len(tokens) - 1)
    ]

    return tokens + bigrams


class Retriever:
    def __init__(self, documents=None, threshold=DEFAULT_THRESHOLD):
        """TODO 3: fit a TfidfVectorizer using your analyze function."""

        self.documents = documents if documents is not None else DOCUMENTS
        self.threshold = threshold

        self.vectorizer = TfidfVectorizer(
            analyzer=analyze,
            lowercase=False
        )

        texts = [document["text"] for document in self.documents]
        self.document_vectors = self.vectorizer.fit_transform(texts)
    def search(self, question, top_k=DEFAULT_TOP_K):
        """
        TODO 4: return a list of (document, score), best first, dropping
        anything below the threshold.

        Returning an empty list is correct and important. It is what tells
        the bot to refuse instead of calling the model with nothing useful.
        """

        question_vector = self.vectorizer.transform([question])

        scores = cosine_similarity(
            question_vector,
            self.document_vectors
        )[0]

        ranked = sorted(
            enumerate(scores),
            key=lambda item: item[1],
            reverse=True
        )

        hits = []

        for index, score in ranked[:top_k]:
            if score >= self.threshold:
                hits.append((self.documents[index], float(score)))

        return hits
    def build_context(self, hits):
        """
        Build grounded context from retrieved documents.
        """
        context_parts = []

        for document, score in hits:
            context_parts.append(
                f"Source: {document['source']}\n"
                f"{document['text']}"
            )

        return "\n\n".join(context_parts)