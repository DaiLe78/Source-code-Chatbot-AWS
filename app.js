// Hàm gửi tin nhắn người dùng tới AWS Lex qua API Gateway
async function sendMessage() {
    const userInput = document.getElementById("user-input").value.trim(); // Lấy tin nhắn từ input và bỏ khoảng trắng
    if (userInput === "") return; // Không gửi yêu cầu nếu input trống

    // Hiển thị tin nhắn người dùng trong giao diện
    displayMessage(userInput, "user");

    // Gửi tin nhắn đến API Gateway để xử lý với Lex
    try {
        const response = await fetch('https://de3tne9q7e.execute-api.ap-southeast-2.amazonaws.com/dev', { // URL của API Gateway (thay đổi với URL của bạn)
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', // Định dạng JSON cho dữ liệu gửi đi
            },
            body: JSON.stringify({
                message: userInput,  // Tin nhắn người dùng
                userId: generateUserId() // ID người dùng ngẫu nhiên
            }),
        });

        if (response.ok) {
            const data = await response.json();
            if (data.message) {
                // Hiển thị tin nhắn trả về từ bot (Lex)
                displayMessage(data.message, "bot");
            } else {
                console.error('No valid response from Lex');
            }
        } else {
            console.error('Error:', response.statusText); // Xử lý lỗi nếu không thành công
        }
    } catch (error) {
        console.error('Error when sending message to API Gateway:', error); // Xử lý lỗi kết nối
    }

    // Làm sạch input sau khi gửi tin nhắn
    document.getElementById("user-input").value = '';
}

// Hàm hiển thị tin nhắn trong giao diện
function displayMessage(message, sender) {
    const messageContainer = document.createElement("div");
    messageContainer.classList.add("message", sender);
    messageContainer.textContent = message;

    document.getElementById("chat-messages").appendChild(messageContainer);

    // Tự động cuộn xuống khi có tin nhắn mới
    const chatMessages = document.getElementById("chat-messages");
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Hàm tạo userId ngẫu nhiên
function generateUserId() {
    return 'user-' + Math.random().toString(36).substr(2, 9);
}

// Lắng nghe sự kiện nhấn nút "Send" hoặc "Enter" để gửi tin nhắn
document.getElementById("send-btn").addEventListener("click", sendMessage);
document.getElementById("user-input").addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
        sendMessage();
    }
});