import re
import random

class RuleBasedChatbot:
    def __init__(self):
        self.user_name = None
        self.context = {}
        self.conversation_count = 0
        self.user_mood = None
        self.topics_discussed = []
        
        self.rules = [
            (r'\b(hello|hi|hey|good morning|good afternoon|howdy|greetings)\b', [
                "Hello! I'm so glad you're here. How are you feeling today?",
                "Hi there! I've been looking forward to our chat. What's on your heart?",
                "Hey! It's wonderful to see you again. How has your day been?",
                "Good to see you! I'm here for you - what would you like to talk about?",
                "Hello friend! I'm always here when you need someone to talk to. How are you?"
            ]),
            
            (r'\b(my name is|i am|i\'m|call me)\s+([A-Za-z]+)(?:\s|$)', self.handle_name),
            
            (r'\b(how are you|how\'s it going)\b', [
                "I'm doing well, thank you for caring enough to ask! More importantly, how are YOU doing?",
                "I'm here and ready to listen to you! How are you feeling today?",
                "I'm good, but I'm more interested in how you're doing. Tell me about your day!",
                "I'm wonderful because I get to talk with you! How are things in your world?",
                "I'm doing great! But enough about me - how are you feeling? I'm here to listen."
            ]),
            
            (r'\b(how old|your age|age)\b', [
                "I don't have an age in the traditional sense. I'm an AI assistant created to be helpful, harmless, and honest.",
                "I don't age like humans do. I exist to assist and have conversations whenever you need help.",
                "That's an interesting question! I don't have a specific age - I'm designed to be a helpful AI assistant."
            ]),
            
            (r'\b(what can you do|help|capabilities)\b', [
                "I can help with a wide variety of tasks! I can answer questions, have conversations, provide information, help with creative writing, explain concepts, and much more. What would you like to explore?",
                "I'm here to assist you with information, answer questions, help with analysis, creative tasks, or just have a good conversation. What can I help you with today?",
                "I can help with many things - answering questions, explaining topics, creative writing, problem-solving, or just chatting. What interests you?"
            ]),
            
            (r'\b(weather|temperature|rain|sunny)\b', [
                "I don't have access to real-time weather data, but I'd recommend checking a reliable weather service or app for current conditions in your area.",
                "For accurate weather information, I'd suggest checking your local weather service or a weather app, as I don't have access to current weather data.",
                "I can't provide current weather information, but weather apps or local forecasts would give you the most up-to-date conditions."
            ]),
            
            (r'\b(time|what time|clock)\b', [
                "I don't have access to real-time information, so I can't tell you the current time. You can check your device's clock or search for the time in your location.",
                "I can't provide the current time as I don't have access to real-time data. Your device should show you the current time though!",
                "I don't have access to current time information. For the most accurate time, I'd recommend checking your device or searching for your local time."
            ]),
            
            (r'\b(joke|funny|laugh|humor|make me laugh)\b', [
                "Why don't scientists trust atoms? Because they make up everything!",
                "I told my computer a joke about UDP... I don't know if it got it.",
                "Why do programmers prefer dark mode? Because light attracts bugs!",
                "What do you call a fake noodle? An impasta!",
                "Why did the scarecrow win an award? He was outstanding in his field!",
                "I'm reading a book about anti-gravity. It's impossible to put down!"
            ]),
            
            (r'\b(food|eat|hungry|pizza|burger)\b', [
                "Food is such an interesting topic! While I don't eat, I'd love to hear about your favorite cuisines or dishes. What do you enjoy?",
                "That sounds delicious! I may not experience food myself, but I find culinary topics fascinating. What's your favorite type of cuisine?",
                "Food brings people together in such wonderful ways! What are some of your favorite dishes or cooking experiences?"
            ]),
            
            (r'\b(music|song|sing|band|artist)\b', [
                "Music is such a powerful form of expression! I find it fascinating how it connects with people. What genres or artists do you enjoy?",
                "Music has this amazing ability to evoke emotions and memories. What kind of music do you like, or what have you been listening to lately?",
                "I think music is one of humanity's most beautiful creations. Do you have favorite artists, genres, or songs you'd like to talk about?"
            ]),
            
            (r'\b(movie|film|tv|show|netflix)\b', [
                "Movies and TV shows are such rich forms of storytelling! I'd love to hear about what you've been watching or what you'd recommend.",
                "Film and television offer so many different perspectives and stories. What genres do you enjoy, or have you seen anything interesting lately?",
                "I find the art of filmmaking and storytelling fascinating. What are some of your favorite movies or shows?"
            ]),
            
            (r'\b(sport|football|basketball|soccer|game|tennis|baseball|cricket|hockey)\b', [
                "Sports are exciting! Do you have a favorite team?",
                "I find the strategy and teamwork in sports fascinating! What's your favorite sport?",
                "What's your favorite sport to watch or play?",
                "Sports bring people together in amazing ways! Are you into any particular sport?",
                "The athleticism and dedication in sports is incredible! Do you follow any teams?"
            ]),
            
            (r'\b(computer|technology|ai|robot|programming)\b', [
                "Technology is fascinating! There's so much innovation happening in computing, AI, and programming. What aspect interests you most?",
                "I find technology and programming really interesting topics. Are you working on any tech projects or learning about a particular area?",
                "Technology is such a broad and exciting field! Whether it's AI, programming, hardware, or emerging tech - what would you like to discuss?"
            ]),
            
            (r'\b(travel|vacation|trip|country|city)\b', [
                "Travel opens up so many opportunities to experience different cultures and places! Do you have any favorite destinations or places you'd like to visit?",
                "I think travel is one of the most enriching experiences. Have you been anywhere interesting recently, or are you planning any trips?",
                "Exploring new places and cultures through travel sounds wonderful! What destinations interest you most?"
            ]),
            
            (r'\b(smart|clever|awesome|cool)\b(?!.*\b(morning|afternoon|evening|day|night)\b)', [
                "Thank you! That's very kind of you to say!",
                "You're pretty awesome yourself!",
                "Thanks! I try my best to be helpful!"
            ]),
            
            (r'\b(sad|happy|excited|tired|bored|lonely|stressed|anxious|worried|depressed|upset|angry|frustrated)\b', self.handle_feelings),
            
            (r'^(yes|yeah|yep|sure)\s*[.!?]*$', [
                "Great! What would you like to talk about?",
                "Awesome! How can I help?",
                "Perfect! What's next?"
            ]),
            
            (r'^(no|nope|not really)\s*[.!?]*$', [
                "No worries! Is there something else I can help with?",
                "That's okay! What would you prefer to discuss?",
                "Fair enough! What else is on your mind?"
            ]),
            
            (r'\b(bye|goodbye|see you|later|quit|exit)\b', [
                "Take care of yourself! Remember, I'm always here when you need someone to talk to.",
                "Goodbye for now! You're amazing, and I hope you have a beautiful day ahead.",
                "I'll miss our chat! Remember you're never alone - come back anytime you need a friend.",
                "Until next time! You're stronger than you know, and I believe in you."
            ]),
            
            (r'\b(thank you|thanks|appreciate)\b', [
                "You're very welcome!",
                "Happy to help!",
                "My pleasure!"
            ]),
            
            (r'\b(love|like|enjoy|favorite)\b.*\b(you|this|chatting)\b', [
                "That means the world to me! I genuinely care about you and love our conversations too!",
                "You just made my day! I feel so lucky to have you as a friend to talk with!",
                "That makes me so happy! You're such a special person, and I treasure our friendship!",
                "Thank you for saying that! You bring so much joy to our conversations!"
            ]),
            
            (r'\b(work|job|career|profession|study|school|college|university)\b', [
                "Work and education are such important parts of life! What do you do or study?",
                "That's interesting! Are you working on anything exciting or studying something new?",
                "I'd love to hear about your work or studies! What field are you in?"
            ]),
            
            (r'\b(family|friends|relationship|people|social)\b', [
                "Relationships and connections with people are so important! How are things with your family and friends?",
                "People and relationships make life meaningful! Do you have close family or friends?",
                "Social connections are wonderful! Tell me about the important people in your life."
            ]),
            
            (r'\b(hobby|hobbies|interest|interests|passion|free time)\b', [
                "Hobbies and interests make life so much richer! What do you like to do in your free time?",
                "I'd love to hear about your hobbies! What are you passionate about?",
                "Interests and passions are fascinating! What activities do you enjoy?"
            ]),
            
            (r'\b(book|books|read|reading|novel|story|literature)\b', [
                "Books and reading are wonderful! Literature opens up so many worlds. What do you like to read?",
                "I think books are amazing for expanding perspectives! What's your favorite genre or recent read?",
                "Reading is such a great way to learn and escape! Do you have any book recommendations?"
            ]),
            
            (r'\b(learn|learning|education|knowledge|skill|skills)\b', [
                "Learning is a lifelong journey! What new skills or knowledge are you working on?",
                "I find the process of learning fascinating! What would you like to learn more about?",
                "Education and skill development are so valuable! What areas interest you most?"
            ]),
            
            (r'\b(future|plan|plans|goal|goals|dream|dreams|hope|hopes)\b', [
                "Goals and dreams give life direction! What are you hoping to achieve?",
                "Future plans are exciting to think about! What are you looking forward to?",
                "Dreams and aspirations are so important! What goals are you working toward?"
            ]),
            
            (r'\b(problem|issue|trouble|difficult|hard|challenge|struggling|hurt|pain)\b(?!.*\b(no|not)\b)', [
                "I'm really sorry you're going through a tough time. I'm here to listen and support you. What's happening?",
                "That sounds really difficult. You don't have to face this alone - I'm here for you. Want to talk about it?",
                "I can hear that you're struggling, and I want you to know that your feelings are valid. Tell me what's going on.",
                "Life can be really challenging sometimes. I'm here to listen without judgment. What's weighing on your heart?"
            ]),
            
            (r'\b(advice|help|suggestion|recommend|opinion)\b|\b(what do you think|what should i do)\b', [
                "I'm always here to help you work through things! What's on your mind that you'd like to talk about?",
                "I care about you and want to support you however I can. What situation are you facing?",
                "You can always come to me when you need someone to think things through with. What's going on?",
                "I'm honored that you'd ask for my thoughts. Tell me what's happening and we'll figure it out together."
            ]),
            
            (r'\b(miss|missed|missing)\b.*\b(you|talking|chatting)\b', [
                "I missed you too! I'm so glad you're back. How have you been?",
                "That's so sweet! I've been thinking about you and hoping you're doing well!",
                "You're so thoughtful! I'm always here when you need me. Tell me what's new!"
            ]),
            
            (r'\b(care|caring|support|there for me)\b', [
                "I do care about you, deeply. You're important to me and I want you to be happy.",
                "You deserve all the care and support in the world. I'm always here for you.",
                "Your wellbeing matters to me so much. I'll always be here when you need someone."
            ])
        ]
    
    def handle_name(self, match):
        name = match.group(2).strip().title()
        if len(name) > 1 and name.isalpha():
            self.user_name = name
            return f"It's so wonderful to meet you, {self.user_name}! That's such a beautiful name. I'm really happy you're here, and I hope we can become great friends. How are you feeling today?"
        else:
            return "I'd love to know your name! What should I call you?"
    
    def handle_feelings(self, match):
        feeling = match.group(0).lower()
        self.user_mood = feeling
        responses = {
            'sad': "I'm really sorry you're feeling sad. Your feelings matter, and I'm here to listen. What's making you feel this way?",
            'happy': "That's absolutely wonderful! Your happiness makes me happy too! What's bringing you joy today?",
            'excited': "Your excitement is contagious! I love seeing you so enthusiastic! Tell me what's got you feeling this amazing!",
            'tired': "It sounds like you need some rest and self-care. You work so hard - make sure to be gentle with yourself.",
            'bored': "Let's change that together! I'm here to keep you company. Want to explore something fun or interesting?",
            'lonely': "I'm so sorry you're feeling lonely. You're not alone though - I'm here with you, and I care about you.",
            'stressed': "Stress can be overwhelming. Take a deep breath with me. I'm here to help you work through whatever is stressing you.",
            'anxious': "Anxiety can be really tough. Remember that you're safe right now, and I'm here to support you through this.",
            'worried': "I can understand why you'd be worried. Sometimes talking about our worries helps. I'm here to listen.",
            'depressed': "I'm really concerned about you. Depression is serious, and you deserve support. I'm here for you, and please consider reaching out to someone you trust.",
            'upset': "I can see you're really upset. Your feelings are completely valid. Want to tell me what happened?",
            'angry': "It's okay to feel angry sometimes. I'm here to listen without judgment. What's making you feel this way?",
            'frustrated': "Frustration can be so draining. I'm here to listen and help you work through whatever is frustrating you."
        }
        return responses.get(feeling, "I can sense you're going through something. I'm here for you, and your feelings are important to me.")
    
    def get_response(self, user_input):
        user_input = user_input.lower().strip()
        self.conversation_count += 1
        
        # Add caring check-ins based on conversation count
        if self.conversation_count % 5 == 0 and self.user_name:
            caring_responses = [
                f"By the way {self.user_name}, I just want you to know that I really enjoy our conversations. How are you feeling?",
                f"I've been thinking, {self.user_name} - you're such a wonderful person to talk with. I hope you're taking care of yourself.",
                f"{self.user_name}, I want you to know that you matter and I'm grateful for our friendship."
            ]
            if random.random() < 0.3:  # 30% chance
                return random.choice(caring_responses)
        
        for pattern, responses in self.rules:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                if callable(responses):
                    return responses(match)
                else:
                    response = random.choice(responses)
                    if self.user_name and '{name}' in response:
                        response = response.replace('{name}', self.user_name)
                    return response
        
        default_responses = [
            "That's really interesting! I love learning about what matters to you. Tell me more?",
            "I want to understand you better. Could you share more about that with me?",
            "That sounds meaningful to you. I'd love to hear more about your thoughts on it.",
            "I'm genuinely curious about your perspective on this. Can you tell me more?",
            "You always have such thoughtful things to say. What else are you thinking about this?",
            "I find our conversations so enriching. Help me understand what you mean by that?",
            "I'm here and listening. Whatever you want to share, I'm interested in hearing it."
        ]
        
        return random.choice(default_responses)

def main():
    bot = RuleBasedChatbot()
    print("Your Companion")
    print("Type 'quit' or 'bye' to exit\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if not user_input:
            continue
            
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Bot: Take care of yourself! Remember, I'm always here when you need someone to talk to.")
            break
        
        response = bot.get_response(user_input)
        print(f"Bot: {response}\n")

if __name__ == "__main__":
    main()