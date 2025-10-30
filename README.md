# Gramartico

A lightweight command line assistant that surfaces common issues while you write. It focuses on fast feedback instead of complex language models so that it can run anywhere.

## Features

- Detects repeated words and accidental double spaces.
- Flags missing terminal punctuation and overly long sentences.
- Spots several high-frequency typos such as *teh* → *the*.
- Emits structured JSON output that can be consumed by editors.

## Usage

Install the project in editable mode and run the CLI:

```bash
pip install -e .
python -m gramartico.cli "This is is a smple sentence"
```

Output:

```
5-7: Repeated word 'is' detected. → 
18-23: Did you mean 'sample'? → sample
```

The CLI also reads from standard input and can report JSON suggestions:

```bash
echo "Finish teh paragraph" | python -m gramartico.cli --json
```

```
[{"start": 7, "end": 10, "message": "Did you mean 'the'?", "replacements": ["the"]}]
```
