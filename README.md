<div align="center">

<img src="https://raw.githubusercontent.com/devarshidavane/devarshidavane/main/header.svg" width="100%" alt="SecureDrive">

<br>

# `SECUREDRIVE`

### Endpoint Security • Malware Detection • Threat Analysis

<br>

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PySide6](https://img.shields.io/badge/PySide6-Qt-41CD52?style=for-the-badge&logo=qt&logoColor=white)](https://doc.qt.io/qtforpython/)
[![Windows](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://www.microsoft.com/windows)
[![Security](https://img.shields.io/badge/Domain-Endpoint%20Security-8B5CF6?style=for-the-badge)](#)

</div>

<br>

---

<img src="https://raw.githubusercontent.com/devarshidavane/devarshidavane/main/h-about.svg" width="100%" alt="About SecureDrive">

## `>_ What is SecureDrive?`

**SecureDrive** is a Windows-focused endpoint-security application built with Python and PySide6.

The project explores how a lightweight endpoint scanner can combine:

```text
                    ┌─────────────────────┐
                    │       FILE          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   FILE ANALYSIS     │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │   HASH GENERATION   │
                    │   MD5 / SHA-256     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ SIGNATURE DATABASE  │
                    └──────────┬──────────┘
                               │
                     ┌─────────┴─────────┐
                     │                   │
                   MATCH              NO MATCH
                     │                   │
                     ▼                   ▼
                ┌──────────┐        ┌─────────┐
                │THREAT    │        │  SAFE   │
                └────┬─────┘        └─────────┘
                     │
                     ▼
                QUARANTINE
                     │
                     ▼
                THREAT LOG
