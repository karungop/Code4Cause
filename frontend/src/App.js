import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ArticleUpload from './teacherUpload';
import ConfigureAssessment from './teacherAssesment';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<ArticleUpload />} />
        <Route path="/configure-assessment" element={<ConfigureAssessment />} />
      </Routes>
    </Router>
  );
}

export default App;