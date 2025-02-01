# Github_Dorker

# 🔍 GitHub Dorking Tool - Automated Secret Hunting 🕵️‍♂️

## 🚀 Introduction  

GitHub Dorking Tool is an **automated script** designed to find **exposed API keys, credentials, cloud secrets, database passwords, and CI/CD tokens** from **public GitHub repositories**.  

🛠 This script automates the **GitHub dorking process**, allowing you to:  
✅ Scan **multiple organizations** at once  
✅ Find **AWS, Google, Azure, PayPal, Stripe keys & more**  
✅ Automate **large-scale GitHub recon**  
✅ **Save time** in bug bounty hunting & penetration testing  

---

## ✨ Features  

✔ **Automated GitHub dorking** using API queries  
✔ **Supports single & multiple organizations**  
✔ **Includes 25+ powerful dorks** for secret discovery  
✔ **Extracts only relevant repositories containing leaks**  
✔ **Easy to use & fast execution**  

---

## 🔧 Installation  

### **1️⃣ Install Dependencies**  
Ensure Python and `requests` are installed:  
```bash
git clone https://github.com/myselfakash20/Github_Dorker.git
cd Github_Dorker
pip install requests
export GITHUB_TOKEN="your_personal_access_token"
python3 github_dorker.py
