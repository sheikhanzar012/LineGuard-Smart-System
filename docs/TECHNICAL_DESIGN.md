# LineGuard Smart System — Technical Design Document

## 1. Project Overview

**LineGuard Smart System** is a software-only digital maintenance safety-interlock prototype designed to demonstrate a safer and more controlled workflow for electrical line maintenance.

The system establishes a digital coordination mechanism between:

- Lineman / Field Personnel
- Grid Control Room

The current prototype uses a controlled state-based workflow for maintenance requests, simulated isolation, maintenance locking, temporary test power, clearance, safety confirmation, and final restoration.

> **Safety Note:** The current implementation is software-only. It does not control, disconnect, energize, verify, or monitor real electrical equipment. The isolators and test power shown in the interface are simulations only.

## 2. Problem Statement

Electrical line maintenance requires reliable coordination between field personnel and grid control operations. LineGuard demonstrates a digital workflow in which maintenance actions and restoration are permitted only through defined states and authorization steps.

## 3. Objectives

- Digitize the maintenance request workflow.
- Provide lineman-to-grid coordination.
- Simulate three-point isolation.
- Implement a digital maintenance lock.
- Block restoration during active maintenance.
- Provide controlled simulated test power.
- Require clearance and safety confirmation before final restoration.
- Maintain an event log.
- Provide a responsive mobile and grid-control interface.
- Provide a foundation for future microcontroller and cloud integration.

## 4. Current Software Architecture

```text
LINEMAN MOBILE BROWSER        GRID CONTROL BROWSER
          |                           |
          +-------------+-------------+
                        |
                        v
                 Flask REST Backend
                     app.py
                        |
              +---------+---------+
              |                   |
         System State         Event Log
              |
       Three Simulated
       Isolation Points
