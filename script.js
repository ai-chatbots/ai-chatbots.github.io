// Dark mode toggle with localStorage support
(function() {
    const toggleBtn = document.getElementById('themeToggle');
    if (toggleBtn) {
      // Set theme based on saved preference
      if (localStorage.getItem('darkMode') === 'true') {
        document.body.classList.add('dark-mode');
      }
      toggleBtn.addEventListener('click', function() {
        document.body.classList.toggle('dark-mode');
        localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
      });
    }
  })();
  
  // Toggle code example visibility with smooth transitions
  function toggleCode(elementId) {
    const codeBlock = document.getElementById(elementId);
    if (codeBlock) {
      if (codeBlock.style.maxHeight) {
        codeBlock.style.maxHeight = null;
        codeBlock.style.opacity = 0;
      } else {
        codeBlock.style.display = 'block';
        codeBlock.style.maxHeight = codeBlock.scrollHeight + "px";
        codeBlock.style.opacity = 1;
      }
    }
  }
  