#!/usr/bin/env python3
"""
Philosophy Quiz Prototype - Test adaptive questioning logic
Simulates the Agent SDK conversation flow without full setup
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple
import json

@dataclass
class QuizState:
    """Track quiz progress and philosophy scores"""
    philosophy_scores: Dict[str, int]
    eliminated: List[str]
    question_number: int
    remaining_count: int
    
    def __init__(self):
        self.philosophy_scores = {
            'classical': 0, 'charlotte_mason': 0, 'montessori': 0, 'waldorf': 0, 'traditional': 0,
            'unschooling': 0, 'project_based': 0, 'unit_studies': 0, 'eclectic': 0, 'interest_led': 0,
            'stem': 0, 'forest_school': 0, 'faith_based': 0, 'microschool': 0, 'open_education': 0
        }
        self.eliminated = []
        self.question_number = 1
        self.remaining_count = 15
    
    def get_remaining_philosophies(self) -> List[str]:
        """Get philosophies that haven't been eliminated"""
        return [p for p in self.philosophy_scores.keys() if p not in self.eliminated]
    
    def get_top_philosophies(self, n: int = 3) -> List[Tuple[str, int]]:
        """Get top N philosophies by score"""
        remaining = self.get_remaining_philosophies()
        scores = [(p, self.philosophy_scores[p]) for p in remaining]
        return sorted(scores, key=lambda x: x[1], reverse=True)[:n]
    
    def eliminate_low_scorers(self, threshold: int = -2):
        """Eliminate philosophies with very low scores"""
        for philosophy, score in self.philosophy_scores.items():
            if score <= threshold and philosophy not in self.eliminated:
                self.eliminated.append(philosophy)
        self.remaining_count = len(self.get_remaining_philosophies())

class QuestionBank:
    """Generate adaptive questions based on current quiz state"""
    
    @staticmethod
    def get_broad_elimination_questions() -> Dict:
        """Questions 1-2: Eliminate large groups"""
        return {
            1: {
                "question": "When you imagine your ideal learning day, which feels most natural?",
                "answers": {
                    "A": "Following a structured schedule with proven curriculum and clear expectations",
                    "B": "Starting with a plan but staying flexible if my child gets fascinated by something", 
                    "C": "Letting my child's interests completely guide what we explore",
                    "D": "Mixing formal lessons in the morning with free exploration in the afternoon"
                },
                "scoring": {
                    "A": {"classical": 3, "traditional": 3, "faith_based": 2, "charlotte_mason": 1},
                    "B": {"charlotte_mason": 3, "waldorf": 3, "unit_studies": 2, "eclectic": 2},
                    "C": {"unschooling": 3, "interest_led": 3, "forest_school": 2, "montessori": 1},
                    "D": {"eclectic": 3, "open_education": 3, "project_based": 2, "microschool": 2}
                },
                "eliminates": {
                    "A": ["unschooling", "interest_led"],
                    "B": ["traditional", "classical"],
                    "C": ["traditional", "classical", "faith_based"],
                    "D": ["unschooling", "traditional"]
                }
            },
            2: {
                "question": "Your child asks 'Why do I have to learn this?' What's your instinct?",
                "answers": {
                    "A": "Because it's part of the foundation you need - we're building your mind systematically",
                    "B": "Let me show you how this connects to something beautiful in the world",
                    "C": "You know what, let's find out if you actually do need to learn this",
                    "D": "Great question! Let's design a project where you'll discover why it matters"
                },
                "scoring": {
                    "A": {"classical": 3, "traditional": 3, "faith_based": 2},
                    "B": {"charlotte_mason": 3, "waldorf": 3, "unit_studies": 2},
                    "C": {"unschooling": 3, "interest_led": 3, "forest_school": 1},
                    "D": {"project_based": 3, "stem": 3, "open_education": 2, "microschool": 2}
                },
                "eliminates": {
                    "A": ["unschooling", "interest_led", "forest_school"],
                    "B": ["traditional", "stem"],
                    "C": ["classical", "traditional", "faith_based"],
                    "D": ["classical", "charlotte_mason"]
                }
            }
        }
    
    @staticmethod
    def get_distinction_questions() -> Dict:
        """Questions 3-4: Distinguish between similar philosophies"""
        return {
            "classical_vs_charlotte_mason": {
                "question": "Your 6-year-old is ready for more formal learning. What's your approach?",
                "answers": {
                    "A": "Start Latin and formal grammar - laying the foundation properly",
                    "B": "Rich living books and nature study - learning through beauty and wonder"
                },
                "scoring": {
                    "A": {"classical": 4, "traditional": 2},
                    "B": {"charlotte_mason": 4, "waldorf": 2}
                }
            },
            "montessori_vs_unschooling": {
                "question": "How much structure should guide a child's learning?",
                "answers": {
                    "A": "Carefully prepared environment with materials they can choose from",
                    "B": "Complete freedom to follow their interests wherever they lead"
                },
                "scoring": {
                    "A": {"montessori": 4, "waldorf": 2, "eclectic": 1},
                    "B": {"unschooling": 4, "interest_led": 3}
                }
            },
            "project_vs_stem": {
                "question": "What makes a learning experience truly valuable?",
                "answers": {
                    "A": "Solving real-world problems that matter to the community",
                    "B": "Building technical skills in science, technology, engineering, and math"
                },
                "scoring": {
                    "A": {"project_based": 4, "microschool": 2, "open_education": 2},
                    "B": {"stem": 4, "traditional": 2}
                }
            },
            "charlotte_mason_vs_waldorf": {
                "question": "When should children start formal academics?",
                "answers": {
                    "A": "Gentle academics from early years using living books and short lessons",
                    "B": "Wait until around 7, focusing on imagination and artistic development first"
                },
                "scoring": {
                    "A": {"charlotte_mason": 4, "unit_studies": 2},
                    "B": {"waldorf": 4, "forest_school": 2}
                }
            }
        }
    
    @staticmethod
    def get_final_clarification() -> Dict:
        """Question 5: Final distinction between top 2-3 candidates"""
        return {
            "question": "What's your biggest priority for your child's education?",
            "answers": {
                "A": "Strong character and moral foundation built through time-tested wisdom",
                "B": "Deep love of learning through beauty, nature, and living ideas", 
                "C": "Self-direction and confidence to pursue their own passions",
                "D": "Practical skills and real-world problem-solving abilities",
                "E": "Flexibility to adapt and use whatever works best for my child"
            },
            "scoring": {
                "A": {"classical": 3, "faith_based": 3, "traditional": 2},
                "B": {"charlotte_mason": 3, "waldorf": 3, "forest_school": 2},
                "C": {"unschooling": 3, "interest_led": 3, "montessori": 2},
                "D": {"project_based": 3, "stem": 3, "microschool": 2},
                "E": {"eclectic": 3, "open_education": 3, "unit_studies": 2}
            }
        }

class PhilosophyQuiz:
    """Main quiz logic with adaptive questioning"""
    
    def __init__(self):
        self.state = QuizState()
        self.broad_questions = QuestionBank.get_broad_elimination_questions()
        self.distinction_questions = QuestionBank.get_distinction_questions()
        self.final_question = QuestionBank.get_final_clarification()
    
    def get_next_question(self):
        """Determine next question based on current state"""
        remaining = self.state.get_remaining_philosophies()
        top_3 = self.state.get_top_philosophies(3)
        
        print(f"\n--- Question {self.state.question_number} ---")
        print(f"Remaining philosophies: {len(remaining)}")
        print(f"Top candidates: {[f'{p}({s})' for p, s in top_3]}")
        print(f"Eliminated: {self.state.eliminated}\n")
        
        # Broad elimination phase
        if self.state.question_number <= 2:
            return self.broad_questions[self.state.question_number]
        
        # Final clarification
        elif len(remaining) <= 3 or self.state.question_number >= 5:
            return self.final_question
        
        # Distinction phase - pick based on top candidates
        else:
            top_philosophies = [p for p, s in top_3[:2]]
            
            # Choose appropriate distinction question
            if "classical" in top_philosophies and "charlotte_mason" in top_philosophies:
                return self.distinction_questions["classical_vs_charlotte_mason"]
            elif "montessori" in top_philosophies and "unschooling" in top_philosophies:
                return self.distinction_questions["montessori_vs_unschooling"]
            elif "project_based" in top_philosophies and "stem" in top_philosophies:
                return self.distinction_questions["project_vs_stem"]
            elif "charlotte_mason" in top_philosophies and "waldorf" in top_philosophies:
                return self.distinction_questions["charlotte_mason_vs_waldorf"]
            else:
                # Default to final question if no specific distinction applies
                return self.final_question
    
    def process_answer(self, question_data, answer_key):
        """Process user answer and update state"""
        # Apply scoring
        if answer_key in question_data.get("scoring", {}):
            for philosophy, points in question_data["scoring"][answer_key].items():
                if philosophy not in self.state.eliminated:
                    self.state.philosophy_scores[philosophy] += points
        
        # Apply eliminations
        if "eliminates" in question_data and answer_key in question_data["eliminates"]:
            for philosophy in question_data["eliminates"][answer_key]:
                if philosophy not in self.state.eliminated:
                    self.state.eliminated.append(philosophy)
        
        # Eliminate very low scorers
        self.state.eliminate_low_scorers()
        self.state.remaining_count = len(self.state.get_remaining_philosophies())
        self.state.question_number += 1
    
    def get_results(self):
        """Generate final results and recommendations"""
        top_3 = self.state.get_top_philosophies(3)
        
        if not top_3:
            return "No clear philosophy match - try eclectic approach!"
        
        primary = top_3[0]
        secondary = top_3[1] if len(top_3) > 1 else None
        
        result = {
            "primary_philosophy": primary[0],
            "primary_score": primary[1],
            "secondary_philosophy": secondary[0] if secondary else None,
            "secondary_score": secondary[1] if secondary else 0,
            "all_scores": dict(self.state.philosophy_scores),
            "profile_description": self.get_profile_description(primary[0], secondary[0] if secondary else None)
        }
        
        return result
    
    def get_profile_description(self, primary, secondary=None):
        """Generate personality profile description"""
        descriptions = {
            "classical": "You value time-tested wisdom, systematic learning, and character formation through great literature and ideas.",
            "charlotte_mason": "You believe in gentle learning through living books, nature study, and nurturing a love of beautiful ideas.",
            "montessori": "You trust children's natural development and believe in prepared environments that allow self-directed exploration.",
            "unschooling": "You have radical trust in children's natural learning ability and believe life itself is the best curriculum.",
            "project_based": "You value real-world application and believe children learn best by solving authentic problems.",
            "eclectic": "You're pragmatic and believe the best approach combines elements from multiple philosophies.",
            "open_education": "You believe in radical flexibility and empowering children to architect their own education.",
            "stem": "You prioritize scientific thinking and technical skills as preparation for the modern world.",
            "faith_based": "You integrate religious values and believe education should form both mind and character.",
            "waldorf": "You value artistic development, imagination, and age-appropriate developmental stages.",
            "interest_led": "You believe passion-driven learning creates the deepest and most lasting education.",
            "unit_studies": "You prefer integrated, thematic learning that connects all subjects around central ideas.",
            "microschool": "You value small-group learning with peer interaction and shared teaching responsibilities.",
            "forest_school": "You believe nature is the best classroom and outdoor experiences create resilient learners.",
            "traditional": "You value structured, systematic education with clear standards and proven methods."
        }
        
        primary_desc = descriptions.get(primary, "You have a unique educational philosophy!")
        
        if secondary and secondary != primary:
            secondary_desc = descriptions.get(secondary, "")
            return f"{primary_desc} You also incorporate elements of {secondary.replace('_', ' ')} approach: {secondary_desc.lower()}"
        
        return primary_desc

def simulate_quiz():
    """Simulate the quiz with sample answers"""
    quiz = PhilosophyQuiz()
    
    print("=== OpenEd Philosophy Quiz Prototype ===")
    print("This simulates the adaptive questioning logic\n")
    
    # Simulate a parent's journey (Your original answers: D, D, C, C, C)
    sample_answers = ["D", "D", "B", "C", "C"]  # Your profile from earlier
    
    for i, answer in enumerate(sample_answers):
        if quiz.state.question_number > 5:
            break
            
        question_data = quiz.get_next_question()
        
        print(f"Q{quiz.state.question_number}: {question_data['question']}")
        for key, text in question_data["answers"].items():
            print(f"  {key}) {text}")
        
        print(f"\nSimulated answer: {answer}")
        print(f"Answer text: {question_data['answers'][answer]}")
        
        quiz.process_answer(question_data, answer)
        
        if len(quiz.state.get_remaining_philosophies()) <= 2 and quiz.state.question_number >= 3:
            break
    
    # Show results
    print("\n" + "="*50)
    print("RESULTS")
    print("="*50)
    
    results = quiz.get_results()
    print(f"\nYour Primary Philosophy: {results['primary_philosophy'].replace('_', ' ').title()}")
    if results['secondary_philosophy']:
        print(f"Secondary Influence: {results['secondary_philosophy'].replace('_', ' ').title()}")
    
    print(f"\nProfile: {results['profile_description']}")
    
    print(f"\nFinal Scores:")
    top_scores = sorted(results['all_scores'].items(), key=lambda x: x[1], reverse=True)[:5]
    for philosophy, score in top_scores:
        if score > 0:
            print(f"  {philosophy.replace('_', ' ').title()}: {score}")

def interactive_quiz():
    """Run interactive version for testing"""
    quiz = PhilosophyQuiz()
    
    print("=== OpenEd Philosophy Quiz (Interactive) ===")
    print("Answer 5 questions to discover your homeschool philosophy!\n")
    
    for _ in range(5):
        if quiz.state.question_number > 5:
            break
            
        question_data = quiz.get_next_question()
        
        print(f"Q{quiz.state.question_number}: {question_data['question']}")
        for key, text in question_data["answers"].items():
            print(f"  {key}) {text}")
        
        while True:
            answer = input(f"\nYour answer (A-D): ").upper().strip()
            if answer in question_data["answers"]:
                break
            print("Please enter A, B, C, or D")
        
        quiz.process_answer(question_data, answer)
        
        # Stop early if we have a clear winner
        remaining = quiz.state.get_remaining_philosophies()
        if len(remaining) <= 2 and quiz.state.question_number >= 3:
            break
    
    # Show results
    print("\n" + "="*60)
    print("YOUR HOMESCHOOL PHILOSOPHY RESULTS")
    print("="*60)
    
    results = quiz.get_results()
    
    print(f"\n🎯 Primary Philosophy: {results['primary_philosophy'].replace('_', ' ').title()}")
    if results['secondary_philosophy']:
        print(f"🔄 Secondary Influence: {results['secondary_philosophy'].replace('_', ' ').title()}")
    
    print(f"\n📖 Your Profile:")
    print(f"{results['profile_description']}")
    
    print(f"\n📊 Top Philosophy Scores:")
    top_scores = sorted(results['all_scores'].items(), key=lambda x: x[1], reverse=True)[:5]
    for philosophy, score in top_scores:
        if score > 0:
            print(f"  • {philosophy.replace('_', ' ').title()}: {score} points")
    
    return results

if __name__ == "__main__":
    # Run simulation by default for testing
    simulate_quiz()
    
    print("\n" + "="*60)
    print("Now testing with different parent profile...")
    print("="*60)
    
    # Test with different answers (Unschooling parent)
    quiz2 = PhilosophyQuiz()
    sample_answers_2 = ["C", "C", "B", "C"]
    
    for i, answer in enumerate(sample_answers_2):
        if quiz2.state.question_number > 5:
            break
            
        question_data = quiz2.get_next_question()
        print(f"\nQ{quiz2.state.question_number}: {question_data['question'][:60]}...")
        print(f"Answer: {answer} - {question_data['answers'][answer][:80]}...")
        
        quiz2.process_answer(question_data, answer)
        
        if len(quiz2.state.get_remaining_philosophies()) <= 2 and quiz2.state.question_number >= 3:
            break
    
    results2 = quiz2.get_results()
    print(f"\nSecond Parent Result: {results2['primary_philosophy'].replace('_', ' ').title()}")
    print(f"Profile: {results2['profile_description'][:100]}...")