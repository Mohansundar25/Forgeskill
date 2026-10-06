import { useState } from "react";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function App() {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    if (!file || !jobDescription.trim()) {
      setError("Please upload a resume and paste a job description.");
      return;
    }
    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("job_description", jobDescription);

    try {
      const res = await fetch(`${API_URL}/api/match`, { method: "POST", body: formData });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Something went wrong");
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="container">
      <h1>Forgeskill</h1>
      <p className="subtitle">See how well your resume matches a job, and what to learn next.</p>

      <form onSubmit={handleSubmit} className="card">
        <label>Resume (PDF)</label>
        <input type="file" accept="application/pdf" onChange={(e) => setFile(e.target.files[0])} />

        <label>Job description</label>
        <textarea
          rows={8}
          placeholder="Paste the job description here..."
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
        />

        <button type="submit" disabled={loading}>
          {loading ? "Analyzing..." : "Analyze match"}
        </button>
        {error && <p className="error">{error}</p>}
      </form>

      {result && (
        <div className="card">
          <h2>Match score: {result.match_score}%</h2>
          <div className="bar">
            <div className="fill" style={{ width: `${result.match_score}%` }} />
          </div>

          <h3>Matched skills</h3>
          <div className="chips">
            {result.matched_skills.map((s) => (
              <span key={s} className="chip ok">{s}</span>
            ))}
          </div>

          <h3>Missing skills</h3>
          <div className="chips">
            {result.missing_skills.length === 0 && <span>None</span>}
            {result.missing_skills.map((s) => (
              <span key={s} className="chip missing">{s}</span>
            ))}
          </div>

          {result.recommendations.length > 0 && (
            <>
              <h3>How to close the gap</h3>
              <ul>
                {result.recommendations.map((r) => (
                  <li key={r.skill}>
                    <strong>{r.skill}:</strong> {r.why} <em>{r.how_to_learn}</em>
                  </li>
                ))}
              </ul>
            </>
          )}
          {result.summary && <p className="summary">{result.summary}</p>}
        </div>
      )}
    </div>
  );
}
