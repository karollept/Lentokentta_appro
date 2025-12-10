'use strict';

class Merkki {
    constructor(array) {
        this.page = 1
        this.spot = 1
        this.array =array
    }

    Update () {
        if (this.spot < 8) {
            this.spot ++;
        }
        else if (this.spot >= 8) {
            this.spot = 1;
            this.page += 1;
        }
    }

    addPicture (name) {
        const src = `../static/img/${name}.png`;

        const id = this.page.toString() + this.spot.toString();
        const element = document.getElementById(id);

        if (!element) return;
        element.src = src;
    }
}
let merkki;
document.addEventListener("DOMContentLoaded", () => {
    fetch("/haalarimerkki/get_value")
        .then(response => response.json())
        .then(data => {
            const haalariMerkit = Array.isArray(data) ? data : [];
            merkki = new Merkki(haalariMerkit);
            console.log(merkki.array);

            for (let i = 0; i < merkki.array.length; i++) {
                merkki.addPicture(merkki.array[i]);
                merkki.Update();
            }

            let totalSpots = merkki.array.length;
            const placeHolderPic = ['greyCircle', 'greySquare'];
            while (totalSpots < 48) {
                let randomImg = Math.floor(Math.random() * 2);
                merkki.addPicture(placeHolderPic[randomImg]);
                merkki.Update();
                totalSpots++;
            }
        })
        .catch(err => {
            console.warn("Fetch epäonnistui:", err)

            merkki = new Merkki([]);
            const placeHolderPic = ['greyCircle', 'greySquare'];
            let totalSpots = 0;
            while (totalSpots < 48) {
                let randomImg = Math.floor(Math.random() * 2);
                merkki.addPicture(placeHolderPic[randomImg]);
                merkki.Update();
                totalSpots++;
            }
        })


});

