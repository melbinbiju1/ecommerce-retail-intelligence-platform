# Data Lineage

## Project Name

E-Commerce Retail Intelligence Platform with Operational Anomaly Detection and AI Business Insights

## Purpose

This document explains how data flows through the project from raw Olist CSV files to final Power BI, FastAPI, and AI business insight outputs.

---

## 1. High-Level Lineage

```text
Olist CSV files
      ↓
Python raw ingestion
      ↓
Raw SQLite tables
      ↓
Raw data quality checks
      ↓
dbt staging models
      ↓
dbt warehouse models
      ↓
dbt KPI models
      ↓
dbt operational metric models
      ↓
Python anomaly detection
      ↓
Operational event pipeline
      ↓
dbt operational KPI views
      ↓
Power BI exports
      ↓
Power BI dashboard / FastAPI / AI assistant