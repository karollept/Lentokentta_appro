async function fetchStory() {
    const response = await fetch("/game/get_story");
    const data = await response.json();
    const textField = document.getElementById('storyContent')
    textField.textContent = data.story
}
