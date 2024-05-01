const BASE_URL = 'https://quantumkb.azurewebsites.net';

window.onload = function() {
    fetch(`${BASE_URL}/links`)
        .then(response => response.json())
        .then(links => {
            const container = document.getElementById('linksContainer');
            links.forEach(link => {
                const div = document.createElement('div');
                div.className = 'link';
                div.innerHTML = `
                    <img class="thumbnail" src="${link.thumbnail}" alt="Thumbnail">
                    <h2>${link.title}</h2>
                    <p class="description">${link.description}</p>
                    <a href="${link.url}" target="_blank">Visit Link</a>
                `;
                container.appendChild(div);
            });
        })
        .catch(error => console.error('Error fetching data:', error));
};
