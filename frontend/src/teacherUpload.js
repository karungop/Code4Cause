import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './TeacherUpload.css';

const ArticleUpload = () => {
  const [articleUrl, setArticleUrl] = useState('');
  const [pdfFile, setPdfFile] = useState(null);
  const [uploadMethod, setUploadMethod] = useState('url');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
  
    try {
      if (uploadMethod === 'url') {
        // Send the URL to Flask
        const response = await fetch('http://127.0.0.1:5000/api/articles/upload-url', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ url: articleUrl }),
        });
  
        if (!response.ok) {
          throw new Error('Failed to upload URL');
        }
  
        const data = await response.json();
        console.log('Success:', data);
      } else {
        // Handle PDF upload
    if (!pdfFile) {
      throw new Error('Please select a PDF file');
    }

    const formData = new FormData();
    formData.append('pdf', pdfFile);

    const response = await fetch('http://127.0.0.1:5000/api/articles/upload-pdf', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to process PDF');
    }

    const data = await response.json();
    console.log('PDF processing success:', data);
    alert(`Successfully processed PDF!\nFilename: ${data.details.filename}\nPages: ${data.page_count || 'N/A'}\nSize: ${(data.details.size_bytes)}`);
  }
  
      // Navigate after successful submission
      navigate('/configure-assessment');
    } catch (error) {
      console.error('Error:', error);
      alert('Failed to upload. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="upload-container">
      <h1 className="upload-title">Upload Article</h1>
      
      <div className="upload-card">
        <div className="method-toggle">
          <button
            onClick={() => setUploadMethod('url')}
            className={`toggle-btn ${uploadMethod === 'url' ? 'active' : ''}`}
          >
            URL
          </button>
          <button
            onClick={() => setUploadMethod('pdf')}
            className={`toggle-btn ${uploadMethod === 'pdf' ? 'active' : ''}`}
          >
            PDF Upload
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          {uploadMethod === 'url' ? (
            <div className="form-group">
              <label htmlFor="article-url" className="form-label">
                Article URL
              </label>
              <input
                type="url"
                id="article-url"
                value={articleUrl}
                onChange={(e) => setArticleUrl(e.target.value)}
                className="form-input"
                placeholder="https://example.com/article"
                required
              />
            </div>
          ) : (
            <div className="form-group">
              <label htmlFor="pdf-upload" className="form-label">
                PDF File
              </label>
              <input
                type="file"
                id="pdf-upload"
                accept=".pdf"
                onChange={(e) => setPdfFile(e.target.files[0])}
                className="form-input"
                required
              />
              {pdfFile && (
                <p className="file-selected">Selected: {pdfFile.name}</p>
              )}
            </div>
          )}

          <div className="form-actions">
            <button
              type="submit"
              disabled={isLoading}
              className="submit-btn"
            >
              {isLoading ? 'Processing...' : 'Continue'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ArticleUpload;