import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';  // Import useParams to get the assignment ID from the URL

const StudentAssignment = () => {
  const { id } = useParams();  // Get the assignment ID from the URL params
  const [assignment, setAssignment] = useState(null);  // State to store the assignment data

  // Fetch the assignment data from the API using the ID
  useEffect(() => {
    fetch(`http://127.0.0.1:5000/api/articles/${id}`)
      .then((response) => response.json())
      .then((data) => setAssignment(data))  // Update the state with the fetched data
      .catch((error) => console.error('Error fetching assignment:', error));
  }, [id]);  // Re-fetch when the ID changes

  if (!assignment) {
    return <p>Loading...</p>;  // Display loading message while fetching data
  }

  return (
    <div className="assignment-detail">
      <h1 className="assignment-title">{assignment.title}</h1>
      <h2 className="assignment-author">Author: {assignment.author}</h2>
      <p className="assignment-content">{assignment.content}</p>
      <p className="assignment-due">
        Assigned At: {new Date(assignment.created_at).toLocaleDateString()}
      </p>
      <p className="assignment-updated">
        Last Updated: {new Date(assignment.updated_at).toLocaleDateString()}
      </p>
    </div>
  );
};

export default StudentAssignment;
