# ELIZA — Python Recreation (1966)

**Recreating one of the earliest famous chatbots using Python.**

ELIZA is one of the earliest and most influential conversational programs in the history of Artificial Intelligence.

Originally developed by Joseph Weizenbaum at MIT in 1966, ELIZA simulated human conversation through pattern matching, keyword recognition, and predefined response rules.

This project is an educational Python recreation inspired by ELIZA's famous **DOCTOR** script.

It demonstrates how surprisingly conversational behavior can emerge from relatively simple rule-based mechanisms — without neural networks, machine learning, or language models.

---

## Overview

The original ELIZA did not understand natural language in the way modern AI systems do.

Instead, it analyzed user input, identified relevant keywords, matched predefined patterns, and generated responses using predefined templates.

This implementation recreates several of those fundamental mechanisms in Python.

### Example Conversation

```text
ELIZA: Hello. How are you feeling today?

You: I'm feeling unhappy.

ELIZA: Do you think coming here will help you not to feel unhappy?

You: My family doesn't understand me.

ELIZA: Tell me more about your family.

You: I feel alone.

ELIZA: Do you often feel alone?

You: quit

ELIZA: Goodbye. It was nice talking to you.
```

*Responses may vary between executions because the program selects from multiple response templates.*

---

## Features

- **Keyword Recognition:** Identifies important words and phrases in user input.
- **Keyword Prioritization:** Processes higher-priority keywords before lower-priority ones.
- **Pattern Matching:** Matches user statements against predefined linguistic patterns.
- **Decomposition & Reassembly:** Extracts parts of an input and reconstructs them into conversational responses.
- **Pronoun Transformation:** Converts pronouns and related expressions to maintain conversational perspective.
- **Rule-Based Response Generation:** Selects responses according to predefined rules and templates.
- **Simple Memory Mechanism:** Stores selected user statements and occasionally refers to them later.
- **Conversation History:** Maintains and displays the current conversation.
- **Interactive Terminal Interface:** Supports real-time text conversations.
- **Zero External Dependencies:** Uses only the Python standard library.

---

## How It Works

The conversation engine follows a rule-based processing pipeline:

```text
           User Input
                |
                v
       Text Normalization
                |
                v
       Keyword Recognition
                |
                v
      Keyword Prioritization
                |
                v
        Pattern Matching
                |
                v
       Input Decomposition
                |
                v
      Pronoun Transformation
                |
                v
       Response Reassembly
                |
                v
          ELIZA Response
```

### Core Mechanisms

| Mechanism | Description |
|---|---|
| Keyword Recognition | Detects relevant words in user input |
| Priority System | Determines which keyword rule to process first |
| Pattern Matching | Finds predefined sentence structures |
| Decomposition | Extracts relevant parts of the input |
| Reflection | Transforms pronouns and expressions |
| Reassembly | Builds a response using predefined templates |
| Memory | Stores selected statements for later reference |

### 1. Keyword Recognition

ELIZA searches for predefined keywords in the user's input.

For example:

```text
Input: My family doesn't understand me.

Detected keyword: family
```

Each keyword is associated with a priority and a set of response rules.

### 2. Pattern Matching

The system uses regular expressions to identify sentence structures.

For example:

```python
r"i feel (.*)"
```

This pattern can match statements such as:

```text
I feel unhappy.
I feel nervous.
I feel lonely.
```

### 3. Decomposition and Reassembly

After matching a pattern, the program extracts relevant parts of the input and inserts them into predefined response templates.

For example:

```text
Input:
I need help.

Extracted phrase:
help

Possible response:
Why do you need help?
```

### 4. Pronoun Transformation

ELIZA uses a reflection mechanism to transform expressions from the user's perspective into the chatbot's conversational perspective.

Examples:

| Original | Reflected |
|---|---|
| I | you |
| my | your |
| me | you |
| you | I |
| am | are |
| myself | yourself |

This helps construct responses that appear contextually relevant.

---

## Installation

### Requirements

- Python 3.10 or later
- No external packages required

### Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/eliza-python-recreation.git

cd eliza-python-recreation
```

### Run the Program

```bash
python eliza_recreated.py
```

---

## Available Commands

| Command | Description |
|---|---|
| `help` | Displays available commands |
| `history` | Shows conversation history |
| `clear` | Clears conversation history and memory |
| `quit` | Ends the conversation |
| `exit` | Ends the conversation |
| `bye` | Ends the conversation |

---

## Project Structure

```text
eliza-python-recreation/
│
├── eliza_recreated.py
└── README.md
```

---

## Historical Background

ELIZA was developed by **Joseph Weizenbaum** at the Massachusetts Institute of Technology (MIT) and introduced in 1966.

Its most famous script, **DOCTOR**, simulated the conversational style of a Rogerian psychotherapist.

The original implementation was written using **MAD-SLIP**, not Python.

ELIZA became historically significant not only because of its conversational behavior, but also because of how people responded to it.

Some users attributed understanding and intelligence to a program that primarily relied on pattern matching and predefined responses.

This phenomenon became known as the **ELIZA Effect**.

### Why ELIZA Still Matters

ELIZA illustrates an important distinction in Artificial Intelligence:

> Generating convincing language is not necessarily the same as understanding it.

Decades later, this question remains relevant as we interact with increasingly sophisticated Large Language Models.

The underlying technology has changed dramatically, but the distinction between convincing communication and genuine understanding remains an important topic in AI research.

---

## Implementation Scope and Limitations

This project is an **educational recreation**, not a source-code restoration or an exact reproduction of the original 1966 ELIZA implementation.

Important distinctions:

- The original ELIZA was implemented using MAD-SLIP.
- This recreation is written in Python.
- Its response rules are inspired by the DOCTOR script.
- The memory mechanism, command interface, and conversation-history functionality are additional implementation features.
- Its pattern matching and response generation are rule-based rather than neural or statistical language generation.
- The implementation is primarily designed for English-language interaction.

The goal is to demonstrate the fundamental conversational mechanisms behind early rule-based chatbots.

---

## Technologies

- Python
- Regular Expressions (`re`)
- Random Response Selection (`random`)
- Dataclasses
- Python Standard Library

---

## Connect with Me

I'm interested in Artificial Intelligence, LLMs, AI Agents, and the evolution of intelligent systems.

- **LinkedIn:** [Mahdi Ahmadi](https://www.linkedin.com/in/aimahdix)
- **GitHub:** [aiMahdiX](https://github.com/aiMahdiX)

Feel free to connect, share your thoughts, or explore more of my AI projects.

---

## License

Choose an appropriate open-source license before publishing this repository. If you intend to allow reuse and modification, the MIT License is a common permissive option.

---

**A small experiment in the history of Artificial Intelligence.**

From pattern matching in 1966 to Large Language Models today, the evolution of conversational AI is worth understanding — not just using.
