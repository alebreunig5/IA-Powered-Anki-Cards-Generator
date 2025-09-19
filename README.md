# IA-Powered-Anki-Cards-Generator
Python script designed to automate the process of creating flashcards for Anki using the Gemini API model.

## Context
This script was created to automate the generation of English Cards to extend the vocabulary, but could be potencially used for anything that you want to learn. For example,
- Learn specific terminology
- Summaries
- Large explanations


## How It Works
The script, AnkiTranslation.py, uses the Google Gemini API to get detailed information about an English word, including:

- Meaning: A list of meanings in Spanish.
- Pronunciation: A simplified phonetic pronunciation.
- Etymology: The word's origin and history.
- Example Sentences: Contextual examples, including a specific one for medical use.

After the AI generates the data, the script presents it to the user. You can then choose to either create the card directly or edit the information before saving it. This allows for a quick and customizable workflow.

The script then uses the AnkiConnect add-on to automatically add the new flashcard to your specified deck in Anki. The flashcard has two sides:

- **Front**: The word, its pronunciation, and the medical example sentence.

- **Back**: A list of the word's meanings.

## Requirements and Setup
To use this script, you'll need the following:

1. Python Libraries
First, install the necessary Python libraries by running this command in your terminal:
```pip install -r requirements.txt```. The ```requirements.txt``` file should contain:

- ```google-generativeai```
- ```requests```
- ```python-dotenv```

2. API Key
The script requires a Google Gemini API key. Create a .env file in the same directory as the script and add your key like this:
```GOOGLE_API_KEY="your-api-key-here"```

3. Anki and AnkiConnect
You must have the Anki desktop application installed and running. AnkiConnect is an essential add-on that allows external applications to interact with Anki.

- Download and install the AnkiConnect add-on directly from Anki using the code: 2055492159.

- For more information on the capabilities of AnkiConnect, check out its official GitHub page: https://github.com/amikey/anki-connect.

## Customization
The script is designed to be easily modified to suit your specific needs. Here's how you can make it your own:

- Prompt Engineering: You can adjust the AI prompt within the obtener_info_completa_ia function. This allows you to change the type of information the AI generates. For instance, you could ask for more example sentences, different grammatical details, or information in a different language.

- Flashcard Format: The crear_tarjeta_anki function controls how the information is formatted and what content goes on the front and back of the flashcard. You can easily modify the contenido_front and contenido_back variables to change the layout.

- Anki Model: The script is currently set to use the "Basic" and "Basic (and reversed card)" models. You can change this to match any custom model you've created in Anki. Just update the modelName variable.

