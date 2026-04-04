
---

# Ollama LAN Setup on Ubuntu 24.04 with NVIDIA GPU

## Overview

This document explains how we set up **Ollama** on an Ubuntu machine with an **NVIDIA RTX 3060 Ti (8 GB VRAM)** so that:

* it runs **on demand**
* it does **not** start automatically on boot
* it uses the **GPU**
* it exposes the API to the **local home network**
* other laptops on the same network can use it

---

## System Details

### OS

* Ubuntu 24.04.4 LTS

### GPU

* NVIDIA GeForce RTX 3060 Ti
* 8 GB VRAM

### Driver / CUDA

* Driver Version: 580.126.09
* CUDA Version: 13.0

### Verified GPU Use

We confirmed Ollama was using the GPU with:

```bash
ollama ps
```

Output showed:

```text
qwen3:8b    ...    100% GPU
```

This confirmed the selected model was running fully on the GPU.

---

## Model Selection

We chose:

```text
qwen3:8b
```

### Why this model

* good fit for **8 GB VRAM**
* runs fully on GPU on RTX 3060 Ti
* strong general-purpose model for chat, coding, and reasoning
* suitable for local API serving

---

## Important Architecture Note

Ollama works in two layers:

### 1. Server

```bash
ollama serve
```

This starts the Ollama API server.

### 2. Client / model usage

```bash
ollama run qwen3:8b
```

This talks to the running server and loads/uses the model.

### API usage

The same running server can also be called with:

```bash
curl http://127.0.0.1:11434/api/generate ...
```

So the intended flow is:

1. start the server once
2. use `ollama run`, `curl`, Python, or another laptop
3. stop the server when done

---

## Initial Problem

At first, a manual launch script failed with:

```text
Error: listen tcp 0.0.0.0:11434: bind: address already in use
```

### Root cause

Ollama was already running as a **systemd service**:

```bash
sudo systemctl status ollama
```

The service was:

* enabled
* running
* bound to `127.0.0.1:11434`

That meant:

* the port was already occupied
* the manual script could not start a second server
* the existing service was only reachable from localhost, not from other laptops

---

## Decision

We decided to:

* **disable** the systemd service
* **not** run Ollama on startup
* launch it manually with a script when needed
* expose it to the LAN using `0.0.0.0:11434`

---

## Service Cleanup

We stopped and disabled the existing startup service:

```bash
sudo systemctl stop ollama
sudo systemctl disable ollama
```

Then we verified the port was free:

```bash
sudo ss -ltnp | grep 11434 || true
```

---

## LAN Startup Script

We created a manual startup script named:

```bash
~/start-ollama-lan.sh
```

### Script

```bash
#!/usr/bin/env bash
set -euo pipefail

HOST="0.0.0.0"
PORT="11434"
CTX="4096"
KEEP_ALIVE="30m"
IP="$(hostname -I | awk '{print $1}')"

is_ollama_up() {
  curl -fsS "http://127.0.0.1:${PORT}/api/version" >/dev/null 2>&1
}

port_in_use() {
  ss -ltn "( sport = :${PORT} )" | grep -q LISTEN
}

echo "Checking Ollama..."

if is_ollama_up; then
  echo "Ollama is already running."
  echo "Local API: http://127.0.0.1:${PORT}"
  echo "LAN API:   http://${IP}:${PORT}"
  exit 0
fi

if port_in_use; then
  echo "Port ${PORT} is already in use by another process."
  sudo lsof -iTCP:${PORT} -sTCP:LISTEN -P -n || true
  exit 1
fi

export OLLAMA_HOST="${HOST}:${PORT}"
export OLLAMA_CONTEXT_LENGTH="${CTX}"
export OLLAMA_KEEP_ALIVE="${KEEP_ALIVE}"

echo "Starting Ollama on ${OLLAMA_HOST}"
echo "Local API: http://127.0.0.1:${PORT}"
echo "LAN API:   http://${IP}:${PORT}"
echo "Press Ctrl+C to stop."
echo

exec ollama serve
```

### Make it executable

```bash
chmod +x ~/start-ollama-lan.sh
```

### Run it

```bash
~/start-ollama-lan.sh
```

---

## Why These Environment Variables Were Used

### `OLLAMA_HOST=0.0.0.0:11434`

This makes Ollama listen on all network interfaces instead of only localhost.

Without this, other machines in the house cannot access the API.

### `OLLAMA_CONTEXT_LENGTH=4096`

Keeps context conservative for an 8 GB GPU.

### `OLLAMA_KEEP_ALIVE=30m`

Keeps the model loaded for 30 minutes after use, reducing reload time.

---

## LAN Access

When the script starts, it prints something like:

```text
Local API: http://127.0.0.1:11434
LAN API:   http://192.168.1.111:11434
```

The second URL is the one other laptops on the same home network can use.

---

## Model Storage Issue We Hit

After successfully starting the manual server, API calls returned:

```json
{"error":"model 'qwen3:8b' not found"}
```

### Root cause

The earlier systemd service and the new manual script were likely using **different model stores**.

The manual server log showed:

```text
OLLAMA_MODELS:/home/harsh/.ollama/models
```

But the previously running service likely had models under:

```text
/usr/share/ollama/.ollama/models
```

So the manual server could start successfully, but it could not see the already-downloaded model.

---

## Resolution for Model Not Found

The cleanest fix was:

```bash
ollama pull qwen3:8b
```

Run this as the same user who starts the manual script.

This ensures the model is downloaded into the same model directory the manual server uses.

### Verify available models

```bash
ollama list
```

### Verify through API

```bash
curl -s http://127.0.0.1:11434/api/tags
```

---

## Correct API Test Command

Use:

```bash
curl -s http://127.0.0.1:11434/api/generate -d '{
  "model": "qwen3:8b",
  "prompt": "Say hello in one short sentence.",
  "stream": false
}'
```

A previous failed test included a paste typo in the command body, so use the clean version above.

---

## Stop Script

We also created a stop script:

```bash
~/stop-ollama-lan.sh
```

### Script

```bash
#!/usr/bin/env bash
set -euo pipefail
pkill -f "^ollama serve$" && echo "Ollama stopped." || echo "Ollama was not running."
```

### Make executable

```bash
chmod +x ~/stop-ollama-lan.sh
```

### Use it

```bash
~/stop-ollama-lan.sh
```

---

## Final Workflow

### Start server

```bash
~/start-ollama-lan.sh
```

### Use locally

```bash
ollama run qwen3:8b
```

or:

```bash
curl -s http://127.0.0.1:11434/api/generate -d '{
  "model": "qwen3:8b",
  "prompt": "Explain what you are.",
  "stream": false
}'
```

### Use from another laptop

```bash
curl -s http://192.168.1.111:11434/api/generate -d '{
  "model": "qwen3:8b",
  "prompt": "Say hello from another laptop.",
  "stream": false
}'
```

### Stop server

```bash
~/stop-ollama-lan.sh
```

---

## Troubleshooting

### Error: `bind: address already in use`

This means something is already listening on port `11434`.

Check:

```bash
sudo ss -ltnp | grep 11434
sudo lsof -iTCP:11434 -sTCP:LISTEN -P -n
```

Common cause:

* Ollama systemd service still running
* another manual `ollama serve` already active

### Error: `model 'qwen3:8b' not found`

This means the server is running, but the model is not in the current Ollama model store.

Fix:

```bash
ollama pull qwen3:8b
```

### Check server health

```bash
curl -s http://127.0.0.1:11434/api/version
```

### Check model list

```bash
curl -s http://127.0.0.1:11434/api/tags
ollama list
```

### Check GPU usage

```bash
ollama ps
```

You want to see:

```text
PROCESSOR: 100% GPU
```

---

## Security Note

Because Ollama is bound to:

```text
0.0.0.0:11434
```

it is reachable from other devices on the local network.

This is fine for a trusted home network, but:

* do not expose this port directly to the public internet
* do not forward port `11434` from your router unless you add proper protections

---

## Final Outcome

We successfully moved from:

* auto-starting local-only Ollama service

to:

* manually launched Ollama
* LAN-accessible API
* GPU-backed `qwen3:8b`
* reusable on-demand workflow

---

