import os
import re
from Corpus.TurkishSplitter import TurkishSplitter
from Corpus.Sentence import Sentence

input_folder = 'books/New/'
output_folder = 'books/New/splitted/'

os.makedirs(output_folder, exist_ok=True)

remove_patterns = [
    r'\(edited-S\.Ç\.\)', r'\(edited\)', r'\(S\.Ç\.\)', r'\(EDITED\)', r'\(S\.U\)', r'Abdullah_'
]

splitter = TurkishSplitter()

for file_name in os.listdir(input_folder):
    input_path = os.path.join(input_folder, file_name)

    # Skip folders just in case
    if os.path.isdir(input_path):
        continue

    # Try reading file with utf-8, fallback to windows-1254
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            text = f.read()
        encoding_used = "utf-8"
    except:
        try:
            with open(input_path, 'r', encoding='windows-1254') as f:
                text = f.read()
            encoding_used = "windows-1254"
        except Exception as e:
            print(f"Failed to read: {file_name} due to {e}")
            continue

    # Ensure filename ends with .txt
    if not file_name.lower().endswith(".txt"):
        logical_name = file_name + ".txt"
    else:
        logical_name = file_name

    # Clean filename for output
    clean_name = logical_name
    for pattern in remove_patterns:
        clean_name = re.sub(pattern, '', clean_name, flags=re.IGNORECASE)

    clean_name = clean_name.strip()
    base_name = os.path.splitext(clean_name)[0]

    # Output filename
    output_filename = base_name + "-Melisa_Danafar.txt"
    output_path = os.path.join(output_folder, output_filename)

    # Fix special characters
    text = re.sub(r'-(?=[A-ZÇĞİÖŞÜ])| -(?=[a-zçğıöşü])', "–­", text)
    text = (text.replace("□", "–").replace("—", "–­").replace("’", "'")
                .replace("‒", "–").replace("<<", "«").replace(">>", "»")
                .replace("–", "–­").replace("•", "–"))

    # Split and save
    paragraphs = text.split("\n\n")
    final_sentences = []

    for paragraph in paragraphs:
        sentences = splitter.split(paragraph)
        final_sentences.extend(sentence.toString().strip() for sentence in sentences)
        final_sentences.append("\n")

    with open(output_path, 'w', encoding='utf-8', newline='\n') as out_f:
        for sentence in final_sentences:
            out_f.write(sentence + "\n")

    print(f"✔ Saved: {output_filename} ({encoding_used})")

print("\nDONE! All files processed successfully!")
