# 🕷️ Wiki Crawler

A simple yet powerful Python-based web crawler built to extract and structure content from Wikipedia pages. Originally developed to build a diverse, high-quality dataset for a **plagiarism checker**, this tool is ideal for NLP tasks involving textual similarity, paraphrasing, summarization, and more.

> ⚠️ **Note:** The `main` branch is currently empty. Please refer to the [`master`](https://github.com/yourusername/wiki-crawler/tree/master) or [`bbao_main`](https://github.com/yourusername/wiki-crawler/tree/bbao_main) branches for the actual implementation.

## 🚀 Features

- Crawl Wikipedia starting from any topic or category
- Traverse internal links up to a defined depth
- Extract clean, structured content from each article
- Optionally store metadata (e.g., page titles, URLs)
- Save output in plain text, JSON, or CSV formats
- Designed with modularity for easy extension

## 🧠 Use Case

This crawler was specifically used to **generate a dataset** of authentic Wikipedia content for training and testing a **plagiarism detection model**. The goal was to simulate realistic text reuse scenarios using paraphrased and direct excerpts.

## 🛠️ Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/wiki-crawler.git
cd wiki-crawler
git checkout master  # or bbao_main
pip install -r requirements.txt
