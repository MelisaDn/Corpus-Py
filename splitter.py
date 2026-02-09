from Corpus.TurkishSplitter import TurkishSplitter
from Corpus.Sentence import Sentence
import re

# Input and output file names
file_name = "books/New/Yılkı Atı-Abbas Sayar (S.U).txt"
output_file = "books/New/splitted/Yılkı Atı-Melisa_Danafar.txt"

# Read file content
# Using 'windows-1254' encoding to handle special Turkish characters
with open(file_name, 'r', encoding='utf-8') as file:
    text = file.read()

# Replace specific characters 

# text = re.sub(r'-(?=[A-ZÇĞİÖŞÜ])| -(?=[a-zçğıöşü])', "–­", text)
text = text.replace("□", "–").replace("—", "–­").replace("’", "'").replace("‒", "–").replace("<<", "«").replace(">>", "»").replace("–", "–­").replace("•", "–")

# Split text into paragraphs
paragraphs = text.split("\n\n")  

splitter = TurkishSplitter()
final_sentences = []

# Process each paragraph
for paragraph in paragraphs:
    sentences = splitter.split(paragraph)
    final_sentences.extend(sentence.toString().strip() for sentence in sentences)
    final_sentences.append("\n")  # Preserve paragraph spacing

# Save output
with open(output_file, 'w', encoding='utf-8', newline='\n') as file:
    for sentence in final_sentences:
        file.write(sentence + "\n")

print(f"File {output_file} has been saved.")