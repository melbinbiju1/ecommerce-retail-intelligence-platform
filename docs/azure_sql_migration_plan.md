# Azure SQL Migration Plan

## Project Name

E-Commerce Retail Intelligence Platform with Operational Anomaly Detection and AI Business Insights

## Purpose

This document explains how the local SQLite version of the project will be migrated to Azure SQL Database.

The local SQLite database is used for development because it is simple, lightweight, and easy to run on a local machine. The production-style cloud version will use Azure SQL Database.

---

## 1. Current Local Architecture

```text
Olist CSV files
      ↓
Python ingestion
      ↓
SQLite database
      ↓
dbt transformations
      ↓
Power BI exports / FastAPI / AI assistant