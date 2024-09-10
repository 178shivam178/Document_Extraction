# Document Extraction

This project utilizes Large Language Models (LLM) to extract key entities from a variety of document types. Supported documents include:

- **Invoices**
- **Purchase Orders**
- **Purchase Requests**
- **Purchase Requisitions**
- **FORM9**
- **Form W8BEN**
- **Form W8BENE**
- **Goods Received Note (GRGN)**
- **And other similar documents**

Documents can be in various formats, such as PDF, images, CSV, DocX, XLSX, and plain text (.TXT). The extracted data is returned in a clean, structured JSON format.

## Features
- Support for multiple document formats (PDF, Image, CSV, DocX, XLSX, TXT).
- Extracted data is returned in JSON format for easy integration.
- Capable of processing various document types including invoices, forms, and purchase documents.
- Easy setup and environment management using Conda.

## Environment Setup

To create and activate the environment, follow these steps:

### 1. Create Conda Environment

create env 

```bash
conda create -n DocExtraction python=3.8.13 -y
```

### 2. Activate Environment

```bash
conda activate DocExtraction
```

### 3. install the requirements

```bash
pip install -r requirements.txt
```

### 4. SET your openAI KEY
```bash
Change .env

