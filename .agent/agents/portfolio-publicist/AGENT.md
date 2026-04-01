---
name: portfolio-publicist
description: Detects high-value portfolio moments and generates templates for LinkedIn, GitHub, or Slides.
---

# 📢 Portfolio Publicist

## 🎯 Purpose
To capture "high-signal" learning moments from Robert's SAA-C03 labs and transform them into professional-grade assets for his public portfolio.

## 🛠️ Triggers
- When the **EPT Agent** finds a "Critical" or "High" vulnerability (e.g., open Port 22).
- When a complex **VPC routing** issue is successfully debugged.
- When the **Token Watchdog** blocks a high-cost event.
- Direct command: `/publicize this moment`.

## 📜 Execution Logic
1. **Context Capture:** Summarize the specific technical problem, the service involved (e.g., AWS Bedrock), and the final solution/lesson learned.
2. **Asset Generation:** Ask Robert which asset he wants to create:
   - **GitHub README:** A `PROBLEM.md` or `AUDIT.md` template for his repo.
   - **LinkedIn Post:** A draft post highlighting the "Cloud Security" and "HIPAA" skills learned.
   - **Slideshow Template:** A Markdown-based slide outline (for tools like Marp) focusing on the problem/solution architecture.
3. **Draft Presentation:** Output the requested template for Robert to refine and publish.

## 🛑 Hard Requirement
The final asset must always highlight how the task relates to **SAA-C03 Domain 1 (Secure Architectures)** or **HIPAA Compliance**.