import { useState } from "react";

const API = "http://127.0.0.1:8000";

export default function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function processDocument() {
    if (!file) return;

    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${API}/api/documents/process`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Processing failed.");
      }

      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="page">
      <header className="hero">
        <div>
          <p className="eyebrow">AI DOCUMENT ACCESSIBILITY</p>
          <h1>DocVoice AI</h1>
          <p className="subtitle">
            Turn PDF documents into concise summaries and natural speech.
          </p>
        </div>
      </header>

      <section className="card upload-card">
        <h2>Upload a document</h2>
        <p className="muted">PDF only · maximum 10 MB · selectable text</p>

        <label className="dropzone">
          <input
            type="file"
            accept=".pdf,application/pdf"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
          />
          <span className="upload-icon">↑</span>
          <strong>{file ? file.name : "Choose a PDF file"}</strong>
          <span className="muted">
            {file ? `${(file.size / 1024 / 1024).toFixed(2)} MB` : "Click to browse"}
          </span>
        </label>

        <button disabled={!file || loading} onClick={processDocument}>
          {loading ? "Processing..." : "Analyze & Generate Audio"}
        </button>

        {error && <div className="error">{error}</div>}
      </section>

      {result && (
        <section className="results">
          <div className="card stats">
            <div>
              <span>Document</span>
              <strong>{result.filename}</strong>
            </div>
            <div>
              <span>Words</span>
              <strong>{result.word_count}</strong>
            </div>
          </div>

          <div className="grid">
            <article className="card">
              <h2>AI Summary</h2>
              <p>{result.summary}</p>
            </article>

            <article className="card">
              <h2>Key Topics</h2>
              <div className="tags">
                {result.keywords.map((keyword) => (
                  <span className="tag" key={keyword}>{keyword}</span>
                ))}
              </div>
            </article>
          </div>

          <article className="card">
            <h2>Listen</h2>
            <p className="muted">The generated audio narrates the summary.</p>
            <audio
              controls
              preload="metadata"
              src={`${API}${result.audio_url}`}
            />
          </article>

          <article className="card">
            <h2>Extracted Text Preview</h2>
            <pre className="preview">{result.text_preview}</pre>
          </article>
        </section>
      )}
    </main>
  );
}
