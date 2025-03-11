// Dark mode toggle with localStorage support using Tailwind's dark mode classes
(function() {
  const toggleBtns = document.querySelectorAll('#themeToggle');
  // Apply saved preference to document root
  if (localStorage.getItem('darkMode') === 'true') {
    document.documentElement.classList.add('dark');
  }
  // Attach event listener to each toggle button found
  toggleBtns.forEach(toggleBtn => {
    toggleBtn.addEventListener('click', function() {
      document.documentElement.classList.toggle('dark');
      localStorage.setItem('darkMode', document.documentElement.classList.contains('dark'));
    });
  });
})();

// Interactive Dashboard Functionality (if used in pages with dashboard)
function showDashboardContent(section) {
  const dashboardContent = document.getElementById('dashboardContent');
  if (!dashboardContent) return;
  let content = '';
  switch(section) {
    case 'strategy':  // Renamed from 'overview' to 'strategy'
      content = '<h3 class="text-xl font-bold mb-2">Strategy</h3><p>This is the dashboard strategy content.</p>';
      break;
    case 'analytics':
      content = '<h3 class="text-xl font-bold mb-2">Analytics</h3><p>Here you can view detailed analytics of your chatbot performance.</p>';
      break;
    case 'settings':
      content = '<h3 class="text-xl font-bold mb-2">Settings</h3><p>Adjust your dashboard settings and preferences here.</p>';
      break;
    default:
      content = '<p>Click on a button above to view dashboard content.</p>';
  }
  dashboardContent.innerHTML = content;
}
