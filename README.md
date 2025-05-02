# 📡 3GPP-UE-Capa-Analyzer

A powerful and intuitive tool for parsing and visualizing **UE Capability Information** based on 3GPP specifications — **TS 36.331 (LTE)** and **TS 38.331 (NR)**.

This tool enables engineers and analysts to extract and summarize supported **band combinations** for **EUTRA (LTE)**, **NR (5G)**, and **MRDC (EN-DC)** technologies from protocol logs such as QXDM traces or Wireshark PCAPs.

### 🔧 Key Features

* Analyze UE Capability messages from QXDM or Wireshark decoded logs.
* Automatically extract and organize **band combination** information.
* Support for **EUTRA**, **NR**, and **MRDC** summaries in a user-friendly format.
* GUI-based interaction for quick execution and log loading.

---

### 🚀 How to Use

#### 1. **Run the analyzer**

```bash
python main_UE_Capa_Analyzer.py
```

#### 2. **Using the Paste tab**

* Navigate to the **'Paste'** tab.
* Copy and paste a decoded `"UE Capability"` message (from QXDM or Wireshark).
* Click the **'Execute'** button to process the data and see the result.

#### 3. **Using the File tab**

* Navigate to the **'File'** tab.
* Click **'Open'** to load a `.txt` file that contains logs.
* The analyzer will parse and display the supported bands and combinations automatically.

---

![image](https://github.com/user-attachments/assets/1bfc1212-aaec-4edf-aa06-3f6ea8b31869)

![image](https://github.com/user-attachments/assets/062f4c95-a540-4817-aa5a-ddc8f8e6d9c6)

