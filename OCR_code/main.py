import pytesseract
import json
import subprocess

def extract_text(image_path):
    # Perform OCR
    custom_config = r'--oem 3 --psm 6'  # custom configurations
    text = pytesseract.image_to_string(image_path, config=custom_config)

    # Extract the tag and title from the text
    first_line = text.split('\n')[0].strip()
    last_word = first_line.split()[-1]  # Get the last word of the first line
    tag = last_word
    title = ' '.join(first_line.split()[:-1])  # Get all words except the last one

    # Combine the extracted information
    extracted_info = {
        "tag": tag,
        "title": title.strip(),
        "text": text.strip()
    }

    return extracted_info

def main():
    # Define the input image path
    image_path = 'lined_final_edited.jpg'

    # Extract text from the image
    extracted_info = extract_text(image_path)

    # # Define the output JSON file path
    output_file_path = "extracted_info.json"

    # # Write the extracted information to a JSON file
    # with open(output_file_path, "w") as json_file:
    #     json.dump(extracted_info, json_file, indent=4)

    # print(f"Extracted information has been stored in {output_file_path}")

    # Initialize image_found.py
    completed_process = subprocess.run(["python", "image_found.py", output_file_path], capture_output=True)

    # Check if image_found.py produced any output
    if completed_process.stdout:
        # Combine the output from image_found.py with the extracted information
        with open('image_found_output.json') as f:
            image_found_output = json.load(f)

        combined_output = {**extracted_info, **image_found_output}

        # Define the combined output JSON file path
        combined_output_file_path = "extracted_data.json"

        # Write the combined output to a JSON file
        with open(combined_output_file_path, "w") as json_file:
            json.dump(combined_output, json_file, indent=4)

        print(f"Combined output has been stored in {combined_output_file_path}")
    else:
        # Write only the extracted information to the combined output JSON file
        with open("extracted_data.json", "w") as json_file:
            json.dump(extracted_info, json_file, indent=4)

if __name__ == "__main__":
    main()
