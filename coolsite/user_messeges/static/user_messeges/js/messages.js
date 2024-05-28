  var wsStart = 'ws://';
  if (window.location.protocol === 'https:') {
    wsStart = 'wss://';
  }
  var endpoint = wsStart + window.location.host + window.location.pathname;
  var socket = new WebSocket(endpoint);

  socket.onmessage = function(e) {
    console.log("Message", e.data);
    var chatContainer = document.querySelector(".chat-container");
    var jsonData = JSON.parse(e.data);
    var messageContainer = document.createElement('div');
    messageContainer.classList.add("message-container");


    if (jsonData.message_owner == "self") {
      messageContainer.classList.add("right");
    } else {
      messageContainer.classList.add("left");
    }
console.log(jsonData);

const messageElement = document.createElement('div');

 messageContainer.innerHTML = `
 <div class="messages">
     <img class="profile-pic" src="${jsonData.user_info.profile_image_url}">

     <p>${jsonData.message}</p>
<!--      <div class="time_mess" align="right">${jsonData.time}</div>-->
  </div>
  <hr>
`;

    chatContainer.appendChild(messageContainer);
    chatContainer.scrollTop = chatContainer.scrollHeight;
  };

  socket.onopen = function(e) {
    console.log("Open", e);
  }

  socket.onerror = function(e) {
    console.log("Error", e);
  }

  socket.onclose = function(e) {
    console.log("Close", e);
  }


  function sendMessage(e) {
    e.preventDefault();
    var messageInput = document.getElementById('message-input');
    var message = messageInput.value;
    socket.send(JSON.stringify({'message': message}));
    messageInput.value = '';
  }


  var form = document.querySelector('form');
  form.addEventListener('submit', sendMessage);


    document.querySelector('.dropbtn').addEventListener('click', function() {
    document.querySelector('.dropdown-content').style.display =
        document.querySelector('.dropdown-content').style.display === 'none' ? 'block' : 'none';
});


document.addEventListener("DOMContentLoaded", function(event) {
    var lastMessage = document.getElementById('last-message');
    if (lastMessage) {
        lastMessage.scrollIntoView();
    }
});