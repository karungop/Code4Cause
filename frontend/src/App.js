import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ArticleUpload from './teacherUpload';
import ConfigureAssessment from './teacherAssesment';
import StudentDashboard from './students';
import Recording from './recording';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<ArticleUpload />} />
        <Route path="/configure-assessment" element={<ConfigureAssessment />} />
        <Route path="/students" element={<StudentDashboard/>}/>
        <Route path="/recording" element={<Recording/>}/>
      </Routes>
    </Router>
  );
}

export default App;