import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ArticleUpload from './teacherUpload';
import ConfigureAssessment from './teacherAssesment';
import Students from './students';
import AssignmentDetail from './AssignmentDetail';  // The component to show assignment details


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<ArticleUpload />} />
        <Route path="/configure-assessment" element={<ConfigureAssessment />} />
        <Route path="/students" element={<Students />} />
        <Route path="/assignment/:id" element={<AssignmentDetail />} />
      </Routes>
    </Router>
  );
}

export default App;