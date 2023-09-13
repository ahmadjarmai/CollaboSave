const toggleSwitch = document.getElementById('toggleSwitch');
const container = document.querySelector('.container');

toggleSwitch.addEventListener('change', function () {
    if (this.checked) {
        container.classList.add('dark-mode');
        document.body.classList.add('dark-mode');
    } else {
        container.classList.remove('dark-mode');
        document.body.classList.remove('dark-mode');
    }
});