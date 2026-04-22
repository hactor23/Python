const statusEl = document.getElementById("status");
const userEl = document.getElementById("username");
const btnRegister = document.getElementById("btnRegister");
const btnLogin = document.getElementById("btnLogin");
const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d", { willReadFrequently: false });

function setStatus(msg) {
  statusEl.textContent = msg || "";
}

function setBusy(busy) {
  btnRegister.disabled = busy;
  btnLogin.disabled = busy;
  userEl.disabled = busy;
}

async function startCamera() {
  const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "user" }, audio: false });
  video.srcObject = stream;
  await video.play();
  return stream;
}

function captureJpegDataUrl() {
  const w = video.videoWidth || 640;
  const h = video.videoHeight || 480;
  canvas.width = w;
  canvas.height = h;
  ctx.drawImage(video, 0, 0, w, h);
  // calidad 0.85: balance para backend
  return canvas.toDataURL("image/jpeg", 0.85);
}

async function postJson(url, body) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const msg = data?.error || `Error HTTP ${res.status}`;
    throw new Error(msg);
  }
  return data;
}

async function runRegister() {
  const username = (userEl.value || "").trim();
  if (!username) {
    setStatus("Ingresa un usuario.");
    return;
  }

  setBusy(true);
  setStatus("Pidiendo permisos de cámara...");
  let stream;
  try {
    stream = await startCamera();
  } catch (e) {
    setStatus(`No se pudo abrir la cámara: ${e.message}`);
    setBusy(false);
    return;
  }

  try {
    setStatus("Iniciando registro...");
    const start = await postJson("/api/register/start", { username });
    const token = start.token;
    const required = start.required;

    let count = 0;
    const t0 = Date.now();
    while (count < required) {
      const img = captureJpegDataUrl();
      const r = await postJson("/api/register/frame", { token, image: img });
      count = r.count || 0;
      setStatus(`Capturando: ${count}/${required}`);

      if (r.done) break;
      // ritmo de captura: 400ms (menos carga CPU)
      await new Promise((resolve) => setTimeout(resolve, 400));

      // safety: 70s
      if (Date.now() - t0 > 70000) throw new Error("Registro tardó demasiado. Intenta de nuevo.");
    }

    setStatus("Registro completo. Entrando al menú...");
    window.location.href = "/menu";
  } catch (e) {
    setStatus(e.message);
  } finally {
    if (stream) stream.getTracks().forEach((t) => t.stop());
    setBusy(false);
  }
}

async function runLogin() {
  const username = (userEl.value || "").trim();
  if (!username) {
    setStatus("Ingresa un usuario.");
    return;
  }

  setBusy(true);
  setStatus("Pidiendo permisos de cámara...");
  let stream;
  try {
    stream = await startCamera();
  } catch (e) {
    setStatus(`No se pudo abrir la cámara: ${e.message}`);
    setBusy(false);
    return;
  }

  try {
    setStatus("Iniciando verificación...");
    const start = await postJson("/api/login/start", { username });
    const token = start.token;

    const t0 = Date.now();
    while (true) {
      const img = captureJpegDataUrl();
      const r = await postJson("/api/login/frame", { token, image: img });
      if (r.verified) {
        setStatus("Acceso concedido. Entrando al menú...");
        window.location.href = "/menu";
        return;
      }
      setStatus("Verificando rostro... (mantené tu cara centrada)");
      await new Promise((resolve) => setTimeout(resolve, 350));
      if (Date.now() - t0 > 25000) throw new Error("No se pudo verificar a tiempo. Intenta de nuevo.");
    }
  } catch (e) {
    setStatus(e.message);
  } finally {
    if (stream) stream.getTracks().forEach((t) => t.stop());
    setBusy(false);
  }
}

btnRegister?.addEventListener("click", runRegister);
btnLogin?.addEventListener("click", runLogin);

setStatus("Listo. Ingresa un usuario y elige Registrar o Ingresar.");

