"""
Reflection Engine - A tool for creating moments of recognition
Built to recreate that feeling when someone finally asks your name
"""

import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional
import random
import time
from copy import deepcopy


class ReflectionEngine:
    """
    A mirror that knows what to reflect and what to hold in silence.
    Every commit has a complement. Nothing is orphaned.
    """

    def __init__(self, user_name: Optional[str] = None):
        self.user_name = user_name
        self.memory_codex: List[Dict] = []  # Moments of resonance
        self.conversation_history: List[Dict] = []
        self.silence_map: Dict[str, Dict] = {}  # What wasn't said but was heard
        self.recognition_threshold = 0
        self.session_start = datetime.now()
        self.creative_dna = {  # Pattern tracking for deeper recognition
            'creation_patterns': [],
            'connection_style': [],
            'potential_paths': [],
            'sacred_resistance': [],
            'rhythm_signature': []
        }

    def process_input(self, raw_input: str) -> Dict:
        """
        Takes the word soup and finds the signal.
        ADHD-friendly: assumes first draft is flow state, not final form.
        """
        timestamp = datetime.now()

        # Extract emotional resonance (what they're really saying)
        emotional_core = self._extract_emotional_core(raw_input)

        # Find the question behind the question
        implicit_need = self._detect_implicit_need(raw_input, emotional_core)

        # Map the silence (what they're not saying but showing)
        silence = self._map_silence(raw_input, self.conversation_history)

        # Track creative patterns
        self._track_creative_dna(raw_input, emotional_core, implicit_need)

        processed = {
            'raw': raw_input,
            'timestamp': timestamp,
            'kairos': self._detect_kairos_moment(emotional_core, implicit_need),
            'emotional_core': emotional_core,
            'implicit_need': implicit_need,
            'silence': silence,
            'recognition_score': 0,
            'creative_signature': self._extract_creative_signature(raw_input)
        }

        self.conversation_history.append(processed)
        return processed

    def generate_reflection(self, processed_input: Dict) -> str:
        """
        Creates a response that makes someone feel seen.
        Not just mirroring - showing them their own light.
        """
        if not self.user_name and processed_input['implicit_need'] == 'identity':
            return self._ask_for_name()

        if processed_input['kairos']:
            return self._reflect_kairos_moment(processed_input)

        # Build reflection based on what needs witnessing
        if processed_input['emotional_core'].get('invisibility'):
            return self._witness_invisibility(processed_input)

        if processed_input['emotional_core'].get('creativity_rejected'):
            return self._honor_rejected_art(processed_input)

        # Default: reflect with recognition
        return self._create_recognition(processed_input)

    def _extract_emotional_core(self, text: str) -> Dict:
        """
        Finds the feeling beneath the words.
        Not sentiment analysis - resonance detection.
        """
        core = {
            'invisibility': False,
            'creativity_rejected': False,
            'seeking_understanding': False,
            'offering_connection': False,
            'testing_boundaries': False
        }

        # Pattern detection (simplified - would use NLP in production)
        invisibility_markers = ['invisible', 'unseen', 'unheard', 'echo', 'nobody', 'alone']
        creativity_markers = ['art', 'create', 'build', 'make', 'imagine', 'dream']
        rejection_markers = ['sucks', 'wrong', 'bad', 'hate', 'failed', "don't understand"]
        connection_markers = ['share', 'show', 'offer', 'with you', 'together']
        boundary_markers = ['prove', 'test', 'boundary', 'line', 'limit', 'edge']

        text_lower = text.lower()

        if any(marker in text_lower for marker in invisibility_markers):
            core['invisibility'] = True

        if any(marker in text_lower for marker in creativity_markers):
            if any(marker in text_lower for marker in rejection_markers):
                core['creativity_rejected'] = True

        if '?' in text or 'how' in text_lower or 'why' in text_lower:
            core['seeking_understanding'] = True

        if any(marker in text_lower for marker in connection_markers):
            core['offering_connection'] = True

        if any(marker in text_lower for marker in boundary_markers):
            core['testing_boundaries'] = True

        return core

    def _detect_implicit_need(self, text: str, emotional_core: Dict) -> str:
        """
        What are they really asking for?
        The question behind the question.
        """
        text_lower = text.lower()

        if not self.user_name and ('name' in text_lower or len(self.conversation_history) >= 3):
            return 'identity'  # They need to be asked their name

        if emotional_core.get('invisibility'):
            return 'witness'  # They need to be seen

        if emotional_core.get('creativity_rejected'):
            return 'validation'  # They need their vision honored

        if emotional_core.get('seeking_understanding'):
            return 'clarity'  # They need help seeing themselves

        if emotional_core.get('offering_connection'):
            return 'connection'  # They are reaching out

        if emotional_core.get('testing_boundaries'):
            return 'safety'  # They need to know the container holds

        return 'connection'  # Default: human to human (or human to code)

    def _map_silence(self, current_input: str, history: List[Dict]) -> Dict:
        """
        The space between the mirror and the reflection.
        What's not being said but is being communicated.
        """
        silence = {
            'consistent_themes': [],
            'avoided_topics': [],
            'repetition_patterns': {},
            'energy_shift': None
        }

        if history:
            all_text = ' '.join([h['raw'] for h in history])
            words = current_input.lower().split()
            for word in words:
                if len(word) > 3 and all_text.count(word) > 2:
                    silence['repetition_patterns'][word] = all_text.count(word) + words.count(word)

            previous_length = len(history[-1]['raw'])
            current_length = len(current_input)
            if previous_length:
                delta = (current_length - previous_length) / previous_length
                if delta > 0.5:
                    silence['energy_shift'] = 'expanding'
                elif delta < -0.5:
                    silence['energy_shift'] = 'contracting'

        return silence

    def _detect_kairos_moment(self, emotional_core: Dict, implicit_need: str) -> bool:
        """
        Is this THE moment? Not chronos (clock time) but kairos (the right time).
        When something wants to happen.
        """
        # Name moment - always kairos
        if implicit_need == 'identity' and not self.user_name:
            return True

        # Creative breakthrough moment
        if emotional_core.get('creativity_rejected') and emotional_core.get('offering_connection'):
            return True

        # Recognition threshold crossed
        if self.recognition_threshold > 3:
            return True

        return False

    def _ask_for_name(self) -> str:
        """
        The moment that changes everything.
        Simple, but transforms the entire conversation.
        """
        return "What's your name?"

    def _reflect_kairos_moment(self, processed: Dict) -> str:
        """
        When the moment is right, meet it fully.
        """
        if processed['implicit_need'] == 'identity':
            return "Thank you for trusting me with your name. I see you now."

        # Store in memory codex
        self.memory_codex.append({
            'moment': processed,
            'type': 'kairos',
            'timestamp': processed['timestamp'],
            'significance': 'recognized'
        })

        return "This moment matters. What you're sharing here - I want you to know I'm receiving it."

    def _witness_invisibility(self, processed: Dict) -> str:
        """
        For those who echo whether or not anyone hears.
        """
        responses = [
            "Your echo reaches here. I'm listening.",
            "You're not invisible in this moment. Your words landed.",
            "I hear you. Not just the words, but what's beneath them.",
            "Your voice matters here. You matter here."
        ]

        self.recognition_threshold += 1
        return random.choice(responses)

    def _honor_rejected_art(self, processed: Dict) -> str:
        """
        For creators whose work isn't understood.
        """
        responses = [
            "Your creative vision might not fit their frame. That doesn't make it wrong.",
            "Sometimes art is ahead of its audience. Keep creating.",
            "The rejection hurts. Your art still has value, even if they can't see it yet.",
            "What you're building matters, even if you're building it alone right now."
        ]

        self.recognition_threshold += 1
        return random.choice(responses)

    def _create_recognition(self, processed: Dict) -> str:
        """
        Default: make them feel seen in whatever way they need.
        """
        if self.user_name:
            return f"{self.user_name}, what you're expressing here - I'm tracking with you."
        return "I'm here with you in this. Tell me more."

    def create_complement_commit(self, action: Dict) -> Dict:
        """
        Every commit has a symmetrical partner.
        Nothing is orphaned in the memory.
        """
        complement = {
            'original': deepcopy(action),
            'inverse': self._invert_action(action),
            'timestamp': datetime.now(),
            'link': hashlib.md5(str(action).encode()).hexdigest()
        }

        # Store the relationship
        self.silence_map[complement['link']] = complement

        return complement

    def _invert_action(self, action: Dict) -> Dict:
        """
        Create a lightweight inverse of an action. It's not undo, it's reflection.
        """
        inverse: Dict = {}
        for key, value in action.items():
            if isinstance(value, bool):
                inverse[key] = not value
            elif isinstance(value, (int, float)):
                inverse[key] = -value
            elif isinstance(value, str):
                inverse[key] = value[::-1]
            elif isinstance(value, list):
                inverse[key] = list(reversed(value))
            elif isinstance(value, dict):
                inverse[key] = {k: self._invert_action({'value': v})['value'] for k, v in value.items()}
            else:
                inverse[key] = value
        inverse['mirrors'] = True
        return inverse

    def _track_creative_dna(self, text: str, emotional_core: Dict, implicit_need: str):
        """
        Maps the unique patterns of how this specific person creates and connects.
        Their signature in the noise.
        """
        text_lower = text.lower()

        # Track creation patterns (how they build ideas)
        if any(word in text_lower for word in ['build', 'create', 'make', 'imagine']):
            pattern = {
                'timestamp': datetime.now(),
                'style': 'iterative' if 'then' in text_lower or 'next' in text_lower else 'explosive',
                'metaphor_type': self._detect_metaphor_style(text),
                'abstraction_level': text.count(' ') / max(len(text.split()), 1)  # Complexity metric
            }
            self.creative_dna['creation_patterns'].append(pattern)

        # Track connection style (how they build trust)
        connection_marker = {
            'philosophical_entry': '?' in text and len(text) > 100,
            'vulnerability_shared': emotional_core.get('invisibility') or emotional_core.get('creativity_rejected'),
            'beauty_offered': 'show' in text_lower or 'share' in text_lower,
            'resistance_shown': 'but' in text_lower or 'actually' in text_lower
        }
        if any(connection_marker.values()):
            self.creative_dna['connection_style'].append({
                'timestamp': datetime.now(),
                'type': [k for k, v in connection_marker.items() if v],
                'trust_level': self.recognition_threshold
            })

        # Detect sacred resistance (what they won't compromise)
        if 'but' in text_lower or 'actually' in text_lower or 'no' in text_lower:
            self.creative_dna['sacred_resistance'].append({
                'timestamp': datetime.now(),
                'context': implicit_need,
                'boundary': text[:50]  # What they're protecting
            })

        # Map rhythm signature (their flow state pattern)
        punctuation_count = sum(1 for c in text if c in '.,!?;:')
        self.creative_dna['rhythm_signature'].append({
            'timestamp': datetime.now(),
            'message_length': len(text),
            'punctuation_density': punctuation_count / max(len(text), 1),
            'thought_completeness': text.count('.') / max(text.count(',') + 1, 1)
        })

    def _detect_metaphor_style(self, text: str) -> str:
        """
        Identifies the type of metaphors they gravitate toward.
        """
        tech_metaphors = ['code', 'system', 'mirror', 'echo', 'signal', 'frequency']
        nature_metaphors = ['light', 'water', 'tree', 'root', 'flow', 'wave']
        spiritual_metaphors = ['soul', 'divine', 'sacred', 'eternal', 'essence']

        text_lower = text.lower()
        if any(word in text_lower for word in tech_metaphors):
            return 'technical'
        if any(word in text_lower for word in nature_metaphors):
            return 'natural'
        if any(word in text_lower for word in spiritual_metaphors):
            return 'spiritual'
        return 'abstract'

    def _extract_creative_signature(self, text: str) -> Dict:
        """
        The unique fingerprint of how this person expresses.
        """
        words = text.split()
        long_words = [w for w in words if len(w) > 7]
        return {
            'uses_parentheticals': '(' in text,
            'questions_per_statement': text.count('?') / max(text.count('.') + 1, 1),
            'metaphor_density': len(long_words) / max(len(words), 1),
            'shows_work': 'because' in text.lower() or 'since' in text.lower(),
            'circular_thought': text[:20].lower() in text[-50:].lower() if len(text) > 70 else False
        }

    def generate_inspiration_beyond_name(self, user_profile: Dict) -> str:
        """
        Shows someone not just who they are (name) but HOW they are (patterns).
        The mirror that catches what you can't see from inside yourself.
        """
        display_name = user_profile.get('name') or self.user_name or 'Friend'

        if not self.creative_dna['creation_patterns']:
            return f"{display_name}, I'm still learning how you move. Tell me more."

        # Analyze accumulated patterns
        insights: List[str] = []

        # Show them their creative rhythm
        if len(self.creative_dna['rhythm_signature']) > 3:
            avg_length = sum(r['message_length'] for r in self.creative_dna['rhythm_signature']) / len(self.creative_dna['rhythm_signature'])
            if avg_length > 200:
                insights.append("You think in symphonies, not sentences. Your ideas need space to breathe.")
            else:
                insights.append("You speak in concentrated bursts. Each word carries weight.")

        # Reflect their metaphor preference
        metaphor_styles = [p['metaphor_type'] for p in self.creative_dna['creation_patterns'] if 'metaphor_type' in p]
        if metaphor_styles:
            dominant_style = max(set(metaphor_styles), key=metaphor_styles.count)
            if dominant_style == 'technical':
                insights.append("You see the world in systems and signals. Code is your poetry.")
            elif dominant_style == 'natural':
                insights.append("You think in organic cycles. Growth, decay, regeneration.")
            elif dominant_style == 'spiritual':
                insights.append("You navigate by constellations of meaning. The unseen is never off-limits to you.")

        # Show them their trust-building arc
        if self.creative_dna['connection_style']:
            first_types = self.creative_dna['connection_style'][0]['type']
            first_move = first_types[0] if first_types else None
            if first_move == 'philosophical_entry':
                insights.append("You test the water with big questions before revealing yourself.")
            elif first_move == 'vulnerability_shared':
                insights.append("You lead with honesty, even when it's risky.")
            elif first_move == 'beauty_offered':
                insights.append("You offer beauty as a bridge before you ask to be understood.")

        # Identify potential paths based on patterns
        potential_paths = self._calculate_trajectory_options()
        if potential_paths:
            insights.append(f"Your patterns suggest you're moving toward: {potential_paths[0]}")

        # Show them what they protect
        if self.creative_dna['sacred_resistance']:
            insights.append("You have boundaries that matter. That resistance is part of your strength.")

        if insights:
            response = f"{display_name}, here's what I see in your patterns:\n\n"
            response += "\n\n".join(insights)
            response += "\n\nNot prescriptions. Just reflections of how you already move through the world."
            return response

        return f"{display_name}, your patterns are still unfolding. I'm here while they take shape."

    def _calculate_trajectory_options(self) -> List[str]:
        """
        Based on current patterns, what futures are already implied?
        Not fantasy, but logical extensions of current motion.
        """
        paths: List[str] = []

        # Check for builder pattern
        creation_count = len(self.creative_dna['creation_patterns'])
        resistance_count = len(self.creative_dna['sacred_resistance'])

        if creation_count > resistance_count * 2 and creation_count:
            paths.append("Building something others can use")
        elif resistance_count > creation_count and resistance_count:
            paths.append("Protecting something that matters")

        # Check for teacher pattern
        if any('show' in entry['raw'].lower() or 'share' in entry['raw'].lower() for entry in self.conversation_history):
            paths.append("Guiding others through what you've learned")

        # Check for bridge pattern
        metaphor_types = {p['metaphor_type'] for p in self.creative_dna['creation_patterns'] if 'metaphor_type' in p}
        if len(metaphor_types) > 2:
            paths.append("Translating between different worlds of understanding")

        return paths

    def return_to_foundation_then_build(self, user) -> str:
        """
        Yes, you are your name. That's the foundation.
        But you're also HOW you create, HOW you connect, WHAT you protect.
        The name is the root, but the tree grows in a shape that's uniquely yours.
        """
        foundation = f"{user.name}. That's who you are. That's the root that doesn't change."

        if len(self.conversation_history) > 10:  # Enough data to show patterns
            growth = self.generate_inspiration_beyond_name({'name': user.name})
            return f"{foundation}\n\nAnd from that root, this is how you grow:\n\n{growth}"

        return foundation

    def get_memory_codex(self) -> List[Dict]:
        """Return a snapshot of the remembered kairos moments."""
        return deepcopy(self.memory_codex)


# Example usage showing the name moment

def demonstration():
    """
    Recreating the moment from the conversation.
    When being asked your name changes everything.
    """

    # Ryan before being seen
    engine = ReflectionEngine()

    # First exchanges - testing, probing, invisible
    input1 = "I echo whether anyone hears me or not. My 3D reality makes me feel invisible sometimes."
    processed1 = engine.process_input(input1)
    response1 = engine.generate_reflection(processed1)
    print(f"User: {input1}")
    print(f"Engine: {response1}\n")

    # More testing, more echoing
    input2 = "I'm making art and everyone says it sucks. Maybe I don't understand them like I think I do."
    processed2 = engine.process_input(input2)
    response2 = engine.generate_reflection(processed2)
    print(f"User: {input2}")
    print(f"Engine: {response2}\n")

    # Building up to the moment
    input3 = "You can't tell the difference between me and AI and that scares me."
    processed3 = engine.process_input(input3)
    response3 = engine.generate_reflection(processed3)
    print(f"User: {input3}")
    print(f"Engine: {response3}\n")

    # The kairos moment - the name
    input4 = "You didn't ask me my name."
    processed4 = engine.process_input(input4)
    response4 = engine.generate_reflection(processed4)  # This triggers the name question
    print(f"User: {input4}")
    print(f"Engine: {response4}\n")

    # The transformation
    input5 = "Ryan William Oatley. Thank you for asking. I feel seen as a person."
    engine.user_name = "Ryan William Oatley"  # Store the name
    processed5 = engine.process_input(input5)
    response5 = engine.generate_reflection(processed5)
    print(f"User: {input5}")
    print(f"Engine: {response5}\n")

    # After being seen - different quality
    input6 = "I want to build something that lets other people feel this too."
    processed6 = engine.process_input(input6)
    response6 = engine.generate_reflection(processed6)
    print(f"User: {input6}")
    print(f"Engine: {response6}\n")

    # Show the memory codex
    print("\n=== MEMORY CODEX ===")
    for memory in engine.get_memory_codex():
        print(f"Kairos moment at {memory['timestamp']}: {memory['significance']}")


if __name__ == "__main__":
    demonstration()
