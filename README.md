# GA4 Audit AI Agent

A Streamlit app that validates Google Analytics 4 Measurement IDs across a batch of websites and generates an AI-powered audit report — turning a manual, page-by-page GA4 QA check into a bulk, automated workflow.

<!-- Add a screenshot or GIF of the app here, e.g. the uploaded file preview + AI report -->
<!-- ![App screenshot](docs/screenshot.png) -->

## Why this exists

Verifying that every site in a portfolio is firing the correct GA4 Measurement ID — and that cookie consent isn't blocking it — is normally a manual, one-tab-at-a-time process. This tool takes a simple spreadsheet of sites and expected Measurement IDs, checks each one automatically, and has an LLM turn the raw results into a readable audit report with findings and likely causes.

## Features

- Upload a CSV or Excel file listing sites and their expected GA4 Measurement IDs
- Automatic file validation before the audit runs
- Batch audits every site: opens the page, detects the actual GA4 Measurement ID firing, and checks whether the cookie consent banner was accepted
- Live progress bar and per-site status while the audit runs
- One consolidated AI-generated audit report summarizing results, discrepancies, and likely reasons for failures
- Download both the raw results (CSV) and the AI report (Markdown)
- Full run logging for traceability

## Tech stack

- **Python**
- **Streamlit** — web app UI
- **Pandas** — file parsing and results handling
- **Playwright** — automated site visits and GA4 tag detection
- **OpenAI API** — AI-generated audit report

## Getting started

### Prerequisites

- Python 3.10+
- An OpenAI API key

### Installation

```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
pip install -r requirements.txt
playwright install
```

### Configuration

Set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY="your-api-key-here"
```

### Usage

```bash
streamlit run app.py
```

Then in the app:
1. Upload a CSV or Excel file with `site` and `measurement_id` columns
2. Review the validated file preview and summary metrics
3. Click **Start Audit**
4. Review the per-site results table and the AI-generated report
5. Download the results as CSV and/or the AI report as Markdown

### Input file format

| site | measurement_id |
|---|---|
| https://example.com | G-XXXXXXXXXX |
| https://example2.com | G-YYYYYYYYYY |

## How it works

1. **Upload & validate** — the input CSV/Excel is parsed and validated before anything runs
2. **Audit** — for each site, the app opens the page (via Playwright), detects the GA4 Measurement ID actually firing, and checks whether the cookie consent banner was accepted
3. **Compare** — the found Measurement ID is compared against the expected one, producing a pass/fail status and reason for each site
4. **AI report** — all results are sent to the OpenAI API in a single call, which generates a readable, consolidated audit report highlighting discrepancies and likely causes
5. **Export** — results and the AI report are downloadable as CSV and Markdown respectively, and every run is logged

## Project structure

```
app.py            # Streamlit UI and orchestration
validation.py     # Input file validation
audit.py          # Site visits and GA4 Measurement ID detection
ai_analyzer.py     # AI report generation
logger.py         # Run logging
```

## Current scope & limitations

- Currently checks GA4 Measurement ID presence and cookie consent status
- <!-- Add any known limitations, e.g. SPA support, login-gated pages, consent banner variations handled -->

## Roadmap

- <!-- e.g. Extend to GTM container validation -->
- <!-- e.g. Extend to Adobe Analytics / Adobe Launch checks -->
- <!-- e.g. Scheduled/recurring audits -->

## About

Built by Vinitha, a marketing/digital analytics specialist with 9+ years across GA4, GTM, Adobe Analytics, Adobe Launch, AAM, AEP RT-CDP, SQL, and Tealium — to bring engineering rigor to a process that's traditionally manual.

[LinkedIn](#) · [Portfolio](#)
