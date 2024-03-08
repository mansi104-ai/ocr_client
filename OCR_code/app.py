from flask import Flask, jsonify
import subprocess
import json
import os

app = Flask(__name__)

def run_model1():
    # Run your python file (test.py) in the background
    subprocess.run(['python', 'test.py'])

    # Check if the extracted_info.json has been updated
    json_file = 'extracted_info.json'
    before = os.path.getmtime(json_file)

    # Perform some operations or checks here

    after = os.path.getmtime(json_file)
    if before != after:
        print("JSON file has been updated")
        return "JSON file has been updated"
    else:
        print("JSON file has not been updated")
        return "JSON file has not been updated"

def run_model2():
    # Run your python file (footer_circle.py) in the background
    subprocess.run(['python', 'footer_circle.py'])

    # Check if the extraction_info.json has been updated
    json_file = 'extraction_info.json'
    before = os.path.getmtime(json_file)

    # Perform some operations or checks here

    after = os.path.getmtime(json_file)
    if before != after:
        print("JSON file has been updated")
        return "JSON file has been updated"
    else:
        print("JSON file has not been updated")
        return "JSON file has not been updated"

def main():
    output_data = {
        "model1_output": run_model1(),
        "model2_output": run_model2()
    }

    with open('output.json', 'w') as f:
        json.dump(output_data, f)

@app.route('/main', methods=['GET'])
def main_route():
    main()
    
    with open('output.json', 'r') as f:
        output_data = json.load(f)
    
    return jsonify(output_data)

if __name__ == '__main__':
    app.run(debug=False)