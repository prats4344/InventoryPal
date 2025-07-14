# 📦 InventoryPal – Smart Inventory Management System

> A complete inventory tracking web application with real-time barcode scanning, analytics dashboard, user authentication, and stock grouping — built with Flask, SQLite, and JavaScript.

---

## ✨ Overview

**InventoryPal** is a full-stack inventory management solution designed for warehouse, retail, and logistics workflows. It supports real-time barcode scanning using your device camera, tracks stock inflow, categorizes products by vendor, date, or price group, and provides a visual dashboard with live analytics.

---

## 🔑 Features

- 📷 Real-time **Barcode Scanner** using device camera (ZXing library)
- 🔐 **User Authentication** – Secure login & registration with password hashing
- 🧾 **Add / Edit / Delete Products**
  - Product Name, Quantity, Unit Price
  - Vendor (source), Arrival Date, Box ID
- 📊 **Dashboard with Grouping & Charts**
  - Filter and group by **Vendor**, **Date**, **Price Range**
  - **Live charting** with Chart.js
- 🎵 **Beep Sound** on successful barcode detection
- 📱 **Mobile-Friendly UI** with responsive Bootstrap layout
- 💽 **SQLite Database** for persistent product tracking

---

## 🛠️ Tech Stack

| Layer         | Technology       |
|---------------|------------------|
| 🧠 Backend     | Python (Flask)    |
| 🎨 Frontend    | HTML5, CSS3, Bootstrap 5 |
| 🎯 Logic       | JavaScript, ZXing, Chart.js |
| 🗃️ Database    | SQLite3           |
| 🔊 Audio       | WAV trigger on scan |

---

🔗 Live Demo: [https://inventorypal.onrender.com](https://inventorypal.onrender.com)

---

## 🚀 Getting Started

### 🔧 Requirements

- Python 3.7+
- Flask

### 📦 Installation

```bash
# Clone the repo
git clone https://github.com/prats4344/InventoryPal.git
cd InventoryPal

# (Optional) Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
# or
source venv/bin/activate  # macOS/Linux

# Install Flask
pip install flask




