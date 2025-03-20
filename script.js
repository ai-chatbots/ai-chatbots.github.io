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
  });
})();

// Updated Dashboard Functionality
function showDashboardContent(section) {
  const dashboardContent = document.getElementById('dashboardContent');
  if (!dashboardContent) return;
  let content = '';
  switch(section) {
    case 'strategy':
      content = `
        <h3 class="text-2xl font-bold mb-4">Business Strategy</h3>
        <p class="mb-4">Outline your business strategy based on the AI agents you have integrated.</p>
        <textarea id="strategyText" class="w-full p-4 border border-gray-300 rounded" placeholder="Enter your business strategy here..."></textarea>
        <button class="mt-4 bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600" onclick="saveStrategy()">Save Strategy</button>
      `;
      break;
    case 'agents':
      content = `
        <h3 class="text-2xl font-bold mb-4">Build Your Agent System</h3>
        <div class="flex justify-center space-x-4 mb-4">
          <button class="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600" onclick="addAgent('square')">Add Square</button>
          <button class="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600" onclick="addAgent('circle')">Add Circle</button>
          <button class="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600" onclick="addAgent('triangle')">Add Triangle</button>
        </div>
        <div id="agentsArea" class="relative border border-dashed border-gray-400 h-80 mb-4"></div>
        <button class="bg-orange-500 text-white py-2 px-4 rounded hover:bg-orange-600" onclick="connectAgents()">Connect Agents</button>
      `;
      break;
    case 'ideaAnalytics':
      content = `
        <h3 class="text-2xl font-bold mb-4">Idea Analytics</h3>
        <p class="mb-4">View and analyze performance data for your new agent ideas. Customize dashboards, review trends, and make data-driven decisions.</p>
        <!-- You could later embed interactive charts here -->
        <div class="border p-4 rounded bg-gray-100 dark:bg-gray-800">
          <p>Interactive analytics charts coming soon...</p>
        </div>
      `;
      break;
    case 'ideaSettings':
      content = `
        <h3 class="text-2xl font-bold mb-4">Idea Settings</h3>
        <p class="mb-4">Configure settings for your new agent modules. Adjust parameters, integrate with other tools, and save custom configurations.</p>
        <div class="space-y-4">
          <label class="block">
            <span class="font-semibold">Integration API Key:</span>
            <input type="text" class="w-full border border-gray-300 p-2 rounded" placeholder="Enter API key">
          </label>
          <label class="block">
            <span class="font-semibold">Default Behavior:</span>
            <select class="w-full border border-gray-300 p-2 rounded">
              <option>Standard</option>
              <option>Aggressive</option>
              <option>Conservative</option>
            </select>
          </label>
          <button class="bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600">Save Settings</button>
        </div>
      `;
      break;
    default:
      content = '<p>Click on a button above to view dashboard content.</p>';
  }
  dashboardContent.innerHTML = content;
}

// Save Strategy Function
function saveStrategy() {
  const strategy = document.getElementById('strategyText').value;
  alert("Strategy saved: " + strategy);
}

// Agents Constructor Functions
function addAgent(shape) {
  const agentsArea = document.getElementById('agentsArea');
  const agent = document.createElement('div');
  agent.classList.add('agent', 'absolute', 'cursor-move');
  // Randomize initial position
  agent.style.top = Math.random() * 70 + "%";
  agent.style.left = Math.random() * 70 + "%";
  
  if(shape === 'square') {
    agent.style.width = "50px";
    agent.style.height = "50px";
    agent.style.backgroundColor = "#3b82f6";
    agent.textContent = "SQ";
  } else if(shape === 'circle') {
    agent.style.width = "50px";
    agent.style.height = "50px";
    agent.style.backgroundColor = "#ef4444";
    agent.style.borderRadius = "50%";
    agent.textContent = "CI";
  } else if(shape === 'triangle') {
    agent.style.width = "0";
    agent.style.height = "0";
    agent.style.borderLeft = "25px solid transparent";
    agent.style.borderRight = "25px solid transparent";
    agent.style.borderBottom = "50px solid #10b981";
    agent.textContent = "";
  }
  agent.setAttribute("draggable", "true");
  agent.addEventListener("dragstart", dragStart);
  agentsArea.appendChild(agent);
}

function dragStart(e) {
  e.dataTransfer.setData("text/plain", null);
  this.classList.add("dragging");
}

const agentsArea = document.getElementById("agentsArea");
if(agentsArea) {
  agentsArea.addEventListener("dragover", e => {
    e.preventDefault();
    const dragging = document.querySelector(".dragging");
    if (dragging) {
      const rect = agentsArea.getBoundingClientRect();
      dragging.style.left = (e.clientX - rect.left - dragging.offsetWidth/2) + "px";
      dragging.style.top = (e.clientY - rect.top - dragging.offsetHeight/2) + "px";
    }
  });
  agentsArea.addEventListener("drop", e => {
    e.preventDefault();
    const dragging = document.querySelector(".dragging");
    if(dragging) {
      dragging.classList.remove("dragging");
    }
  });
}

function connectAgents() {
  const agentsArea = document.getElementById('agentsArea');
  let canvas = document.getElementById('agentsCanvas');
  if (canvas) { canvas.remove(); }
  canvas = document.createElement('canvas');
  canvas.id = 'agentsCanvas';
  canvas.width = agentsArea.offsetWidth;
  canvas.height = agentsArea.offsetHeight;
  canvas.style.position = 'absolute';
  canvas.style.top = 0;
  canvas.style.left = 0;
  canvas.style.pointerEvents = 'none';
  agentsArea.appendChild(canvas);
  const ctx = canvas.getContext('2d');
  const agentElements = agentsArea.querySelectorAll('.agent');
  const positions = [];
  agentElements.forEach(agent => {
    const rect = agent.getBoundingClientRect();
    const containerRect = agentsArea.getBoundingClientRect();
    const x = rect.left - containerRect.left + rect.width / 2;
    const y = rect.top - containerRect.top + rect.height / 2;
    positions.push({ x, y });
  });
  ctx.strokeStyle = "#000";
  ctx.lineWidth = 2;
  for (let i = 0; i < positions.length - 1; i++) {
    ctx.beginPath();
    ctx.moveTo(positions[i].x, positions[i].y);
    ctx.lineTo(positions[i+1].x, positions[i+1].y);
    ctx.stroke();
  }
}

// ---------- Simple Auth UI Handling ----------

// This function updates the auth links in the top bar based on whether the user is logged in.
function updateAuthUI() {
  const loginLink = document.getElementById('openLoginModal');
  const signupLink = document.getElementById('openSignupModal');
  let logoutLink = document.getElementById('logoutLink');

  const token = localStorage.getItem('access_token');
  if (token) {
    // If logged in, hide login/signup and show logout link
    if (loginLink) loginLink.style.display = 'none';
    if (signupLink) signupLink.style.display = 'none';
    if (!logoutLink) {
      logoutLink = document.createElement('a');
      logoutLink.href = '#';
      logoutLink.id = 'logoutLink';
      logoutLink.className = "text-white font-semibold hover:text-yellow-300";
      logoutLink.textContent = "Logout";
      // Append the logout link to the same container as login/signup links.
      const authContainer = loginLink.parentElement;
      authContainer.appendChild(logoutLink);
      logoutLink.addEventListener('click', (e) => {
        e.preventDefault();
        localStorage.removeItem('access_token');
        alert('Logged out successfully.');
        updateAuthUI();
      });
    } else {
      logoutLink.style.display = 'inline-block';
    }
  } else {
    // Not logged in: show login and signup, hide logout
    if (loginLink) loginLink.style.display = 'inline-block';
    if (signupLink) signupLink.style.display = 'inline-block';
    if (logoutLink) logoutLink.style.display = 'none';
  }
}
updateAuthUI();

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
        document.getElementById('loginModal').classList.add('hidden');
        updateAuthUI();
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
        document.getElementById('signupModal').classList.add('hidden');
      }
    } catch (error) {
      showError('signupError', 'Network error. Please try again.');
    }
  });
}

// ---------- Modal Toggle Handling ----------
const loginModal = document.getElementById('loginModal');
const signupModal = document.getElementById('signupModal');
const openLoginModal = document.getElementById('openLoginModal');
const openSignupModal = document.getElementById('openSignupModal');
const closeLoginModal = document.getElementById('closeLoginModal');
const closeSignupModal = document.getElementById('closeSignupModal');

function setupModalClose(modal) {
  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      modal.classList.add('hidden');
    }
  });
}

if (openLoginModal) {
  openLoginModal.addEventListener('click', () => { loginModal.classList.remove('hidden'); });
}
if (openSignupModal) {
  openSignupModal.addEventListener('click', () => { signupModal.classList.remove('hidden'); });
}
if (closeLoginModal) {
  closeLoginModal.addEventListener('click', () => { loginModal.classList.add('hidden'); });
}
if (closeSignupModal) {
  closeSignupModal.addEventListener('click', () => { signupModal.classList.add('hidden'); });
}

setupModalClose(loginModal);
setupModalClose(signupModal);
