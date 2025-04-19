# 🕷️ Wiki Crawler

A Python-based web crawler designed to extract and structure content from Wikipedia pages. It was originally developed to support the creation of a diverse and high-quality dataset for use in a plagiarism detection system. The tool may also be applicable to other natural language processing tasks such as textual similarity, paraphrase detection, and summarization.

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
