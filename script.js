// Dark mode toggle with localStorage support using Tailwind's dark mode classes
(function() {
  const toggleBtns = document.querySelectorAll('#themeToggle');
  if (localStorage.getItem('darkMode') === 'true') {
    document.documentElement.classList.add('dark');
  }
  toggleBtns.forEach(toggleBtn => {
    toggleBtn.addEventListener('click', function() {
      document.documentElement.classList.toggle('dark');
      localStorage.setItem('darkMode', document.documentElement.classList.contains('dark'));
    });
    // Also listen to touch events
    toggleBtn.addEventListener('touchstart', function() {
      document.documentElement.classList.toggle('dark');
      localStorage.setItem('darkMode', document.documentElement.classList.contains('dark'));
    });
  });
})();

// Dashboard Functionality
function showDashboardContent(section) {
  const dashboardContent = document.getElementById('dashboardContent');
  if (!dashboardContent) return;
  let content = '';
  switch(section) {
    case 'strategy':
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

// ---------- Authentication Handling ----------

// Helper function to show error messages
function showError(elementId, message) {
  document.getElementById(elementId).textContent = message;
}

// Login form handling
const loginForm = document.getElementById('loginForm');
if (loginForm) {
  loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    showError('loginError', '');
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    try {
      const response = await fetch('http://127.0.0.1:8000/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
      });
      const data = await response.json();
      if (!response.ok) {
        showError('loginError', data.detail || 'Login failed');
      } else {
        localStorage.setItem('access_token', data.access_token);
        alert('Login successful!');
        loginModal.classList.add('hidden');
      }
    } catch (error) {
      showError('loginError', 'Network error. Please try again.');
    }
  });
}

// Sign Up form handling
const signupForm = document.getElementById('signupForm');
if (signupForm) {
  signupForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    showError('signupError', '');
    const full_name = document.getElementById('signupName').value;
    const email = document.getElementById('signupEmail').value;
    const password = document.getElementById('signupPassword').value;
    try {
      const response = await fetch('http://127.0.0.1:8000/auth/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ full_name, email, password })
      });
      const data = await response.json();
      if (!response.ok) {
        showError('signupError', data.detail || 'Sign up failed');
      } else {
        alert('Sign up successful! You can now log in.');
        signupModal.classList.add('hidden');
      }
    } catch (error) {
      showError('signupError', 'Network error. Please try again.');
    }
  });
}

// ---------- Modal Toggle Handling with Touch Events ----------
const loginModal = document.getElementById('loginModal');
const signupModal = document.getElementById('signupModal');
const openLoginModal = document.getElementById('openLoginModal');
const openSignupModal = document.getElementById('openSignupModal');
const closeLoginModal = document.getElementById('closeLoginModal');
const closeSignupModal = document.getElementById('closeSignupModal');

if (openLoginModal) {
  openLoginModal.addEventListener('click', () => {
    loginModal.classList.remove('hidden');
  });
  openLoginModal.addEventListener('touchstart', () => {
    loginModal.classList.remove('hidden');
  });
}

if (openSignupModal) {
  openSignupModal.addEventListener('click', () => {
    signupModal.classList.remove('hidden');
  });
  openSignupModal.addEventListener('touchstart', () => {
    signupModal.classList.remove('hidden');
  });
}

if (closeLoginModal) {
  closeLoginModal.addEventListener('click', () => {
    loginModal.classList.add('hidden');
  });
  closeLoginModal.addEventListener('touchstart', () => {
    loginModal.classList.add('hidden');
  });
}

if (closeSignupModal) {
  closeSignupModal.addEventListener('click', () => {
    signupModal.classList.add('hidden');
  });
  closeSignupModal.addEventListener('touchstart', () => {
    signupModal.classList.add('hidden');
  });
}
