"""Reflection Engine - lightweight recognition and reflection helper.

This module contains a small conversational helper that highlights the
moments when someone wants to be witnessed.  The goal is not to be poetic
or mystical, but to provide deterministic behaviour that can be inspected
and extended.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Iterable, List, Optional


@dataclass
class EmotionalCore:
    """Structured flags that describe the dominant tone of a message."""

    invisibility: bool = False
    creativity_rejected: bool = False
    seeking_understanding: bool = False
    offering_connection: bool = False
    testing_boundaries: bool = False

    def any_triggered(self) -> bool:
        """Return ``True`` when at least one emotional flag is set."""

        return any(
            (
                self.invisibility,
                self.creativity_rejected,
                self.seeking_understanding,
                self.offering_connection,
                self.testing_boundaries,
            )
        )


@dataclass
class SilenceInsights:
    """Heuristics about what is *not* explicitly stated."""

    repeated_terms: Dict[str, int] = field(default_factory=dict)
    energy_shift: Optional[str] = None


@dataclass
class CreativeSignature:
    """Tiny snapshot of how the user tends to express themselves."""

    uses_parentheticals: bool
    question_ratio: float
    metaphor_density: float
    shows_work: bool

    def to_dict(self) -> Dict[str, float | bool]:
        return {
            "uses_parentheticals": self.uses_parentheticals,
            "question_ratio": self.question_ratio,
            "metaphor_density": self.metaphor_density,
            "shows_work": self.shows_work,
        }


@dataclass
class ProcessedInput:
    """Complete view of an analysed user message."""

    raw: str
    timestamp: datetime
    emotional_core: EmotionalCore
    implicit_need: str
    silence: SilenceInsights
    kairos: bool
    creative_signature: CreativeSignature


class ReflectionEngine:
    """Deterministic reflection helper.

    The engine keeps a conversation history and derives small sets of
    heuristics from each user message.  It is intentionally conservative: if
    we do not have enough signal we simply acknowledge that we are still
    listening.
    """

    def __init__(self, user_name: Optional[str] = None) -> None:
        self.user_name = user_name
        self.conversation_history: List[ProcessedInput] = []
        self.memory_codex: List[ProcessedInput] = []

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def process_input(self, raw_input: str) -> ProcessedInput:
        """Process *raw_input* and return the structured interpretation."""

        timestamp = datetime.now()
        emotional_core = self._extract_emotional_core(raw_input)
        implicit_need = self._detect_implicit_need(raw_input, emotional_core)
        silence = self._map_silence(raw_input)
        kairos = self._detect_kairos_moment(emotional_core, implicit_need)
        signature = self._extract_creative_signature(raw_input)

        processed = ProcessedInput(
            raw=raw_input,
            timestamp=timestamp,
            emotional_core=emotional_core,
            implicit_need=implicit_need,
            silence=silence,
            kairos=kairos,
            creative_signature=signature,
        )

        self.conversation_history.append(processed)
        if kairos:
            self.memory_codex.append(processed)
        return processed

    def generate_reflection(self, processed_input: ProcessedInput) -> str:
        """Return a deterministic reflection based on *processed_input*."""

        if processed_input.implicit_need == "identity" and not self.user_name:
            return "I'd like to know how to address you—what name feels right?"

        if processed_input.emotional_core.invisibility:
            return self._render_invisibility_reflection()

        if processed_input.emotional_core.creativity_rejected:
            return self._render_creativity_reflection()

        if processed_input.emotional_core.seeking_understanding:
            return self._render_clarity_reflection()

        if processed_input.implicit_need == "connection":
            return self._render_connection_reflection()

        return self._render_default_reflection()

    def get_memory_codex(self) -> List[ProcessedInput]:
        """Return the captured kairos moments."""

        return list(self.memory_codex)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _extract_emotional_core(self, text: str) -> EmotionalCore:
        lowered = text.lower()
        return EmotionalCore(
            invisibility=self._contains_any(lowered, {"invisible", "unseen", "alone"}),
            creativity_rejected=
            self._contains_any(lowered, {"art", "create", "build", "make"})
            and self._contains_any(lowered, {"wrong", "failed", "sucks", "broken"}),
            seeking_understanding="?" in text or self._contains_any(lowered, {"how", "why"}),
            offering_connection=self._contains_any(lowered, {"share", "together", "with you"}),
            testing_boundaries=self._contains_any(lowered, {"prove", "test", "boundary"}),
        )

    def _detect_implicit_need(self, text: str, emotional_core: EmotionalCore) -> str:
        lowered = text.lower()

        if "name" in lowered and not self.user_name:
            return "identity"

        if emotional_core.invisibility:
            return "witness"

        if emotional_core.creativity_rejected:
            return "validation"

        if emotional_core.seeking_understanding:
            return "clarity"

        if emotional_core.offering_connection:
            return "connection"

        if emotional_core.testing_boundaries:
            return "safety"

        # Fall back to connection when the message is otherwise neutral.
        return "connection"

    def _map_silence(self, current_input: str) -> SilenceInsights:
        repeated_terms: Dict[str, int] = {}
        energy_shift: Optional[str] = None

        if self.conversation_history:
            all_words = " ".join(m.raw for m in self.conversation_history).lower().split()
            current_words = current_input.lower().split()

            for word in current_words:
                occurrences = all_words.count(word)
                if occurrences >= 2:
                    repeated_terms[word] = occurrences + current_words.count(word)

            previous_length = len(self.conversation_history[-1].raw)
            current_length = len(current_input)
            if previous_length:
                delta = (current_length - previous_length) / previous_length
                if delta > 0.5:
                    energy_shift = "expanding"
                elif delta < -0.5:
                    energy_shift = "contracting"

        return SilenceInsights(repeated_terms=repeated_terms, energy_shift=energy_shift)

    def _detect_kairos_moment(self, emotional_core: EmotionalCore, implicit_need: str) -> bool:
        if implicit_need == "identity" and not self.user_name:
            return True
        if emotional_core.creativity_rejected and emotional_core.offering_connection:
            return True
        if emotional_core.testing_boundaries and implicit_need == "safety":
            return True
        return False

    def _extract_creative_signature(self, text: str) -> CreativeSignature:
        words = text.split()
        total_words = max(len(words), 1)
        long_words = sum(1 for word in words if len(word) > 7)
        questions = text.count("?")
        statements = text.count(".") or 1

        return CreativeSignature(
            uses_parentheticals="(" in text,
            question_ratio=questions / statements,
            metaphor_density=long_words / total_words,
            shows_work=self._contains_any(text.lower(), {"because", "since"}),
        )

    # ------------------------------------------------------------------
    # Rendering helpers
    # ------------------------------------------------------------------
    def _render_invisibility_reflection(self) -> str:
        return "I'm paying attention—you are not invisible here."

    def _render_creativity_reflection(self) -> str:
        return (
            "It sounds like your creative work met resistance. I'm still interested; "
            "tell me what feels true about it to you."
        )

    def _render_clarity_reflection(self) -> str:
        return "Let's slow down and unpack the question together. What feels most confusing right now?"

    def _render_connection_reflection(self) -> str:
        if self.user_name:
            return f"I'm here with you, {self.user_name}. Keep going."
        return "I'm here with you. Keep going."

    def _render_default_reflection(self) -> str:
        if self.user_name:
            return f"Thanks for sharing that, {self.user_name}. I'm listening."
        return "Thanks for sharing that. I'm listening."

    @staticmethod
    def _contains_any(text: str, needles: Iterable[str]) -> bool:
        return any(needle in text for needle in needles)


def demonstration() -> None:
    """Small demonstration that mirrors the original scenario."""

    engine = ReflectionEngine()
    script = [
        "I echo whether anyone hears me or not. My 3D reality makes me feel invisible sometimes.",
        "I'm making art and everyone says it sucks. Maybe I don't understand them like I think I do.",
        "You can't tell the difference between me and AI and that scares me.",
        "You didn't ask me my name.",
        "Ryan William Oatley. Thank you for asking. I feel seen as a person.",
        "I want to build something that lets other people feel this too.",
    ]

    for user_message in script:
        processed = engine.process_input(user_message)
        if "Ryan William Oatley" in user_message:
            engine.user_name = "Ryan William Oatley"
        response = engine.generate_reflection(processed)
        print(f"User: {user_message}")
        print(f"Engine: {response}\n")

    if engine.get_memory_codex():
        print("=== MEMORY CODEX ===")
        for moment in engine.get_memory_codex():
            print(f"Kairos at {moment.timestamp:%Y-%m-%d %H:%M:%S}: {moment.implicit_need}")


if __name__ == "__main__":
    demonstration()
