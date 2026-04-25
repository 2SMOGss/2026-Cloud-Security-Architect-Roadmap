# Workspace Reorganization Implementation Plan

> **For Antigravity:** REQUIRED WORKFLOW: Use `.agent/workflows/execute-plan.md` to execute this plan in single-flow mode.

**Goal:** Refactor the directory structure to improve organization, moving CABs, documents, and images into a centralized `assets/` structure while keeping the root clean and focused.

**Architecture:** We will use a systematic "Create -> Move -> Update Links" approach. All CABs move to `assets/cab/`, documentation moves to `assets/docs/`, and media moves to `assets/images/`.

**Tech Stack:** PowerShell (for file operations), Ripgrep (for path discovery).

---

### Task 1: Create New Directory Structure

**Files:**
- Create: `assets/cab/`
- Create: `assets/docs/`
- Create: `assets/images/`

**Step 1: Create directories**

Run: `mkdir -p assets/cab, assets/docs, assets/images`
Expected: Directories created successfully.

**Step 2: Commit**

Run: `git add assets/`
Run: `git commit -m "chore: initialize new assets structure"`

---

### Task 2: Relocate Cloud Architecture Badges (CABs)

**Files:**
- Modify: `assets/cab/`
- Move: `CAB-01_CDK_Zero-Trust`
- Move: `CAB-03_KMS_PHI_Protection`
- Move: `CAB-04_Bedrock_Guardrails`

**Step 1: Move active CABs**

Run: `mv CAB-01_CDK_Zero-Trust assets/cab/`
Run: `mv CAB-03_KMS_PHI_Protection assets/cab/`
Run: `mv CAB-04_Bedrock_Guardrails assets/cab/`
Expected: Folders moved to `assets/cab/`.

**Step 2: Archive trash and old backups**

Run: `mv CAB-04_Bedrock_Guardrails_TRASH archive/`
Run: `mv EC2_Backup archive/`
Expected: Folders moved to `archive/`.

**Step 3: Commit**

Run: `git add assets/cab archive/`
Run: `git commit -m "chore: relocate CABs and archive old backups"`

---

### Task 3: Relocate Documentation and Learning Materials

**Files:**
- Modify: `assets/docs/`
- Move: `docs/*`
- Move: `learning_teach/*`

**Step 1: Move docs content**

Run: `mv docs/* assets/docs/`
Expected: All files from `docs/` moved to `assets/docs/`.

**Step 2: Move learning materials**

Run: `mv learning_teach assets/docs/`
Expected: `learning_teach` folder moved under `assets/docs/`.

**Step 3: Elevate current roadmap**

Run: `mv assets/docs/roadmap-v3.2.md ./`
Expected: `roadmap-v3.2.md` moved to the root.

**Step 4: Archive old roadmap**

Run: `mv Roadmap_2026.md archive/`
Expected: Old roadmap moved to `archive/`.

**Step 5: Cleanup empty folders**

Run: `rmdir docs`
Expected: Empty `docs` folder removed.

**Step 6: Commit**

Run: `git add assets/docs roadmap-v3.2.md archive/`
Run: `git commit -m "chore: reorganize documentation and elevate roadmap v3.2"`

---

### Task 4: Relocate Media Assets

**Files:**
- Modify: `assets/images/`
- Move: Root and assets-level `.png`, `.jpg`, `.mp4`

**Step 1: Move images from root assets**

Run: `mv assets/*.png assets/images/`
Run: `mv assets/*.mp4 assets/images/`
Expected: Media files moved to `assets/images/`.

**Step 2: Commit**

Run: `git add assets/images/`
Run: `git commit -m "chore: consolidate media assets into assets/images"`

---

### Task 5: Update Internal Links

**Files:**
- Modify: `README.md`
- Modify: `CONTEXT.md`
- Modify: `MINDMAP.md`
- Modify: `assets/docs/**/*`

**Step 1: Search for broken paths**

Run: `rg "CAB-"` and `rg "docs/"` to find outdated links.

**Step 2: Update links in key files**

Update paths to include `assets/cab/`, `assets/docs/`, and `assets/images/` as appropriate.

**Step 3: Commit**

Run: `git commit -m "fix: update internal links to match new structure"`
