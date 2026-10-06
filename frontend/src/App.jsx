import { useState } from 'react';

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function Chips({ items, kind }) {
  if (!items?.length) return <p className='muted'>None</p>;
  return (
    <div className='chips'>
      {items.map((s) => (
        <span key={s} className={`chip ${kind}`}>{s}</span>
      ))}
    </div>
  );
}

export default function App() {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  async function analyze(e) {
    e.preventDefault();
    if (!file || !jobDescription.trim()) {
      setError('Upload a PDF resume and paste a job description.');
      return;
    }
    setError('');
    setLoading(true);
    setResult(null);
    try {
      const form = new FormData();
      form.append('file', file);
      form.append('job_description', jobDescription);
      const res = await fetch(`${API}/api/analyze`, { method: 'POST', body: form });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Request failed');
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className='container'>
      <h1>🔨 Forgeskill</h1>
      <p className='muted'>AI-powered resume–job matching and skill-gap analysis</p>

      <form onSubmit={analyze} className='card'>
        <label>Resume (PDF)</label>
        <input type='file' accept='application/pdf' onChange={(e) => setFile(e.target.files[0])} />
        <label>Job description</label>
        <textarea rows={8} value={jobDescription} onChange={(e) => setJobDescription(e.target.value)} placeholder='Paste the job description here…' />
        <button disabled={loading}>{loading ? '🤖 Analyzing with AI…' : 'Analyze match'}</button>
        {error && <p className='error'>{error}</p>}
      </form>

      {result && (
        <div className='card'>
          <h2>Match score: {result.match_score}%</h2>
          <div className='bar'><div style={{ width: `${result.match_score}%` }} /></div>
          {result.summary && <p><b>🤖 AI summary:</b> {result.summary}</p>}
          <h3>Matched skills</h3>
          <Chips items={result.matched_skills} kind='ok' />
          <h3>Missing skills</h3>
          <Chips items={result.missing_skills} kind='miss' />
          <h3>AI learning recommendations</h3>
          <ul>
            {result.recommendations.map((r) => (
              <li key={r.skill}><b>{r.skill}</b> — {r.why} <i>Next step: {r.how_to_learn}</i></li>
            ))}
          </ul>
          <h3>Skills found in your resume</h3>
          <Chips items={result.resume_skills} kind='neutral' />
        </div>
      )}
    </div>
  );
}
