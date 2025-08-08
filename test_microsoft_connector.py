import requests

BASE_URL = "http://localhost:8084/api/v1/microsoft"
USER_EMAIL = "your-email@example.com"  # Replace with your test email

def test_auth_url():
    resp = requests.get(f"{BASE_URL}/auth-url", params={"user_email": USER_EMAIL})
    print("Auth URL:", resp.json())

def test_emails():
    resp = requests.get(f"{BASE_URL}/outlook/emails", params={"user_email": USER_EMAIL})
    print("Outlook Emails:", resp.json())

def test_files():
    resp = requests.get(f"{BASE_URL}/onedrive/files", params={"user_email": USER_EMAIL})
    print("OneDrive Files:", resp.json())

def test_events():
    resp = requests.get(f"{BASE_URL}/calendar/events", params={"user_email": USER_EMAIL})
    print("Calendar Events:", resp.json())

if __name__ == "__main__":
    test_auth_url()
    # After authenticating, run these:
    test_emails()
    test_files()
    test_events()
