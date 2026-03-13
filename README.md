# RepRegistry
A desktop workout tracking application built with Python and CustomTkinter. This project is currently in progress.
---
## Features
- User Authentication — Sign up and log in with a personal account
- Workout Management — View and manage workout days (e.g. Push Day, Pull Day)
- Set Tracking — Dynamically add or remove sets per exercise (min 1, max 6)
- Rep & Weight Logging — Input boxes for weight and reps on each set
- Persistent Storage — User data saved locally via JSON files (SQLite migration in progress)
- Clean UI — Minimal dark/light themed interface built with CustomTkinter
---
## Tech Stack
| Tool | Purpose |
|---|---|
| Python 3 | Core language |
| CustomTkinter | GUI framework |
| Pillow (PIL) | Image rendering |
| JSON | Data persistence |
| SQLite3 | Database (in progress) |
---
## Getting Started
### Prerequisites
pip install customtkinter pillow
### Run the App
python main.py
### File Structure
RepRegistry/
│
├── main.py               # Main application file
├── exercises.json        # Exercise metadata (names, images)
├── Users/                # Saved user JSON files
└── Graphics/             # UI images and icons
    ├── RepRegistry.png
    ├── +.png
    └── -.png
---
## Data Storage
Currently, user data is stored as individual .json files in the Users/ folder. A migration to SQLite is underway, which will consolidate all user data into a single Users.db database for better scalability and data integrity.
---
## Roadmap
- [x] User sign up and login
- [x] Dynamic set add/remove per exercise
- [x] Weight and rep input per set
- [ ] SQLite database migration
- [ ] Add and delete custom workouts
- [ ] Search and select exercises from a full exercise list
- [ ] Password hashing for security
- [ ] Progress tracking over time
---
## Development Notes
CustomTkinter syntax and JSON file handling were learned with the assistance of Claude AI (Anthropic) during development.
---
## License
This project is for personal/educational use.
Documentation and goals for project in the documentation file.
