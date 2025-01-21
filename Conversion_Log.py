import csv
import hashlib
import os
from collections import defaultdict

# Step 1: Map letters to numbers
letter_map = {chr(i + 97): i + 1 for i in range(26)}  # a=1, b=2, ..., z=26

# Step 2: Function to map words to sequences based on letters
def map_word_to_sequence(word):
    return [letter_map[letter] for letter in word if letter in letter_map]

# Step 3: Function to hash sequences for unique identification
def hash_sequence(sequence):
    sequence_str = "-".join(map(str, sequence))
    return hashlib.md5(sequence_str.encode()).hexdigest()

# Step 4: Function to log data to a CSV file
def log_to_csv(data, filename="conversation_dna_log.csv"):
    if not os.path.exists(filename):
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Sentence", "Word", "Word Sequence", "Hash"])
    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        for sentence, word_data in data.items():
            for word, (sequence, word_hash) in word_data.items():
                writer.writerow([sentence, word, sequence, word_hash])

# Step 5: Main function to process sentences
def process_sentences(sentences):
    data_log = defaultdict(dict)
    
    for sentence in sentences:
        words = sentence.lower().split()
        for word in words:
            word_sequence = map_word_to_sequence(word)
            word_hash = hash_sequence(word_sequence)
            data_log[sentence][word] = (word_sequence, word_hash)
    
    return data_log

# Step 6: Check for input.txt file
def get_sentences_from_file(filename="input.txt"):
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as file:
            file.write("Enter your sentences here, one per line.")
        print(f"'{filename}' created. Add your sentences and run the script again.")
        return []
    else:
        with open(filename, "r", encoding="utf-8") as file:
            sentences = [line.strip() for line in file if line.strip()]
        return sentences

# Example usage
if __name__ == "__main__":
    input_file = "input.txt"
    sentences = get_sentences_from_file(input_file)

    if sentences:
        data_log = process_sentences(sentences)
        log_to_csv(data_log)
        print("Data logged to conversation_dna_log.csv")
    else:
        print("No sentences found in 'input.txt'. Please add sentences and rerun the script.")
