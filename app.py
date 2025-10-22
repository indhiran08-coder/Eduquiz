import streamlit as st
import random
import time

# ======================
# 🎨 PAGE CONFIG & PREMIUM UI THEME
# ======================
st.set_page_config(
    page_title="EduQuiz - Adaptive Quiz System",
    page_icon="🎓",
    layout="centered"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    html, body, [class*="css"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%) !important;
        background-attachment: fixed !important;
        background-size: 400% 400% !important;
        color: #1a1a2e !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .main, .block-container {
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 32px !important;
        padding: 48px 40px !important;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4), 
                    0 0 0 1px rgba(255, 255, 255, 0.3) inset !important;
        backdrop-filter: blur(40px);
        max-width: 800px;
        margin: 40px auto;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Header Styling */
    .quiz-header {
        text-align: center;
        margin-bottom: 40px;
        position: relative;
    }
    
    .quiz-title {
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 8px;
        letter-spacing: -0.02em;
        line-height: 1.1;
        animation: titlePulse 3s ease-in-out infinite;
    }
    
    @keyframes titlePulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    .quiz-subtitle {
        font-size: 1.25rem;
        color: #6b7280;
        font-weight: 500;
        margin-bottom: 8px;
    }
    
    .quiz-caption {
        font-size: 0.95rem;
        color: #9ca3af;
        font-weight: 400;
    }
    
    /* Stats Bar */
    .stats-container {
        display: flex;
        justify-content: space-around;
        gap: 16px;
        margin-bottom: 32px;
    }
    
    .stat-card {
        flex: 1;
        background: linear-gradient(135deg, #f8f9ff 0%, #fff5f7 100%);
        border-radius: 16px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 2px 12px rgba(240, 147, 251, 0.1);
        border: 2px solid rgba(240, 147, 251, 0.15);
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(240, 147, 251, 0.25);
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 900;
        background: linear-gradient(135deg, #667eea 0%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 4px;
    }
    
    .stat-label {
        font-size: 0.85rem;
        color: #6b7280;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Timer Styling */
    .timer-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-size: 200% 200%;
        border-radius: 20px;
        padding: 20px 32px;
        margin-bottom: 32px;
        box-shadow: 0 8px 32px rgba(240, 147, 251, 0.4);
        position: relative;
        overflow: hidden;
        animation: gradientMove 8s ease infinite;
    }
    
    @keyframes gradientMove {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .timer-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .timer {
        font-size: 1.5rem;
        color: white;
        text-align: center;
        font-weight: 700;
        letter-spacing: 0.05em;
        position: relative;
        z-index: 1;
    }
    
    .timer.warning {
        animation: timerWarning 0.5s ease-in-out infinite;
    }
    
    @keyframes timerWarning {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    /* Question Card */
    .question-card {
        background: linear-gradient(135deg, #f8f9ff 0%, #fff5f7 50%, #ffffff 100%);
        border-radius: 24px;
        padding: 40px 36px;
        margin-bottom: 32px;
        box-shadow: 0 4px 20px rgba(240, 147, 251, 0.12);
        border: 2px solid rgba(240, 147, 251, 0.15);
        position: relative;
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .question-card::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 6px;
        background: linear-gradient(180deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        border-radius: 24px 0 0 24px;
    }
    
    .question-number {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        color: white;
        padding: 6px 16px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 700;
        margin-bottom: 16px;
        letter-spacing: 0.05em;
        box-shadow: 0 4px 12px rgba(240, 147, 251, 0.3);
    }
    
    .difficulty-indicator {
        display: inline-block;
        margin-left: 12px;
        padding: 6px 16px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 0.05em;
    }
    
    .diff-easy {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
    }
    
    .diff-medium {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
    }
    
    .diff-hard {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
    }
    
    .question-text {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1a1a2e;
        line-height: 1.5;
        margin-top: 12px;
    }
    
    /* Radio Buttons */
    .stRadio {
        margin-top: 24px;
    }
    
    .stRadio > label {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: #374151 !important;
        margin-bottom: 16px !important;
    }
    
    .stRadio > div {
        gap: 12px;
    }
    
    .stRadio [data-baseweb="radio"] {
        background: white;
        border: 2px solid #e5e7eb;
        border-radius: 16px;
        padding: 18px 24px;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .stRadio [data-baseweb="radio"]:hover {
        border-color: #f093fb;
        background: linear-gradient(135deg, #f8f9ff 0%, #fff5f7 100%);
        transform: translateX(4px);
        box-shadow: 0 4px 12px rgba(240, 147, 251, 0.15);
    }
    
    .stRadio [data-baseweb="radio"] > div {
        font-size: 1.05rem !important;
        font-weight: 500 !important;
        color: #374151 !important;
    }
    
    /* Submit Button */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%) !important;
        background-size: 200% 200% !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 1.15rem !important;
        border-radius: 16px !important;
        padding: 18px 48px !important;
        margin-top: 28px !important;
        border: none !important;
        box-shadow: 0 8px 24px rgba(240, 147, 251, 0.4) !important;
        transition: all 0.3s ease !important;
        width: 100%;
        letter-spacing: 0.02em;
        animation: buttonGradient 3s ease infinite;
    }
    
    @keyframes buttonGradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 32px rgba(240, 147, 251, 0.5) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Feedback Messages */
    .stSuccess, .stError, .stWarning {
        font-size: 1.1rem !important;
        border-radius: 16px !important;
        padding: 20px 28px !important;
        margin-top: 24px !important;
        font-weight: 600 !important;
        border: none !important;
        animation: fadeIn 0.4s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: scale(0.95); }
        to { opacity: 1; transform: scale(1); }
    }
    
    .stSuccess {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.3) !important;
    }
    
    .stError {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
        color: white !important;
        box-shadow: 0 4px 16px rgba(239, 68, 68, 0.3) !important;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%) !important;
        color: white !important;
        box-shadow: 0 4px 16px rgba(245, 158, 11, 0.3) !important;
    }
    
    /* Progress Section */
    .progress-section {
        margin-top: 40px;
        padding-top: 32px;
        border-top: 2px solid #f3f4f6;
    }
    
    .progress-label {
        font-size: 0.95rem;
        font-weight: 600;
        color: #6b7280;
        margin-bottom: 12px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .stProgress > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%) !important;
        border-radius: 10px !important;
        height: 12px !important;
    }
    
    .stProgress > div {
        background: #f3f4f6 !important;
        border-radius: 10px !important;
        height: 12px !important;
    }
    
    /* Streak Badge */
    .streak-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: linear-gradient(135deg, #ff6b6b 0%, #feca57 100%);
        color: white;
        padding: 8px 20px;
        border-radius: 50px;
        font-size: 0.95rem;
        font-weight: 700;
        margin-bottom: 24px;
        box-shadow: 0 4px 16px rgba(255, 107, 107, 0.3);
        animation: bounceIn 0.6s ease-out;
    }
    
    @keyframes bounceIn {
        0% { transform: scale(0); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    
    /* Results Page */
    .results-container {
        text-align: center;
        padding: 40px 20px;
    }
    
    .results-title {
        font-size: 2.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 24px;
    }
    
    .score-display {
        font-size: 4rem;
        font-weight: 900;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 32px 0;
        line-height: 1;
    }
    
    .performance-badge {
        display: inline-block;
        padding: 16px 40px;
        border-radius: 50px;
        font-size: 1.3rem;
        font-weight: 800;
        margin: 24px 0;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
        animation: badgePop 0.6s ease-out;
    }
    
    @keyframes badgePop {
        0% { transform: scale(0) rotate(-180deg); }
        50% { transform: scale(1.1) rotate(10deg); }
        100% { transform: scale(1) rotate(0deg); }
    }
    
    .perf-excellent {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .perf-good {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
    }
    
    .perf-average {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
    }
    
    .perf-needswork {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
    }
    
    .difficulty-badge {
        display: inline-block;
        padding: 12px 32px;
        border-radius: 50px;
        font-size: 1.2rem;
        font-weight: 700;
        margin: 24px 0;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    }
    
    .difficulty-easy {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
    }
    
    .difficulty-medium {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
    }
    
    .difficulty-hard {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 16px;
        margin: 32px 0;
    }
    
    .result-stat {
        background: linear-gradient(135deg, #f8f9ff 0%, #fff5f7 100%);
        padding: 20px;
        border-radius: 16px;
        border: 2px solid rgba(240, 147, 251, 0.15);
    }
    
    .result-stat-value {
        font-size: 2rem;
        font-weight: 900;
        background: linear-gradient(135deg, #667eea 0%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .result-stat-label {
        font-size: 0.9rem;
        color: #6b7280;
        font-weight: 600;
        margin-top: 8px;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .quiz-title {
            font-size: 2.5rem;
        }
        .question-text {
            font-size: 1.25rem;
        }
        .main, .block-container {
            padding: 32px 24px !important;
        }
        .stats-container {
            flex-direction: column;
        }
        .stats-grid {
            grid-template-columns: 1fr;
        }
    }
    </style>
""", unsafe_allow_html=True)

# ======================
# 📘 QUIZ DATA: 20 QUESTIONS PER LEVEL
# ======================
data = {
    "easy": [
        {"question": "What is 2 + 2?", "options": ["3", "4", "5", "6"], "answer": "4"},
        {"question": "Which color is the sky?", "options": ["Blue", "Green", "Red", "Yellow"], "answer": "Blue"},
        {"question": "What is the capital of England?", "options": ["London", "Paris", "Berlin", "Madrid"], "answer": "London"},
        {"question": "How many legs does a dog have?", "options": ["2", "4", "6", "8"], "answer": "4"},
        {"question": "Which fruit is yellow and curved?", "options": ["Apple", "Banana", "Grape", "Cherry"], "answer": "Banana"},
        {"question": "What shape has three sides?", "options": ["Square", "Triangle", "Circle", "Rectangle"], "answer": "Triangle"},
        {"question": "Which animal says 'meow'?", "options": ["Dog", "Cat", "Cow", "Horse"], "answer": "Cat"},
        {"question": "Which day comes after Monday?", "options": ["Tuesday", "Wednesday", "Thursday", "Friday"], "answer": "Tuesday"},
        {"question": "What do bees make?", "options": ["Milk", "Honey", "Bread", "Eggs"], "answer": "Honey"},
        {"question": "Which liquid do plants need to grow?", "options": ["Oil", "Water", "Juice", "Coffee"], "answer": "Water"},
        {"question": "How many wheels does a bicycle have?", "options": ["1", "2", "3", "4"], "answer": "2"},
        {"question": "What color are strawberries?", "options": ["Green", "Red", "Blue", "Yellow"], "answer": "Red"},
        {"question": "Which is the smallest planet in the solar system?", "options": ["Earth", "Mercury", "Jupiter", "Mars"], "answer": "Mercury"},
        {"question": "What is the opposite of 'up'?", "options": ["Down", "Left", "Right", "Forward"], "answer": "Down"},
        {"question": "Which month is the first of the year?", "options": ["January", "March", "June", "December"], "answer": "January"},
        {"question": "How many fingers on one hand?", "options": ["3", "4", "5", "6"], "answer": "5"},
        {"question": "Which animal is known for its trunk?", "options": ["Lion", "Elephant", "Tiger", "Bear"], "answer": "Elephant"},
        {"question": "Which is a mammal?", "options": ["Whale", "Shark", "Crocodile", "Goldfish"], "answer": "Whale"},
        {"question": "What is H2O commonly known as?", "options": ["Salt", "Water", "Sugar", "Oxygen"], "answer": "Water"},
        {"question": "Which season is coldest?", "options": ["Spring", "Summer", "Autumn", "Winter"], "answer": "Winter"},
    ],
    "medium": [
        {"question": "What is the capital of France?", "options": ["Rome", "Paris", "London", "Berlin"], "answer": "Paris"},
        {"question": "Which planet is known as the Red Planet?", "options": ["Venus", "Mars", "Jupiter", "Earth"], "answer": "Mars"},
        {"question": "Who wrote 'Romeo and Juliet'?", "options": ["Shakespeare", "Dickens", "Tolkien", "Rowling"], "answer": "Shakespeare"},
        {"question": "What gas do plants breathe in?", "options": ["Oxygen", "Carbon Dioxide", "Nitrogen", "Helium"], "answer": "Carbon Dioxide"},
        {"question": "What is the largest ocean?", "options": ["Atlantic", "Pacific", "Indian", "Arctic"], "answer": "Pacific"},
        {"question": "How many continents are there?", "options": ["5", "6", "7", "8"], "answer": "7"},
        {"question": "What is the boiling point of water?", "options": ["50°C", "100°C", "150°C", "200°C"], "answer": "100°C"},
        {"question": "Which element has the chemical symbol 'O'?", "options": ["Gold", "Oxygen", "Silver", "Iron"], "answer": "Oxygen"},
        {"question": "What is the largest mammal?", "options": ["Elephant", "Blue Whale", "Giraffe", "Hippo"], "answer": "Blue Whale"},
        {"question": "Who painted the Mona Lisa?", "options": ["Van Gogh", "Da Vinci", "Picasso", "Rembrandt"], "answer": "Da Vinci"},
        {"question": "What is the smallest prime number?", "options": ["1", "2", "3", "5"], "answer": "2"},
        {"question": "Which country is known as the Land of the Rising Sun?", "options": ["China", "Japan", "Thailand", "Korea"], "answer": "Japan"},
        {"question": "Which organ pumps blood around the body?", "options": ["Lungs", "Heart", "Kidneys", "Liver"], "answer": "Heart"},
        {"question": "Who invented the telephone?", "options": ["Edison", "Bell", "Tesla", "Newton"], "answer": "Bell"},
        {"question": "What is the largest desert?", "options": ["Sahara", "Arabian", "Gobi", "Kalahari"], "answer": "Sahara"},
        {"question": "Which country has the most people?", "options": ["India", "USA", "China", "Brazil"], "answer": "China"},
        {"question": "What do you call animals that eat only plants?", "options": ["Carnivores", "Herbivores", "Omnivores", "Insectivores"], "answer": "Herbivores"},
        {"question": "Who discovered gravity?", "options": ["Einstein", "Newton", "Galileo", "Copernicus"], "answer": "Newton"},
        {"question": "What is the hardest natural substance?", "options": ["Gold", "Diamond", "Iron", "Platinum"], "answer": "Diamond"},
        {"question": "Which blood type is universal donor?", "options": ["A", "B", "O", "AB"], "answer": "O"},
    ],
    "hard": [
        {"question": "Who developed the theory of relativity?", "options": ["Newton", "Einstein", "Tesla", "Bohr"], "answer": "Einstein"},
        {"question": "What is the square root of 144?", "options": ["10", "12", "14", "16"], "answer": "12"},
        {"question": "What is the currency of Japan?", "options": ["Yuan", "Won", "Yen", "Ringgit"], "answer": "Yen"},
        {"question": "Which scientist proposed the three laws of motion?", "options": ["Newton", "Einstein", "Maxwell", "Galileo"], "answer": "Newton"},
        {"question": "What year did World War II end?", "options": ["1942", "1945", "1950", "1955"], "answer": "1945"},
        {"question": "What is the chemical formula for table salt?", "options": ["NaCl", "KCl", "CaCO3", "MgSO4"], "answer": "NaCl"},
        {"question": "Which planet has the most moons?", "options": ["Earth", "Jupiter", "Saturn", "Mars"], "answer": "Saturn"},
        {"question": "What is the longest river in the world?", "options": ["Amazon", "Nile", "Yangtze", "Mississippi"], "answer": "Nile"},
        {"question": "Who wrote 'War and Peace'?", "options": ["Tolstoy", "Dostoevsky", "Chekhov", "Pushkin"], "answer": "Tolstoy"},
        {"question": "Which element has the highest melting point?", "options": ["Carbon", "Tungsten", "Iron", "Gold"], "answer": "Tungsten"},
        {"question": "Who invented calculus?", "options": ["Newton", "Leibniz", "Gauss", "Euler"], "answer": "Newton"},
        {"question": "What is the capital of Canada?", "options": ["Toronto", "Ottawa", "Vancouver", "Montreal"], "answer": "Ottawa"},
        {"question": "Which is the largest internal organ?", "options": ["Heart", "Liver", "Lung", "Kidney"], "answer": "Liver"},
        {"question": "What is the powerhouse of the cell?", "options": ["Nucleus", "Mitochondria", "Ribosome", "Golgi"], "answer": "Mitochondria"},
        {"question": "Which country hosted the 2016 Summer Olympics?", "options": ["China", "Brazil", "Russia", "UK"], "answer": "Brazil"},
        {"question": "Which mathematician solved Fermat's Last Theorem?", "options": ["Andrew Wiles", "Gauss", "Euler", "Lagrange"], "answer": "Andrew Wiles"},
        {"question": "Who painted 'The Starry Night'?", "options": ["Van Gogh", "Monet", "Da Vinci", "Picasso"], "answer": "Van Gogh"},
        {"question": "What is the most abundant gas in Earth's atmosphere?", "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Argon"], "answer": "Nitrogen"},
        {"question": "Which is the smallest bone in the human body?", "options": ["Stapes", "Femur", "Tibia", "Scapula"], "answer": "Stapes"},
        {"question": "Who is known as the father of computers?", "options": ["Charles Babbage", "Alan Turing", "Bill Gates", "Ada Lovelace"], "answer": "Charles Babbage"},
    ]
}

DIFFICULTY_ORDER = ["easy", "medium", "hard"]

# ======================
# ⚙️ SESSION STATE SETUP
# ======================
def init_state():
    if "questions_done" not in st.session_state:
        st.session_state.questions_done = []
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "question_num" not in st.session_state:
        st.session_state.question_num = 0
    if "level_idx" not in st.session_state:
        st.session_state.level_idx = 0
    if "start_time" not in st.session_state:
        st.session_state.start_time = time.time()
    if "feedback" not in st.session_state:
        st.session_state.feedback = ""
    if "selected_option" not in st.session_state:
        st.session_state.selected_option = None
    if "finished" not in st.session_state:
        st.session_state.finished = False
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
    if "streak" not in st.session_state:
        st.session_state.streak = 0
    if "max_streak" not in st.session_state:
        st.session_state.max_streak = 0
    if "correct_answers" not in st.session_state:
        st.session_state.correct_answers = 0
    if "wrong_answers" not in st.session_state:
        st.session_state.wrong_answers = 0
    if "total_time" not in st.session_state:
        st.session_state.total_time = 0

init_state()

# ======================
# ⏱️ TIMER FUNCTION
# ======================
def display_timer(duration=30):
    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(0, duration - elapsed)
    warning_class = " warning" if remaining <= 10 else ""
    st.markdown(f"<div class='timer-container'><div class='timer{warning_class}'>⏱️ Time Remaining: {remaining}s</div></div>", unsafe_allow_html=True)
    if remaining == 0:
        st.session_state.finished = True
        st.warning("⌛ Time's up!")
        st.session_state.feedback = ""
        st.rerun()

# ======================
# 📊 SCORE REPORT
# ======================
def show_results():
    percentage = (st.session_state.score / 10) * 100
    
    # Determine performance level
    if percentage >= 90:
        perf_class = "perf-excellent"
        perf_text = "🏆 EXCELLENT!"
    elif percentage >= 70:
        perf_class = "perf-good"
        perf_text = "✨ GREAT JOB!"
    elif percentage >= 50:
        perf_class = "perf-average"
        perf_text = "👍 GOOD EFFORT!"
    else:
        perf_class = "perf-needswork"
        perf_text = "📚 KEEP PRACTICING!"
    
    st.markdown("<div class='results-container'>", unsafe_allow_html=True)
    st.markdown("<div class='results-title'>🎉 Quiz Completed!</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='score-display'>{st.session_state.score} / 10</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='performance-badge {perf_class}'>{perf_text}</div>", unsafe_allow_html=True)
    
    # Stats Grid
    st.markdown("<div class='stats-grid'>", unsafe_allow_html=True)
    st.markdown(f"""
        <div class='result-stat'>
            <div class='result-stat-value'>✅ {st.session_state.correct_answers}</div>
            <div class='result-stat-label'>Correct Answers</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
        <div class='result-stat'>
            <div class='result-stat-value'>❌ {st.session_state.wrong_answers}</div>
            <div class='result-stat-label'>Wrong Answers</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
        <div class='result-stat'>
            <div class='result-stat-value'>🔥 {st.session_state.max_streak}</div>
            <div class='result-stat-label'>Best Streak</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
        <div class='result-stat'>
            <div class='result-stat-value'>📊 {percentage:.0f}%</div>
            <div class='result-stat-label'>Accuracy</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    level_show = DIFFICULTY_ORDER[min(st.session_state.level_idx, 2)]
    difficulty_class = f"difficulty-{level_show}"
    emoji_map = {"easy": "🟢", "medium": "🟡", "hard": "🔴"}
    
    st.markdown(
        f"<div class='difficulty-badge {difficulty_class}'>{emoji_map[level_show]} Highest Level: {level_show.upper()}</div>",
        unsafe_allow_html=True
    )
    
    progress = min(st.session_state.score / 10, 1.0)
    st.progress(progress)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.balloons()
    
    if st.button("🔁 Retry Quiz"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

# ======================
# 🧠 QUIZ LOGIC
# ======================
st.markdown("""
    <div class='quiz-header'>
        <div class='quiz-title'>EduQuiz 🎓</div>
        <div class='quiz-subtitle'>Adaptive Quiz System</div>
        <div class='quiz-caption'>An intelligent quiz that adapts to your performance</div>
    </div>
""", unsafe_allow_html=True)

if not st.session_state.finished:
    display_timer(30)

# If quiz completed or time up
if st.session_state.question_num >= 10 or st.session_state.finished:
    show_results()
    st.stop()

# Stats Dashboard
level_names = {"easy": "🟢 Easy", "medium": "🟡 Medium", "hard": "🔴 Hard"}
current_level = DIFFICULTY_ORDER[st.session_state.level_idx]

st.markdown("<div class='stats-container'>", unsafe_allow_html=True)
st.markdown(f"""
    <div class='stat-card'>
        <div class='stat-value'>{st.session_state.score}</div>
        <div class='stat-label'>Score</div>
    </div>
    <div class='stat-card'>
        <div class='stat-value'>{level_names[current_level]}</div>
        <div class='stat-label'>Current Level</div>
    </div>
    <div class='stat-card'>
        <div class='stat-value'>{st.session_state.streak}</div>
        <div class='stat-label'>🔥 Streak</div>
    </div>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Show streak badge if streak >= 3
if st.session_state.streak >= 3:
    st.markdown(f"<div class='streak-badge'>🔥 {st.session_state.streak} Answer Streak! On Fire!</div>", unsafe_allow_html=True)

# Get current difficulty and question
level = DIFFICULTY_ORDER[st.session_state.level_idx]
questions_pool = [
    q for q in data[level]
    if (level, q['question']) not in st.session_state.questions_done
]
if not questions_pool:
    st.session_state.questions_done = [
        pair for pair in st.session_state.questions_done if pair[0] != level
    ]
    questions_pool = [
        q for q in data[level]
        if (level, q['question']) not in st.session_state.questions_done
    ]

# Only pick a new question if not already set for this step
if st.session_state.current_question is None:
    question = random.choice(questions_pool)
    st.session_state.current_question = question
else:
    question = st.session_state.current_question

# Difficulty indicator mapping
diff_class_map = {"easy": "diff-easy", "medium": "diff-medium", "hard": "diff-hard"}
diff_emoji_map = {"easy": "🟢", "medium": "🟡", "hard": "🔴"}

# Question UI
st.markdown(f"""
    <div class='question-card'>
        <span class='question-number'>QUESTION {st.session_state.question_num + 1}</span>
        <span class='difficulty-indicator {diff_class_map[level]}'>{diff_emoji_map[level]} {level.upper()}</span>
        <div class='question-text'>{question['question']}</div>
    </div>
""", unsafe_allow_html=True)

# Show radio options clearly
selected = st.radio(
    "Choose your answer:",
    question["options"],
    key=f"radio_{st.session_state.question_num}",
    index=0
)

# Show feedback if any
if st.session_state.feedback:
    if "Correct" in st.session_state.feedback:
        st.success(st.session_state.feedback)
    else:
        st.error(st.session_state.feedback)

# Move to next question after answer
if st.button("Submit Answer", key=f"submit_{st.session_state.question_num}"):
    elapsed_time = int(time.time() - st.session_state.start_time)
    st.session_state.total_time += elapsed_time
    
    st.session_state.selected_option = selected
    correct = selected == question["answer"]
    st.session_state.questions_done.append((level, question['question']))
    
    if correct:
        st.session_state.score += 1
        st.session_state.correct_answers += 1
        st.session_state.streak += 1
        
        # Update max streak
        if st.session_state.streak > st.session_state.max_streak:
            st.session_state.max_streak = st.session_state.streak
        
        # Feedback based on time
        if elapsed_time <= 10:
            st.session_state.feedback = "✅ Correct! Lightning fast! ⚡"
        elif elapsed_time <= 20:
            st.session_state.feedback = "✅ Correct! Great job! 🎯"
        else:
            st.session_state.feedback = "✅ Correct! Well done! 👍"
        
        if st.session_state.question_num < 2:
            if st.session_state.level_idx < 2:
                st.session_state.level_idx += 1
        else:
            st.session_state.level_idx = 2
    else:
        st.session_state.wrong_answers += 1
        st.session_state.streak = 0
        st.session_state.feedback = f"❌ Wrong! The correct answer is: {question['answer']}"
        if st.session_state.question_num >= 2 and st.session_state.level_idx > 0:
            st.session_state.level_idx -= 1
    
    st.session_state.question_num += 1
    st.session_state.start_time = time.time()
    st.session_state.selected_option = None
    st.session_state.current_question = None
    st.rerun()

# Progress bar
st.markdown("<div class='progress-section'>", unsafe_allow_html=True)
st.markdown("<div class='progress-label'>Quiz Progress</div>", unsafe_allow_html=True)
st.progress(st.session_state.question_num / 10)
st.markdown("</div>", unsafe_allow_html=True)
