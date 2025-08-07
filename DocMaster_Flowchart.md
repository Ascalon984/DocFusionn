
# DocMaster System Flowchart & Detailed Feature Workflow (Mermaid)

## 1. System Architecture Overview

```mermaid
flowchart TD
    Frontend["DocMaster.html (Frontend UI)"]
    MainAPI["main.py (Flask API)"]
    AdminAPI["admin_backend.py (Admin Flask API)"]
    Database[("docmaster_admin.db (SQLite DB)")]
    
    Frontend -- "API Request (Document, AI, Translate, Feature Access, Plagiarism, Reference, Numbering, Chatbot)" --> MainAPI
    Frontend -- "Admin API Request (User, Analytics, Transaction)" --> AdminAPI
    MainAPI -- "Query/Update (User, Token, Subscription)" --> AdminAPI
    AdminAPI -- "DB Query/Update" --> Database
    MainAPI -- "Serve DocMaster.html, DocMaster_Simple.html" --> Frontend
    AdminAPI -- "Serve DocMaster.html (Admin Panel)" --> Frontend
```

---

## 2. Feature Workflows

### 2.1. Document Upload & Parsing

```mermaid
sequenceDiagram
    participant User
    participant Frontend as DocMaster.html
    participant MainAPI as main.py
    User->>Frontend: Upload file (docx/pdf/doc)
    Frontend->>MainAPI: POST /api/parse (file in base64)
    MainAPI->>MainAPI: Parse file (mammoth, PyPDF2, textract)
    MainAPI-->>Frontend: Parsed text/content
    Frontend-->>User: Display document content
```

### 2.2. AI Document Processing (Auto-format, Typo Fix, Capitalize, Tab, etc)

```mermaid
sequenceDiagram
    User->>Frontend: Click AI processing (e.g., Auto-format)
    Frontend->>MainAPI: POST /api/format (text, mode)
    MainAPI->>MainAPI: Process with HuggingFace/Mistral API
    MainAPI-->>Frontend: Formatted text
    Frontend-->>User: Show formatted result
```

### 2.3. Translation

```mermaid
sequenceDiagram
    User->>Frontend: Select Translate
    Frontend->>MainAPI: POST /api/translate (text, src, dest)
    MainAPI->>MainAPI: Use Googletrans or Mistral API
    MainAPI-->>Frontend: Translated text
    Frontend-->>User: Show translation
```

### 2.4. Plagiarism/Similarity Check

```mermaid
sequenceDiagram
    User->>Frontend: Click Plagiarism Check
    Frontend->>MainAPI: POST /api/similarity (text1, text2)
    MainAPI->>MainAPI: Use SentenceTransformer (MiniLM)
    MainAPI-->>Frontend: Similarity score
    Frontend-->>User: Show similarity result
```

### 2.5. AI Detection (Is this text AI-generated?)

```mermaid
sequenceDiagram
    User->>Frontend: Click AI Detection
    Frontend->>MainAPI: POST /api/ai-detect (text)
    MainAPI->>MainAPI: Use Roberta, GLTR, Perplexity, IndoBERT
    MainAPI-->>Frontend: AI probability & details
    Frontend-->>User: Show AI detection result
```

### 2.6. Reference Parsing & Formatting

```mermaid
sequenceDiagram
    User->>Frontend: Upload reference file (RIS/BibTeX/Word)
    Frontend->>MainAPI: POST /api/parse-reference (file, ext)
    MainAPI->>MainAPI: Parse with rispy/bibtexparser/mammoth/AI
    MainAPI-->>Frontend: Parsed references (JSON)
    Frontend->>MainAPI: POST /api/format-reference (ref, style)
    MainAPI-->>Frontend: Formatted citation
    Frontend-->>User: Show formatted reference
```

### 2.7. Page Numbering

```mermaid
sequenceDiagram
    User->>Frontend: Select page numbering options
    Frontend->>MainAPI: POST /api/numbering (file, type, from, to, position)
    MainAPI->>MainAPI: Process with python-docx
    MainAPI-->>Frontend: Preview numbered doc
    Frontend-->>User: Show preview/download
```

### 2.8. Chatbot (AI Assistant)

```mermaid
sequenceDiagram
    User->>Frontend: Open Chatbot, send message
    Frontend->>MainAPI: POST /api/chat (history)
    MainAPI->>MainAPI: Use Llama/Mistral API
    MainAPI-->>Frontend: AI reply
    Frontend-->>User: Show chat response
```

### 2.9. Feature Access Control (Premium/Token)

```mermaid
sequenceDiagram
    User->>Frontend: Try to use premium feature
    Frontend->>MainAPI: POST /api/feature/access (email, feature)
    MainAPI->>AdminAPI: GET user info (by email)
    alt Premium user
        AdminAPI-->>MainAPI: subscription_type = premium
        MainAPI-->>Frontend: allowed: true
    else Non-premium user
        AdminAPI-->>MainAPI: tokens > 0 ?
        alt Token available
            MainAPI->>AdminAPI: update tokens -1
            MainAPI-->>Frontend: allowed: true
        else No token
            MainAPI-->>Frontend: allowed: false, reason: Token habis
        end
    end
    Frontend-->>User: Show access result
```

### 2.10. Admin Panel (Monitoring, Analytics, Transactions)

```mermaid
sequenceDiagram
    Admin->>Frontend: Login as admin
    Frontend->>AdminAPI: POST /api/admin/check-access (email)
    AdminAPI-->>Frontend: is_admin: true/false
    Frontend->>AdminAPI: GET /api/admin/dashboard
    AdminAPI-->>Frontend: Metrics, recent users, transactions
    Frontend-->>Admin: Show dashboard, analytics, export, etc
```

---

## 3. Notes
- All API endpoints are handled by `main.py` (user features) and `admin_backend.py` (admin features).
- Database operations (user, token, subscription, analytics, transactions) are managed by `admin_backend.py` and stored in `docmaster_admin.db`.
- AI/ML features use HuggingFace, OpenRouter (Mistral/Llama), and other Python libraries.
- The frontend (`DocMaster.html`) interacts with both backends via REST API.
- Feature access is controlled by premium status or token count.
- Admin panel provides real-time monitoring, analytics, and data export.

---

> **How to use:**
> - Place this file in your repository (e.g., `DocMaster_Flowchart.md`).
> - View on GitHub or any Mermaid-compatible Markdown viewer for rendered diagrams.
> - Update as new features are added.
