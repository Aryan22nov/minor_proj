import { useEffect, useMemo, useRef, useState } from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";
import jsPDF from "jspdf";
import html2canvas from "html2canvas";

const DISEASE_INFO = {
  Acne: {
    severity: "low",
    description: "Common skin condition caused by clogged hair follicles and sebum production.",
    symptoms: ["Pimples", "Blackheads", "Whiteheads", "Redness", "Inflammation"],
    causes: ["Excess oil production", "Bacterial growth", "Clogged pores", "Hormonal changes"],
    precautions: [
      "Keep skin clean and dry",
      "Avoid touching your face",
      "Use non-comedogenic products",
      "Maintain a healthy diet",
      "Consult a dermatologist if severe"
    ]
  },
  Eczema: {
    severity: "medium",
    description: "A chronic inflammatory skin condition causing dry, itchy, and inflamed skin.",
    symptoms: ["Intense itching", "Dry skin", "Sensitive skin", "Redness", "Small raised bumps"],
    causes: ["Weak skin barrier", "Immune system dysfunction", "Stress", "Environmental triggers"],
    precautions: [
      "Moisturize regularly",
      "Avoid harsh soaps",
      "Identify and avoid triggers",
      "Keep nails trimmed",
      "Seek medical treatment"
    ]
  },
  Melanoma: {
    severity: "high",
    description: "A serious form of skin cancer developed from melanocyte cells. Early detection is crucial.",
    symptoms: ["Asymmetrical moles", "Irregular borders", "Multiple colors", "Large size (>6mm)", "Changing appearance"],
    causes: ["UV exposure", "Genetic predisposition", "Fair skin", "Family history of skin cancer"],
    precautions: [
      "Use SPF 30+ sunscreen daily",
      "Avoid prolonged sun exposure",
      "Wear protective clothing",
      "Perform monthly skin self-checks",
      "Consult a dermatologist immediately"
    ]
  },
  Psoriasis: {
    severity: "medium",
    description: "An autoimmune condition causing thick, scaly patches of skin.",
    symptoms: ["Red patches", "Silvery scales", "Thickened skin", "Bleeding", "Joint pain"],
    causes: ["Immune system dysfunction", "Genetics", "Stress", "Infections", "Certain medications"],
    precautions: [
      "Manage stress levels",
      "Keep skin moisturized",
      "Avoid skin trauma",
      "Limit alcohol consumption",
      "Work with a dermatologist"
    ]
  }
};

const SEVERITY_COLOR = {
  low: "#16a34a",
  medium: "#f59e0b",
  high: "#dc2626"
};

const ACCEPTED_TYPES = ["image/jpeg", "image/png", "image/webp"];

function formatPercent(value) {
  return `${(value * 100).toFixed(1)}%`;
}

function Spinner() {
  return (
    <div className="spinner" role="status" aria-label="Loading">
      <div />
      <div />
      <div />
      <div />
    </div>
  );
}

function ConfidenceExplanation({ confidence }) {
  let level = "very low";
  if (confidence >= 0.9) level = "very high";
  else if (confidence >= 0.75) level = "high";
  else if (confidence >= 0.6) level = "moderate";
  else if (confidence >= 0.4) level = "low";

  return (
    <div className="explanation">
      <p>
        <strong>Understanding the result:</strong> The model is {level} in its prediction
        ({formatPercent(confidence)}). This means the model's features strongly align with the detected condition.
        However, always consult a medical professional for an accurate diagnosis.
      </p>
    </div>
  );
}

function PredictionChart({ scores }) {
  if (!scores) return null;

  const data = Object.entries(scores)
    .map(([name, score]) => ({
      name,
      score: parseFloat((score * 100).toFixed(1))
    }))
    .sort((a, b) => b.score - a.score);

  return (
    <div className="chart-container">
      <h4>Confidence Distribution</h4>
      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis label={{ value: "Confidence (%)", angle: -90, position: "insideLeft" }} domain={[0, 100]} />
          <Tooltip formatter={(value) => `${value}%`} />
          <Bar dataKey="score" fill="#3b82f6" radius={[8, 8, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

function DiseaseInfoCard({ diseaseName, info }) {
  return (
    <div className="disease-info">
      <div className="info-header">
        <h3>{diseaseName}</h3>
        <span className="badge" style={{ background: SEVERITY_COLOR[info.severity] }}>
          {info.severity.toUpperCase()}
        </span>
      </div>

      <p className="description">{info.description}</p>

      <div className="info-grid">
        <div className="info-box">
          <h5>Symptoms</h5>
          <ul>
            {info.symptoms.map((s, i) => <li key={i}>{s}</li>)}
          </ul>
        </div>
        <div className="info-box">
          <h5>Causes</h5>
          <ul>
            {info.causes.map((c, i) => <li key={i}>{c}</li>)}
          </ul>
        </div>
      </div>

      <div className="info-box full">
        <h5>Precautions</h5>
        <ul>
          {info.precautions.map((p, i) => <li key={i}>{p}</li>)}
        </ul>
      </div>
    </div>
  );
}

function PredictionResult({ prediction, onDownloadReport }) {
  if (!prediction) return null;

  const info = DISEASE_INFO[prediction.disease] ?? {};
  const severity = info.severity ?? "low";
  const accent = SEVERITY_COLOR[severity] ?? SEVERITY_COLOR.low;

  // Top 3 predictions
  const topPredictions = Object.entries(prediction.scores)
    .map(([name, score]) => ({ name, score }))
    .sort((a, b) => b.score - a.score)
    .slice(0, 3);

  return (
    <div className="prediction-result" id="prediction-report">
      <div className="result-header">
        <div>
          <h2 className="result-title">{prediction.disease}</h2>
          <p className="result-subtitle">{info.description?.split(".")[0] || "Detected condition"}</p>
        </div>
        <span className="badge result-badge" style={{ background: accent }}>
          {severity.toUpperCase()}
        </span>
      </div>

      <div className="confidence-container">
        <div className="confidence-label">
          <span>Overall Confidence</span>
          <span className="confidence-value">{formatPercent(prediction.confidence)}</span>
        </div>
        <div className="progress-bar">
          <div
            className="progress-fill"
            style={{
              width: Math.round(prediction.confidence * 100) + "%",
              background: accent
            }}
          />
        </div>
      </div>

      <ConfidenceExplanation confidence={prediction.confidence} />

      <div className="top-predictions">
        <h4>Model's Top 3 Predictions</h4>
        <div className="predictions-list">
          {topPredictions.map((pred, idx) => (
            <div key={pred.name} className="prediction-item">
              <span className="rank">#{idx + 1}</span>
              <span className="name">{pred.name}</span>
              <span className="score">{formatPercent(pred.score)}</span>
            </div>
          ))}
        </div>
      </div>

      <PredictionChart scores={prediction.scores} />

      {info.description && <DiseaseInfoCard diseaseName={prediction.disease} info={info} />}

      <button className="download-btn" onClick={() => onDownloadReport(prediction)}>
        📥 Download Report
      </button>
    </div>
  );
}

function CameraCapture({ onClose, onCapture }) {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [isCameraActive, setIsCameraActive] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!isCameraActive) return;

    const startCamera = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: "environment" }
        });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch (err) {
        setError("Camera access denied or not available.");
      }
    };

    startCamera();

    return () => {
      if (videoRef.current && videoRef.current.srcObject) {
        videoRef.current.srcObject.getTracks().forEach((track) => track.stop());
      }
    };
  }, [isCameraActive]);

  const captureFrame = () => {
    if (videoRef.current && canvasRef.current) {
      const ctx = canvasRef.current.getContext("2d");
      canvasRef.current.width = videoRef.current.videoWidth;
      canvasRef.current.height = videoRef.current.videoHeight;
      ctx.drawImage(videoRef.current, 0, 0);

      canvasRef.current.toBlob((blob) => {
        const file = new File([blob], "camera-capture.png", { type: "image/png" });
        onCapture(file);
        onClose();
      }, "image/png");
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3>📷 Capture from Camera</h3>
          <button className="close-btn" onClick={onClose}>×</button>
        </div>

        {!isCameraActive ? (
          <div className="camera-placeholder">
            <div className="camera-icon">📹</div>
            <p>Point your camera at the skin area</p>
            <button
              type="button"
              className="primary"
              onClick={() => setIsCameraActive(true)}
            >
              Start Camera
            </button>
          </div>
        ) : (
          <>
            <div className="camera-container">
              <video
                ref={videoRef}
                autoPlay
                playsInline
                className="camera-video"
              />
              <canvas ref={canvasRef} className="visuallyHidden" />
            </div>
            {error && <p className="message error">{error}</p>}
            <div className="modal-actions">
              <button
                type="button"
                className="secondary"
                onClick={() => setIsCameraActive(false)}
              >
                Cancel
              </button>
              <button type="button" className="primary" onClick={captureFrame}>
                📸 Capture
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

function ImageEditor({ imageUrl, onClose, onApply }) {
  const [rotation, setRotation] = useState(0);
  const [zoomLevel, setZoomLevel] = useState(1);

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3>Image Editor</h3>
          <button className="close-btn" onClick={onClose}>×</button>
        </div>

        <div className="editor-preview">
          <img
            src={imageUrl}
            alt="Edit preview"
            style={{
              transform: `rotate(${rotation}deg) scale(${zoomLevel})`
            }}
          />
        </div>

        <div className="editor-controls">
          <div className="control">
            <label>Rotation: {rotation}°</label>
            <input
              type="range"
              min="-180"
              max="180"
              value={rotation}
              onChange={(e) => setRotation(Number(e.target.value))}
            />
          </div>
          <div className="control">
            <label>Zoom: {zoomLevel.toFixed(2)}x</label>
            <input
              type="range"
              min="0.5"
              max="3"
              step="0.1"
              value={zoomLevel}
              onChange={(e) => setZoomLevel(Number(e.target.value))}
            />
          </div>
        </div>

        <div className="modal-actions">
          <button className="secondary" onClick={onClose}>Cancel</button>
          <button className="primary" onClick={() => onApply(rotation, zoomLevel)}>Apply</button>
        </div>
      </div>
    </div>
  );
}

export default function App() {
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [status, setStatus] = useState("idle");
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const [history, setHistory] = useState([]);
  const [showEditor, setShowEditor] = useState(false);
  const [showCamera, setShowCamera] = useState(false);
  const [rotation, setRotation] = useState(0);
  const [zoomLevel, setZoomLevel] = useState(1);
  const [comparisonImages, setComparisonImages] = useState([]);
  const [showComparison, setShowComparison] = useState(false);

  const fileInputRef = useRef(null);
  const uploadSectionRef = useRef(null);

  // Load history from localStorage
  useEffect(() => {
    const saved = localStorage.getItem("predictionHistory");
    if (saved) setHistory(JSON.parse(saved));
  }, []);

  useEffect(() => {
    document.body.classList.toggle("dark", darkMode);
  }, [darkMode]);

  const canSubmit = file && status !== "pending";

  const handleFile = (incomingFile) => {
    if (!incomingFile) return;

    if (!ACCEPTED_TYPES.includes(incomingFile.type)) {
      setError("Unsupported file type. Please upload a JPG, PNG, or WEBP image.");
      setFile(null);
      setPreviewUrl(null);
      return;
    }

    setError(null);
    setPrediction(null);
    setFile(incomingFile);
    setRotation(0);
    setZoomLevel(1);

    const url = URL.createObjectURL(incomingFile);
    setPreviewUrl(url);
  };

  const onFileChange = (event) => {
    handleFile(event.target.files?.[0] ?? null);
  };

  const onDrop = (event) => {
    event.preventDefault();
    setDragActive(false);
    handleFile(event.dataTransfer.files?.[0] ?? null);
  };

  const onDragOver = (event) => {
    event.preventDefault();
    setDragActive(true);
  };

  const onDragLeave = () => {
    setDragActive(false);
  };

  const downloadReport = async (pred) => {
    try {
      const element = document.getElementById("prediction-report");
      const canvas = await html2canvas(element, { scale: 2, useCORS: true });
      const imgData = canvas.toDataURL("image/png");
      
      const pdf = new jsPDF("p", "mm", "a4");
      const imgWidth = 210;
      const imgHeight = (canvas.height * imgWidth) / canvas.width;
      
      pdf.addImage(imgData, "PNG", 0, 0, imgWidth, imgHeight);
      pdf.save(`skin-disease-report-${new Date().toISOString().slice(0, 10)}.pdf`);
    } catch (err) {
      console.error("PDF download failed:", err);
    }
  };

  async function onSubmit(event) {
    event.preventDefault();
    if (!file) {
      setError("Please upload a skin image before analyzing.");
      return;
    }

    setStatus("pending");
    setError(null);

    const formData = new FormData();
    formData.append("image", file);

    try {
      const response = await fetch("/predict", {
        method: "POST",
        body: formData
      });

      if (!response.ok) {
        const text = await response.text();
        throw new Error(`Server error ${response.status}: ${text}`);
      }

      const data = await response.json();

      if (data.error) {
        throw new Error(data.error);
      }

      setPrediction(data);

      // Save to history
      const newResult = {
        id: Date.now(),
        disease: data.disease,
        confidence: data.confidence,
        timestamp: new Date().toLocaleString(),
        scores: data.scores
      };
      const updated = [newResult, ...history].slice(0, 10);
      setHistory(updated);
      localStorage.setItem("predictionHistory", JSON.stringify(updated));
    } catch (err) {
      setError(err.message);
      setPrediction(null);
    } finally {
      setStatus("idle");
    }
  }

  const scrollToUpload = () => {
    uploadSectionRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  return (
    <div className="app">
      <header className="hero">
        <div className="heroContent">
          <h1>🏥 AI Skin Disease Detector</h1>
          <p className="heroSubtitle">
            Upload a photo and get an instant AI-powered prediction for common skin conditions.
          </p>
          <div className="heroActions">
            <button type="button" className="cta" onClick={scrollToUpload}>
              Upload Image
            </button>
            <button
              type="button"
              className="toggle"
              onClick={() => setDarkMode((prev) => !prev)}
              aria-label="Toggle dark mode"
            >
              {darkMode ? "☀️ Light" : "🌙 Dark"}
            </button>
          </div>
        </div>
      </header>

      <main>
        {/* Medical Disclaimer */}
        <section className="disclaimer">
          <div className="disclaimer-content">
            <strong>⚠️ Medical Disclaimer:</strong>
            <p>
              This AI tool provides predictions based on image analysis. It is NOT a substitute for professional medical diagnosis.
              Always consult a qualified dermatologist or healthcare professional for accurate diagnosis and treatment.
            </p>
          </div>
        </section>

        {/* Upload Section */}
        <section className="section" ref={uploadSectionRef}>
          <div className="sectionHeader">
            <h2>Upload your skin image</h2>
            <p>Drag & drop or select an image to analyze.</p>
          </div>

          <form className="uploadCard" onSubmit={onSubmit}>
            <div
              className={`dropzone ${dragActive ? "active" : ""}`}
              onDrop={onDrop}
              onDragOver={onDragOver}
              onDragLeave={onDragLeave}
              onClick={() => fileInputRef.current?.click()}
            >
              <div className="dropContent">
                <div className="dropIcon" aria-hidden="true">
                  📸
                </div>
                <div>
                  <p className="dropTitle">Drag & drop your image here</p>
                  <p className="dropSubtitle">PNG, JPG, or WEBP (max 10MB)</p>
                  <button type="button" className="buttonLink">
                    Browse files
                  </button>
                </div>
              </div>
              <input
                ref={fileInputRef}
                type="file"
                accept={ACCEPTED_TYPES.join(",")}
                onChange={onFileChange}
                className="visuallyHidden"
              />
            </div>

            {previewUrl ? (
              <div className="preview-section">
                <div className="preview">
                  <img
                    src={previewUrl}
                    alt="Preview"
                    style={{ transform: `rotate(${rotation}deg) scale(${zoomLevel})` }}
                  />
                </div>
                <button
                  type="button"
                  className="edit-btn"
                  onClick={() => setShowEditor(true)}
                >
                  ✏️ Edit Image
                </button>
              </div>
            ) : (
              <div className="preview placeholder">Selected image preview will appear here.</div>
            )}

            <button
              type="button"
              className="secondary"
              onClick={() => setShowCamera(true)}
              style={{ marginTop: "12px" }}
            >
              📷 Capture from Camera
            </button>

            <button type="submit" disabled={!canSubmit} className="primary">
              {status === "pending" ? "Analyzing..." : "🔍 Analyze Image"}
            </button>

            {error && <p className="message error">{error}</p>}
            {status === "pending" && <Spinner />}
          </form>

          {prediction && <PredictionResult prediction={prediction} onDownloadReport={downloadReport} />}
        </section>

        {/* How It Works Section */}
        <section className="section alternate">
          <h2>How It Works</h2>
          <div className="steps">
            <div className="step">
              <div className="stepIcon">1️⃣</div>
              <div>
                <h3>Upload Image</h3>
                <p>Select a clear photo of the affected skin area.</p>
              </div>
            </div>
            <div className="step">
              <div className="stepIcon">2️⃣</div>
              <div>
                <h3>Image Preprocessing</h3>
                <p>Image is resized, normalized, and prepared for the CNN model.</p>
              </div>
            </div>
            <div className="step">
              <div className="stepIcon">3️⃣</div>
              <div>
                <h3>CNN Analysis</h3>
                <p>Deep learning model analyzes features and patterns in the image.</p>
              </div>
            </div>
            <div className="step">
              <div className="stepIcon">4️⃣</div>
              <div>
                <h3>Prediction Output</h3>
                <p>Get confidence scores and detailed information about the prediction.</p>
              </div>
            </div>
          </div>
        </section>

        {/* History Section */}
        {history.length > 0 && (
          <section className="section">
            <h2>📋 Prediction History</h2>
            <div className="history-list">
              {history.map((item) => (
                <div key={item.id} className="history-item">
                  <div className="history-info">
                    <strong>{item.disease}</strong>
                    <span className="history-time">{item.timestamp}</span>
                  </div>
                  <div className="history-confidence">{formatPercent(item.confidence)}</div>
                </div>
              ))}
            </div>
          </section>
        )}
      </main>

      <footer className="footer">
        <div>
          <strong>🏥 AI Skin Disease Detector</strong> — Built with React, Flask, TensorFlow & CNN
        </div>
        <div>For educational and research purposes only.</div>
      </footer>

      {showEditor && previewUrl && (
        <ImageEditor
          imageUrl={previewUrl}
          onClose={() => setShowEditor(false)}
          onApply={(rot, zoom) => {
            setRotation(rot);
            setZoomLevel(zoom);
            setShowEditor(false);
          }}
        />
      )}
    </div>
  );
}
