# index.py — Streamlit version of your flashcards app
# Run locally:  streamlit run index.py
# Deploy on Streamlit Cloud with requirements: streamlit

import os
import json
import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(page_title="Flashcard App", page_icon="🃏", layout="centered")


def load_flashcards():
    """
    Load flashcards from data.json.
    Accepts either {"flashcards":[...]} or a raw list [... ].
    """
    here = os.path.dirname(__file__)
    candidates = [
        os.path.join(here, "data.json"),
        os.path.join(here, "..", "data.json"),
    ]
    for p in candidates:
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict) and "flashcards" in data and isinstance(data["flashcards"], list):
                return data["flashcards"]
            if isinstance(data, list):
                return data
    return []


cards = load_flashcards()

# Inject your exact HTML+CSS+JS, but feed data from Python into JS.
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Flashcard App</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body {{
      font-family: 'Inter', sans-serif;
      background-color: #f3f4f6;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      padding: 1rem;
    }}
    .flashcard-container {{
      width: 100%;
      max-width: 640px;
      background-color: #ffffff;
      border-radius: 1.5rem;
      box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05);
      padding: 2rem;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      min-height: 500px;
    }}
    .card-content {{
      flex-grow: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      padding: 1rem;
      width: 100%;
    }}
    .card-content p {{
      font-size: 1.5rem;
      line-height: 1.75rem;
      font-weight: 500;
      color: #374151;
      margin-bottom: 1rem;
    }}
  </style>
</head>
<body>
  <div class="flashcard-container">
    <h1 class="text-3xl font-bold text-gray-800 mb-4">Speaking Flashcards for Jing</h1>
    <hr class="w-full h-1 bg-gray-200 rounded my-4">

    <div class="flex flex-col sm:flex-row justify-center gap-4 mb-6 w-full">
      <div class="flex items-center space-x-2">
        <input type="radio" id="sentences" name="card_type" value="sentence" class="form-radio text-blue-600 h-4 w-4" checked>
        <label for="sentences" class="text-lg font-medium text-gray-700">Sentences</label>
      </div>
      <div class="flex items-center space-x-2">
        <input type="radio" id="vocabulary" name="card_type" value="vocabulary" class="form-radio text-blue-600 h-4 w-4">
        <label for="vocabulary" class="text-lg font-medium text-gray-700">Vocabulary</label>
      </div>
    </div>

    <div class="text-gray-500 mb-4" id="card-counter"></div>

    <div class="card-content border border-gray-300 rounded-xl p-6 w-full flex flex-col justify-center items-center">
      <div id="chinese-text" class="text-2xl sm:text-3xl font-semibold text-gray-800 mb-4 text-center"></div>
      <div id="english-text" class="text-xl sm:text-2xl text-gray-600 transition-opacity duration-300 ease-in-out opacity-0 mt-4 text-center"></div>
    </div>

    <div class="flex flex-wrap justify-center gap-4 mt-8 w-full">
      <button id="show-hide-btn" class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-full shadow-lg transition-transform transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50">
        Show/Hide English
      </button>
      <button id="next-btn" class="bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-6 rounded-full shadow-lg transition-transform transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50">
        Next Card
      </button>
      <button id="shuffle-btn" class="bg-yellow-500 hover:bg-yellow-600 text-white font-bold py-3 px-6 rounded-full shadow-lg transition-transform transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:ring-opacity-50">
        Shuffle Cards
      </button>
    </div>
  </div>

  <script>
    // Data injected from Streamlit
    const flashcardData = {json.dumps(cards, ensure_ascii=False)};

    let filteredData = [];
    let cardIndex = 0;
    let showTranslation = false;

    const chineseText = document.getElementById('chinese-text');
    const englishText = document.getElementById('english-text');
    const cardCounter = document.getElementById('card-counter');
    const showHideBtn = document.getElementById('show-hide-btn');
    const nextBtn = document.getElementById('next-btn');
    const shuffleBtn = document.getElementById('shuffle-btn');
    const cardTypeRadios = document.getElementsByName('card_type');

    function shuffleArray(array) {{
      for (let i = array.length - 1; i > 0; i--) {{
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
      }}
    }}

    function filterAndShuffleCards() {{
      const selectedType = document.querySelector('input[name="card_type"]:checked')?.value || 'sentence';
      filteredData = (flashcardData || []).filter(card => card.type === selectedType);
      shuffleArray(filteredData);
      cardIndex = 0;
      showTranslation = false;
    }}

    function renderCard() {{
      if (filteredData.length === 0) {{
        chineseText.innerText = "No cards available.";
        englishText.innerText = "";
        englishText.classList.add('opacity-0');
        cardCounter.innerText = "0/0";
        return;
      }}
      const currentCard = filteredData[cardIndex];
      chineseText.innerText = currentCard.chinese || "";
      englishText.innerText = currentCard.english || "";
      if (showTranslation) {{
        englishText.classList.remove('opacity-0');
      }} else {{
        englishText.classList.add('opacity-0');
      }}
      cardCounter.innerText = `${{cardIndex + 1}}/${{filteredData.length}}`;
    }}

    function handleShowHide() {{ showTranslation = !showTranslation; renderCard(); }}
    function handleNextCard() {{ cardIndex = (cardIndex + 1) % filteredData.length; showTranslation = false; renderCard(); }}
    function handleShuffle() {{ filterAndShuffleCards(); renderCard(); }}

    showHideBtn.addEventListener('click', handleShowHide);
    nextBtn.addEventListener('click', handleNextCard);
    shuffleBtn.addEventListener('click', handleShuffle);

    cardTypeRadios.forEach(radio => {{
      radio.addEventListener('change', () => {{
        filterAndShuffleCards();
        renderCard();
      }});
    }});

    // Initial setup
    window.onload = () => {{
      filterAndShuffleCards();
      renderCard();
    }};

    // Keyboard shortcuts
    window.addEventListener('keydown', (e) => {{
      if (e.code === 'Space') {{ e.preventDefault(); handleShowHide(); }}
      if (e.code === 'ArrowRight') {{ e.preventDefault(); handleNextCard(); }}
    }});
  </script>
</body>
</html>"""

# Render the full HTML app inside Streamlit
# Increase height if needed
html(html_content, height=900, scrolling=True)
