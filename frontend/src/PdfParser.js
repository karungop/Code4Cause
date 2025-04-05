import { useState } from 'react';
import * as pdfjsLib from 'pdfjs-dist';

const PdfParser = () => {
  const [extractedText, setExtractedText] = useState('');

  const handlePdfUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // Initialize PDF.js worker
    pdfjsLib.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjsLib.version}/pdf.worker.min.js`;

    const arrayBuffer = await file.arrayBuffer();
    
    try {
      const pdf = await pdfjsLib.getDocument(arrayBuffer).promise;
      let fullText = '';

      for (let i = 1; i <= pdf.numPages; i++) {
        const page = await pdf.getPage(i);
        const textContent = await page.getTextContent();
        const pageText = textContent.items.map(item => item.str).join(' ');
        fullText += pageText + '\n\n';
      }

      setExtractedText(fullText);
    } catch (error) {
      console.error('Error parsing PDF:', error);
    }
  };

  return (
    <div>
      <input type="file" accept=".pdf" onChange={handlePdfUpload} />
      <div className="extracted-text">
        <h3>Extracted Text:</h3>
        <pre>{extractedText || 'No text extracted yet'}</pre>
      </div>
    </div>
  );
};

export default PdfParser;

