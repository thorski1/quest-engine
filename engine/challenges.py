"""
challenges.py - Challenge runner for Terminal Quest
Handles quiz, flag_quiz, fill_blank, and live challenge types.
"""

import os
import re
import shutil
import subprocess
import tempfile
import uuid
from pathlib import Path
from typing import Any

SANDBOX_BASE = Path(tempfile.gettempdir())
SANDBOX_TIMEOUT = 15  # seconds


class ChallengeResult:
    def __init__(self, success: bool, message: str = "", output: str = ""):
        self.success = success
        self.message = message
        self.output = output

    def __bool__(self):
        return self.success


class ChallengeRunner:
    def __init__(self):
        self._current_sandbox: Path | None = None

    # ── Sandbox Management ────────────────────────────────────────────────────

    def setup_sandbox(self, setup: dict) -> Path:
        """Create and populate a fresh sandbox directory."""
        sandbox = SANDBOX_BASE / f"tq_sandbox_{uuid.uuid4().hex[:8]}"
        sandbox.mkdir(parents=True, exist_ok=True)

        # Create directories first
        for d in setup.get("dirs", []):
            (sandbox / d).mkdir(parents=True, exist_ok=True)

        # Populate files
        for filepath, content in setup.get("files", {}).items():
            full_path = sandbox / filepath
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content)

        self._current_sandbox = sandbox
        return sandbox

    def cleanup_sandbox(self, sandbox: Path):
        """Remove sandbox directory."""
        try:
            if sandbox and sandbox.exists():
                shutil.rmtree(sandbox, ignore_errors=True)
        except Exception:
            pass

    # ── Command Execution ─────────────────────────────────────────────────────

    def run_command(self, cmd: str, cwd: Path) -> tuple[bool, str, str]:
        """
        Run a shell command in cwd.
        Returns (success, stdout, stderr).
        """
        try:
            result = subprocess.run(
                ["bash", "-c", cmd],
                cwd=str(cwd),
                capture_output=True,
                text=True,
                timeout=SANDBOX_TIMEOUT,
                env={**os.environ, "HOME": str(Path.home()), "TERM": "dumb"},
            )
            return (result.returncode == 0, result.stdout, result.stderr)
        except subprocess.TimeoutExpired:
            return (False, "", "Command timed out after 15 seconds.")
        except Exception as e:
            return (False, "", str(e))

    # ── Validation ────────────────────────────────────────────────────────────

    def validate(self, validation: dict, sandbox: Path, stdout: str, stderr: str) -> ChallengeResult:
        vtype = validation.get("type")

        if vtype == "dir_exists":
            target = sandbox / validation["target"]
            if target.is_dir():
                return ChallengeResult(True, f"Directory '{validation['target']}' exists!")
            return ChallengeResult(False, f"Directory '{validation['target']}' was not found.")

        elif vtype == "file_exists":
            target = sandbox / validation["target"]
            if target.is_file():
                return ChallengeResult(True, f"File '{validation['target']}' exists!")
            return ChallengeResult(False, f"File '{validation['target']}' was not found.")

        elif vtype == "file_missing":
            target = sandbox / validation["target"]
            if not target.exists():
                return ChallengeResult(True, f"File '{validation['target']}' was successfully removed!")
            return ChallengeResult(False, f"File '{validation['target']}' still exists.")

        elif vtype == "output_contains":
            expected = validation["expected"]
            combined = stdout + stderr
            if expected in combined:
                return ChallengeResult(True, f"Output contains '{expected}'!")
            return ChallengeResult(
                False,
                f"Expected output to contain: '{expected}'\nActual output: {combined[:200] or '(empty)'}",
                combined,
            )

        elif vtype == "file_contains":
            target = sandbox / validation["target"]
            expected = validation["expected"]
            if target.is_file():
                content = target.read_text()
                if expected in content:
                    return ChallengeResult(True, f"File contains '{expected}'!")
                return ChallengeResult(
                    False, f"File '{validation['target']}' exists but doesn't contain '{expected}'.\nContent: {content[:200]}"
                )
            return ChallengeResult(False, f"File '{validation['target']}' does not exist.")

        elif vtype == "file_executable":
            target = sandbox / validation["target"]
            if target.is_file() and os.access(str(target), os.X_OK):
                return ChallengeResult(True, f"File '{validation['target']}' is executable!")
            return ChallengeResult(False, f"File '{validation['target']}' is not executable (or doesn't exist).")

        elif vtype == "file_perms":
            target = sandbox / validation["target"]
            if not target.exists():
                return ChallengeResult(False, f"File '{validation['target']}' does not exist.")
            actual_mode = oct(target.stat().st_mode)[-3:]
            expected_mode = validation["expected_mode"]
            if actual_mode == expected_mode:
                return ChallengeResult(True, f"Permissions are {expected_mode}!")
            return ChallengeResult(
                False, f"Expected permissions {expected_mode}, got {actual_mode}."
            )

        elif vtype == "multi":
            for check in validation.get("checks", []):
                result = self.validate(check, sandbox, stdout, stderr)
                if not result.success:
                    return ChallengeResult(False, f"Check failed: {result.message}")
            return ChallengeResult(True, "All checks passed!")

        else:
            return ChallengeResult(False, f"Unknown validation type: {vtype}")

    # ── Challenge Types ───────────────────────────────────────────────────────

    def run_quiz(self, challenge: dict, user_answer: str) -> ChallengeResult:
        """Validate text answer for quiz/flag_quiz/fill_blank challenges.

        Supports three answer formats:
          1. answer + options: multiple-choice (user types A/B/C/D or the option text)
          2. answer only:      single string match (fill-in-the-blank)
          3. answers list:     free-text multi-answer (nexus format)
        """
        user_clean = user_answer.strip().lower()

        # ── Multiple-choice: answer letter + options list ──────────────────────
        answer = challenge.get("answer")
        options = challenge.get("options", [])
        if answer is not None and options:
            answer_lower = str(answer).lower()
            correct_idx = ord(answer_lower) - ord("a")
            correct_text = options[correct_idx].lower() if 0 <= correct_idx < len(options) else ""
            if user_clean == answer_lower or (correct_text and user_clean == correct_text):
                return ChallengeResult(True, "Correct!")
            # Also accept 1-based numeric input
            try:
                if int(user_clean) - 1 == correct_idx:
                    return ChallengeResult(True, "Correct!")
            except ValueError:
                pass
            correct_option = options[correct_idx] if 0 <= correct_idx < len(options) else str(answer)
            return ChallengeResult(False, f"Not quite! The answer was {answer_lower.upper()}: {correct_option}")

        # ── Single-string fill-blank: answer only, no options ──────────────────
        if answer is not None:
            if user_clean == str(answer).lower():
                return ChallengeResult(True, "Correct!")
            return ChallengeResult(False, f"Not quite. The answer was: {answer}")

        # ── Free-text multi-answer (nexus format): answers list ────────────────
        valid_answers = [a.lower() for a in challenge.get("answers", [])]
        if not valid_answers:
            return ChallengeResult(False, "No valid answers configured for this challenge.")

        if user_clean in valid_answers:
            return ChallengeResult(True, "Correct!")

        # Strip leading dashes for flag quizzes
        user_stripped = user_clean.lstrip("-")
        for ans in valid_answers:
            if ans.lstrip("-") == user_stripped:
                return ChallengeResult(True, "Correct! (with or without the dash prefix)")

        # Substring match (e.g. "ls -la" contains "-la")
        for ans in valid_answers:
            if ans in user_clean:
                return ChallengeResult(True, f"Correct! (contains '{ans}')")

        return ChallengeResult(
            False,
            f"Not quite. Valid answers include: {', '.join(challenge.get('answers', []))}",
        )

    def run_fill_blank(self, challenge: dict, user_answer: str) -> ChallengeResult:
        """Validate fill-in-the-blank answers."""
        return self.run_quiz(challenge, user_answer)

    def run_live(self, challenge: dict, user_cmd: str) -> tuple[ChallengeResult, str]:
        """
        Run a live command in sandbox and validate.
        Returns (result, output_text)
        """
        setup = challenge.get("setup", {})
        sandbox = self.setup_sandbox(setup)
        try:
            ok, stdout, stderr = self.run_command(user_cmd, sandbox)
            combined_output = stdout + (f"\n[stderr]: {stderr}" if stderr.strip() else "")

            if not ok and stderr.strip() and not stdout.strip():
                # Command failed entirely
                result = ChallengeResult(
                    False,
                    f"Command returned an error:\n{stderr.strip()}",
                    combined_output,
                )
            else:
                validation = challenge.get("validation", {})
                result = self.validate(validation, sandbox, stdout, stderr)
                result.output = combined_output

            return result, combined_output
        finally:
            self.cleanup_sandbox(sandbox)

    def run_challenge(self, challenge: dict, user_input: str) -> tuple[ChallengeResult, str]:
        """Dispatch to the correct runner based on challenge type."""
        ctype = challenge.get("type", "quiz")
        output = ""

        if ctype in ("quiz", "flag_quiz"):
            result = self.run_quiz(challenge, user_input)
        elif ctype == "fill_blank":
            result = self.run_fill_blank(challenge, user_input)
        elif ctype == "live":
            result, output = self.run_live(challenge, user_input)
        else:
            result = ChallengeResult(False, f"Unknown challenge type: {ctype}")

        return result, output

    def get_hint(self, challenge: dict, hint_index: int) -> str:
        """Return the hint at the given index."""
        hints = challenge.get("hints", [])
        if not hints:
            return "No hints available for this challenge."
        idx = min(hint_index, len(hints) - 1)
        return hints[idx]
