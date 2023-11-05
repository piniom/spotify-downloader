function initialize_buttons() {
    const buttons = [document.createElement('button'), document.createElement('button')];
    buttons
    for (button of buttons) {
        document.body.appendChild(button);
        button.style.position = 'fixed';
        button.style.bottom = '5px';
        button.style.right = '20%';
        button.style.zIndex = '1000'; 
        button.style.cursor = 'pointer'
        button.style.backgroundColor = 'rgba(0,0,0,0)';
        button.style.border = 'none';
        button.style.fontWeight = 'bold';
        button.style.fontSize = '1.5em'
    }

    buttons[0].innerText = '+ 💻';
    buttons[1].innerText = '+ ⌚';
    buttons[1].style.right = '25%';
    
    return buttons;
}

const buttons = initialize_buttons();

function isSpotifyTrackPage() {
    return window.location.href.includes('https://open.spotify.com/track/');
}

async function show_watch() {
    const response = await fetch('http://localhost:3000/watch');
    const data = await response.json();
    return data.show
}

async function is_server_ok() {
    try {
        await show_watch()
        return true
    } catch {
        return false
    }
}

async function updateButtonVisibility() {
    try {
        const is_track = isSpotifyTrackPage()
        buttons[0].style.display = is_track ? 'block' : 'none';
        buttons[1].style.display = is_track && await show_watch() ? 'block' : 'none';
    } catch (error) {
        for (button of buttons) {
            button.style.display = 'none'
        }
        return
    }
    
}

updateButtonVisibility()

const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
        for (node of mutation.addedNodes) {
            for (button of buttons) {
                if (button == node) return;
            }
        }
        updateButtonVisibility()
      })
});
is_server_ok().then((ok) => {
    if(ok) observer.observe(document, { childList: true, subtree: true })
});

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
