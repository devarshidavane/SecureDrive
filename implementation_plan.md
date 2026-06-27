# Implementation Plan: Secure Drive Hybrid Architecture

This document outlines the architectural overhaul of **Secure Drive** to transform it from a standard hash-checking scanner into a lightweight, enterprise-grade Hybrid Antivirus system.

## User Review Required
> [!IMPORTANT]
> This is a massive architectural shift that will fundamentally change how Secure Drive works. Please review the phases below. We will build this iteratively, starting with Phase 1. Do you approve of this roadmap?

## Open Questions
> [!WARNING]
> 1. **Server Network:** Will the older laptop (the Server) be on the same local Wi-Fi network as the client, or will you want it accessible over the internet (requiring port forwarding/cloud hosting)?
> 2. **Windows Version:** Can we assume the target users for the Sandbox feature will be running Windows 10/11 Pro or Enterprise (required for Windows Sandbox)?

---

## Proposed Architectural Changes

The project will be split into two main components:
1. **The Server (The Brain)**: Runs on the old AMD laptop. Handles heavy databases, Machine Learning, and complex analysis.
2. **The Client (The Agent)**: Runs on the user's PC. Extremely lightweight, relies on Bloom filters, and handles UI and real-time interception.

We will execute this in **Three Phases**.

### Phase 1: Storage Optimization & Server Foundation

Our first goal is to reduce the disk footprint on the client PC and offload the heavy database to the server.

#### [NEW] `Server/api_server.py`
We will create a lightweight Python web server (using `FastAPI` or `Flask`) that will run on your old laptop.
- It will host the master `Malware Hash Database` (SQLite).
- It will provide an endpoint (e.g., `/check_hash`) for the client to query.

#### [NEW] `Client/utils/bloom_filter.py`
- We will implement a Bloom Filter on the Client. 
- The Client will download a tiny (~2MB) Bloom filter file from the Server on startup. The scanner will use this for instant, 0-latency checks.

#### [MODIFY] `c:\Dmce\Secure drive\UI\QT\Scans\scanner.py`
- Refactor the scanner to first check the Bloom filter. 
- If the filter returns "suspicious", the scanner will make a network request to the Server for absolute confirmation, eliminating the need to store the full database locally.

---

### Phase 2: Dynamic Analysis (The Detonation Chamber)

We will introduce the safe environment for analyzing large or highly suspicious files.

#### [NEW] `Client/sandbox/sandbox_manager.py`
- We will write a Python module that dynamically generates a `.wsb` (Windows Sandbox configuration) file.
- It will map a shared folder between the host and the Sandbox.
- The UI will get a new feature: **"Deep Scan in Sandbox"**. When clicked, it will copy the file to the shared folder and boot the Sandbox automatically.

#### [NEW] `Client/sandbox/monitor.py`
- A tiny script injected into the Sandbox that monitors what the file does and writes the results to a text log in the shared folder for the main UI to read.

---

### Phase 3: Real-Time API Hooking (Mini-Sandbox)

This is the most advanced phase, bringing the Next-Gen EDR capabilities.

#### [NEW] `Client/protection/api_hook.py`
- We will integrate a dynamic instrumentation library (like `Frida`).
- When `Real_time_scan.py` detects a new executable launching, it will launch it in a `SUSPENDED` state.
- `api_hook.py` will inject into the process memory to monitor dangerous Windows API calls (e.g., `DeleteFile`, `RegSetValue`).
- If malicious behavior is detected, it terminates the process instantly.

---

## Verification Plan

### Automated Tests
- We will create dummy "malware" files (e.g., EICAR test files) to ensure the Bloom filter correctly flags them.
- We will test the Server API response times to ensure latency is under 50ms.

### Manual Verification
- Deploy the Server code to the old AMD laptop.
- Run the Client UI on your main PC.
- Attempt to scan a 1GB file and ensure the system remains responsive.
- Trigger the Windows Sandbox generation and confirm the isolated environment launches successfully.
