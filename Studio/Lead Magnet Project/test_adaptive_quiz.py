#!/usr/bin/env python3
"""
Test the adaptive nature of the philosophy quiz
Shows how different answers lead to different question paths
"""

from philosophy_quiz_prototype import PhilosophyQuiz

def demonstrate_adaptive_paths():
    """Show how different initial answers lead to different questions"""
    
    print("=== DEMONSTRATING ADAPTIVE QUESTION PATHS ===\n")
    
    # Path 1: Structure-loving parent
    print("PATH 1: Structure-Loving Parent")
    print("-" * 40)
    quiz1 = PhilosophyQuiz()
    
    print("Q1: Ideal learning day?")
    print("Answer: A - Following a structured schedule...")
    question1 = quiz1.get_next_question()
    quiz1.process_answer(question1, "A")
    
    print("\nQ2: Why learn this?")
    print("Answer: A - Building your mind systematically...")
    question2 = quiz1.get_next_question()
    quiz1.process_answer(question2, "A")
    
    print("\nBecause they chose structure (A, A), they get:")
    question3 = quiz1.get_next_question()
    print(f"Q3: {question3['question']}")
    print("This distinguishes between Classical and Charlotte Mason!\n")
    
    # Path 2: Freedom-loving parent
    print("\nPATH 2: Freedom-Loving Parent")
    print("-" * 40)
    quiz2 = PhilosophyQuiz()
    
    print("Q1: Ideal learning day?")
    print("Answer: C - Child's interests completely guide...")
    question1 = quiz2.get_next_question()
    quiz2.process_answer(question1, "C")
    
    print("\nQ2: Why learn this?")
    print("Answer: C - Let's find out if you need to...")
    question2 = quiz2.get_next_question()
    quiz2.process_answer(question2, "C")
    
    print("\nBecause they chose freedom (C, C), they get:")
    question3 = quiz2.get_next_question()
    print(f"Q3: {question3['question']}")
    print("This distinguishes between Montessori and Unschooling!\n")
    
    # Path 3: Balanced parent
    print("\nPATH 3: Balanced Parent")
    print("-" * 40)
    quiz3 = PhilosophyQuiz()
    
    print("Q1: Ideal learning day?")
    print("Answer: D - Mix formal lessons with exploration...")
    question1 = quiz3.get_next_question()
    quiz3.process_answer(question1, "D")
    
    print("\nQ2: Why learn this?")
    print("Answer: D - Let's design a project...")
    question2 = quiz3.get_next_question()
    quiz3.process_answer(question2, "D")
    
    print("\nBecause they chose balance/projects (D, D), they get:")
    question3 = quiz3.get_next_question()
    print(f"Q3: {question3['question']}")
    print("This distinguishes between Project-Based and STEM!\n")
    
    # Show final results
    print("\n" + "="*60)
    print("FINAL RESULTS FROM DIFFERENT PATHS:")
    print("="*60)
    
    # Complete Path 1
    quiz1.process_answer(question3, "A")
    results1 = quiz1.get_results()
    print(f"\nPath 1 (A→A→A): {results1['primary_philosophy'].replace('_', ' ').title()}")
    
    # Complete Path 2  
    quiz2.process_answer(question3, "B")
    results2 = quiz2.get_results()
    print(f"Path 2 (C→C→B): {results2['primary_philosophy'].replace('_', ' ').title()}")
    
    # Complete Path 3
    quiz3.process_answer(question3, "A")
    results3 = quiz3.get_results()
    print(f"Path 3 (D→D→A): {results3['primary_philosophy'].replace('_', ' ').title()}")
    
    print("\n🎯 Each parent got different questions based on their answers!")

def show_all_distinction_questions():
    """Display all possible distinction questions"""
    from philosophy_quiz_prototype import QuestionBank
    
    print("\n\n=== ALL DISTINCTION QUESTIONS IN THE BANK ===")
    print("(These appear in Q3-4 based on remaining philosophies)\n")
    
    distinctions = QuestionBank.get_distinction_questions()
    
    for key, q in distinctions.items():
        print(f"{key.upper()}:")
        print(f"Q: {q['question']}")
        print(f"A: {q['answers']['A']}")
        print(f"B: {q['answers']['B']}")
        print()

if __name__ == "__main__":
    demonstrate_adaptive_paths()
    show_all_distinction_questions()