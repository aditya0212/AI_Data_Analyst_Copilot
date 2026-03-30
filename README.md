# AI Data Analyst Copilot

> Talk to your data. Get answers instantly — no SQL, no scripts, no guesswork.

Most data tools assume you already know what you're doing. This one doesn't. You upload a CSV, ask a question in plain English, and get back a chart or a number — the same way you'd ask a colleague.

---

## What it does

You drop in a dataset. You ask something like *"Which region had the highest sales last quarter?"* The app figures out what you mean, writes the Pandas code, runs it, and shows you the result — with a chart if it makes sense to have one.

No query language. No manual plotting. Just a question and an answer.

---

## Why I built this

I kept running into the same problem: non-technical teammates needed quick answers from data but had to wait on someone (usually me) to write a script or pull a number. I wanted a tool where they could just... ask. This is that tool.

---

## Tech Stack

| Layer | Tool |
|---|---|
| UI | Streamlit |
| Data processing | Pandas |
| Visualization | Matplotlib |
| LLM backend | OpenRouter API |
| Language | Python |

---

## How it works

```
User uploads CSV
      ↓
User types a question in plain English
      ↓
Question + dataframe schema → sent to LLM
      ↓
LLM returns Pandas code
      ↓
Code is sanitized and validated before execution
      ↓
Result rendered as table or chart
```

The part most people skip over: the LLM output goes through a post-processing step before any code runs. It strips markdown artifacts, checks for unsafe operations, and normalizes column references against the actual dataframe — so the app doesn't break when the model gets creative with variable names.

---

## Example queries you can try

- `"What's the average order value by category?"`
- `"Show me monthly revenue as a bar chart"`
- `"Which product had the most returns in Q3?"`
- `"Compare profit margins across regions"`


---

## What's next

- [ ] Support for Excel and JSON uploads
- [ ] Export conversation + charts as a PDF report
- [ ] Hosted demo on Streamlit Cloud

---

## Known limitations

- Works best on structured, well-labeled CSVs. Messy column names confuse the model.
- Very large files (100k+ rows) can slow down response time.
- The LLM occasionally misreads ambiguous questions — rephrasing usually fixes it.

---

Built by [Aditya Singh](https://github.com/aditya0212)  
Open to feedback, issues, and PRs.
