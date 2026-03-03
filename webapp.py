import os
from flask import Flask, render_template, request, jsonify, send_file
from modules.dictionary_gen import DictionaryGenerator
from modules.strength_analyzer import PasswordStrengthAnalyzer
from modules.brute_force_sim import BruteForceSimulator
from modules.hash_extractor_sim import HashExtractorSim
from modules.report_generator import ReportGenerator

app = Flask(__name__)

# Initialize modules
dict_gen = DictionaryGenerator()
analyzer = PasswordStrengthAnalyzer()
simulator = BruteForceSimulator()
extractor = HashExtractorSim()
reporter = ReportGenerator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate_dict', methods=['POST'])
def generate_dict():
    data = request.json
    words = data.get('words', [])
    if not words:
        return jsonify({'error': 'No words provided'})
    
    base_set = dict_gen.generate_base_words(words)
    mutated = dict_gen.apply_mutations(base_set)
    out_file = "download_wordlist.txt"
    count = dict_gen.export_wordlist(mutated, out_file)
    return jsonify({'message': f'Successfully generated {count} words', 'count': count, 'file': out_file})

@app.route('/api/analyze', methods=['POST'])
def analyze_password():
    data = request.json
    pwd = data.get('password', '')
    if not pwd:
        return jsonify({'error': 'No password provided'})
    
    res = analyzer.analyze(pwd)
    recs = analyzer.generate_recommendations(res)
    return jsonify({'result': res, 'recommendations': recs})

@app.route('/api/brute_force', methods=['POST'])
def brute_force():
    data = request.json
    pwd = data.get('password', '')
    htype = data.get('hash_type', 'ntlm')
    
    if not pwd:
        return jsonify({'error': 'No password provided'})
        
    res = simulator.estimate_brute_force_time(pwd, hash_type=htype)
    return jsonify(res)

@app.route('/api/extract', methods=['POST'])
def extract_hashes():
    data = request.json
    os_type = data.get('os_type', 'linux')
    
    # In a real tool this would use actual files, here we use our test demos
    if os_type == 'linux':
        file = "test_shadow.txt"
        with open(file, 'w') as f:
            f.write("root:$6$xyz$abc:18777:0:99999:7:::\nuser1:$1$lmn$opq:18777:0:99999:7:::\n")
        accounts = extractor.parse_linux_shadow(file)
    else:
         file = "test_sam.txt"
         with open(file, 'w') as f:
             f.write("Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::\n")
         accounts = extractor.parse_windows_sam_dump(file)
         
    return jsonify({'accounts': accounts})

@app.route('/api/report', methods=['POST'])
def generate_report():
    data = request.json
    passwords = data.get('passwords', [])
    if not passwords:
        return jsonify({'error': 'No passwords provided for audit'})
        
    results = [analyzer.analyze(p) for p in passwords]
    fname = reporter.generate_audit_report(results)
    
    # Read the markdown
    with open(fname, 'r') as f:
        md_content = f.read()
        
    return jsonify({'filename': fname, 'markdown': md_content})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
