/* ============================================================================
   PAGE NAVIGATION
   ============================================================================ */

let currentPage = 'home';

function navigateTo(pageName) {
  console.log(`🔀 Navigating to: ${pageName}`);
  // Hide all pages
  document.querySelectorAll('.page').forEach(page => {
    page.classList.remove('active');
  });

  // Show selected page
  const page = document.getElementById(pageName + '-page');
  if (page) {
    page.classList.add('active');
    currentPage = pageName;
    window.scrollTo({ top: 0, behavior: 'smooth' });
    updateNavigation();
    console.log(`✅ Successfully navigated to ${pageName}`);
  } else {
    console.error(`❌ Page not found: ${pageName}-page`);
  }
}

function updateNavigation() {
  // Update navbar active state
  document.querySelectorAll('.nav-link').forEach(link => {
    link.classList.remove('active');
  });

  // Set active nav link based on current page
  const navButtons = document.querySelectorAll('.nav-link');
  navButtons.forEach((btn, idx) => {
    if ((currentPage === 'home' && idx === 0) ||
        (currentPage === 'upload' && idx === 1) ||
        (currentPage === 'history' && idx === 2)) {
      btn.classList.add('active');
    }
  });
}

/* ============================================================================
   DISEASE DATABASE
   ============================================================================ */

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
    causes: ["UV exposure", "Genetic predisposition", "Fair skin", "Family history"],
    precautions: [
      "Use SPF 30+ sunscreen daily",
      "Avoid prolonged sun exposure",
      "Wear protective clothing",
      "Perform monthly self-checks",
      "Consult a dermatologist immediately"
    ]
  },
  Psoriasis: {
    severity: "medium",
    description: "An autoimmune condition causing thick, scaly patches of skin.",
    symptoms: ["Red patches", "Silvery scales", "Thickened skin", "Bleeding", "Joint pain"],
    causes: ["Immune dysfunction", "Genetics", "Stress", "Infections", "Medications"],
    precautions: [
      "Manage stress levels",
      "Keep skin moisturized",
      "Avoid skin trauma",
      "Limit alcohol consumption",
      "Work with a dermatologist"
    ]
  }
};

const SEVERITY_COLORS = {
  low: "#10b981",
  medium: "#f59e0b",
  high: "#ef4444"
};

let predictionChart = null;
let currentPrediction = null;
let selectedFile = null;

/* ============================================================================
   EVENT LISTENERS - INITIALIZATION
   ============================================================================ */

document.addEventListener('DOMContentLoaded', () => {
  console.log('✅ DOMContentLoaded fired - Initializing app...');
  initializeEventListeners();
  loadHistoryFromStorage();
  applyThemePreference();
  console.log('✅ App initialization complete');
});

function initializeEventListeners() {
  // Theme toggle
  document.getElementById('themeToggle').addEventListener('click', toggleTheme);

  // File input
  const fileInput = document.getElementById('fileInput');
  fileInput.addEventListener('change', handleFileSelect);

  // Drag and drop
  const dropzone = document.getElementById('dropzone');
  dropzone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropzone.classList.add('active');
  });
  dropzone.addEventListener('dragleave', () => dropzone.classList.remove('active'));
  dropzone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropzone.classList.remove('active');
    const files = e.dataTransfer.files;
    if (files.length > 0) handleFileSelect({ target: { files } });
  });
}

/* ============================================================================
   THEME MANAGEMENT
   ============================================================================ */

function toggleTheme() {
  const isDark = document.body.classList.toggle('dark');
  localStorage.setItem('theme', isDark ? 'dark' : 'light');
  updateThemeIcon();
}

function applyThemePreference() {
  const theme = localStorage.getItem('theme') || 'light';
  if (theme === 'dark') {
    document.body.classList.add('dark');
  }
  updateThemeIcon();
}

function updateThemeIcon() {
  const icon = document.getElementById('themeToggle').querySelector('.theme-icon');
  icon.textContent = document.body.classList.contains('dark') ? '☀️' : '🌙';
}

/* ============================================================================
   FILE HANDLING
   ============================================================================ */

function handleFileSelect(event) {
  console.log('📁 File selected');
  const files = event.target.files;
  if (!files || files.length === 0) {
    console.warn('⚠️ No files in selection');
    return;
  }

  const file = files[0];
  const validTypes = ['image/jpeg', 'image/png', 'image/webp'];

  console.log(`📸 File: ${file.name}, Type: ${file.type}, Size: ${(file.size / 1024).toFixed(2)}KB`);

  if (!validTypes.includes(file.type)) {
    console.error('❌ Invalid file type');
    showError('Unsupported file format. Please upload JPG, PNG, or WEBP.');
    return;
  }

  if (file.size > 10 * 1024 * 1024) {
    console.error('❌ File too large');
    showError('File size exceeds 10MB. Please choose a smaller image.');
    return;
  }

  selectedFile = file;
  displayPreview(file);
  clearError();
  console.log('✅ File validated and preview displaying');
}

function displayPreview(file) {
  const reader = new FileReader();
  reader.onload = (e) => {
    const previewImage = document.getElementById('previewImage');
    previewImage.src = e.target.result;

    document.getElementById('fileName').textContent = `📄 ${file.name}`;
    document.getElementById('fileSize').textContent = `${(file.size / 1024).toFixed(2)} KB`;

    document.getElementById('previewSection').style.display = 'block';
    document.getElementById('analyzeBtn').disabled = false;
  };
  reader.readAsDataURL(file);
}

function resetImage() {
  selectedFile = null;
  document.getElementById('fileInput').value = '';
  document.getElementById('previewSection').style.display = 'none';
  document.getElementById('analyzeBtn').disabled = true;
  document.getElementById('resultSection').style.display = 'none';
}

/* ============================================================================
   CAMERA CAPTURE
   ============================================================================ */

let cameraStream = null;

async function openCamera() {
  document.getElementById('cameraModal').style.display = 'flex';
}

function closeCamera() {
  stopCamera();
  document.getElementById('cameraModal').style.display = 'none';
}

async function startCamera() {
  try {
    cameraStream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: 'environment', width: { ideal: 1280 }, height: { ideal: 720 } }
    });

    const video = document.getElementById('cameraVideo');
    video.srcObject = cameraStream;

    document.getElementById('cameraPlaceholder').style.display = 'none';
    document.getElementById('cameraView').style.display = 'block';
    document.getElementById('startCameraBtn').style.display = 'none';
    document.getElementById('stopCameraBtn').style.display = 'block';
    document.getElementById('captureBtn').style.display = 'block';
  } catch (err) {
    showError('Camera access denied. Please check your permissions.');
  }
}

function stopCamera() {
  if (cameraStream) {
    cameraStream.getTracks().forEach(track => track.stop());
    cameraStream = null;
  }

  document.getElementById('cameraView').style.display = 'none';
  document.getElementById('cameraPlaceholder').style.display = 'flex';
  document.getElementById('startCameraBtn').style.display = 'block';
  document.getElementById('stopCameraBtn').style.display = 'none';
  document.getElementById('captureBtn').style.display = 'none';
}

function capturePhoto() {
  const video = document.getElementById('cameraVideo');
  const canvas = document.getElementById('captureCanvas');

  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;

  const ctx = canvas.getContext('2d');
  ctx.drawImage(video, 0, 0);

  canvas.toBlob((blob) => {
    const file = new File([blob], 'camera-capture.png', { type: 'image/png' });
    selectedFile = file;
    displayPreview(file);
    closeCamera();
  }, 'image/png');
}

/* ============================================================================
   PREDICTION
   ============================================================================ */

async function handleSubmit(event) {
  console.log('📤 Form submitted');
  event.preventDefault();

  if (!selectedFile) {
    console.warn('⚠️ No file selected');
    showError('Please select or capture an image first.');
    return;
  }

  console.log(`📸 Analyzing image: ${selectedFile.name}`);
  clearError();
  showLoading();

  const formData = new FormData();
  formData.append('image', selectedFile);

  try {
    console.log('🚀 Sending request to /predict...');
    const response = await fetch('/predict', {
      method: 'POST',
      body: formData
    });

    console.log(`📡 Response status: ${response.status}`);

    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ Prediction received:', data);

    if (data.error) {
      throw new Error(data.error);
    }

    currentPrediction = data;
    displayPrediction(data);
    savePredictionToHistory(data);

  } catch (err) {
    console.error('❌ Error:', err);
    showError(`Prediction failed: ${err.message}`);
  } finally {
    hideLoading();
  }
}

function displayPrediction(prediction) {
  const info = DISEASE_INFO[prediction.disease] || {};
  const severity = info.severity || 'low';

  // Render result card HTML
  let resultHTML = `
    <div class="prediction-card">
      <div class="prediction-header">
        <div>
          <h2 class="disease-name">${prediction.disease}</h2>
          <p class="disease-description">${info.description || ''}</p>
        </div>
        <span class="severity-badge ${severity}">
          ${severity.toUpperCase()}
        </span>
      </div>

      <div class="confidence-section">
        <div class="confidence-label">
          <span>Overall Confidence</span>
          <span class="confidence-value">${formatPercent(prediction.confidence)}</span>
        </div>
        <div class="confidence-bar">
          <div class="confidence-progress" style="width: ${Math.round(prediction.confidence * 100)}%; background: ${SEVERITY_COLORS[severity]};"></div>
        </div>
        <p class="confidence-explanation">${getConfidenceExplanation(prediction.confidence)}</p>
      </div>

      <div class="top-predictions">
        <h3>Model's Top 3 Predictions</h3>
        <div class="predictions-list">
  `;

  // Top 3 predictions
  const topPredictions = Object.entries(prediction.scores)
    .map(([name, score]) => ({ name, score }))
    .sort((a, b) => b.score - a.score)
    .slice(0, 3);

  topPredictions.forEach((pred, idx) => {
    resultHTML += `
      <div class="prediction-item">
        <span class="rank">#${idx + 1}</span>
        <span class="name">${pred.name}</span>
        <span class="score">${formatPercent(pred.score)}</span>
      </div>
    `;
  });

  resultHTML += `
        </div>
      </div>
  `;

  // Chart (lazy load)
  resultHTML += `
      <div class="chart-container">
        <h3>Confidence Distribution</h3>
        <canvas id="predictionChart"></canvas>
      </div>
  `;

  // Disease info
  if (info.description) {
    resultHTML += getDiseaseInfoHTML(prediction.disease, info);
  }

  resultHTML += `
      <button class="btn-report" onclick="downloadReport()">📥 Download Report</button>

      <div class="result-nav-buttons">
        <button class="btn-secondary" onclick="navigateTo('upload')">📤 Upload Another</button>
        <button class="btn-secondary" onclick="navigateTo('history')">📋 View History</button>
      </div>
    </div>
  `;

  document.getElementById('resultSection').innerHTML = resultHTML;
  navigateTo('result');

  // Render chart after navigation
  setTimeout(() => {
    displayChart(prediction.scores);
  }, 100);
}

function formatPercent(value) {
  return `${(value * 100).toFixed(1)}%`;
}

function getConfidenceExplanation(confidence) {
  let level = 'very low';
  if (confidence >= 0.9) level = 'very high';
  else if (confidence >= 0.75) level = 'high';
  else if (confidence >= 0.6) level = 'moderate';
  else if (confidence >= 0.4) level = 'low';

  return `The model is ${level} in its prediction (${formatPercent(confidence)}). This means the model's features strongly align with the detected condition. However, always consult a medical professional for an accurate diagnosis.`;
}

/* ============================================================================
   CHART VISUALIZATION
   ============================================================================ */

function displayChart(scores) {
  const ctx = document.getElementById('predictionChart');
  if (!ctx) return;

  const data = Object.entries(scores)
    .map(([name, score]) => ({
      label: name,
      value: parseFloat((score * 100).toFixed(1))
    }))
    .sort((a, b) => b.value - a.value);

  if (predictionChart) {
    predictionChart.destroy();
  }

  document.getElementById('chartContainer').style.display = 'block';

  predictionChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: data.map(d => d.label),
      datasets: [{
        label: 'Confidence (%)',
        data: data.map(d => d.value),
        backgroundColor: '#3b82f6',
        borderRadius: 8,
        borderSkipped: false
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      indexAxis: 'y',
      plugins: {
        legend: { display: false }
      },
      scales: {
        x: {
          max: 100,
          ticks: {
            callback: function(value) {
              return value + '%';
            }
          }
        }
      }
    }
  });
}

/* ============================================================================
   DISEASE INFORMATION
   ============================================================================ */

function getDiseaseInfoHTML(diseaseName, info) {
  let html = `
    <div class="disease-info-section">
      <div class="disease-info-card">
        <h4>📋 Description</h4>
        <p>${info.description}</p>
      </div>
  `;

  if (info.symptoms && info.symptoms.length > 0) {
    html += `
      <div class="disease-info-card">
        <h4>🔴 Typical Symptoms</h4>
        <ul>${info.symptoms.map(s => `<li>${s}</li>`).join('')}</ul>
      </div>
    `;
  }

  if (info.causes && info.causes.length > 0) {
    html += `
      <div class="disease-info-card">
        <h4>🔍 Common Causes</h4>
        <ul>${info.causes.map(c => `<li>${c}</li>`).join('')}</ul>
      </div>
    `;
  }

  if (info.precautions && info.precautions.length > 0) {
    html += `
      <div class="disease-info-card">
        <h4>✅ Precautions & Recommendations</h4>
        <ul>${info.precautions.map(p => `<li>${p}</li>`).join('')}</ul>
      </div>
    `;
  }

  html += '</div>';
  return html;
}

function displayDiseaseInfo(diseaseName, info) {
  const container = document.getElementById('diseaseInfo');
  
  let html = `
    <div class="disease-info-card">
      <h4>📋 Description</h4>
      <p>${info.description}</p>
    </div>
  `;

  if (info.symptoms && info.symptoms.length > 0) {
    html += `
      <div class="disease-info-card">
        <h4>🔴 Typical Symptoms</h4>
        <ul>${info.symptoms.map(s => `<li>${s}</li>`).join('')}</ul>
      </div>
    `;
  }

  if (info.causes && info.causes.length > 0) {
    html += `
      <div class="disease-info-card">
        <h4>🔍 Common Causes</h4>
        <ul>${info.causes.map(c => `<li>${c}</li>`).join('')}</ul>
      </div>
    `;
  }

  if (info.precautions && info.precautions.length > 0) {
    html += `
      <div class="disease-info-card">
        <h4>✅ Precautions & Recommendations</h4>
        <ul>${info.precautions.map(p => `<li>${p}</li>`).join('')}</ul>
      </div>
    `;
  }

  container.innerHTML = html;
}

/* ============================================================================
   HISTORY MANAGEMENT
   ============================================================================ */

function savePredictionToHistory(prediction) {
  let history = JSON.parse(localStorage.getItem('skinPredictionHistory') || '[]');

  const entry = {
    id: Date.now(),
    disease: prediction.disease,
    confidence: prediction.confidence,
    scores: prediction.scores,
    timestamp: new Date().toLocaleString()
  };

  history.unshift(entry);
  history = history.slice(0, 20); // Keep last 20

  localStorage.setItem('skinPredictionHistory', JSON.stringify(history));
  displayHistory();
}

function loadHistoryFromStorage() {
  const history = JSON.parse(localStorage.getItem('skinPredictionHistory') || '[]');
  if (history.length > 0) {
    displayHistory();
  }
}

function displayHistory() {
  const history = JSON.parse(localStorage.getItem('skinPredictionHistory') || '[]');

  if (history.length === 0) {
    document.getElementById('historyContent').style.display = 'none';
    document.getElementById('historyEmpty').style.display = 'flex';
    document.getElementById('historyNavBtn').style.display = 'none';
    return;
  }

  const historyList = document.getElementById('historyList');
  historyList.innerHTML = history
    .map(item => `
      <div class="history-item">
        <div class="history-info">
          <strong>${item.disease}</strong>
          <span class="history-time">${item.timestamp}</span>
        </div>
        <div class="history-confidence">${formatPercent(item.confidence)}</div>
      </div>
    `)
    .join('');

  document.getElementById('historyContent').style.display = 'block';
  document.getElementById('historyEmpty').style.display = 'none';
  document.getElementById('historyNavBtn').style.display = 'block';
}

function clearHistory() {
  if (confirm('Clear all prediction history?')) {
    localStorage.removeItem('skinPredictionHistory');
    displayHistory();
  }
}

/* ============================================================================
   REPORT GENERATION
   ============================================================================ */

async function downloadReport() {
  if (!currentPrediction) return;

  try {
    // Check if html2canvas and jsPDF are available
    if (typeof html2canvas === 'undefined' || typeof jspdf === 'undefined') {
      showError('Report generation libraries are loading. Please try again in a moment.');
      return;
    }

    const element = document.getElementById('resultSection');
    const canvas = await html2canvas(element, {
      scale: 2,
      allowTaint: true,
      useCORS: true,
      backgroundColor: '#ffffff'
    });

    const imgData = canvas.toDataURL('image/png');
    const jsPDF = window.jspdf.jsPDF;
    const pdf = new jsPDF('p', 'mm', 'a4');

    const pageWidth = pdf.internal.pageSize.getWidth();
    const pageHeight = pdf.internal.pageSize.getHeight();
    const imgWidth = pageWidth - 20;
    const imgHeight = (canvas.height * imgWidth) / canvas.width;

    let heightLeft = imgHeight;
    let position = 0;

    pdf.addImage(imgData, 'PNG', 10, position, imgWidth, imgHeight);
    heightLeft -= pageHeight - 20;

    while (heightLeft > 0) {
      position = heightLeft - imgHeight;
      pdf.addPage();
      pdf.addImage(imgData, 'PNG', 10, position, imgWidth, imgHeight);
      heightLeft -= pageHeight;
    }

    const date = new Date().toISOString().split('T')[0];
    pdf.save(`skin-disease-report-${date}.pdf`);
  } catch (err) {
    console.error('PDF generation failed:', err);
    showError('Failed to generate report. Please try again.');
  }
}

/* ============================================================================
   UI HELPERS
   ============================================================================ */

function showLoading() {
  document.getElementById('loadingState').style.display = 'flex';
}

function hideLoading() {
  document.getElementById('loadingState').style.display = 'none';
}

function showError(message) {
  const errorDiv = document.getElementById('errorMessage');
  errorDiv.textContent = message;
  errorDiv.style.display = 'block';
}

function clearError() {
  document.getElementById('errorMessage').style.display = 'none';
}
