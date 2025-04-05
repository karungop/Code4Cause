import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './teacherUpload.css';

const ArticleUpload = () => {
  const [articleUrl, setArticleUrl] = useState('');
  const [pdfFile, setPdfFile] = useState(null);
  const [uploadMethod, setUploadMethod] = useState('url');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    setIsLoading(true);
    
    setTimeout(() => {
      setIsLoading(false);
      navigate('/configure-assessment');
    }, 1500);
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