function sendBoolean(value) {
    fetch('http://127.0.0.1:5000/minigame/check', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({value: value})
    })
        .then ( response => response.json())
        .then(data => {
            console.log('Lähetetty:', data);
        })
        .catch(err => console.error('Post error:', err));
}