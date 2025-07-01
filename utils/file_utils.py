import os
from datetime import datetime

def save_transcript(transcript_text, output_dir="output"):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Create timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"transcript_{timestamp}.txt"
    file_path = os.path.join(output_dir, filename)

    # Save transcript
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(transcript_text)

    return file_path


