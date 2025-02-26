import React, { useState } from "react";

function HomePage() {
  const [problemDescription, setProblemDescription] = useState("");
  const [solutionOutline, setSolutionOutline] = useState("");
  const [loading, setLoading] = useState(false);

  const generateSolutionOutline = async () => {
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:5000/generate_solution", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ problem_description: problemDescription }),
      });

      if (!response.ok) {
        throw new Error("Failed to generate solution outline.");
      }

      const data = await response.json();
      setSolutionOutline(data.solutionOutline); // Assuming your backend returns { solutionOutline: "..." }
    } catch (error) {
      console.error("Error generating solution outline:", error);
      setSolutionOutline("Failed to generate solution outline. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <h1 className="app-title">LeetCode Helper</h1>
      <div className="card">
        <textarea
          value={problemDescription}
          onChange={(e) => setProblemDescription(e.target.value)}
          placeholder="Paste or type the LeetCode problem description here..."
          className="text-area"
          rows="6"
        ></textarea>
        <button
          onClick={generateSolutionOutline}
          disabled={loading}
          className="generate-btn"
        >
          {loading ? "Loading..." : "Generate Solution Outline"}
        </button>
        {solutionOutline && (
          <div className="solution-container">
            <h3 className="solution-title">Solution Outline</h3>
            <div className="solution-content">{solutionOutline}</div>
          </div>
        )}
      </div>
    </div>
  );
}

export default HomePage;
