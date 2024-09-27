document.getElementById('miFormulario').addEventListener('submit', function(event) {
    event.preventDefault();

    const nombre = document.getElementById('nombre').value;
    const email = document.getElementById('email').value;


    fetch('http://127.0.0.1:8000/users/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ nombre, email }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('resultado').innerText = 'Respuesta: ' + JSON.stringify(data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});
