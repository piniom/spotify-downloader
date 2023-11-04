import pyautogui 
import notify2

def display_notification(title: str, message: str):
    notify2.init("Spotify Downloader")
    n = notify2.Notification(title, message)
    n.show()