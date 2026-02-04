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

