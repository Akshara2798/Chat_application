// ================= CHAT FUNCTION =================
async function sendMessage() {

    // Get input field
    const input = document.getElementById("message");

    // Get message
    const message = input.value;

    // Empty check
    if (!message) return;

    // Send request to backend
    const response = await fetch("/chat", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            message: message
        })

    });

    // Convert response to JSON
    const data = await response.json();

    // Get chat box
    const chatBox = document.getElementById("chat-box");

    // Add messages
    chatBox.innerHTML += `
        <p><b>You:</b> ${message}</p>
        <p><b>AI:</b> ${data.reply}</p>
        <hr>
    `;

    // Clear input
    input.value = "";

    // Auto scroll
    chatBox.scrollTop = chatBox.scrollHeight;
}


// ================= PDF UPLOAD FUNCTION =================
async function sendMessage_1() {

    // Get file input
    const fileInput = document.getElementById("fileInput");

    // Get selected file
    const file = fileInput.files[0];

    // Check file selected
    if (!file) {

        alert("Please select a PDF");

        return;
    }

    // Create FormData
    const formData = new FormData();

    // Append file
    formData.append("file", file);

    // Send request
    const response = await fetch("/upload-pdf", {

        method: "POST",

        body: formData

    });

    // Convert response
    const data = await response.json();

    // Get chat box
    const chatBox = document.getElementById("chat-box");

    // PRINT SUCCESS MESSAGE
    chatBox.innerHTML += `

        <div class="message system-message">

            ✅ PDF Uploaded Successfully

        </div>

    `;

    // Auto scroll
    chatBox.scrollTop = chatBox.scrollHeight;
}