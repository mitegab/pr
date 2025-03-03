"""Manages the touch typing curriculum and lessons."""

import json
import os
from pathlib import Path
from config import RESOURCES_DIR

# Define lessons directory
LESSONS_DIR = RESOURCES_DIR / "lessons"
LESSONS_DIR.mkdir(exist_ok=True)

# Define the curriculum structure
CURRICULUM = {
    "beginner": [
        {
            "id": "home_row",
            "title": "Home Row Keys",
            "description": "Learn the home row keys: a, s, d, f, j, k, l, ;",
            "keys": ["a", "s", "d", "f", "j", "k", "l", ";"],
            "exercises": [
                "fff jjj fff jjj",
                "fj fj fj fj fj fj",
                "ddd kkk ddd kkk",
                "dk dk dk dk dk dk",
                "sss lll sss lll",
                "sl sl sl sl sl sl",
                "aaa ;;; aaa ;;;",
                "a; a; a; a; a; a;",
                "asdf jkl; asdf jkl;",
                "fjdk slaf ;dkj fsal"
            ]
        },
        {
            "id": "home_row_words",
            "title": "Home Row Words",
            "description": "Practice words using only home row keys",
            "keys": ["a", "s", "d", "f", "j", "k", "l", ";"],
            "prerequisites": ["home_row"],
            "exercises": [
                "ad ad ad ad ad ad", 
                "fad fad fad fad fad",
                "sad sad sad sad sad",
                "lad lad lad lad lad",
                "ask ask ask ask ask",
                "fall fall fall fall fall",
                "salad salad salad salad",
                "flask flask flask flask",
                "all falls asks salad",
                "jak jak jak jak jak"
            ]
        },
        {
            "id": "e_and_i",
            "title": "E and I Keys",
            "description": "Learn the E and I keys on the top row",
            "keys": ["a", "s", "d", "f", "e", "i", "j", "k", "l", ";"],
            "prerequisites": ["home_row_words"],
            "exercises": [
                "e e e e e e e e e e",
                "i i i i i i i i i i",
                "fe fe fe fe fe fe fe",
                "ji ji ji ji ji ji ji",
                "desi desi desi desi",
                "like like like like",
                "file file file file",
                "side side side side",
                "isle isle isle isle",
                "idea idea idea idea"
            ]
        }
    ],
    "intermediate": [
        {
            "id": "top_row",
            "title": "Top Row Keys",
            "description": "Learn the complete top row: q, w, e, r, t, y, u, i, o, p",
            "keys": ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
            "prerequisites": ["e_and_i"],
            "exercises": [
                "q q q q q p p p p p",
                "w w w w w o o o o o",
                "e e e e e i i i i i",
                "r r r r r u u u u u",
                "t t t t t y y y y y",
                "qwerty qwerty qwerty",
                "poiuy poiuy poiuy",
                "queue quiet quill",
                "power tower lower",
                "type your top row"
            ]
        },
        {
            "id": "bottom_row",
            "title": "Bottom Row Keys",
            "description": "Learn the bottom row: z, x, c, v, b, n, m, comma",
            "keys": ["z", "x", "c", "v", "b", "n", "m", ","],
            "prerequisites": ["top_row"],
            "exercises": [
                "z z z z z m m m m m",
                "x x x x x n n n n n",
                "c c c c c b b b b b",
                "v v v v v v v v v v",
                "zxcv zxcv zxcv zxcv",
                "bnm, bnm, bnm, bnm,",
                "zinc zinc zinc zinc",
                "boxes boxes boxes",
                "calm calm calm calm",
                "verb verb verb verb"
            ]
        },
        {
            "id": "full_alphabet",
            "title": "Full Alphabet Practice",
            "description": "Practice with all letters of the alphabet",
            "keys": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", 
                    "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"],
            "prerequisites": ["bottom_row"],
            "exercises": [
                "the quick brown fox jumps over the lazy dog",
                "pack my box with five dozen liquor jugs",
                "amazingly few discotheques provide jukeboxes",
                "sphinx of black quartz judge my vow",
                "how quickly daft jumping zebras vex",
                "crazy fredrick bought many very exquisite opal jewels",
                "quick zephyrs blow vexing daft jim",
                "waxy and quivering jocks fumble the pizza",
                "five or six big jet planes zoomed quickly by the tower",
                "a quick movement of the enemy will jeopardize five gunboats"
            ]
        }
    ],
    "advanced": [
        {
            "id": "numbers",
            "title": "Number Keys",
            "description": "Learn the number keys: 1, 2, 3, 4, 5, 6, 7, 8, 9, 0",
            "keys": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
            "prerequisites": ["full_alphabet"],
            "exercises": [
                "1 1 1 1 1 1 1 1 1 1",
                "2 2 2 2 2 2 2 2 2 2",
                "3 3 3 3 3 3 3 3 3 3",
                "4 4 4 4 4 4 4 4 4 4",
                "5 5 5 5 5 5 5 5 5 5",
                "67890 67890 67890",
                "12345 12345 12345",
                "100 200 300 400 500",
                "2022 1984 3000 5280",
                "1234567890 0987654321"
            ]
        },
        {
            "id": "symbols",
            "title": "Symbol Keys",
            "description": "Learn common symbols: !, @, #, $, %, ^, &, *, (, ), -",
            "keys": ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-"],
            "prerequisites": ["numbers"],
            "exercises": [
                "! ! ! ! ! ! ! ! ! !",
                "@ @ @ @ @ @ @ @ @ @",
                "# # # # # # # # # #",
                "$ $ $ $ $ $ $ $ $ $",
                "% % % % % % % % % %",
                "^&*() ^&*() ^&*()",
                "!@#$% !@#$% !@#$%",
                "Hello! How are you?",
                "He paid $5.99 for lunch.",
                "(Note: 100% of the work is done.)"
            ]
        },
        {
            "id": "speed_building",
            "title": "Speed Building",
            "description": "Advanced exercises to build typing speed",
            "prerequisites": ["symbols"],
            "exercises": [
                "The early morning sun rose over the quiet town.",
                "She quickly jumped over the fence to catch the bus.",
                "Programming requires attention to detail and logical thinking.",
                "In 2023, the company reported 45% growth in Q3.",
                "Please submit your assignment by Friday, August 12th.",
                "The package will arrive at 123 Main St., Apt #4.",
                "He scored 98.5% on his final exam!",
                "The software update (version 3.2.1) includes important security fixes.",
                "\"To be or not to be, that is the question,\" wrote Shakespeare.",
                "Email me at john.doe@example.com or call 555-123-4567."
            ]
        }
    ]
}

class LessonManager:
    """Manages typing lessons and user progress."""
    
    def __init__(self):
        """Initialize the lesson manager."""
        self.ensure_lessons_exist()
    
    def ensure_lessons_exist(self):
        """Create default lessons if they don't exist."""
        if not LESSONS_DIR.exists():
            LESSONS_DIR.mkdir(parents=True)
        
        # Check for existing lessons
        has_lessons = False
        for difficulty in CURRICULUM.keys():
            difficulty_dir = LESSONS_DIR / difficulty
            if difficulty_dir.exists() and any(difficulty_dir.iterdir()):
                has_lessons = True
                break
        
        # Create sample lessons if none exist
        if not has_lessons:
            for difficulty, lessons in CURRICULUM.items():
                difficulty_dir = LESSONS_DIR / difficulty
                difficulty_dir.mkdir(exist_ok=True)
                
                for lesson in lessons:
                    lesson_file = difficulty_dir / f"{lesson['id']}.json"
                    with open(lesson_file, 'w') as f:
                        json.dump(lesson, f, indent=4)
    
    def get_lessons(self, difficulty=None):
        """Get available lessons, optionally filtered by difficulty."""
        lessons = {}
        
        # Get all lesson directories (difficulties)
        for difficulty_dir in LESSONS_DIR.iterdir():
            if difficulty_dir.is_dir():
                difficulty_name = difficulty_dir.name
                
                # Skip if not matching the requested difficulty
                if difficulty and difficulty_name != difficulty:
                    continue
                
                lessons[difficulty_name] = []
                
                # Load lessons for this difficulty
                for lesson_file in difficulty_dir.glob("*.json"):
                    try:
                        with open(lesson_file, 'r') as f:
                            lesson = json.load(f)
                            lessons[difficulty_name].append(lesson)
                    except Exception as e:
                        print(f"Error loading lesson {lesson_file}: {e}")
        
        # If no lessons found, use the sample lessons
        if not lessons and difficulty in CURRICULUM:
            lessons[difficulty] = CURRICULUM[difficulty]
        elif not lessons and not difficulty:
            lessons = CURRICULUM
        
        return lessons
    
    def get_lesson(self, difficulty, lesson_id):
        """Get a specific lesson by difficulty and ID."""
        lesson_file = LESSONS_DIR / difficulty / f"{lesson_id}.json"
        
        if lesson_file.exists():
            try:
                with open(lesson_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading lesson {lesson_file}: {e}")
        
        # Fallback to sample lessons
        if difficulty in CURRICULUM:
            for lesson in CURRICULUM[difficulty]:
                if lesson["id"] == lesson_id:
                    return lesson
        
        return None
    
    def get_user_progress(self, username):
        """Get the user's lesson progress."""
        from config import USER_DATA_FILE
        
        if not USER_DATA_FILE.exists():
            return {}
        
        try:
            with open(USER_DATA_FILE, 'r') as f:
                data = json.load(f)
                if username in data.get("users", {}):
                    return data["users"][username].get("lesson_progress", {})
        except Exception as e:
            print(f"Error loading user progress: {e}")
        
        return {}
    
    def update_lesson_progress(self, username, difficulty, lesson_id, stats):
        """Update the user's progress for a specific lesson."""
        from config import USER_DATA_FILE
        
        if not USER_DATA_FILE.exists():
            return False
        
        try:
            with open(USER_DATA_FILE, 'r') as f:
                data = json.load(f)
            
            if username not in data.get("users", {}):
                return False
            
            # Get user data
            user = data["users"][username]
            
            # Initialize lesson progress if not exist
            if "lesson_progress" not in user:
                user["lesson_progress"] = {}
            
            if difficulty not in user["lesson_progress"]:
                user["lesson_progress"][difficulty] = {}
            
            if lesson_id not in user["lesson_progress"][difficulty]:
                user["lesson_progress"][difficulty][lesson_id] = {
                    "completed": False,
                    "best_wpm": 0,
                    "best_accuracy": 0,
                    "attempts": 0,
                    "last_attempt": None
                }
            
            # Update lesson progress
            lesson = user["lesson_progress"][difficulty][lesson_id]
            lesson["completed"] = True
            lesson["attempts"] = lesson.get("attempts", 0) + 1
            lesson["last_attempt"] = stats
            
            if stats.get("wpm", 0) > lesson.get("best_wpm", 0):
                lesson["best_wpm"] = stats["wpm"]
            
            if stats.get("accuracy", 0) > lesson.get("best_accuracy", 0):
                lesson["best_accuracy"] = stats["accuracy"]
            
            # Save updated data
            with open(USER_DATA_FILE, 'w') as f:
                json.dump(data, f, indent=4)
            
            return True
            
        except Exception as e:
            print(f"Error updating lesson progress: {e}")
            return False
    
    def get_next_lesson(self, username):
        """Get the next lesson for the user based on their progress."""
        # Get all lessons
        all_lessons = self.get_lessons()
        
        # Get user progress
        progress = self.get_user_progress(username)
        
        # Define difficulty progression
        difficulties = ["beginner", "intermediate", "advanced"]
        
        # Find the next uncompleted lesson
        for difficulty in difficulties:
            if difficulty not in all_lessons:
                continue
                
            for lesson in all_lessons[difficulty]:
                lesson_id = lesson["id"]
                
                # Check if lesson is completed
                is_completed = (
                    difficulty in progress and
                    lesson_id in progress[difficulty] and
                    progress[difficulty][lesson_id].get("completed", False)
                )
                
                if not is_completed:
                    return difficulty, lesson
        
        # If all lessons are completed, return the last advanced lesson for practice
        if "advanced" in all_lessons and all_lessons["advanced"]:
            last_lesson = all_lessons["advanced"][-1]
            return "advanced", last_lesson
        
        # If no lessons available
        return None, None
