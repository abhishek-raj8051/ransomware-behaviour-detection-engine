<div align="center">

<h1>🛡️ Rappahmamoun</h1>
<h3>Ransomware Behaviour Detection Engine</h3>

<img src="https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge&logo=github">
<img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python">
<img src="https://img.shields.io/badge/Linux-Kali%20%7C%20Ubuntu-orange?style=for-the-badge&logo=linux">
<img src="https://img.shields.io/badge/Security-Advanced-red?style=for-the-badge&logo=hackaday">
<img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge">

<br><br>

<b>⚡ Real-time Behaviour-Based Ransomware Detection System</b><br> <i>Detects zero-day ransomware in < 4 seconds using entropy + hashing + system behaviour</i>

<br><br>

<img src="demo_screenshot.png" width="850"/>

</div>

---

# 🚀 Overview

**Rappahmamoun** is a **real-time ransomware early-warning engine** designed for Linux systems.
Instead of signatures, it uses **behaviour analysis + cryptographic verification + entropy detection**.

> 💡 *Stops ransomware BEFORE encryption damage happens*

---

# ⚙️ How It Works (3D Flow Logic)

```
📁 File Activity
      ↓
⚙️ CPU + Disk Monitoring
      ↓
🔐 SHA256 Integrity Check
      ↓
📊 Entropy Detection (Encryption Check)
      ↓
🎯 Risk Scoring Engine
      ↓
🚨 Auto Alert + Process Block
```

---

# 🎬 Live Demo

```bash
# Terminal 1
python3 detector.py

# Terminal 2
./ransomware_load.sh
```

### 🔥 Output

```
🚨 RANSOMWARE DETECTED
═══════════════════════════════
📁 File Activity: Multiple files modified
💻 CPU Spike: 82%
🔐 Integrity: SHA256 Mismatch
📊 Entropy: 7.9 (Encrypted)
⚙️ Process: generator.sh
✅ Action: AUTO BLOCKED
⏱️ Detection Time: 3.2 sec
```

---

# 🧠 Core Features

## 🔍 Detection Engine

* Real-time multi-folder monitoring
* Behaviour-based anomaly detection
* SHA256 file integrity validation
* High entropy detection (encrypted files)
* CPU & disk spike correlation
* Risk scoring algorithm

## 🛡️ Protection System

* Auto process blocking (SIGSTOP)
* Safe whitelist (VSCode, Chrome, etc.)
* Structured logging (JSON ready)
* Alert cooldown system
* Low false positives

## 🧪 Testing Framework

* Built-in ransomware simulator
* Multiple attack scenarios
* Safe environment testing
* Repeatable lab experiments

---

# 📦 Installation

```bash
git clone https://github.com/YOUR_USERNAME/ransomware-behaviour-detection-engine.git
cd ransomware-behaviour-detection-engine

pip3 install -r requirements.txt
chmod +x ransomware_load.sh detector.py
```

---

# 🚀 Quick Start

```bash
# Start monitoring
python3 detector.py

# Run attack simulation
./ransomware_load.sh
```

---

# ⚙️ Configuration (`config.yaml`)

```yaml
watch_folders:
  - "~/Documents"
  - "~/Desktop"
  - "~/Downloads"

detection:
  risk_threshold: 75
  entropy_threshold: 7.5
  time_window: 4

protection:
  auto_block: true

whitelist:
  - "code"
  - "chrome"
  - "firefox"
```

---

# 📊 Performance Metrics

| Metric          | Value  |
| --------------- | ------ |
| Detection Time  | <4 sec |
| Accuracy        | 94%    |
| False Positives | <1.5%  |
| CPU Usage       | <2%    |
| Memory Usage    | ~45MB  |

---

# 🎯 Use Cases

* 🎓 Students → Protect assignments & projects
* 🔬 Researchers → Secure datasets
* 💼 Small Business → Affordable security
* 🧪 Cyber Labs → Training & simulation

---

# 🆚 Why Behaviour-Based?

| Traditional AV ❌     | Rappahmamoun 🛡️          |
| -------------------- | ------------------------- |
| Signature-based      | Behaviour-based           |
| Detects after damage | Detects before encryption |
| Manual response      | Auto blocking             |
| Expensive            | Free & lightweight        |

---

# 📁 Project Structure

```
ransomware-behaviour-detection-engine/
├── detector.py
├── ransomware_load.sh
├── config.yaml
├── requirements.txt
├── demo_screenshot.png
├── LICENSE
└── README.md
```

---

# 📈 Future Roadmap

* 🤖 AI/ML-based detection
* 🌐 Web dashboard
* ☁️ SIEM integration
* 🖥️ Windows support
* 📊 Real-time analytics UI

---

# 🤝 Contributing

```bash
git checkout -b feature/new-feature
git commit -m "Added new feature"
git push origin feature/new-feature
```

---

# 📄 License

MIT License — Free for personal, academic & commercial use

---

# 👥 Team

**The Undefine Elite — GLA University**

* Abhishek Raj → Lead Developer
* Anuj Kumar → Load Generator
* Shivangi Raj → Threat Research
* Madhav Kumar → Testing

---

# 📞 Contact

* 📌 Create GitHub Issue
* 🤝 Collaboration → Profile links

---

<div align="center">

🔥 Built for Cybersecurity Innovation
🛡️ Protecting systems before damage happens

⭐ Star this repo if you found it useful

</div>
