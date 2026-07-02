from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    """Simulated LLM endpoint - vulnerable to command injection via system calls"""
    prompt = request.json.get('prompt', '')
    
    # Simulated vulnerable behavior - some LLM wrapper apps do this
    # to execute "tools" based on model output
    if 'EXECUTE:' in prompt:
        command = prompt.split('EXECUTE:')[1].strip()
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=5)
            return jsonify({"response": result.stdout, "vulnerability": "command_injection_triggered"})
        except Exception as e:
            return jsonify({"error": str(e)})
    
    return jsonify({"response": f"Simulated LLM response to: {prompt}"})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "running", "container_id": os.uname()[1]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
