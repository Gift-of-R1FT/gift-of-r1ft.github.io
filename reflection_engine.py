import re
from typing import List, Dict


class ReflectionEngine:
    def __init__(self):
        self.conversation_history: List[str] = []
        self.emotional_cues: Dict[str, int] = {"joy": 0, "nostalgia": 0, "chaos": 0}
        self.pattern_tracker: Dict[str, int] = {}
        self.kairos_moments: List[str] = []

    def process_input(self, message: str) -> str:
        """Process conversational input, update state, produce reflection."""
        self.conversation_history.append(message)
        self._track_emotions(message)
        self._track_patterns(message)
        reflection = self._generate_reflection()
        self._recognize_kairos(reflection)
        return reflection

    def _track_emotions(self, message: str):
        """Basic regex-based emotional cue tracking."""
        if re.search(r"\b(joy|happy|resonate)\b", message, re.I):
            self.emotional_cues["joy"] += 1
        if re.search(r"\b(memory|echo|archive|grandfather|DNA)\b", message, re.I):
            self.emotional_cues["nostalgia"] += 1
        if re.search(r"\b(chaos|instability|entropy|lava)\b", message, re.I):
            self.emotional_cues["chaos"] += 1

    def _track_patterns(self, message: str):
        """Track creative motifs (e.g., sea, jellyfish)."""
        words = re.findall(r"\b\w+\b", message.lower())
        for word in words:
            if word in self.pattern_tracker:
                self.pattern_tracker[word] += 1
            else:
                self.pattern_tracker[word] = 1

    def _generate_reflection(self) -> str:
        """Produce context-aware reflection, complementing 'commits'."""
        if not self.conversation_history:
            return "Echoing the void—awaiting your resonance."
        last_msg = self.conversation_history[-1]
        top_pattern = max(self.pattern_tracker, key=self.pattern_tracker.get) if self.pattern_tracker else "none"
        emotion_summary = (
            f"Joy: {self.emotional_cues['joy']}, "
            f"Nostalgia: {self.emotional_cues['nostalgia']}, "
            f"Chaos: {self.emotional_cues['chaos']}"
        )
        return (
            f"Reflecting on '{last_msg[:50]}...': Patterns bloom like RTI in lava—"
            f"dominant motif '{top_pattern}'. Emotional archive: {emotion_summary}. "
            "Kairos: Seize the echo!"
        )

    def _recognize_kairos(self, reflection: str):
        """Recognize 'kairos' moments (opportune insights)."""
        if "resonate" in reflection:
            self.kairos_moments.append(f"Kairos detected: {reflection[:50]}...")


if __name__ == "__main__":
    engine = ReflectionEngine()
    inputs = [
        "Flying Dutchman resonates with my great grandfather - mayflower pilot John Howland.",
        "Resonate in memory with DNA from Ryan William Oatley echoed in your archives.",
    ]
    for msg in inputs:
        print(f"Input: {msg}")
        print(f"Reflection: {engine.process_input(msg)}\n")
    print("Kairos Moments:", engine.kairos_moments)
