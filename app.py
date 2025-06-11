import requests
from bs4 import BeautifulSoup
import json
import os
from twilio.rest import Client
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
MY_PHONE_NUMBER = os.getenv("MY_PHONE_NUMBER")

SIMPLIFY_INTERNSHIPS_README_URL = "https://raw.githubusercontent.com/SimplifyJobs/Summer2025-Internships/main/README.md"
MLH_HACKATHONS_URL = "https://mlh.io/hackathons/events"
LAST_KNOWN_DATA_FILE = "last_known_data.json"

def send_sms(message):
    """Sends an SMS message using Twilio."""
    if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, MY_PHONE_NUMBER]):
        print("Twilio credentials or phone numbers not fully configured in .env. Skipping SMS.")
        return False
    
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            to=MY_PHONE_NUMBER,
            from_=TWILIO_PHONE_NUMBER,
            body=message
        )
        print(f"SMS sent successfully! Message SID: {message.sid}")
        return True
    except Exception as e:
        print(f"Error sending SMS: {e}")
        return False

def load_last_known_data():
    if os.path.exists(LAST_KNOWN_DATA_FILE):
        with open(LAST_KNOWN_DATA_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print("Error decoding last_known_data.json. Starting fresh.")
                return {}
    return {}

def save_current_data(data):
    with open(LAST_KNOWN_DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def fetch_simplify_internships():
    """Fetches and parses internships from SimplifyJobs GitHub README."""
    print("Fetching Simplify internships...")
    response = requests.get(SIMPLIFY_INTERNSHIPS_README_URL)
    response.raise_for_status()
    
    lines = response.text.split('\n')
    internships = []
    in_table_section = False
    table_started = False
    header_found = False
    
    for line in lines:
        line = line.strip()
        
        if "# 💻 Software Engineering Internship Roles" in line:
            in_table_section = True
            continue
        
        if in_table_section:
            if line.startswith('Company | Role'):
                header_found = True
                table_started = True
                continue
            if table_started and line.startswith('---'):
                continue
            
            if table_started and line:
                parts = [p.strip() for p in line.split('|')]
                cleaned_parts = [p.strip() for p in parts if p.strip()]

                if len(cleaned_parts) >= 5:
                    company = cleaned_parts[0]
                    role = cleaned_parts[1]
                    location = cleaned_parts[2]
                    age = cleaned_parts[4]

                    internships.append({
                        'source': 'Simplify',
                        'company': company,
                        'role': role,
                        'location': location,
                        'age': age,
                        'id': f"simplify-{company}-{role}-{location}"
                    })
            elif table_started and not line:
                table_started = False
                in_table_section = False

    print(f"Found {len(internships)} Simplify internships.")
    return internships

def fetch_mlh_hackathons():
    """Fetches and parses MLH hackathons from their events page."""
    print("Fetching MLH hackathons...")
    try:
        response = requests.get(MLH_HACKATHONS_URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        hackathons = []
        event_cards = soup.find_all('div', class_='event-card')
        
        if not event_cards:
            print("No specific 'event-card' elements found. Trying generic links.")
            event_links = soup.find_all('a', href=True)
            for link in event_links:
                href = link.get('href')
                if href and '/hackathons/' in href and not href.endswith('/events'):
                    title = link.get_text(strip=True)
                    if title and title not in hackathons:
                        hackathons.append({
                            'source': 'MLH',
                            'title': title,
                            'url': f"https://mlh.io{href}" if href.startswith('/') else href,
                            'id': f"mlh-{title}-{href}"
                        })
            if not hackathons:
                print("Could not find any hackathon links with basic scraping.")

        for card in event_cards:
            title_tag = card.find('h3')
            link_tag = card.find('a', href=True)
            
            if title_tag and link_tag:
                title = title_tag.get_text(strip=True)
                url = link_tag.get('href')
                if url.startswith('/'):
                    url = f"https://mlh.io{url}"

                hackathons.append({
                    'source': 'MLH',
                    'title': title,
                    'url': url,
                    'id': f"mlh-{title}-{url}"
                })
        
        print(f"Found {len(hackathons)} MLH hackathons.")
        return hackathons

    except requests.exceptions.RequestException as e:
        print(f"Error fetching MLH hackathons: {e}")
        return []
    except Exception as e:
        print(f"Error parsing MLH hackathons HTML: {e}")
        return []

def main():
    print("--- Starting Automation Script ---")
    
    all_current_postings = []
    all_current_postings.extend(fetch_simplify_internships())
    all_current_postings.extend(fetch_mlh_hackathons())

    last_known_data = load_last_known_data()
    new_postings = []
    current_posting_ids = {p['id'] for p in all_current_postings}

    for posting in all_current_postings:
        is_new_entry = posting['id'] not in last_known_data
        
        if posting['source'] == 'Simplify' and (posting['age'] == '0d' or is_new_entry):
            new_postings.append(posting)
        elif is_new_entry:
            new_postings.append(posting)

    if new_postings:
        notification_message = "🚀 New Openings/Hackathons!\n\n"
        for p in new_postings:
            if p['source'] == 'Simplify':
                notification_message += f"💼 Simplify: {p['role']} at {p['company']} ({p['location']}) - Age: {p['age']}\n"
            elif p['source'] == 'MLH':
                notification_message += f"💻 MLH Hackathon: {p['title']} - {p.get('url', 'N/A')}\n"
        
        notification_message += "\nCheck your sources for more details!"
        print(f"\n--- Sending Notification ---\n{notification_message}")
        send_sms(notification_message)
    else:
        print("No new openings or hackathons found today.")

if __name__ == "__main__":
    main()
