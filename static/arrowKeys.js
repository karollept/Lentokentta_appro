'use strict';
class Counter {
    constructor() {
        this.page = 1
    }

    left () {
        if (this.page > 1) {
            this.page --;
        }
        else if (this.page === 1) {
            this.page = 6
        }
    }

    right () {
        if (this.page === 6) {
            this.page = 1
        } else if (this.page < 6) {
            this.page ++;
        }
    }

    number() {
        const element = document.getElementById('page');
        element.src = "../static/img/sivu_" + this.page + ".png";
    }

}

const page = new Counter();

const rightArrow = document.getElementById('arrowRight')
const leftArrow = document.getElementById('arrowLeft')

rightArrow.addEventListener('click', () => {
    const id1 = "page" + page.page
    const element1 = document.getElementById(id1)
    element1.className = "merkitPage"

    page.right();
    page.number();

    const id = "page" + page.page
    const element = document.getElementById(id)
    element.className = "merkitPage visible"

});

leftArrow.addEventListener('click', () => {
    const id1 = "page" + page.page
    const element1 = document.getElementById(id1)
    element1.className = "merkitPage"

    page.left();
    page.number();

    const id = "page" + page.page
    const element = document.getElementById(id)
    element.className = "merkitPage visible"
});

