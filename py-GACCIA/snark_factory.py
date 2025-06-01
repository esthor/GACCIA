#!/usr/bin/env python3
"""
GACCIA Snark Factory 🏭

Generate endless hilarious snark between Python and TypeScript!
Because sometimes you just need to watch languages roast each other.
"""

import os
from dotenv import load_dotenv
import random
import time
from gaccia_evaluators import SnarkGenerator

# Load environment variables from .env file
load_dotenv()


class SnarkFactory:
    """Factory for generating endless programming language snark."""
    
    def __init__(self, use_koyeb: bool = False):
        """Initialize the snark generators."""
        print("🏭 Initializing Snark Factory...")
        self.python_snark = SnarkGenerator("python", use_koyeb=use_koyeb)
        self.typescript_snark = SnarkGenerator("typescript", use_koyeb=use_koyeb)
        
        # Sample code snippets and evaluation summaries for variety
        self.sample_scenarios = [
            {
                "code": """
function fibonacci(n: number): number {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}
                """.strip(),
                "summary": "Basic recursive implementation with no optimization",
                "language": "typescript"
            },
            {
                "code": """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
                """.strip(),
                "summary": "Simple recursive approach, no type hints",
                "language": "python"
            },
            {
                "code": """
interface User {
    id: number;
    name: string;
    email?: string;
}

class UserManager {
    private users: User[] = [];
    
    addUser(user: User): void {
        this.users.push(user);
    }
}
                """.strip(),
                "summary": "Object-oriented design with interfaces and type safety",
                "language": "typescript"
            },
            {
                "code": """
class UserManager:
    def __init__(self):
        self.users = []
    
    def add_user(self, user):
        self.users.append(user)
                """.strip(),
                "summary": "Duck typing approach with dynamic attributes",
                "language": "python"
            },
            {
                "code": """
const processData = async (data: unknown[]): Promise<string[]> => {
    return data
        .filter((item): item is string => typeof item === 'string')
        .map(item => item.toUpperCase());
};
                """.strip(),
                "summary": "Functional style with type guards and async processing",
                "language": "typescript"
            },
            {
                "code": """
def process_data(data):
    return [item.upper() for item in data if isinstance(item, str)]
                """.strip(),
                "summary": "Pythonic list comprehension with runtime type checking",
                "language": "python"
            }
        ]
    
    def generate_snark_battle(self, rounds: int = 5) -> None:
        """Generate a snark battle between Python and TypeScript."""
        print("\n🥊 SNARK BATTLE ROYALE! 🥊")
        print("=" * 60)
        print("Python 🐍 vs TypeScript 📘")
        print("=" * 60)
        
        for round_num in range(1, rounds + 1):
            print(f"\n🔥 ROUND {round_num} 🔥")
            print("-" * 40)
            
            # Pick a random scenario
            scenario = random.choice(self.sample_scenarios)
            
            if scenario["language"] == "python":
                # TypeScript mocking Python
                print("📘 TypeScript's Take:")
                ts_snark = self.typescript_snark.generate_snark(
                    scenario["code"], 
                    scenario["summary"]
                )
                print(f"   💬 {ts_snark}")
                
                print("\n🐍 Python's Retort:")
                # Python defending itself
                py_counter = self.python_snark.generate_snark(
                    "TypeScript boilerplate with 47 interfaces",
                    "Over-engineered type gymnastics"
                )
                print(f"   💬 {py_counter}")
                
            else:
                # Python mocking TypeScript
                print("🐍 Python's Take:")
                py_snark = self.python_snark.generate_snark(
                    scenario["code"],
                    scenario["summary"]
                )
                print(f"   💬 {py_snark}")
                
                print("\n📘 TypeScript's Retort:")
                # TypeScript defending itself
                ts_counter = self.typescript_snark.generate_snark(
                    "def mystery_function(x): return x + 1",
                    "Runtime error waiting to happen"
                )
                print(f"   💬 {ts_counter}")
            
            if round_num < rounds:
                print("\n⏳ Preparing next round...")
                time.sleep(2)  # Dramatic pause
    
    def continuous_snark_stream(self, perspective: str = "alternating") -> None:
        """Generate continuous stream of snark."""
        print("\n🌊 CONTINUOUS SNARK STREAM 🌊")
        print("Press Ctrl+C to stop the madness!")
        print("=" * 50)
        
        try:
            counter = 1
            while True:
                scenario = random.choice(self.sample_scenarios)
                
                if perspective == "python" or (perspective == "alternating" and counter % 2 == 1):
                    print(f"\n🐍 Python Snark #{counter}:")
                    snark = self.python_snark.generate_snark(
                        scenario["code"],
                        scenario["summary"]
                    )
                    print(f"   💬 {snark}")
                else:
                    print(f"\n📘 TypeScript Snark #{counter}:")
                    snark = self.typescript_snark.generate_snark(
                        scenario["code"],
                        scenario["summary"]
                    )
                    print(f"   💬 {snark}")
                
                counter += 1
                time.sleep(3)  # Pause between snarks
                
        except KeyboardInterrupt:
            print(f"\n\n🛑 Snark stream stopped after {counter-1} roasts!")
            print("Thanks for enjoying the show! 🎭")
    
    def themed_snark_session(self, theme: str, count: int = 10) -> None:
        """Generate themed snark about specific programming concepts."""
        themes = {
            "performance": {
                "scenarios": [
                    ("Nested loops with O(n³) complexity", "Performance nightmare"),
                    ("Synchronous file operations blocking the event loop", "Blocking operations"),
                    ("Memory leaks from unclosed resources", "Resource management issues")
                ]
            },
            "typing": {
                "scenarios": [
                    ("Dynamic typing with no hints", "Type safety concerns"),
                    ("Complex generic constraints", "Over-engineered type system"),
                    ("Runtime type errors", "Type system failures")
                ]
            },
            "tooling": {
                "scenarios": [
                    ("Webpack configuration hell", "Build tool complexity"),
                    ("Package management chaos", "Dependency issues"),
                    ("Linting and formatting setup", "Tooling overhead")
                ]
            }
        }
        
        if theme not in themes:
            print(f"❌ Unknown theme: {theme}")
            print(f"Available themes: {', '.join(themes.keys())}")
            return
        
        print(f"\n🎯 THEMED SNARK SESSION: {theme.upper()} 🎯")
        print("=" * 50)
        
        scenarios = themes[theme]["scenarios"]
        
        for i in range(count):
            scenario_desc, summary = random.choice(scenarios)
            
            # Alternate between perspectives
            if i % 2 == 0:
                print(f"\n🐍 Python's perspective on {theme} #{i+1}:")
                snark = self.python_snark.generate_snark(scenario_desc, summary)
            else:
                print(f"\n📘 TypeScript's perspective on {theme} #{i+1}:")
                snark = self.typescript_snark.generate_snark(scenario_desc, summary)
            
            print(f"   💬 {snark}")
            
            if i < count - 1:
                time.sleep(1)


def main():
    """Main function with interactive menu."""
    print("🎭 Welcome to the GACCIA Snark Factory! 🎭")
    print("Where programming languages come to roast each other!")
    
    # Use OpenAI by default
    use_koyeb = False
    
    factory = SnarkFactory(use_koyeb=use_koyeb)
    
    while True:
        print("\n" + "="*50)
        print("🏭 SNARK FACTORY MENU 🏭")
        print("="*50)
        print("1. 🥊 Snark Battle (5 rounds)")
        print("2. 🌊 Continuous Snark Stream")
        print("3. 🎯 Themed Snark Session")
        print("4. 🎲 Random Single Snark")
        print("5. 🚪 Exit")
        
        choice = input("\n🎮 Choose your snark adventure (1-5): ").strip()
        
        if choice == "1":
            rounds = int(input("🔢 How many rounds? (default 5): ") or "5")
            factory.generate_snark_battle(rounds)
            
        elif choice == "2":
            perspective = input("👀 Perspective (python/typescript/alternating): ").lower() or "alternating"
            factory.continuous_snark_stream(perspective)
            
        elif choice == "3":
            print("📋 Available themes: performance, typing, tooling")
            theme = input("🎯 Choose theme: ").lower()
            count = int(input("🔢 How many snarks? (default 10): ") or "10")
            factory.themed_snark_session(theme, count)
            
        elif choice == "4":
            scenario = random.choice(factory.sample_scenarios)
            perspective = random.choice(["python", "typescript"])
            
            print(f"\n🎲 Random {perspective.upper()} snark:")
            if perspective == "python":
                snark = factory.python_snark.generate_snark(scenario["code"], scenario["summary"])
            else:
                snark = factory.typescript_snark.generate_snark(scenario["code"], scenario["summary"])
            print(f"   💬 {snark}")
            
        elif choice == "5":
            print("\n👋 Thanks for visiting the Snark Factory!")
            print("May your code be bug-free and your roasts be spicy! 🌶️")
            break
            
        else:
            print("❌ Invalid choice! Please pick 1-5.")


if __name__ == "__main__":
    main()
