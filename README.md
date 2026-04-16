# Agentic_Pay
# 🚀 Agentic Pay

Agentic Pay is a Python-based multi-agent system that automates invoice processing and payment workflows using intelligent agents, email parsing, and risk analysis.

The system simulates a real-world autonomous payment pipeline where invoices are received via email, processed into structured data, evaluated for risk, and executed through a buyer agent.

---

## 🧠 Key Features

* 📧 **Email-Based Invoice Detection**
  Automatically listens for incoming emails and extracts invoice data

* 🧾 **Invoice Parsing & Structuring**
  Converts raw email content into structured JSON invoices

* 🤖 **AI Buyer Agent**
  Validates invoices, manages wallet data, and processes transactions

* 🔐 **Risk Analysis (ML Model)**
  Uses a trained machine learning model to detect risky transactions

* 💰 **Wallet & Payment Handling**
  Simulates secure payment execution with account and wallet storage

* 🔗 **Agent Communication**
  Invoice Agent and Buyer Agent communicate via APIs

---

## ⚙️ System Architecture

### 🧾 Invoice Agent

* Listens to emails (IMAP idle listener)
* Extracts and summarizes invoice data
* Converts invoices into structured JSON
* Sends data to Buyer Agent

### 🤖 Buyer Agent

* Receives invoice data via API
* Validates transaction details
* Checks wallet balance
* Calls risk model before processing payment

### 🧠 Risk Model

* Machine learning model trained on transaction data
* Predicts whether a transaction is risky or safe
* Integrated into payment decision flow

---

## 🔄 Workflow

1. Invoice received via email
2. Invoice Agent parses and structures data
3. Invoice sent to Buyer Agent
4. Buyer Agent validates & checks balance
5. Risk model evaluates transaction
6. Payment is approved or rejected

---

## 🛠️ Tech Stack

* **Python**
* **Flask (APIs)**
* **Machine Learning (Scikit-learn / Pickle Model)**
* **Email Processing (IMAP)**
* **JSON-based data handling**

---

## 📂 Project Structure

```
Agentic Pay/
│
├── AI Buyer Agent/
│   ├── api/
│   ├── models/
│   ├── processor.py
│   ├── validators.py
│   ├── wallet_store.py
│   └── main.py
│
├── Invoice Agent/
│   ├── api/
│   ├── getEmails.py
│   ├── parsetoJson.py
│   ├── summarizeMails.py
│   ├── send_to_buyer_agent.py
│   └── main.py
│
├── risk-model/
│   ├── train_model.py
│   ├── model.pkl
│   ├── api.py
│   └── transactions.csv
```

---

## ▶️ How to Run

### 1. Clone the repository

```
git clone https://github.com/your-username/agentic-pay.git
cd agentic-pay
```

---

### 2. Start Risk Model API

```
cd risk-model
python api.py
```

---

### 3. Start Buyer Agent

```
cd "AI Buyer Agent"
python main.py
```

---

### 4. Start Invoice Agent

```
cd "Invoice Agent"
python main.py
```

---

## 📌 Example Use Case

* A user receives an invoice via email
* The system automatically detects and parses it
* Buyer Agent validates and checks funds
* Risk model evaluates transaction safety
* Payment is executed if safe

---

## 🚀 Future Enhancements

* Add real payment gateway integration (Stripe / Razorpay)
* Replace polling with message queues (Kafka / RabbitMQ)
* Enhance ML model with real-world fraud datasets
* Add authentication & secure APIs
* Build a frontend dashboard

---

## 💡 Why This Project Stands Out

* Combines **AI agents + ML + system design**
* Demonstrates **real-world automation use case**
* Includes **end-to-end workflow (Email → Payment)**
* Goes beyond CRUD into **intelligent systems**

---

## 👨‍💻 Author

Deep Gandhi

