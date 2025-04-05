import openai
import fitz  # PyMuPDF

# Set your OpenAI API key
openai.api_key = "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"

# Path to your PDF file
pdf_file_path = "C:\\Users\\Nithin\\Downloads\\_.._storage_pdfs_english-text-wonderful-family.pdf"

# Function to extract text from the PDF
def extract_text_from_pdf(pdf_path):
    try:
        # Open the PDF file
        doc = fitz.open(pdf_path)
        
        # Initialize an empty string to store the extracted text
        full_text = ""
        
        # Extract text from each page
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            full_text += page.get_text()
        
        return full_text
    except Exception as e:
        print(f"Error reading PDF: {str(e)}")
        return None

# Extract text from the PDF
pdf_text = extract_text_from_pdf(pdf_file_path)

if pdf_text:
    try:
        # Print the first 500 characters of the extracted text (for debugging)
        print("Extracted Text (First 500 chars): ", pdf_text[:500])

        # Limit text to stay within the token limit (approx. 4000 tokens for GPT-3.5)
        input_text = pdf_text[:2000]  # Adjust as needed

        # Send the extracted text to OpenAI for processing
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Or "gpt-4"
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Please process the text extracted from the PDF."},
                {"role": "user", "content": input_text},
            ]
        )

        # Access the response correctly
        if 'choices' in response and len(response['choices']) > 0:
            result_text = response['choices'][0]['message']['content'].strip()
            print("Processed Text from OpenAI: ", result_text)
        else:
            print("No valid response from OpenAI.")
        
    except Exception as e:
        print(f"Error processing with OpenAI: {str(e)}")
else:
    print("Failed to extract text from PDF.")
