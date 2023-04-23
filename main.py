import csv
import re
import time
import psutil
with open('t8.shakespeare.txt', 'r') as f:
    input_text = f.read()
with open('find_words.txt', 'r') as f:
    find_words = [word.strip() for word in f.readlines()]
with open('french_dictionary.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)
    french_dict = {row[0]: row[1] for row in reader}
replaced_words = {}
output_text = ''
start_time = time.time()
for line in input_text.split('\n'):
    output_line = ''
    for word in re.findall(r'\w+|[^\w\s]', line):
        if word.lower() in find_words:
            if word in replaced_words:
                replaced_words[word] += 1
            else:
                replaced_words[word] = 1
            if word in french_dict:
                output_word = french_dict[word]
                if word.isupper():
                    output_word = output_word.upper()
                elif word.istitle():
                    output_word = output_word.title()
                output_line += output_word
            else:
                output_line += word
        else:
            output_line += word
    output_text += output_line + '\n'
with open('t8.shakespeare.translated.txt', 'w') as f:
    f.write(output_text)
with open('frequency.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['English word', 'French word', 'Frequency'])
    for word, count in replaced_words.items():
        if word in french_dict:
            writer.writerow([word, french_dict[word], count])
with open('performance.txt', 'w') as f:
    f.write(f'Time to process: {time.time() - start_time} seconds\n')
    f.write(f'Memory used: {psutil.Process().memory_info().rss / 1024 / 1024} MB\n')
