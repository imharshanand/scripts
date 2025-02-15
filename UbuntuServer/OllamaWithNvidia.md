---

## **Setting Up NVIDIA CUDA, PyTorch, and Ollama on Ubuntu 24.04 LTS Server**

This guide provides step-by-step instructions for installing and verifying **NVIDIA CUDA**, **PyTorch**, and **Ollama** on an **Ubuntu 24.04 LTS server**.

---

### **1️⃣ Check System Information**
Before installing anything, check your OS version:
```bash
lsb_release -a
```
```
Distributor ID: Ubuntu
Description:    Ubuntu 24.04.2 LTS # Server
Release:        24.04
Codename:       noble
```

---

### **2️⃣ Install NVIDIA Drivers**
#### **Check if NVIDIA GPU is detected**
```bash
lspci | grep -i nvidia
nvidia-smi
```
If no GPU is detected, install the latest NVIDIA drivers:
```bash
sudo apt update
sudo apt install -y nvidia-driver-560
```
Reboot the system after installation:
```bash
sudo reboot
```
After reboot, verify the installation:
```bash
nvidia-smi
```

---

### **3️⃣ Install CUDA 12.8**
#### **Add CUDA Repository & Install CUDA**
```bash
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2404/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt update
sudo apt install -y cuda
```
#### **Set up environment variables**
```bash
echo 'export PATH=/usr/local/cuda/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc
```
#### **Verify CUDA installation**
```bash
nvcc --version
echo $PATH | grep cuda
echo $LD_LIBRARY_PATH | grep cuda
```

---

### **4️⃣ Install CuDNN**
```bash
sudo apt install -y libcudnn9
```
Check if CuDNN is installed correctly:
```bash
cat /usr/local/cuda/include/cudnn_version.h | grep CUDNN_MAJOR -A 2
```

---

### **5️⃣ Install PyTorch with CUDA 12.1**
**Create a virtual environment (recommended)**
```bash
python3 -m venv ~/venv
source ~/venv/bin/activate
```
**Install PyTorch, torchvision, and torchaudio with CUDA support**
```bash
pip install --upgrade pip
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```
**Verify PyTorch Installation**
```bash
python3 -c "import torch; print(torch.__version__)"
python3 -c "import torch; print(torch.cuda.is_available())"
python3 -c "import torch; print(torch.backends.cudnn.version())"
```

---

### **6️⃣ Install Ollama**
```bash
curl -fsSL https://ollama.com/install.sh | sh
source ~/.bashrc
```
**Verify installation**
```bash
ollama --version
```
**Download a model**
```bash
ollama pull mistral
```
**Run the model**
```bash
ollama run mistral
```

---

### **7️⃣ Enable NVIDIA Persistence Mode**
```bash
sudo systemctl enable nvidia-persistenced
sudo systemctl start nvidia-persistenced
systemctl status nvidia-persistenced
```

---

### **8️⃣ Install and Enable Docker (Optional)**
If you want to run models inside containers:
```bash
sudo apt install -y docker.io
sudo systemctl enable --now docker
systemctl status docker
```

---

### **9️⃣ Final Verification**
Run the following to ensure everything is working:
```bash
nvidia-smi
nvcc --version
python3 -c "import torch; print(torch.cuda.is_available())"
ollama run mistral
```
---


# **To reduce **CPU and GPU stress**, you can stop unnecessary services running in the background.***
### Below are the commands to **stop, disable, or restart** services like **Ollama, NVIDIA Persistence Daemon, and Docker.**

### **1️⃣ Stop Ollama Service**
Ollama runs in the background and consumes GPU memory. To stop it:
```bash
sudo systemctl stop ollama
```
To disable it from starting on boot:
```bash
sudo systemctl disable ollama
```
To check its status:
```bash
systemctl status ollama
```
To restart it when needed:
```bash
sudo systemctl start ollama
```
To run a model:
```bash
ollama run mistral
```

---

### **2️⃣ Stop NVIDIA Persistence Daemon**
This service keeps the GPU in a persistent state, but if you don’t need it:
```bash
sudo systemctl stop nvidia-persistenced
```
To disable it from starting at boot:
```bash
sudo systemctl disable nvidia-persistenced
```
Check the status:
```bash
systemctl status nvidia-persistenced
```
To restart it:
```bash
sudo systemctl start nvidia-persistenced
```

---

### **3️⃣ Stop Docker (If Not Needed)**
Docker can consume CPU resources in the background.
To stop it:
```bash
sudo systemctl stop docker
```
To disable it from starting at boot:
```bash
sudo systemctl disable docker
```
To check its status:
```bash
systemctl status docker
```
To restart it:
```bash
sudo systemctl start docker
```

---

### **4️⃣ Free Up GPU Memory Used by Ollama**
Check which processes are using the GPU:
```bash
nvidia-smi
```
Kill the process manually if needed (replace `<PID>` with the actual process ID):
```bash
sudo kill -9 <PID>
```
For example, if `ollama` is consuming memory, find its **PID** and stop it:
```bash
sudo kill -9 $(pgrep ollama)
```

---

### **5️⃣ Reduce CPU & GPU Load**
If you want to **temporarily suspend GPU usage**, switch to a lower power mode:
```bash
sudo nvidia-smi -pm 0  # Disable persistent mode
sudo nvidia-smi --auto-boost-default=0
```
To re-enable it:
```bash
sudo nvidia-smi -pm 1  # Enable persistent mode
```

---

### **6️⃣ Reduce Background Tasks**
If your system is running heavy processes, check with:
```bash
top
htop  # If installed
```
Kill high CPU-consuming processes:
```bash
sudo kill -9 <PID>
```

---

### **7️⃣ Unload NVIDIA Modules (Extreme Case)**
If you **really** want to stop all GPU-related services:
```bash
sudo rmmod nvidia_uvm
sudo rmmod nvidia_drm
sudo rmmod nvidia_modeset
sudo rmmod nvidia
```
This will unload the NVIDIA driver until the next reboot.

To reload the modules:
```bash
sudo modprobe nvidia
```

---

## **Summary of Commands to Stop Services**
| Service | Stop Command | Disable from Boot | Check Status | Restart Command |
|---------|-------------|-------------------|--------------|-----------------|
| **Ollama** | `sudo systemctl stop ollama` | `sudo systemctl disable ollama` | `systemctl status ollama` | `sudo systemctl start ollama` |
| **NVIDIA Persistence Daemon** | `sudo systemctl stop nvidia-persistenced` | `sudo systemctl disable nvidia-persistenced` | `systemctl status nvidia-persistenced` | `sudo systemctl start nvidia-persistenced` |
| **Docker** | `sudo systemctl stop docker` | `sudo systemctl disable docker` | `systemctl status docker` | `sudo systemctl start docker` |

---
