# Repository Structure Rules

## ⚠️ "Hard Rule" for New Content

The roadmap moved from ad-hoc `Week_XX` folders to numbered **CAB (Cloud Architecture Block)** modules, each scoped to one SAA-C03 exam domain (see `roadmap-v3.2.md` for the canonical block list and status). All new content **MUST** follow this structure:

1.  **CAB Folder**: Create a new folder for each block under `assets/cab/`.
    *   **Naming Convention**: `CAB-XX_TopicName`
    *   *Example*: `assets/cab/CAB-03_KMS_PHI_Protection`, `assets/cab/CAB-04_Bedrock_Guardrails`.
    *   This is where the CDK app (`app.py`, stack file(s), `cdk.json`, `requirements.txt`) and any `test_*.py` unit tests live.

2.  **Documentation**: Every CAB **MUST** produce an `AUDIT.md` in its folder — the verification proof (what was tested, what the result was, screenshots referenced from `assets/images/`).
    *   Planning docs (design/implementation plans) go in `assets/docs/plans/`.
    *   Finished write-ups go in `assets/docs/reports/` or `assets/docs/portfolio/`.

3.  **Question Bank**: Every CAB **MUST** add its concepts to `assets/docs/SAA_QUESTION_BANK.md`, tagged with the CAB and the exam domain it covers.

4.  **Legacy content**: The `archive/Week_XX_*` folders are frozen under the old convention and exist for history only — do not add new content there. New work always goes under `assets/cab/CAB-XX_*`.

### Example Structure
```text
/
├── roadmap-v3.2.md              <-- Canonical roadmap + status
├── assets/
│   ├── cab/
│   │   ├── CAB-01_CDK_Zero-Trust/
│   │   ├── CAB-03_KMS_PHI_Protection/
│   │   │   ├── app.py
│   │   │   ├── vitalstream_data_stack.py
│   │   │   ├── test_kms_stack.py
│   │   │   └── AUDIT.md
│   │   └── CAB-04_Bedrock_Guardrails/
│   ├── docs/
│   │   ├── SAA_QUESTION_BANK.md
│   │   ├── plans/
│   │   └── reports/
│   └── images/
└── archive/                     <-- Frozen, pre-CAB week folders (history only)
```

## 🎨 Design & Formatting Rules

5.  **Marp Presentation Format**: All `README.md` files must be formatted as **Marp** slides.
    *   **Theme**: Must use `theme: 2smogss`.
    *   **Header**: Must start with the standard frontmatter:
        ```yaml
        ---
        marp: true
        theme: 2smogss
        ---
        ```
    *   **Slide Breaks**: Use `---` to separate logical sections into slides.

6.  **Visuals**: Each CAB **MUST** include its own Mermaid diagram file.
    *   **File Name**: `diagram.mermaid` inside the CAB folder.
    *   **Content**: Visualizes the architecture or process for that specific block.

7.  **⛔ NO Shared Code ("The Time Capsule Rule")**:
    *   **Do not** create shared folders (e.g., `utils/`, `scripts/`) at the root or under `assets/cab/`.
    *   **Do not** reference files from a previous CAB (e.g., `../CAB-01_CDK_Zero-Trust/app.py`).
    *   **Action**: If you need code from a previous CAB, **COPY IT** into the current CAB's folder.
    *   *Why?* This ensures CAB-01 remains "frozen in time" and works forever, even if CAB-07 evolves the code.

8.  **🛡️ Interactive Configuration Rule**:
    *   **Prompt, Don't Assume**: The Agent must never auto-execute configuration commands containing sensitive credentials without explicit user approval.
    *   **User-Driven**: The Agent should prompt the user to input keys, region, or secrets directly into the terminal, rather than passing them as arguments in a background script.
    *   **Credential Safety**: Never commit `.env` files or hardcoded credentials to git.

9.  **📝 The "First-Time" Lab Guide**:
    *   **Requirement**: Every new CAB MUST include a `LAB_GUIDE.md`.
    *   **Content**: A simple, copy-paste friendly checklist for the user to run the lab independently (e.g., "Step 1: Run setup.sh", "Step 2: SSH in").
    *   **Goal**: The user should be able to burn down and rebuild the lab without the Agent's help.

