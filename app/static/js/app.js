// Return Insight Client JavaScript Helpers
console.log("Return Insight Platform Initialized");

async function submitSingleAnalysis(event) {
  event.preventDefault();
  const form = document.getElementById("analysisForm");
  const formData = new FormData(form);
  const data = Object.fromEntries(formData.entries());

  const resultContainer = document.getElementById("analysisResult");
  resultContainer.innerHTML = '<div class="spinner-border text-primary" role="status"></div> Analyzing...';

  try {
    const response = await fetch("/api/analyse", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });
    const res = await response.json();

    let evidenceHtml = "";
    if (res.evidence && res.evidence.evidence_signals) {
      evidenceHtml = res.evidence.evidence_signals.map(s => `<li>${s}</li>`).join("");
    }

    resultContainer.innerHTML = `
      <div class="card card-custom">
        <div class="card-header bg-primary text-white">
          AI Root Cause Prediction Result
        </div>
        <div class="card-body">
          <h5>Return ID: ${res.return_id}</h5>
          <p><strong>Predicted Reason:</strong> <span class="badge bg-primary fs-6">${res.predicted_reason}</span></p>
          <p><strong>Confidence:</strong> ${(res.confidence * 100).toFixed(1)}%</p>
          <p><strong>Root Cause Group:</strong> ${res.root_cause_group}</p>
          <p><strong>Preventable:</strong> <span class="badge bg-success">${res.preventable}</span></p>
          <p><strong>Recommended Owner:</strong> ${res.recommended_owner}</p>
          <p><strong>Priority Level:</strong> <span class="badge bg-danger">${res.priority}</span> (Score: ${res.priority_score})</p>
          <hr/>
          <h6>Multi-Source Evidence (${res.evidence ? res.evidence.agreement_ratio : ''}):</h6>
          <ul>${evidenceHtml}</ul>
          <div class="alert alert-info">
            <strong>Recommended Action:</strong> ${res.recommended_action}
          </div>
        </div>
      </div>
    `;
  } catch (err) {
    resultContainer.innerHTML = `<div class="alert alert-danger">Error running analysis: ${err}</div>`;
  }
}
