import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")  
if not api_key:
    raise ValueError("API key not found. Please add it to the .env file.")
genai.configure(api_key=api_key)

def scrape_character_dialogs(base_url):
    try:

        character_name = unquote(base_url.split('/')[-2].replace('_', ' '))

       
        output_file = f"{character_name}_dialog.txt"


        response = requests.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        dialogs = []


        if '/Dialog' in base_url:
            dialog_headers = soup.find_all('th', string=lambda text: text and "Dialog" in text)
            if not dialog_headers:
                print(f"No dialog sections found for character {character_name}.")
                return

            for dialog_header in dialog_headers:
                table = dialog_header.find_parent('table')
                if not table:
                    print(f"No dialog tables found for character {character_name}.")
                    continue

                dialog_rows = table.find_all('tr')[1:]  # Skip header
                for row in dialog_rows:
                    cells = row.find_all('td')
                    for cell in cells:
                        if cell.find('a') or cell.has_attr('rowspan'):
                            continue
                        dialog_text = cell.get_text(strip=True)
                        if dialog_text:
                            dialogs.append(f"{character_name}: {dialog_text}")

        elif '/Quotes' in base_url:
            quote_tables = soup.find_all('table', class_='cquote')
            if not quote_tables:
                print(f"No quote sections found for character {character_name}.")
                return

            for table in quote_tables:
                rows = table.find_all('tr')
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) >= 3:
                        quote_text = cells[1].get_text(strip=True)
                        if quote_text:
                            dialogs.append(f"{character_name}: {quote_text}")

        else:
            print("URL not recognized as a Dialog or Quotes page.")
            return

    
        if dialogs:
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write('\n'.join(dialogs))
            print(f"Dialogs successfully saved to {output_file}.")
        else:
            print(f"No dialogs found for character {character_name}.")


        enhance = input("Want to enhance dialogue? (y/n): ").strip().lower()
        if enhance == 'y':
            try:
                num_additional = int(input("How many additional dialogues? "))
                new_dialogs = generate_dialog_gemini(character_name, dialogs, num_additional)
                dialogs.extend(new_dialogs)


                with open(output_file, 'w', encoding='utf-8') as file:
                    file.write('\n'.join(dialogs))
                print(f"Dialogs updated with {num_additional} additional dialogues.")
            except ValueError:
                print("Input must be a valid number.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")

def generate_dialog_gemini(character_name, existing_dialogs, count):
    model = genai.GenerativeModel('gemini-pro')
    new_dialogs = set(existing_dialogs)

    while len(new_dialogs) < len(existing_dialogs) + count:
        try:
      
            response = model.generate_content(
                f"Generate a unique, creative dialogue for a character named '{character_name}'. "
                f"The dialogue should be interesting and not repeat any existing dialogues. "
                f"Provide just the dialogue without any additional context or explanation."
            )

            generated_dialog = response.text.strip()
            if generated_dialog and generated_dialog not in new_dialogs:
                new_dialogs.add(f"{character_name}: {generated_dialog}")
        except Exception as e:
            print(f"Error generating dialogue: {e}")
            break
    
    return list(new_dialogs - set(existing_dialogs))


base_url = input("Enter character page URL: ")
scrape_character_dialogs(base_url)
