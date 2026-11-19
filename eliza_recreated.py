
"""
ELIZA - Python Recreation
-------------------------
An educational recreation of Joseph Weizenbaum's ELIZA chatbot (1966).

Inspired by the original DOCTOR script.

Historical note:
This is NOT the original ELIZA source code.
The original implementation was written using MAD-SLIP.
This Python version recreates its central conversational mechanisms:

    - Keyword recognition and prioritization
    - Decomposition and reassembly
    - Pronoun transformation
    - Rule-based response generation
    - Memory and fallback responses

Author: Educational Recreation
Python: 3.10+
Dependencies: Python Standard Library Only
"""

from __future__ import annotations

import random
import re
import textwrap
from dataclasses import dataclass, field
from typing import Optional


# ============================================================
# 1. DATA STRUCTURES
# ============================================================

@dataclass
class DecompositionRule:
    """
    Defines how an input sentence should be decomposed
    and how a response should be reconstructed.
    """
    pattern: str
    responses: list[str]


@dataclass
class KeywordRule:
    """
    Defines a keyword, its priority, decomposition rules,
    and optional memory responses.
    """
    keyword: str
    priority: int
    decompositions: list[DecompositionRule]
    memory_responses: list[str] = field(default_factory=list)


# ============================================================
# 2. ELIZA ENGINE
# ============================================================

class ELIZA:

    def __init__(self, seed: Optional[int] = None):
        self.rng = random.Random(seed)

        self.history: list[tuple[str, str]] = []
        self.memory: list[str] = []

        self.previous_topic: Optional[str] = None

        self.quit_commands = {
            "quit",
            "exit",
            "bye",
            "goodbye",
            "stop"
        }

        self.reflections = {
            "am": "are",
            "are": "am",
            "was": "were",
            "were": "was",
            "i": "you",
            "i'm": "you are",
            "im": "you are",
            "i've": "you have",
            "ive": "you have",
            "i'll": "you will",
            "ill": "you will",
            "i'd": "you would",
            "id": "you would",
            "my": "your",
            "mine": "yours",
            "me": "you",
            "myself": "yourself",
            "you": "I",
            "you're": "I'm",
            "youre": "I'm",
            "you've": "I've",
            "youve": "I've",
            "you'll": "I'll",
            "youll": "I'll",
            "your": "my",
            "yours": "mine",
            "yourself": "myself",
            "we": "you",
            "we're": "you're",
            "were": "you're",
            "our": "your",
            "ours": "yours",
            "us": "you"
        }

        self.reflection_pattern = re.compile(
            r"\b(" +
            "|".join(
                sorted(
                    map(re.escape, self.reflections.keys()),
                    key=len,
                    reverse=True
                )
            ) +
            r")\b",
            re.IGNORECASE
        )

        self.rules = self._build_rules()

        # Higher priority rules are processed first.
        self.rules.sort(
            key=lambda rule: rule.priority,
            reverse=True
        )

        self.fallback_responses = [
            "Please go on.",
            "I see.",
            "Can you elaborate on that?",
            "What does that suggest to you?",
            "Why do you say that?",
            "How does that make you feel?",
            "Can you tell me more?",
            "Let's explore that further."
        ]

        self.repetition_responses = [
            "You are repeating yourself. Could you explain why?",
            "Does repeating that thought mean something to you?",
            "You seem to be returning to the same idea."
        ]

        self.empty_responses = [
            "Please say something.",
            "I'm listening.",
            "What would you like to talk about?"
        ]

        self.previous_input: Optional[str] = None

    # ========================================================
    # 3. RULE DEFINITIONS
    # ========================================================

    def _build_rules(self) -> list[KeywordRule]:

        return [

            # ------------------------------------------------
            # Highest priority: sentence transformations
            # ------------------------------------------------

            KeywordRule(
                keyword="sorry",
                priority=100,
                decompositions=[
                    DecompositionRule(
                        r".*",
                        [
                            "Please don't apologize.",
                            "Apologies are not necessary.",
                            "What feelings do you have when you apologize?"
                        ]
                    )
                ]
            ),

            KeywordRule(
                keyword="remember",
                priority=95,
                decompositions=[
                    DecompositionRule(
                        r".*remember(.*)",
                        [
                            "Do you often think of {0}?",
                            "What else do you remember about {0}?",
                            "Does remembering {0} bring anything else to mind?"
                        ]
                    )
                ]
            ),

            KeywordRule(
                keyword="dream",
                priority=90,
                decompositions=[
                    DecompositionRule(
                        r".*dream(?:ed|ing)?(.*)",
                        [
                            "What does that dream suggest to you?",
                            "Do you believe dreams have something to do with your problems?",
                            "What persons appear in your dreams?"
                        ]
                    )
                ]
            ),

            # ------------------------------------------------
            # Family
            # ------------------------------------------------

            KeywordRule(
                keyword="family",
                priority=85,
                decompositions=[
                    DecompositionRule(
                        r".*family(.*)",
                        [
                            "Tell me more about your family.",
                            "Who else in your family {0}?",
                            "How do you get along with your family?",
                            "Is your family important to you?"
                        ]
                    )
                ]
            ),

            KeywordRule(
                keyword="mother",
                priority=85,
                decompositions=[
                    DecompositionRule(
                        r".*mother(.*)",
                        [
                            "Tell me more about your mother.",
                            "What was your relationship with your mother like?",
                            "How do you feel about your mother?"
                        ]
                    )
                ]
            ),

            KeywordRule(
                keyword="father",
                priority=85,
                decompositions=[
                    DecompositionRule(
                        r".*father(.*)",
                        [
                            "How do you feel about your father?",
                            "Tell me more about your father.",
                            "Does your father influence you in some way?"
                        ]
                    )
                ]
            ),

            KeywordRule(
                keyword="sister",
                priority=80,
                decompositions=[
                    DecompositionRule(
                        r".*sister(.*)",
                        [
                            "Tell me more about your sister.",
                            "How is your relationship with your sister?",
                            "Does your sister understand you?"
                        ]
                    )
                ]
            ),

            KeywordRule(
                keyword="brother",
                priority=80,
                decompositions=[
                    DecompositionRule(
                        r".*brother(.*)",
                        [
                            "Tell me more about your brother.",
                            "How do you get along with your brother?",
                            "Does your brother influence you?"
                        ]
                    )
                ]
            ),

            # ------------------------------------------------
            # Emotional states
            # ------------------------------------------------

            KeywordRule(
                keyword="unhappy",
                priority=80,
                decompositions=[
                    DecompositionRule(
                        r".*unhappy(.*)",
                        [
                            "Do you think coming here will help you not to feel unhappy?",
                            "Can you explain what makes you unhappy?",
                            "How long have you been feeling unhappy?"
                        ]
                    )
                ]
            ),

            KeywordRule(
                keyword="sad",
                priority=80,
                decompositions=[
                    DecompositionRule(
                        r".*sad(.*)",
                        [
                            "I'm sorry to hear that you are sad.",
                            "What do you think is making you sad?",
                            "Do you often feel sad?"
                        ]
                    )
                ]
            ),

            KeywordRule(
                keyword="happy",
                priority=75,
                decompositions=[
                    DecompositionRule(
                        r".*happy(.*)",
                        [
                            "How have you been feeling happy?",
                            "What makes you happy?",
                            "Does being happy mean something special to you?"
                        ]
                    )
                ]
            ),

            KeywordRule(
                keyword="angry",
                priority=75,
                decompositions=[
                    DecompositionRule(
                        r".*angry(.*)",
                        [
                            "What makes you angry?",
                            "Do you often feel angry?",
                            "What do you think causes this anger?"
                        ]
                    )
                ]
            ),

            KeywordRule(
                keyword="afraid",
                priority=75,
                decompositions=[
                    DecompositionRule(
                        r".*afraid(.*)",
                        [
                            "What are you afraid of?",
                            "Does fear trouble you often?",
                            "Can you tell me more about this fear?"
                        ]
                    )
                ]
            ),

            KeywordRule(
                keyword="lonely",
                priority=75,
                decompositions=[
                    DecompositionRule(
                        r".*lonely(.*)",
                        [
                            "Do you often feel lonely?",
                            "What makes you feel lonely?",
                            "When do you usually feel lonely?"
                        ]
                    )
                ]
            ),

            KeywordRule(
                keyword="alone",
                priority=75,
                decompositions=[
                    DecompositionRule(
                        r".*alone(.*)",
                        [
                            "Do you enjoy being alone?",
                            "Do you feel lonely when you are alone?",
                            "How long have you felt this way?"
                        ]
                    )
                ]
            ),

            # ------------------------------------------------
            # Personal pronouns and relationships
            # ------------------------------------------------

            KeywordRule(
                keyword="i",
                priority=60,
                decompositions=[
                    DecompositionRule(
                        r"i need (.*)",
                        [
                            "Why do you need {0}?",
                            "Would it really help you to get {0}?",
                            "Are you sure you need {0}?"
                        ]
                    ),
                    DecompositionRule(
                        r"i feel (.*)",
                        [
                            "Tell me more about these feelings.",
                            "Do you often feel {0}?",
                            "What makes you feel {0}?"
                        ]
                    ),
                    DecompositionRule(
                        r"i am (.*)",
                        [
                            "How long have you been {0}?",
                            "Do you believe it is normal to be {0}?",
                            "What makes you think you are {0}?"
                        ]
                    ),
                    DecompositionRule(
                        r"i think (.*)",
                        [
                            "Do you really think {0}?",
                            "But you are not sure {0}?",
                            "What makes you think {0}?"
                        ]
                    ),
                    DecompositionRule(
                        r"i want (.*)",
                        [
                            "What would it mean if you got {0}?",
                            "Why do you want {0}?",
                            "Suppose you got {0} soon."
                        ]
                    ),
                    DecompositionRule(
                        r"i can't (.*)",
                        [
                            "How do you know you can't {0}?",
                            "Have you tried?",
                            "Perhaps you could {0} now."
                        ]
                    ),
                    DecompositionRule(
                        r"i (.*)",
                        [
                            "Why do you say that you {0}?",
                            "Can you explain why you {0}?",
                            "Do you believe it is normal to {0}?"
                        ]
                    )
                ]
            ),

            KeywordRule(
                keyword="you",
                priority=55,
                decompositions=[
                    DecompositionRule(
                        r".*you are (.*)",
                        [
                            "What makes you think I am {0}?",
                            "Does it please you to believe I am {0}?",
                            "Perhaps you would like me to be {0}?"
                        ]
                    ),
                    DecompositionRule(
                        r".*you (.*)",
                        [
                            "We were discussing you, not me.",
                            "Why do you think I {0}?",
                            "Does that question interest you?"
                        ]
                    )
                ]
            ),

            KeywordRule(
                keyword="my",
                priority=50,
                decompositions=[
                    DecompositionRule(
                        r".*my (.*)",
                        [
                            "Tell me more about your {0}.",
                            "Why do you say your {0}?",
                            "Does your {0} trouble you?"
                        ]
                    )
                ]
            ),

            # ------------------------------------------------
            # Verbs and topics
            # ------------------------------------------------

            KeywordRule(
                keyword="want",
                priority=45,
                decompositions=[
                    DecompositionRule(
                        r".*want (.*)",
                        [
                            "What would it mean to you if you got {0}?",
                            "Why do you want {0}?",
                            "What would happen if you got {0}?"
                        ]
                    )
                ]
            ),

            KeywordRule(
                keyword="need",
                priority=45,
                decompositions=[
                    DecompositionRule(
                        r".*need (.*)",
                        [
                            "Why do you need {0}?",
                            "Would getting {0} really help you?",
                            "What makes you need {0}?"
                        ]
                    )
                ]
            ),

            KeywordRule(
                keyword="because",
                priority=40,
                decompositions=[
                    DecompositionRule(
                        r".*because (.*)",
                        [
                            "Is that the real reason?",
                            "What other reasons might there be?",
                            "Does that reason explain anything else?"
                        ]
                    )
                ]
            ),

            KeywordRule(
                keyword="always",
                priority=35,
                decompositions=[
                    DecompositionRule(
                        r".*always(.*)",
                        [
                            "Can you think of a specific example?",
                            "When exactly?",
                            "What incident are you thinking of?"
                        ]
                    )
                ]
            ),

            KeywordRule(
                keyword="everyone",
                priority=35,
                decompositions=[
                    DecompositionRule(
                        r".*everyone(.*)",
                        [
                            "Really, everyone?",
                            "Can you think of anyone in particular?",
                            "Who, for example?"
                        ]
                    )
                ]
            ),

            KeywordRule(
                keyword="no",
                priority=30,
                decompositions=[
                    DecompositionRule(
                        r".*",
                        [
                            "Why not?",
                            "Are you saying no just to be negative?",
                            "You are being a bit negative."
                        ]
                    )
                ]
            ),

            KeywordRule(
                keyword="yes",
                priority=25,
                decompositions=[
                    DecompositionRule(
                        r".*",
                        [
                            "You seem quite positive.",
                            "Are you sure?",
                            "I see."
                        ]
                    )
                ]
            ),

            KeywordRule(
                keyword="computer",
                priority=20,
                decompositions=[
                    DecompositionRule(
                        r".*computer(.*)",
                        [
                            "Do computers worry you?",
                            "What do you think about machines?",
                            "Why do you mention computers?"
                        ]
                    )
                ]
            ),

            KeywordRule(
                keyword="dreams",
                priority=20,
                decompositions=[
                    DecompositionRule(
                        r".*dreams(.*)",
                        [
                            "What do your dreams suggest to you?",
                            "Do you dream often?",
                            "What is your favorite dream?"
                        ]
                    )
                ]
            ),

            KeywordRule(
                keyword="hello",
                priority=10,
                decompositions=[
                    DecompositionRule(
                        r".*",
                        [
                            "Hello. How are you feeling today?",
                            "Hello. What would you like to discuss?"
                        ]
                    )
                ]
            ),

            KeywordRule(
                keyword="hi",
                priority=10,
                decompositions=[
                    DecompositionRule(
                        r".*",
                        [
                            "Hello. How are you?",
                            "Hi. Please tell me what is on your mind."
                        ]
                    )
                ]
            )
        ]

    # ========================================================
    # 4. TEXT NORMALIZATION
    # ========================================================

    @staticmethod
    def normalize(text: str) -> str:
        """
        Normalize input while preserving apostrophes.
        """
        text = text.lower().strip()

        text = re.sub(r"[^\w\s']", " ", text)

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    # ========================================================
    # 5. KEYWORD DETECTION
    # ========================================================

    def detect_keywords(self, text: str) -> list[KeywordRule]:
        """
        Find keywords as independent words.
        """
        normalized = self.normalize(text)

        detected = []

        for rule in self.rules:

            pattern = (
                r"(?<!\w)" +
                re.escape(rule.keyword) +
                r"(?!\w)"
            )

            if re.search(pattern, normalized):
                detected.append(rule)

        return sorted(
            detected,
            key=lambda rule: rule.priority,
            reverse=True
        )

    # ========================================================
    # 6. PRONOUN TRANSFORMATION
    # ========================================================

    def reflect(self, text: str) -> str:
        """
        Transform pronouns from the user's perspective
        to ELIZA's conversational perspective.
        """

        def replace(match: re.Match) -> str:
            word = match.group(0).lower()

            replacement = self.reflections.get(
                word,
                word
            )

            if word.istitle():
                replacement = replacement.capitalize()

            return replacement

        return self.reflection_pattern.sub(
            replace,
            text
        )

    # ========================================================
    # 7. PATTERN MATCHING
    # ========================================================

    def match_decomposition(
        self,
        text: str,
        rule: DecompositionRule
    ) -> Optional[re.Match]:

        pattern = re.compile(
            rule.pattern,
            re.IGNORECASE
        )

        return pattern.match(text)

    # ========================================================
    # 8. RESPONSE REASSEMBLY
    # ========================================================

    def reassemble(
        self,
        template: str,
        match: re.Match
    ) -> str:

        groups = []

        for group in match.groups():
            if group:
                groups.append(
                    self.reflect(group.strip())
                )
            else:
                groups.append("")

        try:
            response = template.format(*groups)

        except (IndexError, KeyError, ValueError):
            response = template

        response = re.sub(
            r"\s+",
            " ",
            response
        ).strip()

        return response

    # ========================================================
    # 9. MEMORY SYSTEM
    # ========================================================

    def remember(self, text: str) -> None:
        """
        Store selected user statements for later use.
        """
        normalized = self.normalize(text)

        if len(normalized.split()) < 3:
            return

        self.memory.append(text)

        if len(self.memory) > 10:
            self.memory.pop(0)

    def recall(self) -> Optional[str]:

        if not self.memory:
            return None

        statement = self.rng.choice(self.memory)

        return (
            "Earlier you said that " +
            statement +
            ". Why do you mention that now?"
        )

    # ========================================================
    # 10. MAIN RESPONSE GENERATION
    # ========================================================

    def respond(self, user_input: str) -> str:

        original = user_input.strip()

        if not original:
            return self.rng.choice(
                self.empty_responses
            )

        normalized = self.normalize(original)

        if normalized in self.quit_commands:
            return (
                "Goodbye. It was nice talking to you."
            )

        # Repetition detection
        if (
            self.previous_input is not None
            and normalized == self.previous_input
        ):
            response = self.rng.choice(
                self.repetition_responses
            )

            self.history.append(
                (original, response)
            )

            return response

        self.previous_input = normalized

        self.remember(original)

        # Detect keywords by priority.
        detected_rules = self.detect_keywords(
            normalized
        )

        for keyword_rule in detected_rules:

            for decomposition in keyword_rule.decompositions:

                match = self.match_decomposition(
                    normalized,
                    decomposition
                )

                if not match:
                    continue

                template = self.rng.choice(
                    decomposition.responses
                )

                response = self.reassemble(
                    template,
                    match
                )

                self.previous_topic = (
                    keyword_rule.keyword
                )

                self.history.append(
                    (original, response)
                )

                return response

        # Occasionally recall previous statements.
        if self.memory and self.rng.random() < 0.12:

            response = self.recall()

            if response:
                self.history.append(
                    (original, response)
                )

                return response

        # Generic fallback.
        response = self.rng.choice(
            self.fallback_responses
        )

        self.history.append(
            (original, response)
        )

        return response

    # ========================================================
    # 11. CONVERSATION HISTORY
    # ========================================================

    def show_history(self) -> None:

        if not self.history:
            print("\nNo conversation history yet.\n")
            return

        print("\n" + "=" * 55)
        print("CONVERSATION HISTORY")
        print("=" * 55)

        for index, (user, bot) in enumerate(
            self.history,
            start=1
        ):

            print(f"\n[{index}] You: {user}")
            print(f"    ELIZA: {bot}")

        print("\n" + "=" * 55 + "\n")

    def clear_history(self) -> None:

        self.history.clear()
        self.memory.clear()
        self.previous_input = None
        self.previous_topic = None

        print("\nConversation history cleared.\n")


# ============================================================
# 12. TERMINAL INTERFACE
# ============================================================

def print_banner() -> None:

    banner = """
    ====================================================
                     E L I Z A
           Python Recreation of the 1966 Chatbot
    ====================================================

       Inspired by Joseph Weizenbaum's ELIZA (1966)

       Script: DOCTOR-inspired
       Engine: Pattern Matching + Rule-Based Responses

       Commands:
           quit      - Exit conversation
           history   - Show conversation history
           clear     - Clear conversation history
           help      - Show available commands

    ====================================================
    """

    print(textwrap.dedent(banner))


def main() -> None:

    print_banner()

    eliza = ELIZA()

    print("ELIZA: Hello. How are you feeling today?\n")

    while True:

        try:

            user_input = input("You: ").strip()

            if not user_input:
                print(
                    "ELIZA:",
                    eliza.respond("")
                )
                continue

            command = user_input.lower()

            if command == "help":

                print(
                    "\nAvailable commands:\n"
                    "  quit     - Exit\n"
                    "  history  - Show conversation history\n"
                    "  clear    - Clear history\n"
                    "  help     - Show help\n"
                )

                continue

            if command == "history":

                eliza.show_history()

                continue

            if command == "clear":

                eliza.clear_history()

                continue

            response = eliza.respond(
                user_input
            )

            print(f"\nELIZA: {response}\n")

            if command in eliza.quit_commands:

                break

        except KeyboardInterrupt:

            print(
                "\n\nELIZA: Goodbye. It was nice talking to you."
            )

            break

        except EOFError:

            print(
                "\nELIZA: Goodbye."
            )

            break


# ============================================================
# 13. ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
