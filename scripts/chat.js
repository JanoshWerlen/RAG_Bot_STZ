document.getElementById('chatForm').onsubmit = function(event) {
    event.preventDefault();
    var query = document.getElementById('queryInput').value;
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: query }),
    })
    .then(response => response.text())
    .then(data => {
        document.getElementById('responseArea').innerText = data;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
};


function toggleLog() {
    var logContainer = document.getElementById('logContainer');
    logContainer.classList.toggle('hide');
}