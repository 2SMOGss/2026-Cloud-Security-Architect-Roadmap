# Repository Structure Rules

## ⚠️ "Hard Rule" for New Content

To maintain a clean portfolio, all new weekly content **MUST** follow this strict directory structure:

1.  **Weekly Folder**: Create a new folder for each week in the root directory.
    *   **Naming Convention**: `Week_XX_TopicName`
    *   *Example*: `Week_02_Linux_Security`, `Week_03_Cloud_Networking`.

2.  **Documentation**: Every folder **MUST** contain a `README.md`.
    *   This file serves as the "Landing Page" for that week.
    *   It should contain the Lab instructions, concepts, and diagrams.

3.  **Scripts & Assets**: All scripts, images, and config files for that week go **INSIDE** that week's folder.
    *   *Do NOT put weekly scripts in the root directory.*

### Example Structure
```text
/
├── Week_01_Medical_VPC/
│   ├── README.md       <-- The Lab Guide
│   ├── script.sh       <-- The Code
│   └── diagram.png     <-- The Assets
│
├── Week_02_Linux_Security/
│   ├── README.md
│   └── audit_logs.sh
```

## 🎨 Design & Formatting Rules

4.  **Marp Presentation Format**: All `README.md` files must be formatted as **Marp** slides.
    *   **Theme**: Must use `theme: 2smogss`.
    *   **Header**: Must start with the standard frontmatter:
        ```yaml
        ---
        marp: true
        theme: 2smogss
        ---
        ```
    *   **Slide Breaks**: Use `---` to separate logical sections into slides.

5.  **Visuals**: Each week **MUST** include its own Mermaid diagram file.
    *   **File Name**: `diagram.mermaid` inside the weekly folder.
    *   **Content**: Visualizes the architecture or process for that specific week.

6.  **⛔ NO Shared Code ("The Time Capsule Rule")**:
    *   **Do not** create shared folders (e.g., `utils/`, `scripts/`) in the root.
    *   **Do not** reference files from previous weeks (e.g., `../Week_01/script.sh`).
    *   **Action**: If you need a script from a previous week, **COPY IT** into the current week's folder.
    *   *Why?* This ensures that Week 1 remains "frozen in time" and works forever, even if Week 10 evolves the code.

7.  **🛡️ Interactive Configuration Rule**:
    *   **Prompt, Don't Assume**: The Agent must never auto-execute configuration commands containing sensitive credentials without explicit user approval.
    *   **User-Driven**: The Agent should prompt the user to input keys, region, or secrets directly into the terminal, rather than passing them as arguments in a background script.
    *   **Credential Safety**: Never commit `.env` files or hardcoded credentials to git.

8.  **📝 The "First-Time" Lab Guide**:
    *   **Requirement**: Every new week MUST include a `LAB_GUIDE.md`.
    *   **Content**: A simple, copy-paste friendly checklist for the user to run the lab independently (e.g., "Step 1: Run setup.sh", "Step 2: SSH in").
    *   **Goal**: The user should be able to burn down and rebuild the lab without the Agent's help.

