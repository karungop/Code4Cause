import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './teacherAssesment.css';

const ConfigureAssessment = () => {
  const [numQuestions, setNumQuestions] = useState(5);
  const [numMCQ, setNumMCQ] = useState(3);
  const [numShortAnswer, setNumShortAnswer] = useState(1);
  const [numLongAnswer, setNumLongAnswer] = useState(1);
  const [requireVerbalSummary, setRequireVerbalSummary] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
  
    try {
      const response = await fetch('http://127.0.0.1:5000/api/assessments/configure', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          total_questions: numQuestions,
          mcq: numMCQ,
          short_answer: numShortAnswer,
          long_answer: numLongAnswer,
          require_verbal_summary: requireVerbalSummary,
        }),
      });
  
      if (!response.ok) {
        throw new Error('Failed to configure assessment');
      }
  
      const data = await response.json();
      console.log('Success:', data);
      alert('Assessment configured successfully!');
      // Optionally, redirect somewhere after config
      // navigate('/assessment-preview');
    } catch (error) {
      console.error('Error:', error);
      alert('Something went wrong. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };
  

  const totalQuestions = numMCQ + numShortAnswer + numLongAnswer;

  return (
    <div className="config-container">
      <h1 className="config-title">Configure Assessment</h1>
      
      <div className="config-card">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="num-questions" className="form-label">
              Total Questions to Generate: {numQuestions}
            </label>
            <input
              type="range"
              id="num-questions"
              min="1"
              max="20"
              value={numQuestions}
              onChange={(e) => setNumQuestions(parseInt(e.target.value))}
              className="form-range"
            />
          </div>

          <div className="form-group">
            <h2 className="section-title">Question Type Distribution</h2>
            <p className="total-questions">
              Total distributed questions: {totalQuestions} (of {numQuestions} requested)
            </p>

            <div className="range-group">
              <div className="range-item">
                <label htmlFor="num-mcq" className="range-label">
                  Multiple Choice Questions: {numMCQ}
                </label>
                <input
                  type="range"
                  id="num-mcq"
                  min="0"
                  max={numQuestions}
                  value={numMCQ}
                  onChange={(e) => setNumMCQ(parseInt(e.target.value))}
                  className="form-range"
                />
              </div>

              <div className="range-item">
                <label htmlFor="num-short-answer" className="range-label">
                  Short Answer Questions: {numShortAnswer}
                </label>
                <input
                  type="range"
                  id="num-short-answer"
                  min="0"
                  max={numQuestions}
                  value={numShortAnswer}
                  onChange={(e) => setNumShortAnswer(parseInt(e.target.value))}
                  className="form-range"
                />
              </div>

              <div className="range-item">
                <label htmlFor="num-long-answer" className="range-label">
                  Long Answer Questions: {numLongAnswer}
                </label>
                <input
                  type="range"
                  id="num-long-answer"
                  min="0"
                  max={numQuestions}
                  value={numLongAnswer}
                  onChange={(e) => setNumLongAnswer(parseInt(e.target.value))}
                  className="form-range"
                />
              </div>
            </div>
          </div>

          <div className="form-group">
            <div className="checkbox-group">
              <input
                type="checkbox"
                id="verbal-summary"
                checked={requireVerbalSummary}
                onChange={(e) => setRequireVerbalSummary(e.target.checked)}
                className="checkbox-input"
              />
              <label htmlFor="verbal-summary" className="checkbox-label">
                Require Verbal Summary (1-3 minutes)
              </label>
            </div>
            {requireVerbalSummary && (
              <p className="checkbox-help">
                Students will be required to record a verbal summary which will be analyzed for key points, coherence, and vocabulary usage.
              </p>
            )}
          </div>

          <div className="form-actions">
          <button
      type="button"
      className="secondary-btn"
      onClick={() => navigate('/')} // Goes back to upload page
    >
      Back
    </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="primary-btn"
            >
              {isSubmitting ? 'Creating Assessment...' : 'Create Assessment'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ConfigureAssessment;