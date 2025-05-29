import pygame

levels =[
    # Level 1 - Basic platforms 
    
    {
        "platforms": [
            pygame.Rect(200, 450, 150, 20),
            pygame.Rect(400, 350, 150, 20),
            pygame.Rect(600, 250, 150, 20)
        ],
        "questions": [
            {"question": "Which function prints output in Python?", "options": ["echo", "print", "say", "speak"], "answer": 1},
            {"question": "Which one is a valid variable name?", "options": ["2name", "my-name", "name_1", "class"], "answer": 2},
            {"question": "What type is the value 5.0?", "options": ["int", "float", "str", "bool"], "answer": 1}
        ],
        "coins": [],
        "enemies": [],
        "moving_platforms": [],
    },
    # Level 2 - Coins introduced
    {
        "platforms": [
            pygame.Rect(150, 400, 100, 20),
            pygame.Rect(300, 300, 100, 20),
            pygame.Rect(500, 200, 100, 20),
            pygame.Rect(650, 100, 100, 20)
        ],
        "questions": [
            {"question": "What does `'Hello'[0]` return?", "options": ["H", "e", "o", "Error"], "answer": 0},
            {"question": "Which symbol is used for string concatenation?", "options": ["*", "+", "&", "#"], "answer": 1},
            {"question": "What is a list?", "options": ["int", "str", "collection", "bool"], "answer": 2},
            {"question": "What does `len('Python')` return?", "options": ["5", "6", "7", "Error"], "answer": 1}
        ],
        "coins": [
            pygame.Rect(100, 370, 20, 20),  # Above platform 1
            pygame.Rect(320, 400, 20, 20),  # Above platform 2
            pygame.Rect(520, 310, 20, 20),  # Above platform 3
        ],
        "enemies": [],
        "moving_platforms": [],
    },

    # Level 3 - Enemies introduced
    {
        "platforms": [
            pygame.Rect(0, 550, 800, 50),
            pygame.Rect(100, 450, 120, 20),
            pygame.Rect(280, 360, 120, 20),
            pygame.Rect(460, 270, 120, 20)
        ],
        "questions": [
            {"question": "Which function is used to take input?", "options": ["read()", "input()", "scan()", "get()"], "answer": 1},
            {"question": "What does `#` do in Python?", "options": ["Starts a loop", "Comments code", "Imports a file", "Starts a string"], "answer": 1},
            {"question": "What type does `input()` return?", "options": ["int", "float", "bool", "str"], "answer": 3},
            {"question": "How to import a module?", "options": ["include", "module", "load", "import"], "answer": 3}
        ],
        "coins": [
            pygame.Rect(100, 370, 20, 20),  # Above platform 1
            pygame.Rect(320, 400, 20, 20),  # Above platform 2
            pygame.Rect(520, 310, 20, 20),  # Above platform 3
        ],
        "enemies": [
            pygame.Rect(235, 475, 100, 2)
        ],
        "moving_platforms": [],
    },
    # Level 4 - Moving platforms
    {
        "platforms": [
            pygame.Rect(550, 200, 100, 20),
            pygame.Rect(100, 450, 100, 20),
            pygame.Rect(300, 350, 100, 20),
        ],
        "questions": [
            {"question": "Which is a conditional?", "options": ["def", "if", "for", "print"], "answer": 1},
            {"question": "Which is a valid loop?", "options": ["loop x in y", "for x to y", "for x in y", "repeat(x, y)"], "answer": 2},
            {"question": "What keyword ends a loop early?", "options": ["exit", "break", "stop", "end"], "answer": 1},
        ],
        "coins":[
            pygame.Rect(100, 370, 20, 20),  # Above platform 1
            pygame.Rect(320, 400, 20, 20),  # Above platform 2
            pygame.Rect(520, 310, 20, 20),  # Above platform 3
            pygame.Rect(100, 250, 20, 20),
        ],
        "enemies": [],
        "moving_platforms": [
            {'rect': pygame.Rect(50, 110, 100, 20), 'speed': 3, 'direction': 'horizontal', 'min': 50, 'max': 300},
            {'rect': pygame.Rect(200, 275, 100, 20), 'speed': 2, 'direction': 'horizontal', 'min': 200, 'max': 400},

        ],
    },

    # Level 5 - All mechanics combined 
    {
        "platforms": [
            pygame.Rect(100, 450, 100, 20),
            pygame.Rect(230, 360, 100, 20),
            pygame.Rect(550, 115, 100, 20),
            pygame.Rect(520, 400, 100, 20),
        ],
        "questions": [
            {"question": "What keyword defines a function?", "options": ["def", "func", "define", "function"], "answer": 0},
            {"question": "Which is a correct function call?", "options": ["call myFunc", "myFunc()", "myFunc[]", "start myFunc"], "answer": 1},
            {"question": "What is returned by default in a function?", "options": ["None", "0", "False", "Error"], "answer": 0},
            {"question": "What does `return` do?", "options": ["Repeat code", "End function and give a value", "Stop program", "None"], "answer": 1},

        ],
        "coins": [
            pygame.Rect(110, 395,20,20),  
            pygame.Rect(400, 310,20,20), 
            pygame.Rect(590, 200,20,20)
        ],
        "enemies": [
            pygame.Rect(225, 485, 80, 2), 
            pygame.Rect(400, 485, 120, 2)
        ],
        "moving_platforms": [
            {'rect': pygame.Rect(300, 190, 100, 20), 'speed': 2, 'direction': 'horizontal', 'min': 200, 'max': 400},
        ],
    }
]