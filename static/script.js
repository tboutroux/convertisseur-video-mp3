const form = document.querySelector('form');
const loader = document.getElementById('loading');

form.addEventListener('submit', () => {
    loader.style.display = '';
    form.style.display = 'none';
})