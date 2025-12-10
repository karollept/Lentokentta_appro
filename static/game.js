
async function arrayOfConnectionPrice (idents) {
    let prices = []

    for (let i = 0; i < idents.length; i++) {
        const ident1 = idents[i];

        const response = await fetch(`/game/get_price?ident1=${encodeURIComponent(ident1)}`);
        const data = await response.json()

        prices.push(data.price)
    }
    console.log(prices)
    return prices;
}



document.addEventListener('DOMContentLoaded', () => {
    fetch("/game/get_yhteydet")
        .then(response => response.json())
        .then(async data => {
            console.log(data)

            let elements = document.querySelectorAll('.choice')
            const count = Math.min(elements.length, data.length);

            //Kaikkien yhteyksien tunnisteet (ident)
            let connectionIdents = [];
            for (let i = 0; i < count; i++) {
                connectionIdents.push(data[i].ident);
            }

            // KAIKKI HINNAT
            const prices = await arrayOfConnectionPrice(connectionIdents);

            for (let i = 0; i < count; i++) {
                const element = elements[i]; // Tämä on .choice-div
                const destination = data[i].ident;
                const name = data[i].name;

                element.dataset.dest = destination;

                //  nimi päivitys lapsielementtiin (.dest-name)
                const nameElement = element.querySelector('.dest-name');
                if (nameElement) {
                    nameElement.innerHTML = name;
                }

                if (i < prices.length) { // hinta olemassa
                    const priceElement = element.querySelector('.dest-price');
                    if (priceElement) {
                        priceElement.innerHTML = prices[i] + "€";
                    }
                }
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
