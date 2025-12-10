function sendBoolean(value) {
    fetch('/minigame/check', {
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