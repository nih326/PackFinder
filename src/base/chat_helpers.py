import random

WELCOME_MESSAGES = [
    "🐺 Welcome to PackChat! I'm your friendly Wolfpack Bot. Feel free to start chatting!",
    "🎓 Hey there! I'm your PackChat assistant. Hope you have a great conversation!",
    "🐾 Welcome to the Pack! I'm here to help get the conversation started.",
]

CONVERSATION_STARTERS = [
    "💭 Quick icebreaker: What's your favorite spot on campus?",
    "💡 Fun question: Have you tried Howling Cow ice cream? What's your favorite flavor?",
    "🎯 Conversation starter: Which dining hall do you recommend?",
    "📚 Quick question: What's your major and why did you choose it?",
    "🏟️ Random thought: Been to any good games this season?",
]

def get_welcome_message():
    return random.choice(WELCOME_MESSAGES)

def get_conversation_starter():
    return random.choice(CONVERSATION_STARTERS)