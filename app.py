import streamlit as st
import random

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'Page 1'
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'total_questions' not in st.session_state:
    st.session_state.total_questions = 0
if 'difficulty' not in st.session_state:
    st.session_state.difficulty = None
if 'next_game' not in st.session_state:
    st.session_state.next_game = None

# Sample data
elements = [
    {'name': 'Hidrogen', 'symbol': 'H', 'group': 'IA'},
    {'name': 'Helium', 'symbol': 'He', 'group': 'VIIIA'},
    {'name': 'Litium', 'symbol': 'Li', 'group': 'IA'},
    {'name': 'Karbon', 'symbol': 'C', 'group': 'IVA'},
    {'name': 'Oksigen', 'symbol': 'O', 'group': 'VIA'},
]

ions = [
    {'name': 'Bromat', 'formula': 'BrO3⁻'},
    {'name': 'Klorida', 'formula': 'Cl⁻'},
    {'name': 'Nitrat', 'formula': 'NO3⁻'},
    {'name': 'Sulfit', 'formula': 'SO3²⁻'},
    {'name': 'Amonium', 'formula': 'NH4⁺'},
]

def reset_game():
    st.session_state.score = 0
    st.session_state.total_questions = 0
    st.session_state.difficulty = None
    st.session_state.next_game = None

def render_page_1():
    st.markdown("<h1 style='text-align:center; color: pink;'>Checo Games</h1>", unsafe_allow_html=True)
    if st.button("Start Game", key="start_game", help="Mulai Permainan"):
        st.session_state.page = 'Page 2'

def render_page_2():
    st.markdown("<h2 style='text-align:center;'>Main Menu</h2>", unsafe_allow_html=True)
    if st.button("Guess the Element", key="guess_element"):
        st.session_state.page = 'Choose Difficulty'
        st.session_state.next_game = 'Guess the Element'
    if st.button("Guess the Ion", key="guess_ion"):
        st.session_state.page = 'Choose Difficulty'
        st.session_state.next_game = 'Guess the Ion'

def render_choose_difficulty():
    st.markdown("<h2 style='text-align:center;'>Choose Difficulty</h2>", unsafe_allow_html=True)
    st.write(f"Current Page: {st.session_state.page}")
    st.write(f"Next Game: {st.session_state.next_game}")
    if st.button("Easy", key="easy"):
        st.session_state.difficulty = 'easy'
        st.session_state.page = st.session_state.next_game
    if st.button("Medium", key="medium"):
        st.session_state.difficulty = 'medium'
        st.session_state.page = st.session_state.next_game
    if st.button("Hard", key="hard"):
        st.session_state.difficulty = 'hard'
        st.session_state.page = st.session_state.next_game

def render_guess_element():
    st.markdown("<h2 style='text-align:center;'>Guess the Element</h2>", unsafe_allow_html=True)
    question_types = [
        {'type': 'name', 'question': "Yang manakah unsur {element_name}?"},
        {'type': 'group', 'question': "Yang manakah unsur golongan {element_group}?"},
        {'type': 'symbol', 'question': "Apa nama unsur dari simbol {element_symbol}?"},
    ]

    correct_element = random.choice(elements)
    num_options = 2 if st.session_state.difficulty == 'easy' else 4 if st.session_state.difficulty == 'medium' else 6
    options = random.sample([e for e in elements if e != correct_element], num_options - 1) + [correct_element]
    random.shuffle(options)

    question_data = random.choice(question_types)
    question = question_data['question'].format(
        element_name=correct_element['name'],
        element_group=correct_element['group'],
        element_symbol=correct_element['symbol'],
    )

    st.write(f"<div style='text-align:center; margin-bottom:20px;'>{question}</div>", unsafe_allow_html=True)

    for i, option in enumerate(options):
        display_text = option['symbol'] if question_data['type'] == 'name' else option['name']
        if st.button(display_text, key=f"element_{i}"):
            if option == correct_element:
                st.success("Benar! Anda mendapat 10 poin.")
                st.session_state.score += 10
            else:
                st.error(f"Salah! Jawaban yang benar adalah {correct_element['name']} ({correct_element['symbol']}).")
            st.session_state.total_questions += 1
            st.experimental_rerun()

    if st.button("Give Up", key="give_up_element"):
        st.session_state.page = 'Page Result'

def render_guess_ion():
    st.markdown("<h2 style='text-align:center;'>Guess the Ion</h2>", unsafe_allow_html=True)
    question_types = [
        {'type': 'name', 'question': "Yang manakah ion {ion_name}?"},
        {'type': 'formula', 'question': "Apa nama ion dari simbol {ion_formula}?"},
    ]

    correct_ion = random.choice(ions)
    num_options = 2 if st.session_state.difficulty == 'easy' else 4 if st.session_state.difficulty == 'medium' else 6
    options = random.sample([i for i in ions if i != correct_ion], num_options - 1) + [correct_ion]
    random.shuffle(options)

    question_data = random.choice(question_types)
    question = question_data['question'].format(
        ion_name=correct_ion['name'],
        ion_formula=correct_ion['formula'],
    )

    st.write(f"<div style='text-align:center; margin-bottom:20px;'>{question}</div>", unsafe_allow_html=True)

    for i, option in enumerate(options):
        display_text = option['formula'] if question_data['type'] == 'name' else option['name']
        if st.button(display_text, key=f"ion_{i}"):
            if option == correct_ion:
                st.success("Benar! Anda mendapat 10 poin.")
                st.session_state.score += 10
            else:
                st.error(f"Salah! Jawaban yang benar adalah {correct_ion['name']} ({correct_ion['formula']}).")
            st.session_state.total_questions += 1
            st.experimental_rerun()

    if st.button("Give Up", key="give_up_ion"):
        st.session_state.page = 'Page Result'

def render_page_result():
    st.markdown("<h2 style='text-align:center;'>Result</h2>", unsafe_allow_html=True)
    if st.session_state.total_questions > 0:
        percentage = (st.session_state.score / (st.session_state.total_questions * 10)) * 100
    else:
        percentage = 0
    st.write(f"<div style='text-align:center;'>Hasil Akhir: {percentage:.2f}%</div>", unsafe_allow_html=True)
    st.write(f"<div style='text-align:center;'>Benar: {st.session_state.score // 10}</div>", unsafe_allow_html=True)
    st.write(f"<div style='text-align:center;'>Total Soal: {st.session_state.total_questions}</div>", unsafe_allow_html=True)
    if st.button("Menu"):
        st.session_state.page = 'Page 1'
        reset_game()

# Routing pages
if st.session_state.page == 'Page 1':
    render_page_1()
elif st.session_state.page == 'Page 2':
    render_page_2()
elif st.session_state.page == 'Choose Difficulty':
    render_choose_difficulty()
elif st.session_state.page == 'Guess the Element':
    render_guess_element()
elif st.session_state.page == 'Guess the Ion':
    render_guess_ion()
elif st.session_state.page == 'Page Result':
    render_page_result()
