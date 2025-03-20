# ai-chatbots.github.io
a simple, minimalistic, yet creative portfolio website for AION Agents that documents three projects, with three product sections: Coffee Shop Chatbot, Aion Voice Assist Mobile, and Chatbot Popup Integration.

source venv/bin/activate
python -m uvicorn app.main:app --reload



/ai-chatbots.github.io
├── index.html                   # Main page for Chatbots (formerly HOME)
├── tutors.html                  # Tutors page (with SEO keyword tags below each tutor)
├── courses.html                 # Courses page (each course styled like pricing/chatbot cards)
├── script.js                    # Global JavaScript (dark mode toggle, interactive dashboard, code playground, etc.)
├── style.css                    # Custom CSS styles (overrides and additional styling)
├── courses/                      # Folder for image assets
│   ├── 1-text.html 
│   ├── 2-voice.html 
│   ├── 3-enterprise.html 
│   ├── ai-prod.html 
│   ├── ai-prod-pro.html 
│   ├── ai-prod-saas.html 
│   ├── guide.html 
├── images/                      # Folder for image assets
│   ├── FAQ.png
│   ├── SALES.png
│   ├── SUPPORT.png
│   ├── SPEECH-TO-TEXT.png
│   ├── TEXT-TO SPEECH.png
│   ├── TEAM-SUMMARY.png
│   ├── HOME.png
│   ├── AION-HOME.png
│   ├── popup.png
│   ├── course1.png
│   ├── course2.png
│   └── course3.png
└── .github/
    ├── workflows/
        │   ├── jekyll.yml
└── backend/                     # Back‑end application folder
    ├── agents/
    ├── app/
    │   ├── __init__.py
    │   ├── main.py              # Main entry point for the back‑end server
    │   ├── api/                 # API endpoints
    │   │   ├── __init__.py
    │   │   ├── auth.py          # Authentication endpoints
    │   │   ├── chatbot.py       # Chatbot-related endpoints
    │   │   ├── courses.py       # Courses endpoints
    │   │   ├── tutors.py        # Tutors endpoints
    │   │   ├── subscription.py  # Subscription management endpoints
    │   │   └── analytics.py     # Analytics endpoints
    │   ├── models.py            # Database models
    │   ├── schemas.py           # Data validation schemas
    │   ├── database.py          # Database connection/initialization
    │   └── config.py            # Application configuration settings
    └── requirements.txt         # Python dependencies
