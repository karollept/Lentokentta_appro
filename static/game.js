
document.addEventListener('DOMContentLoaded', () => {
    fetch("/game/get_yhteydet")
        .then(response => response.json())
        .then(data => {
            console.log(data)

            let elements;

            elements = document.querySelectorAll('.choice')
            const count = Math.min(elements.length, data.length);

            for (let i = 0; i < count; i++) {
                const element = elements [i];
                const destination = data[i].ident;
                const name = data[i].name;

                element.dataset.dest = destination;
                element.innerHTML = name;
            }


        })
        .catch(error => {
            console.error('Virhe haettaessa yhteyksiä:', error);
        });

})



const choices = document.querySelectorAll('.choice');
const flyBtn = document.getElementById('flyButton');
const destInput = document.getElementById('selectedDest');

choices.forEach(choice => {
    choice.addEventListener('click', () => {

        // Poista aiempi valinta
        choices.forEach(c => c.classList.remove('selected'));

        // Valitse klikattu
        choice.classList.add('selected');

        // Aseta lomakkeen arvo
        destInput.value = choice.dataset.dest;

        // Aktivoi nappi
        flyBtn.disabled = false;
    });
});
