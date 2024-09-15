from flask import Flask, request, jsonify
from transformers import AutoTokenizer
import sentencepiece as spm
import concurrent.futures
import time

app = Flask(__name__)

# Implement tokenization functions
def tokenize_bpe(dataset, vocab_size):
    tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased', use_fast=True)
    start_time = time.time()
    tokens = tokenizer.encode(dataset, return_tensors='pt')
    end_time = time.time()
    return len(tokens), end_time - start_time

def tokenize_wordpiece(dataset, vocab_size):
    tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased', use_fast=True)
    start_time = time.time()
    tokens = tokenizer.encode(dataset, return_tensors='pt')
    end_time = time.time()
    return len(tokens), end_time - start_time

def tokenize_unigram(dataset, vocab_size):
    # Simple implementation of Unigram tokenization
    tokens = dataset.split()
    start_time = time.time()
    end_time = time.time()
    return len(tokens), end_time - start_time

def tokenize_pathpiece(dataset, vocab_size):
    # Simple implementation of PATHPIECE tokenization (simplified for demonstration)
    tokens = dataset.split()
    start_time = time.time()
    end_time = time.time()
    return len(tokens), end_time - start_time

# Define Flask routes
@app.route('/upload_and_benchmark', methods=['POST'])
def upload_and_benchmark():
    file = request.files['file']
    filename = file.filename
    file.save(filename)
    
    with open(filename, 'r') as f:
        data = f.read()
    
    tokenizers = {
        'BPE': tokenize_bpe,
        'WordPiece': tokenize_wordpiece,
        'Unigram': tokenize_unigram,
        'PATHPIECE': tokenize_pathpiece
    }

    results = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(tokenizer, data, 32000): name for name, tokenizer in tokenizers.items()}
        for future in concurrent.futures.as_completed(futures):
            name = futures[future]
            try:
                token_count, time_taken = future.result()
                results[name] = {
                    'token_count': token_count,
                    'time_taken': time_taken
                }
            except Exception as exc:
                results[name] = {'error': str(exc)}
    
    return jsonify(results), 200

if __name__ == '__main__':
    app.run(debug=True)

