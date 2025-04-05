import React, { useState } from "react";
import './recording.css';

const Recordings = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [transcription, setTranscription] = useState("");

  const handleRecording = async () => {
    if (!isRecording) {
      try {
        await fetch("http://127.0.0.1:5000/start", {
          method: "POST",
        });
        setIsRecording(true);
      } catch (error) {
        console.error("Error starting recording:", error);
      }
    } else {
      try {
        const response = await fetch("http://127.0.0.1:5000/stop", {
          method: "POST",
        });
        const data = await response.json();
        setTranscription(data.transcription || "No transcription found.");
        setIsRecording(false);
      } catch (error) {
        console.error("Error stopping recording:", error);
      }
    }
  };

  return (
    <div className="recordingsp">
      {/* Display either the recording animation or the gif depending on the recording state */}
      {isRecording ? (
        <img src="/rec.gif" alt="Recording animation" className = "ra"/>
      ) : (
        <div className="recording-circle"></div>
      )}
      <button
        onClick={handleRecording}
        className="button"
      >
        {isRecording ? "Finish Recording" : "Start Recording"}
      </button>
      {transcription && (
        <div className="divtransc">
          <h2 className="ursum">Your summary:</h2>
          <p>{transcription}</p>
        </div>
      )}
    </div>
  );
};

export default Recordings;
