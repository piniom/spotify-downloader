from selenium import webdriver
from selenium.webdriver.common.by import By
from notifier import display_notification
from driver import *
from flask import Flask, request, jsonify

GECKODRIVER_PATH = '/usr/local/bin/geckodriver'
SPOTIFY_DOWN_URL = 'https://spotifydown.com/'
DOWNLOAD_DIRECTORY = '/home/szymon/dev/spotify-downloader/downloads'
SEARCH_STRING = 'https://open.spotify.com/track/5hILNeWAz0uPjQ0ycg3zwp'

def automate_download_actions(driver: webdriver.Firefox, search_string: str, download_directory: str):
    driver.get(SPOTIFY_DOWN_URL)

    input_box = driver.find_element(by=By.TAG_NAME, value='input')
    input_box.send_keys(search_string)

    find_button(driver, 'Download').click()
    wait_for_download_list(driver)
    find_button(driver, 'Download').click()

    download_link = wait_for_link(driver, 'Download MP3')
    filename = sanitize_filename(download_link.get_attribute('download'))
    if check_file_exists(download_directory, filename):
        display_notification('File exists!', filename)
    else:
        driver.execute_script("arguments[0].click();", download_link)
        wait_file_exists(download_directory, filename)
        display_notification('File downloaded!', filename)
    

def automate_website_interaction(search_string: str):
    driver = get_driver(DOWNLOAD_DIRECTORY) 
    try:
        automate_download_actions(driver, search_string, DOWNLOAD_DIRECTORY)
    finally:
        driver.quit()

app = Flask("Spotify-Downloader-Server")
@app.route('/track', methods=['POST'])
def track():
    data = request.get_json()
    track_url = data.get('trackUrl')
    if track_url:
        try:
            automate_website_interaction(track_url)
            return jsonify({'message': 'Track handled successfully'}), 200
        except:
            return jsonify({'error': 'Server error'}), 400        
    return jsonify({'error': 'No trackUrl provided'}), 400

@app.route('/watch', methods=['GET'])
def watch():
    show_watch_button = True
    return jsonify(show=show_watch_button)

def dev_main():
     app.run(host='0.0.0.0', port=3000)

def main():
    from waitress import serve
    serve(app, host="0.0.0.0", port=3000)

if __name__ == '__main__':
    # main()
    dev_main()
