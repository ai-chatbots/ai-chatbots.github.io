// Dark mode toggle with localStorage support using Tailwind's dark mode classes
(function() {
  const toggleBtn = document.getElementById('themeToggle');
  if (toggleBtn) {
    // Check if dark mode was saved in localStorage
    if (localStorage.getItem('darkMode') === 'true') {
      document.documentElement.classList.add('dark');
    }
    toggleBtn.addEventListener('click', function() {
      document.documentElement.classList.toggle('dark');
      localStorage.setItem('darkMode', document.documentElement.classList.contains('dark'));
    });
  }
})();
