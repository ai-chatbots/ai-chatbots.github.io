(function() {
    const CHATBOT_URL = "http://127.0.0.1:8000";  // Replace with your production server domain if needed
    const sessionId = "session_" + Math.floor(Math.random() * 1000000);

    // ---------- Inject Styles ----------
    const style = document.createElement("style");
    style.innerHTML = `
        /* Expanded chat widget styles */
        #chatbot-widget {
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 350px;
            height: 450px;
            border-radius: 10px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
            background: white;
            font-family: Arial, sans-serif;
            overflow: hidden;
            display: none;  /* Initially hidden */
            flex-direction: column;
            z-index: 1000;
        }
        #chatbot-header {
            background: #00529B;
            color: white;
            padding: 10px;
            font-size: 16px;
            text-align: center;
            position: relative;
        }
        #chatbot-header .close-btn {
            position: absolute;
            right: 10px;
            top: 5px;
            background: transparent;
            border: none;
            color: white;
            font-size: 20px;
            cursor: pointer;
        }
        #chatbot-box {
            flex: 1;
            overflow-y: auto;
            padding: 10px;
            background: #f9f9f9;
        }
        .chatbot-message {
            margin: 8px 0;
            padding: 8px;
            border-radius: 6px;
            max-width: 80%;
            word-wrap: break-word;
        }
        .user-message {
            background: #4CAF50;
            color: white;
            align-self: flex-end;
        }
        .bot-message {
            background: #e0e0e0;
            color: black;
            align-self: flex-start;
        }
        #chatbot-input-area {
            display: flex;
            padding: 10px;
            background: #fff;
        }
        #chatbot-input {
            flex: 1;
            padding: 8px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        #chatbot-send-btn, #chatbot-voice-btn {
            background: #00529B;
            color: white;
            padding: 8px 12px;
            border: none;
            cursor: pointer;
            margin-left: 8px;
            border-radius: 4px;
        }
        #chatbot-send-btn:hover, #chatbot-voice-btn:hover {
            background: #003d7a;
        }
        #typing-indicator {
            font-style: italic;
            color: #666;
            margin-top: 5px;
            text-align: center;
            display: none;
        }
        /* Mobile styles for expanded widget */
        @media (max-width: 480px) {
            #chatbot-widget {
                width: 90%;
                height: 70%;
                bottom: 5%;
                right: 5%;
            }
            #chatbot-input-area {
                flex-direction: column;
            }
            #chatbot-send-btn, #chatbot-voice-btn {
                margin-left: 0;
                margin-top: 5px;
                width: 100%;
            }
        }
        /* Minimized widget (circle) styles */
        #chatbot-minimized {
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: #00529B;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 30px;
            cursor: pointer;
            z-index: 1000;
        }
    `;
    document.head.appendChild(style);

    // ---------- Create Minimized Widget (Circle) ----------
    const chatbotMinimized = document.createElement("div");
    chatbotMinimized.id = "chatbot-minimized";
    chatbotMinimized.innerHTML = "💬";
    document.body.appendChild(chatbotMinimized);

    // ---------- Create Expanded Chat Widget ----------
    const chatbotWidget = document.createElement("div");
    chatbotWidget.id = "chatbot-widget";
    chatbotWidget.innerHTML = `
        <div id="chatbot-header">
            Chat with us!
            <button class="close-btn" id="chatbot-close-btn">&times;</button>
        </div>
        <div id="chatbot-box"></div>
        <div id="typing-indicator">Bot is typing...</div>
        <div id="chatbot-input-area">
            <input type="text" id="chatbot-input" placeholder="Type a message..." />
            <button id="chatbot-send-btn">Send</button>
            <button id="chatbot-voice-btn">🎤 Voice</button>
        </div>
    `;
    document.body.appendChild(chatbotWidget);

    // ---------- Define Variables for Expanded Widget ----------
    const chatBox = document.getElementById("chatbot-box");
    const typingIndicator = document.getElementById("typing-indicator");
    const inputField = document.getElementById("chatbot-input");
    const sendButton = document.getElementById("chatbot-send-btn");
    const voiceButton = document.getElementById("chatbot-voice-btn");
    const closeButton = document.getElementById("chatbot-close-btn");

    function appendMessage(text, isUser = false) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("chatbot-message", isUser ? "user-message" : "bot-message");
        messageDiv.textContent = text;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // ---------- Text Message Sending (using advanced-chat endpoint) ----------
    async function sendTextMessage() {
        const text = inputField.value.trim();
        if (!text) return;

        appendMessage(text, true);
        inputField.value = "";

        try {
            typingIndicator.style.display = "block";

            // Use the advanced-chat endpoint to interact with agents
            const response = await fetch(`${CHATBOT_URL}/api/advanced-chat`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ session_id: sessionId, user_input: text })
            });

            typingIndicator.style.display = "none";

            if (response.ok) {
                const data = await response.json();
                appendMessage(`Bot (${data.agent}): ${data.response || "No response"}`, false);
            } else {
                appendMessage("Error: Could not process your message.", false);
            }
        } catch (error) {
            console.error(error);
            appendMessage("Error: Unable to connect to the server.", false);
            typingIndicator.style.display = "none";
        }
    }

    sendButton.addEventListener("click", sendTextMessage);
    inputField.addEventListener("keydown", (event) => {
        if (event.key === "Enter") sendTextMessage();
    });

    // ---------- Voice Input Feature ----------
    if (window.SpeechRecognition || window.webkitSpeechRecognition) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.lang = 'en-US';
        recognition.interimResults = false;
        
        voiceButton.addEventListener("click", () => {
            voiceButton.disabled = true;
            inputField.disabled = true;
            typingIndicator.style.display = "block";
            typingIndicator.textContent = "Listening...";
            recognition.start();
        });
        
        recognition.onresult = async function(event) {
            const transcript = event.results[0][0].transcript;
            appendMessage(transcript, true);
            recognition.stop();
        
            try {
                typingIndicator.textContent = "Processing...";
                // Call the new advanced voice endpoint instead of the old voice endpoint
                const response = await fetch(`${CHATBOT_URL}/api/advanced-voice`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ session_id: sessionId, user_input: transcript })
                });
                typingIndicator.style.display = "none";
                if (response.ok) {
                    const data = await response.json();
                    appendMessage(`Bot (${data.agent}): ${data.response || "No response"}`, false);
                } else {
                    appendMessage("Error: Could not process your voice message.", false);
                }
            } catch (error) {
                console.error(error);
                appendMessage("Error: Unable to connect to the server.", false);
                typingIndicator.style.display = "none";
            }
            voiceButton.disabled = false;
            inputField.disabled = false;
        };        

        recognition.onerror = function(event) {
            appendMessage("Voice recognition error: " + event.error, false);
            typingIndicator.style.display = "none";
            voiceButton.disabled = false;
            inputField.disabled = false;
        };

        recognition.onend = function() {
            voiceButton.disabled = false;
            inputField.disabled = false;
            typingIndicator.style.display = "none";
        };
    } else {
        voiceButton.style.display = "none";
    }

    // ---------- Clear Chat Feature ----------
    const clearButton = document.getElementById("chatbot-clear-btn");
    if (clearButton) {
        clearButton.addEventListener("click", () => {
            chatBox.innerHTML = "";
        });
    }

    // ---------- Fetch Chat History ----------
    async function fetchChatHistory() {
        try {
            const response = await fetch(`${CHATBOT_URL}/api/history/${sessionId}`);
            if (response.ok) {
                const data = await response.json();
                data.history.forEach(entry => {
                    if (entry.sender === "user") {
                        appendMessage(entry.message, true);
                    } else {
                        appendMessage(`Bot: ${entry.message}`, false);
                    }
                });
            }
        } catch (error) {
            console.error("Error fetching chat history:", error);
        }
    }

    fetchChatHistory();

    // ---------- Toggle Widget Display ----------
    // When the minimized circle is clicked, show the expanded chat widget and hide the circle.
    chatbotMinimized.addEventListener("click", () => {
        chatbotMinimized.style.display = "none";
        chatbotWidget.style.display = "flex";
    });

    // When the close button in the expanded widget is clicked, hide the expanded widget and show the minimized circle.
    closeButton.addEventListener("click", () => {
        chatbotWidget.style.display = "none";
        chatbotMinimized.style.display = "flex";
    });
})();
