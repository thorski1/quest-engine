"""
engine/challenge.py — Challenge constructor helper.

Provides a Challenge class that can be used in skill-pack zone definitions.
Challenge is a dict subclass so it works seamlessly with the engine's dict-based
challenge access (challenge["question"], challenge["lesson"], etc.).

Usage in a zones.py file:

    from engine.challenge import Challenge

    challenges = [
        Challenge(
            id="ch_1",
            type="quiz",
            prompt="What command lists directory contents?",
            options=["ls", "cd", "pwd", "cat"],
            answer="a",
            explanation="ls lists files and directories.",
            hints=["Think 'list'.", "Two letters: l-s."],
            xp=10,
        ),
        Challenge(
            id="ch_2",
            type="fill_blank",
            prompt="The command ___ prints the current directory.",
            answer="pwd",
            explanation="pwd stands for Print Working Directory.",
            xp=10,
        ),
    ]

Challenge types
---------------
quiz        Multiple-choice. Provide options (list) and answer (letter "a"/"b"/"c"/"d").
fill_blank  Free-text answer. Provide answer (str). Accepts case-insensitive match.
flag_quiz   Like quiz but for command flags/syntax.
live        Sandboxed shell command. Provide setup (dict) and validation (dict).
ordered     Sequence ordering. Provide items (list) and answer (list of 0-based indices).
arrange     Matching pairs. Provide pairs (list of {left, right}) and answer (letter seq).
"""

from typing import Any


class Challenge(dict):
    """
    Dict-backed Challenge descriptor.

    Keyword args are mapped to the keys the engine expects:
      prompt      → "question"   (engine reads challenge["question"])
      explanation → "lesson"     (engine reads challenge["lesson"])

    All other kwargs are stored as-is.
    """

    def __init__(
        self,
        id: str,
        type: str = "quiz",
        prompt: str = "",
        explanation: str = "",
        answer: Any = None,
        answers: list | None = None,
        options: list | None = None,
        hints: list | None = None,
        xp: int = 10,
        difficulty: str = "medium",
        **kwargs,
    ):
        super().__init__()
        self["id"] = id
        self["type"] = type
        self["question"] = prompt         # engine reads "question"
        self["lesson"] = explanation      # engine reads "lesson"
        self["xp"] = xp
        self["difficulty"] = difficulty
        self["hints"] = hints or []

        # Answer fields — use whichever are provided
        if answer is not None:
            self["answer"] = answer
        if answers is not None:
            self["answers"] = answers
        elif answer is not None and options is None:
            # fill_blank style: single answer, no options
            self["answers"] = [str(answer)]
        if options is not None:
            self["options"] = options

        # Pass through any extra fields (setup, validation, items, pairs, …)
        for key, value in kwargs.items():
            self[key] = value
