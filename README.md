# LLM Output Evaluator

Compare two AI-generated answers side-by-side. Scores responses on factual accuracy, completeness, clarity, and hallucination risk using Gemini 2.5 Flash.

## Live Demo

[llm-evaluator.streamlit.app](https://llm-evaluator.streamlit.app)

## Features

- Compare two AI answers to the same question
- Score on 4 metrics: Accuracy, Completeness, Clarity, Hallucination Risk
- 1-10 scale with detailed explanations
- Automatic winner detection
- Professional dark SaaS dashboard UI
- Environment variable or manual API key input

## Tech Stack

Python | Streamlit | Gemini 2.5 Flash | Google GenAI SDK

## Quick Start

```bash
git clone https://github.com/Abdulgeni/llm-evaluator.git
cd llm-evaluator
pip install -r requirements.txt
streamlit run app.py
