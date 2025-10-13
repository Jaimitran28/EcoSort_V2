// static/script.js

// Main JavaScript for handling UI interactions, predictions, camera, voice input, and animations

document.addEventListener("DOMContentLoaded", () => {
  const fileInput = document.getElementById("fileInput");
  const dropzone = document.getElementById("dropzone");
  const previewWrap = document.getElementById("imagePreviewWrap");
  const previewImg = document.getElementById("preview");
  const clearBtn = document.getElementById("clearImageBtn");
  const predictImageBtn = document.getElementById("predictImageBtn");
  const predictTextBtn = document.getElementById("predictTextBtn");
  const textInput = document.getElementById("textInput");

  const resultCard = document.getElementById("resultCard");
  const resultEmpty = document.getElementById("resultEmpty");
  const predictedLabel = document.getElementById("predictedLabel");
  const predictedBadge = document.getElementById("predictedBadge");
  const confidenceBar = document.getElementById("confidenceBar");
  const topLabels = document.getElementById("topLabels");
  const tipsList = document.getElementById("tipsList");

  const predictsPopup = document.getElementById("predictsPopup");
  const uploadsPopup = document.getElementById("uploadsPopup");

  const predictsBtn = document.getElementById("predictsBtn");
  const uploadsBtn = document.getElementById("uploadsBtn");
  const openCameraBtn = document.getElementById("openCameraBtn");
  const captureBtn = document.getElementById("captureBtn");
  const cameraFeed = document.getElementById("cameraFeed");
  const cameraCanvas = document.getElementById("cameraCanvas");

  let stream = null;
  let predictsCount = 0;
  let uploadsCount = 0;
  const predictsHistory = [];
  const uploadsHistory = [];

  // Drag & drop image handling
  dropzone.addEventListener("click", () => fileInput.click());
  dropzone.addEventListener("dragover", (e) => e.preventDefault());
  dropzone.addEventListener("drop", (e) => {
    e.preventDefault();
    if (e.dataTransfer.files.length > 0) handleFile(e.dataTransfer.files[0]);
  });

  fileInput.addEventListener("change", () => {
    if (fileInput.files.length > 0) handleFile(fileInput.files[0]);
  });

  clearBtn.addEventListener("click", () => {
    previewImg.src = "";
    previewWrap.classList.add("hidden");
    fileInput.value = "";
    clearResult();
  });

  function handleFile(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      previewImg.src = e.target.result;
      previewWrap.classList.remove("hidden");
      clearResult();
    };
    reader.readAsDataURL(file);
  }

  // Predict Image
  predictImageBtn.addEventListener("click", async () => {
    if (!fileInput.files.length) return alert("Please upload an image first!");

    const formData = new FormData();
    formData.append("image", fileInput.files[0]);

    try {
      const response = await fetch("/predict_image", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      displayResult(data);

      // Save image history
      uploadsCount++;
      uploadsBtn.textContent = `${uploadsCount} uploads`;
      uploadsHistory.push({ src: previewImg.src, data });
    } catch (err) {
      alert("Error processing image.");
      console.error(err);
    }
  });


  // Predict Text
  predictTextBtn.addEventListener("click", async () => {
    const text = textInput.value.trim();
    if (!text) return alert("Please enter an item description!");

    try {
      const payload = { text };

      const response = await fetch("/predict_text", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await response.json();
      displayResult(data);

      // Save predicts history
      predictsCount++;
      predictsBtn.textContent = `${predictsCount} predicts`;
      predictsHistory.push({ text, data });
    } catch (err) {
      alert("Error processing text.");
      console.error(err);
    }
  });

  // Display results
  function displayResult(data) {
    resultEmpty.style.display = "none";
    resultCard.classList.remove("hidden");

    // Typing animations
    typeText("predictedLabel", data.category || "—");
    typeText("predictedBadge", data.category || "—");
    typeText("topLabels", (data.top_labels || []).join(", "));

    // Animate confidence bar
    const confidencePercent = data.confidence ? Math.round(data.confidence * 100) : 0;
    updateConfidenceBar(confidencePercent);

    // Disposal tips with typing
    tipsList.innerHTML = "";
    if (data.tips && data.tips.length) {
      typeList("tipsList", data.tips, 30);
    } else {
      typeList("tipsList", ["No tips available."], 30);
    }

    setTheme(data.category);
    textInput.value = "";
  }

  // Clear previous result
  function clearResult() {
    resultCard.classList.add("hidden");
    resultEmpty.style.display = "block";
    predictedLabel.textContent = "";
    predictedBadge.textContent = "";
    confidenceBar.style.width = "0%";
    confidenceBar.textContent = "";
    topLabels.textContent = "";
    tipsList.innerHTML = "";
  }

  // Theme change
  function setTheme(category) {
    const body = document.body;
    body.classList.remove("theme-trash", "theme-compost", "theme-recycle", "theme-default");
    switch ((category || "").toLowerCase()) {
      case "trash": body.classList.add("theme-trash"); break;
      case "compostable": body.classList.add("theme-compost"); break;
      case "recyclable": body.classList.add("theme-recycle"); break;
      default: body.classList.add("theme-default");
    }
  }

  // Show history in popup
  function showHistory(type) {
    const popup = type === "predicts" ? predictsPopup : uploadsPopup;
    const otherPopup = type === "predicts" ? uploadsPopup : predictsPopup;

    // Hide the other popup
    otherPopup.style.display = "none";

    // Clear current popup content
    popup.innerHTML = "";

    // Select data
    const items = type === "predicts" ? predictsHistory : uploadsHistory;

    if (items.length === 0) {
      popup.innerHTML = '<div class="px-3 py-2 text-xs text-white/70">No history yet.</div>';
    } else {
      items.slice().reverse().forEach((item) => {
        const card = document.createElement("div");
        card.classList.add("history-card", "p-2", "rounded-xl", "mb-1", "text-xs");

        const category = item.data?.category || "—";
        let bg = "bg-gray-800";
        if (category.toLowerCase() === "trash") bg = "bg-red-600";
        else if (category.toLowerCase() === "compostable") bg = "bg-yellow-500";
        else if (category.toLowerCase() === "recyclable") bg = "bg-green-500";
        card.classList.add(bg);

        if (type === "predicts") {
          card.innerHTML = `<strong>Text:</strong> ${item.text}<br><span>${category}</span>`;
        } else {
          const topLabelsText = (item.data.top_labels || []).slice(0,3).join(", ");
          card.innerHTML = `<img src="${item.src}" class="w-12 h-12 rounded-md inline-block mr-2"/><span>${category}</span> <span class="text-xs">Top: ${topLabelsText}</span>`;
        }

        popup.appendChild(card);
      });
    }

    // Toggle visibility
    popup.style.display = popup.style.display === "block" ? "none" : "block";
  }

  // Toggle popups on button click
  predictsBtn.addEventListener("click", () => showHistory("predicts"));
  uploadsBtn.addEventListener("click", () => showHistory("uploads"));

  // Camera Integration
  openCameraBtn.addEventListener("click", async () => {
    try {
      console.log("📸 Open camera clicked");
      if (!stream) {
        // ask for permission
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        console.log("✅ Camera access granted");
        cameraFeed.srcObject = stream;
        cameraFeed.classList.remove("hidden");
        captureBtn.classList.remove("hidden");
        openCameraBtn.textContent = "Close Camera";
      } else {
        stopCamera();
      }
    } catch (err) {
      console.error("❌ Camera error:", err);
      alert("Unable to access camera. Please check browser permissions or HTTPS.");
    }
  });

  function stopCamera() {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      stream = null;
    }
    cameraFeed.classList.add("hidden");
    captureBtn.classList.add("hidden");
    openCameraBtn.textContent = "Open Camera";
  }

  // Capture image from camera
  captureBtn.addEventListener("click", async () => {
    if (!stream) return alert("Camera is not active.");
    const context = cameraCanvas.getContext("2d");
    cameraCanvas.width = cameraFeed.videoWidth;
    cameraCanvas.height = cameraFeed.videoHeight;
    context.drawImage(cameraFeed, 0, 0);
    
    cameraCanvas.toBlob(async (blob) => {
      const file = new File([blob], "capture.jpg", { type: "image/jpeg" });
      const formData = new FormData();
      formData.append("image", file);

      try {
        const response = await fetch("/predict_image", { method: "POST", body: formData });
        const data = await response.json();
        displayResult(data);
      } catch (err) {
        alert("Error processing captured image.");
        console.error(err);
      }
    }, "image/jpeg");
  });

  const micButton = document.getElementById("micButton");
  let recognition;

  // Voice Input using Web Speech API
  if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    micButton.addEventListener("click", () => {
      try {
        recognition.start();
        // Add listening animation
        micButton.classList.add("listening");
        micButton.textContent = "🎙️ Listening…";
      } catch(err) {
        console.error("Recognition start error:", err);
      }
    });

    recognition.onresult = (event) => {
      const speechResult = event.results[0][0].transcript;
      textInput.value = speechResult;
      micButton.classList.remove("listening");
      micButton.textContent = "🎤"; // revert to normal
      // Optionally auto-submit
      // predictTextBtn.click();
    };

    recognition.onspeechend = () => {
      micButton.classList.remove("listening");
      micButton.textContent = "🎤";
      recognition.stop();
    };

    recognition.onerror = (event) => {
      alert("Error in speech recognition: " + event.error);
      micButton.classList.remove("listening");
      micButton.textContent = "🎤";
    };
  } else {
    micButton.disabled = true;
    micButton.title = "Your browser does not support voice input";
  }

  // Floating Particles Background
  const particleContainer = document.createElement("div");
  particleContainer.classList.add("particle-container");
  document.body.appendChild(particleContainer);

  const numParticles = 40; // total number of particles

  for (let i = 0; i < numParticles; i++) {
    const particle = document.createElement("div");
    particle.classList.add("particle");

    // Random size
    const size = Math.random() * 8 + 4; // 4px to 12px
    particle.style.width = `${size}px`;
    particle.style.height = `${size}px`;

    // Random position
    particle.style.top = `${Math.random() * 100}%`;
    particle.style.left = `${Math.random() * 100}%`;

    // Random animation duration & delay
    const duration = Math.random() * 6 + 4; // 4s to 10s
    particle.style.animationDuration = `${duration}s`;
    particle.style.animationDelay = `${Math.random() * 5}s`;

    // Random opacity
    particle.style.opacity = (Math.random() * 0.5 + 0.3).toFixed(2);

    particleContainer.appendChild(particle);
  }


});

// Confidence bar animation
function updateConfidenceBar(confidence) {
  const bar = document.getElementById("confidenceBar");

  bar.style.transition = "none";
  bar.style.width = "0%";
  bar.textContent = "0%";

  requestAnimationFrame(() => {
    bar.style.transition = "width 1.2s ease-in-out";
    bar.style.width = confidence + "%";
    bar.textContent = confidence + "%";
  });

  resultCard.classList.add("visible");


  
}

// Typewriter effect
function typeText(elementId, text, speed = 40) {
  const el = document.getElementById(elementId);
  el.textContent = "";
  let i = 0;

  function typing() {
    if (i < text.length) {
      el.textContent += text.charAt(i);
      i++;
      setTimeout(typing, speed);
    }
  }
  typing();
}

// Typewriter for list items
function typeList(elementId, items, charSpeed = 40, itemDelay = 300) {
  const el = document.getElementById(elementId);
  el.innerHTML = "";
  let i = 0, j = 0;

  function typing() {
    if (i < items.length) {
      // Create the list item if not already
      if (j === 0) {
        const li = document.createElement("li");
        el.appendChild(li);
        li.style.setProperty("--delay", `${i * itemDelay}ms`);
      }

      const li = el.children[i];
      const text = items[i];

      if (j < text.length) {
        li.textContent += text.charAt(j);
        j++;
        setTimeout(typing, charSpeed);
      } else {
        i++;
        j = 0;
        setTimeout(typing, itemDelay); // Delay before starting next item
      }
    }
  }

  typing();
}


// Allow Enter key to trigger text prediction
document.getElementById("textInput").addEventListener("keypress", function (e) {
  if (e.key === "Enter") {
    e.preventDefault(); // prevent accidental form reload
    document.getElementById("predictTextBtn").click();
  }
});

// Server-side fact rotation
const factShort = document.getElementById("factShort");
const factDetail = document.getElementById("factDetail");
const factBox = document.getElementById("factBox");

// Fetch and update fact
async function updateFact() {
  try {
    const res = await fetch("/fact"); // your endpoint
    if (!res.ok) throw new Error("Network error");
    const fact = await res.json();

    // Fade out/in animation
    factBox.classList.add("fade");
    setTimeout(() => {
      factShort.textContent = fact.short;
      factDetail.textContent = fact.detail;
      factBox.classList.remove("fade");
    }, 300);
  } catch (err) {
    console.error("Failed to fetch fact:", err);
    factShort.textContent = "Failed to load fact.";
    factDetail.textContent = "";
  }
}

// Initial load
updateFact();

// Rotate fact every 2 minutes
setInterval(updateFact, 120000);
