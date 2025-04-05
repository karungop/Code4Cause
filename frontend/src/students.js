import React from 'react';
import './students.css';


const Students = () => {
  const assignments = [
    {
      id: 1,
      title: 'The Great Gatsby - Chapter 1',
      description: 'Identify key characters and settings.',
      dueDate: 'April 10, 2025',
    },
    {
      id: 2,
      title: 'To Kill a Mockingbird - Chapter 5',
      description: 'Explore themes of justice and empathy.',
      dueDate: 'April 12, 2025',
    },
    {
      id: 3,
      title: '1984 - Part 1',
      description: 'Discuss surveillance and control.',
      dueDate: 'April 15, 2025',
    },
  ];


  return (
    <div className="student-dashboard">
      <h1 className="dashboard-title">📘 Reading Assignments</h1>
      <div className="assignment-grid">
        {assignments.map((assignment) => (
          <div key={assignment.id} className="assignment-card">
            <h2 className="assignment-title">{assignment.title}</h2>
            <p className="assignment-desc">{assignment.description}</p>
            <p className="assignment-due">Due: {assignment.dueDate}</p>
            <button
              className="assignment-button"
              onClick={() => alert(`Starting: ${assignment.title}`)}
            >
              Start Assignment
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};


export default Students;