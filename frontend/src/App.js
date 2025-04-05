import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ArticleUpload from './TeacherUpload';
import ConfigureAssessment from './TeacherAssesment';
import Students from './students';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<ArticleUpload />} />
        <Route path="/configure-assessment" element={<ConfigureAssessment />} />
        <Route path="/students" element={<Students />} />
      </Routes>
    </Router>
  );
}

export default App;