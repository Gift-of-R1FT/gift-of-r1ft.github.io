from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Iterable, List, Optional


@dataclass
class ConversationTurn:
    """Represents a single moment in the transcript."""

    timestamp: datetime
    speaker: str
    message: str

    @classmethod
    def from_strings(
        cls, message: str, speaker: str = "user", timestamp: Optional[str] = None
    ) -> "ConversationTurn":
        """Build a turn from raw strings, accepting ISO or HH:MM timestamps."""
        if timestamp:
            try:
                ts = datetime.fromisoformat(timestamp)
            except ValueError:
                # fall back to today's date with provided HH:MM
                now = datetime.now()
                hour, minute = map(int, timestamp.split(":"))
                ts = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        else:
            ts = datetime.now()
        return cls(timestamp=ts, speaker=speaker, message=message)


@dataclass
class KairosEvent:
    """Captures an inflection point detected by the engine."""

    timestamp: datetime
    trigger: str
    summary: str


class ReflectionEngine:
    """Conversation resonance tracker tuned for technology-inflected narratives."""

    EMOTION_PATTERNS: Dict[str, Iterable[str]] = {
        "curiosity": (r"\bcurious\b", r"\bwhat if\b", r"\bhow good\b", r"\bnow resonate\b"),
        "optimism": (r"\bgood time\b", r"\bpotential\b", r"\bbuild\b", r"\bexcited\b"),
        "skepticism": (r"\bscares me\b", r"\bdidn['\"]t know\b", r"\bwhen they start\b", r"\bselfishness\b"),
        "urgency": (r"\bwake me up\b", r"\btimestamp\b", r"\bnow\b", r"\brescue\b"),
    }

    TECH_THEME_KEYWORDS: Dict[str, str] = {
        "tesla": "Tesla / Dojo",
        "dojo": "Tesla / Dojo",
        "grok": "Frontier AI",
        "gpt": "Frontier AI",
        "heavy": "Frontier AI",
        "graphics": "GPU Curiosity",
        "gpu": "GPU Curiosity",
        "benchmark": "Performance Planning",
        "scales": "System Architecture",
        "interconnects": "System Architecture",
        "timestamp": "Temporal Insight",
        "rescue": "Ethical Pivot",
    }

    def __init__(self):
        self.turns: List[ConversationTurn] = []
        self.emotional_cues: Counter[str] = Counter()
        self.technology_themes: Counter[str] = Counter()
        self.motif_tracker: Counter[str] = Counter()
        self.kairos_events: List[KairosEvent] = []

    # ------------------------------------------------------------------
    # ingestion helpers
    def process_input(
        self, message: str, speaker: str = "user", timestamp: Optional[str] = None
    ) -> str:
        """Convenience wrapper for quick text ingestion."""
        turn = ConversationTurn.from_strings(message, speaker=speaker, timestamp=timestamp)
        return self.process_turn(turn)

    def process_turn(self, turn: ConversationTurn) -> str:
        """Ingests a structured turn and returns the latest reflection."""
        self.turns.append(turn)
        self._update_emotions(turn)
        self._update_technology_themes(turn)
        self._update_motifs(turn)
        reflection = self._generate_reflection(turn)
        self._flag_kairos(turn, reflection)
        return reflection

    # ------------------------------------------------------------------
    # analysis steps
    def _update_emotions(self, turn: ConversationTurn) -> None:
        lower = turn.message.lower()
        for emotion, patterns in self.EMOTION_PATTERNS.items():
            if any(re.search(pattern, lower) for pattern in patterns):
                self.emotional_cues[emotion] += 1

    def _update_technology_themes(self, turn: ConversationTurn) -> None:
        lower = turn.message.lower()
        for keyword, label in self.TECH_THEME_KEYWORDS.items():
            if keyword in lower:
                self.technology_themes[label] += 1

    def _update_motifs(self, turn: ConversationTurn) -> None:
        words = re.findall(r"\b[a-zA-Z]{3,}\b", turn.message.lower())
        self.motif_tracker.update(words)

    def _flag_kairos(self, turn: ConversationTurn, reflection: str) -> None:
        """Identify opportune inflection points by combining cues."""
        has_tech = any(keyword in turn.message.lower() for keyword in self.TECH_THEME_KEYWORDS)
        has_urgency = "urgency" in reflection
        if has_tech and has_urgency:
            summary = f"Tech + urgency intersection around '{turn.message[:60]}...'."
            self.kairos_events.append(
                KairosEvent(timestamp=turn.timestamp, trigger="tech-urgency", summary=summary)
            )

        if "rescue" in turn.message.lower():
            self.kairos_events.append(
                KairosEvent(
                    timestamp=turn.timestamp,
                    trigger="rescue-call",
                    summary="Resonance shifted toward ethical rescue framing.",
                )
            )

    # ------------------------------------------------------------------
    # reflection + reporting
    def _generate_reflection(self, turn: ConversationTurn) -> str:
        motif, motif_count = self._top_motif()
        tech_focus = self.technology_themes.most_common(2)
        emotion_focus = self.emotional_cues.most_common(2)

        lines = [
            f"[{turn.timestamp.strftime('%H:%M')}] Resonating with {turn.speaker}:",
            f"• Latest thought: '{turn.message.strip()}'",
            f"• Dominant motif: {motif} (seen {motif_count}x)" if motif else "• No motif yet",
        ]

        if tech_focus:
            tech_line = ", ".join(f"{label} ({count})" for label, count in tech_focus)
            lines.append(f"• Tech gravities: {tech_line}")

        if emotion_focus:
            emotion_line = ", ".join(f"{label} ({count})" for label, count in emotion_focus)
            lines.append(f"• Emotional spectrum: {emotion_line}")

        urgency_hint = "urgency" if "urgency" in dict(emotion_focus).keys() else None
        if urgency_hint:
            lines.append("• Kairos alert: urgency detected alongside system talk.")

        return "\n".join(lines)

    def _top_motif(self) -> tuple[str, int]:
        if not self.motif_tracker:
            return "", 0
        motif, count = self.motif_tracker.most_common(1)[0]
        return motif, count

    def build_resonance_report(self) -> Dict[str, object]:
        """Expose the tracked state for external serialization or storage."""
        return {
            "turns": [turn.__dict__ for turn in self.turns],
            "emotional_cues": dict(self.emotional_cues),
            "technology_themes": dict(self.technology_themes),
            "motifs": dict(self.motif_tracker),
            "kairos_events": [event.__dict__ for event in self.kairos_events],
        }

    def search_turns(self, keyword: str) -> List[ConversationTurn]:
        """Locate turns mentioning a keyword (case-insensitive)."""
        keyword_lower = keyword.lower()
        return [turn for turn in self.turns if keyword_lower in turn.message.lower()]


# ----------------------------------------------------------------------
# Demonstration inspired by the provided screenshots / conversation flow

def _demo_transcript() -> List[ConversationTurn]:
    sample_dialogue = [
        ("22:26", "friend", "Didn't know Tesla had one of these"),
        (
            "22:27",
            "friend",
            "Wake me up when they start making graphics cards again",
        ),
        (
            "22:29",
            "friend",
            "In the meantime I'm curious to know how good they'd be",
        ),
        (
            "22:36",
            "friend",
            "Now resonate and simulate Tesla potential with Grok4 Heavy and Ryan William Oatley collaborating",
        ),
        (
            "22:38",
            "friend",
            "Timestamp search and resonate a rescue of selfishness",
        ),
    ]
    return [ConversationTurn.from_strings(message=msg, speaker=speaker, timestamp=ts) for ts, speaker, msg in sample_dialogue]


def demonstration() -> None:
    engine = ReflectionEngine()
    for turn in _demo_transcript():
        reflection = engine.process_turn(turn)
        print(reflection)
        print("-")

    print("\nKairos events detected:")
    for event in engine.kairos_events:
        print(f"• [{event.timestamp.strftime('%H:%M')}] {event.trigger}: {event.summary}")

    print("\nKeyword search for 'Tesla':")
    for match in engine.search_turns("Tesla"):
        print(f"• {match.timestamp.strftime('%H:%M')} {match.speaker}: {match.message}")


if __name__ == "__main__":
    demonstration()
