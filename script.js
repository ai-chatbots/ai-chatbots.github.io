// Toggle dark mode across pages
(function() {
    const toggleBtn = document.getElementById('themeToggle');
    if (toggleBtn) {
      // Check localStorage for dark mode preference
      if (localStorage.getItem('darkMode') === 'true') {
        document.body.classList.add('dark-mode');
      }
  
      toggleBtn.addEventListener('click', function() {
        document.body.classList.toggle('dark-mode');
        // Save preference
        localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
      });
    }
  })();
  
  // Function to toggle code examples in documentation sections
  function toggleCode(elementId) {
    const codeBlock = document.getElementById(elementId);
    if (codeBlock) {
      if (codeBlock.style.display === 'none' || codeBlock.style.display === '') {
        codeBlock.style.display = 'block';
      } else {
        codeBlock.style.display = 'none';
      }
    }
  }
  