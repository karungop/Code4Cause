import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';  // Import Link from react-router-dom
import './students.css';
import { useNavigate } from 'react-router-dom';

const Students = () => {
  const [assignments, setAssignments] = useState([]);

  const navigate = useNavigate();
  const handleStartAssignment = () => {
    navigate('/recording');
  };
  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/articles')
      .then((response) => response.json())
      .then((data) => setAssignments(data))
      .catch((error) => console.error('Error fetching assignments:', error));
  }, []);

  return (
    <div className="student-dashboard">
      <h1 className="dashboard-title">📘 Reading Assignments</h1>
      <div className="assignment-grid">
        {assignments.map((assignment) => (
          <div key={assignment.id} className="assignment-card">
            <h2 className="assignment-title">{assignment.title}</h2>
            <p className="assignment-desc">{assignment.description}</p>
            <p className="assignment-due">Due: {assignment.dueDate}</p>
            <button class = "assignment-button" onClick={handleStartAssignment} className="start-button">
      Start Assignment
    </button >
          </div>
        ))}
        {assignments.length > 0 ? (
          assignments.map((assignment) => (
            <div key={assignment.id} className="assignment-card">
              <h2 className="assignment-title">{assignment.title}</h2>
              <p className="assignment-due">
                Due: {new Date(assignment.created_at).toLocaleDateString()}
              </p>
              <Link to={`/assignment/${assignment.id}`} className="assignment-link">
                View Assignment
              </Link>
            </div>
          ))
        ) : (
          <p>No assignments found</p>
        )}
      </div>
    </div>
  );
};

export default Students;
