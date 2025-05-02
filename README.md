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

### 📊 Interpreting Band Combination and FeatureSet Tables

The analyzer summarizes supported band combinations and layer configurations as shown below.

* **EUTRA BAND COMB** shows LTE-only combinations. The number in parentheses like `1A(4L)` directly indicates the number of layers (**4 Layers**) per band.
* **MRDC BAND COMB** (EN-DC) includes both LTE and NR bands. Here, the number in parentheses (e.g., `n78C(5)`) refers to the **FeatureSet ID**, not the layer count.

> 📝 **Note:**
> For MRDC combinations, refer to the **EUTRA FEATURESET** and **NR FEATURESET** tables below to find the actual layer count and modulation per FeatureSet ID.

---

### 📷 Visual Sample (from tool output)

![image](https://github.com/user-attachments/assets/8f9ab7c6-a7ba-429d-8491-cfb608857c3c)

![image](https://github.com/user-attachments/assets/b1c88de5-a6f6-4fee-8c10-0f1c1947f5b9)


