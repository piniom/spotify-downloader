const buttons = [document.createElement('button'), document.createElement('button')];
for (button of buttons) {
    document.body.appendChild(button);
    button.style.position = 'fixed';
    button.style.bottom = '5px';
    button.style.right = '20%';
    button.style.zIndex = '1000'; 
    button.style.cursor = 'pointer'
    button.style.backgroundColor = 'rgba(0,0,0,0)'
    button.style.border = 'none'
    button.style.fontWeight = 'bold'
}

buttons[0].innerText = 'Local';
buttons[1].innerText = 'Watch';
buttons[1].style.right = '25%';

async function updateWatchButtonVisibility() {
    try {
        const response = await fetch('http://localhost:3000/watch');
        const data = await response.json();
        buttons[1].style.display = data.show ? 'block' : 'none';
    } catch (error) {
        console.error('Failed to fetch watch status:', error);
    }
}

function isSpotifyTrackPage() {
    return window.location.href.includes('https://open.spotify.com/track/');
}

if (!isSpotifyTrackPage()) {
    for (button of buttons) {
        button.style.display = 'none';
    }
    updateWatchButtonVisibility()
}

const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
        for (node of mutation.addedNodes) {
            for (button of buttons) {
                if (button == node) return;
            }
        }
        for (button of buttons) {
            if (isSpotifyTrackPage()) {
                button.style.display = 'block';
            } else {
                button.style.display = 'none';
            }
        }
      })
    
    updateWatchButtonVisibility()
});
observer.observe(document, { childList: true, subtree: true });

function fetch_server(isWatch) {
    const trackUrl = window.location.href;
    fetch('http://localhost:3000/track', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ trackUrl, isWatch }),
    });
}

buttons[0].addEventListener('click', () => {
    fetch_server(false)
});
buttons[1].addEventListener('click', () => {
    fetch_server(true)
});
