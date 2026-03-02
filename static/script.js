const form = document.getElementById("chat-form");
const input = document.getElementById("message");
const chatBox = document.getElementById("chat-box");

form.addEventListener("submit", async function (e) {
    e.preventDefault();  //Prevent page reload

    const message = input.value.trim();
    if (!message) return;

    // Show user message
    chatBox.innerHTML += `<div class="user">You: ${message}</div>`;

    input.value = "";

    // Send to backend
    const response = await fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: message })
    });

    const data = await response.json();

    // Show bot response
    chatBox.innerHTML += `<div class="bot">Bot: ${data.response}</div>`;

    chatBox.scrollTop = chatBox.scrollHeight;
});
