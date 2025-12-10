fetch("http://127.0.0.1:5000/info")
        .then(response => response.json())
        .then(data => {
            const location = data.location;
            const budget = data.budget;

            const elementBudget = document.getElementById('budget');
            const elementLocation = document.getElementById('location');

            elementBudget.innerHTML = budget + "€";
            elementLocation.innerHTML = location;
        })