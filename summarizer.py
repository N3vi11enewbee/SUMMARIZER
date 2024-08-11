import os
import subprocess
import openai
import io
from PyPDF2 import PdfReader
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Set your OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]

def open_pdf_in_viewer(file_path: str):
    """Open the given PDF file in the default PDF viewer."""
    try:
        if os.name == 'nt':  # Windows
            os.startfile(file_path)
        elif os.uname().sysname == 'Darwin':  # macOS
            subprocess.run(['open', file_path])
        else:  # Linux
            
            subprocess.run(['xdg-open', file_path])
    except Exception as e:
        print(f"Failed to open file in viewer: {e}")

def extract_text_from_pdf(file_path: str) -> str:
    with open(file_path, 'rb') as f:
        pdf_reader = PdfReader(f)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def summarize_text(text: str, command: str) -> str:
    """Summarize the text using OpenAI API based on the given command."""
    prompt = f"Please {command} the following document: {text}"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=150,
    )

    summary = response['choices'][0]['message']['content'].strip()
    return summary

if __name__ == "__main__":
    # Hide the main Tkinter window
    Tk().withdraw()

    # Open the file selection dialog
    pdf_path = askopenfilename(
        title="Select a PDF file",
        filetypes=[("PDF files", "*.pdf")]
    )

    # Check if the file was selected
    if not pdf_path:
        print("No file selected. Exiting.")
        exit(1)

    # Open the PDF file in the default viewer
    open_pdf_in_viewer(pdf_path)

    # Wait for the user to review the file
    input("Press Enter after reviewing the PDF to proceed with summarization...")

    # Extract text from the PDF
    text = extract_text_from_pdf(pdf_path)

    # Ask the user for the type of summary
    command = input("Enter the command (e.g., 'summarize', 'extract key points'): ")

    # Summarize the text using OpenAI API
    summary = summarize_text(text, command)

    # Print the summary in the terminal
    print("\nSummary:\n")
    print(summary)
