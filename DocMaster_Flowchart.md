# DocMaster System Flowchart (Mermaid)

```mermaid
flowchart TD
    Frontend["DocMaster.html (Frontend UI)"]
    MainAPI["main.py (Flask API)"]
    AdminAPI["admin_backend.py (Admin Flask API)"]
    Database[("docmaster_admin.db (SQLite DB)")]
    
    Frontend -- "API Request (Document, AI, Translate, Feature Access)" --> MainAPI
    Frontend -- "Admin API Request (User, Analytics, Transaction)" --> AdminAPI
    MainAPI -- "Query/Update (User, Token, Subscription)" --> AdminAPI
    AdminAPI -- "DB Query/Update" --> Database
    MainAPI -- "Serve DocMaster.html, DocMaster_Simple.html" --> Frontend
    AdminAPI -- "Serve DocMaster.html (Admin Panel)" --> Frontend
```

> **Note:**
> - This diagram shows the main signal/data flow between the frontend (`DocMaster.html`), the main backend (`main.py`), the admin backend (`admin_backend.py`), and the database. The price banner is excluded as requested.
> - Place this code block in your `README.md` or a `.md` file on GitHub to render the Mermaid diagram.
