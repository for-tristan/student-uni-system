
const chatForm = document.getElementById("chatForm");
const userInput = document.getElementById("userInput");
const chatMessages = document.getElementById("chatMessages");
const sendButton = document.getElementById("sendButton");

// Add a message to the chat
function addMessage(text, sender) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", sender + "-message");

    const avatar = document.createElement("div");
    avatar.classList.add("avatar");
    avatar.textContent = sender === "bot" ? "🎓" : "👤";

    const content = document.createElement("div");
    content.classList.add("message-content");

    // Display text safely
    content.textContent = text;

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);

    chatMessages.appendChild(messageDiv);

    // Scroll to the latest message
    chatMessages.scrollTop = chatMessages.scrollHeight;

    return messageDiv;
}

// Send question to Flask and receive AI answer
chatForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const question = userInput.value.trim();

    if (!question) {
        return;
    }

    // Show the user's question
    addMessage(question, "user");

    userInput.value = "";
    sendButton.disabled = true;
    sendButton.textContent = "جاري الرد...";

    // Temporary loading message
    const loadingMessage = addMessage(
        "جاري البحث في معلومات الجامعة...",
        "bot"
    );

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question
            })
        });

        const data = await response.json();

        // Remove loading message
        loadingMessage.remove();

        if (!response.ok) {
            addMessage(
                data.answer || "حصل خطأ أثناء إرسال السؤال.",
                "bot"
            );
        } else {
            addMessage(data.answer, "bot");
        }

    } catch (error) {
        loadingMessage.remove();

        addMessage(
            "مش قادر أتصل بالسيرفر. تأكدي إن التطبيق شغال وحاولي تاني.",
            "bot"
        );

        console.error("Chat error:", error);

    } finally {
        sendButton.disabled = false;
        sendButton.textContent = "إرسال";
        userInput.focus();
    }
});