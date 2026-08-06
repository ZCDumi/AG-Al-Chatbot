# Analytics Group — Website Chatbot

A guided chatbot for [analyticsgroup.co.za](https://analyticsgroup.co.za/) that helps site
visitors understand AG's services and points warm leads to a consultation. Built with  *FastAPI backend and a React (Vite) frontend
## What it does

- Greets visitors and explains what Analytics Group does.
- Answers questions about all six services (BI & Data Analytics, Data Fabric & Big Data
  Engineering, Data Ops & Governance, Data Science, Audit CAATs & Data Processes, Systems
  Development), using keyword matching against a knowledge base sourced from the live site.
- Answers FAQs (location, contact details, track record, "data evangelism").
- Runs a light lead-capture flow (name → email → company → need) when a visitor asks for a
  consultation, quote, or to be contacted, and stores it server-side for the AG team.
