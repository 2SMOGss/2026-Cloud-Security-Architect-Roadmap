# Design Document: VPC Packet Journey Study Guide & Roadmap Integration

## Overview
This document outlines the structural design and integration plan for creating a highly visual, professional-grade AWS VPC study presentation. The presentation is designed using MARP (Markdown Presentation Ecosystem) and Mermaid.js flowcharts to prepare the student for the SAA-C03 exam and future architectural interviews.

## 1. Directory Structure & Naming
*   **File Location**: `learning_teach/VPC_Packet_Journey.md`
*   **Purpose**: Centralize exportable, highly polished AWS Architect study decks outside of the main CAB operational codebase.

## 2. Slide Deck Content Architecture
The presentation will follow a structured narrative to track network traffic through an AWS VPC:

1.  **Title Slide**: The Anatomy of a Zero-Trust Medical VPC.
2.  **The Big Picture**: A Mermaid diagram illustrating the overall AWS Region -> VPC -> AZs -> Subnets hierarchy.
3.  **The Inbound Journey**:
    *   **Internet Gateway (IGW) & Route Tables**: Evaluating CIDR blocks.
    *   **Network ACLs**: Explaining stateless subnet-level boundaries.
    *   **Public Security Groups**: Explaining stateful instance-level rules (e.g., ALB traffic on Port 443).
4.  **The Chasm (Public to Private Transition)**: Routing from the public Application Load Balancer to private subnet resources.
5.  **The Outbound Egress**:
    *   **NAT Gateways**: Securing outbound OS patching traffic.
    *   **VPC Endpoints (AWS PrivateLink)**: Preventing S3/Bedrock traffic from traversing the public internet.
6.  **SAA-C03 Cheat Sheet**: A comparison table of Stateful (SG) vs. Stateless (NACL) and Public vs. Private structures.

## 3. Roadmap V3.2 Integration
The `docs/roadmap-v3.2.md` will be updated to formally institutionalize this study method:
*   **CAB-01 Checkpoint**: Insert a mandatory review step: "Create & Master the 'Packet Journey' presentation."
*   **CAB-08 Checkpoint**: Insert a mandatory review step: "Review all 'Architect Blueprint' slide decks before sitting the SAA-C03 exam."

## 4. Acceptance Criteria
*   The MARP document renders successfully with Mermaid diagrams.
*   The presentation adopts the brutally honest, Direct-to-the-Point "AWS Architect Mentor" tone.
*   The 24-Week Roadmap reflects the new study methodology.
