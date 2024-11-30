# Fandom Dialog Scraper

## Description
Fandom Dialog Scraper is a Python script designed to scrape character dialogues or quotes from Fandom pages, save them to a file, and optionally enhance them using AI-generated dialogues via Google's Gemini API.

---

## Getting Started

### Installation

1. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up your environment variables by copying the example `.env` file:
   ```bash
   cp .env-example .env
   ```

---

### Usage

#### 1. Retrieve the Fandom Page Link
   
   Get the URL of the character's "Dialog" or "Quotes" page on Fandom. For example:
   
   ```
   https://projectsekai.fandom.com/wiki/Shinonome_Akito/Dialog
   ```

#### 2. Run the Script
   Execute the script to scrape the dialogues or quotes:
   ```bash
   python fandom.py
   ```

#### 3. Enhance Dialogues (Optional)
   If you wish to enhance the scraped dialogues with AI-generated content, follow these steps:

   1. Obtain an API key from [Google AI Studio](https://aistudio.google.com/apikey).
   
   2. Add the API key to your `.env` file:
      ```env
      GEMINI_API_KEY=your_api_key_here
      ```

   3. Re-run the script and opt for the enhancement option when prompted.

---

## Features
- **Dialog Scraping:** Extracts character dialogues or quotes from Fandom pages.
- **File Output:** Saves dialogues in a neatly formatted text file.
- **AI-Generated Dialogues:** Enhance the content with additional unique dialogues using Gemini AI.

---

## Notes
- Ensure the URL is valid and corresponds to a "Dialog" or "Quotes" page.
- The `.env` file is essential for enabling the AI-enhancement feature.
- Use responsibly and comply with the Fandom platform's terms of service.

---

## Example Output

Upon successful execution, a file named after the character (e.g., `Shinonome_Akito_dialog.txt`) will be created, containing the scraped and/or enhanced dialogues.

Happy Scraping!

