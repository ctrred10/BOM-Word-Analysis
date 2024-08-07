import re
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, words
from nltk.stem import WordNetLemmatizer
import nltk

# Ensure you have the necessary NLTK resources downloaded
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')  # For the lemmatizer
nltk.download('words')  # For dictionary validation

def preprocess_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read().lower()
        text = re.sub(r'[^a-z\s]', '', text)  # Remove everything except letters and spaces
        tokens = word_tokenize(text)
        english_words = set(words.words())

        # Adding custom stopwords
        custom_stopwords = set(stopwords.words('english')) | {'th', 'c'}

        filtered_tokens = [word for word in tokens if word not in custom_stopwords and word in english_words or word == 'jesus']
        lemmatizer = WordNetLemmatizer()
        lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
        return lemmatized_tokens

def analyze_frequency(tokens):
    frequency = Counter(tokens)
    total_words = sum(frequency.values())
    percentage_frequency = {word: round((count / total_words) * 100, 2) for word, count in frequency.items()}
    return frequency, total_words, Counter(percentage_frequency)

def word_search(frequency_data, search_word):
    return frequency_data.get(search_word, 0)

def main():
    book_of_mormon_path = 'book_of_mormon_1830.txt'
    journal_1832_1834_path = 'journal_1832_1834.txt'
    journal_1835_1836_path = 'journal_1835_1836.txt'

    # Process the texts
    bom_tokens = preprocess_text(book_of_mormon_path)
    bom_frequency, bom_total_words, bom_percentage_frequency = analyze_frequency(bom_tokens)

    journal1_tokens = preprocess_text(journal_1832_1834_path)
    journal1_frequency, journal1_total_words, journal1_percentage_frequency = analyze_frequency(journal1_tokens)

    journal2_tokens = preprocess_text(journal_1835_1836_path)
    journal2_frequency, journal2_total_words, journal2_percentage_frequency = analyze_frequency(journal2_tokens)

    # User input for word search
    search_word = input("Enter a word to search: press enter to generate word frequencies: ").strip().lower()

    if search_word:
        # Search results
        bom_count = word_search(bom_frequency, search_word)
        journal1_count = word_search(journal1_frequency, search_word)
        journal2_count = word_search(journal2_frequency, search_word)

        # Display results
        print(f"Occurrences in Book of Mormon: {bom_count} out of {bom_total_words}")
        print(f"Occurrences in Journal 1832-1834: {journal1_count} out of {journal1_total_words}")
        print(f"Occurrences in Journal 1835-1836: {journal2_count} out of {journal2_total_words}")
    else:
        # Display top 10 words by percentage if no input
        print("Top 10 Most Common Words in Book of Mormon:", bom_percentage_frequency.most_common(10))
        print("Top 10 Most Common Words in Journal 1832-1834:", journal1_percentage_frequency.most_common(10))
        print("Top 10 Most Common Words in Journal 1835-1836:", journal2_percentage_frequency.most_common(10))

if __name__ == "__main__":
    main()
