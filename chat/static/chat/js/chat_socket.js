// Extract courseId written by django using json_script in the html template

const courseId = JSON.parse(document.getElementById("course-id").textContent);

// Creating a new websocket from the url
var url = `ws://${window.location.host}/ws/chat/room/${courseId}/`;

var chatSocket = new WebSocket(url);

// Logic to execute when a new message is received
chatSocket.onmessage = function (e) {
  var data = JSON.parse(e.data);
  var message = data.message;

  var dateOptions = { hour: "numeric", minute: "numeric", hour12: true };
  var datetime = new Date(data["datetime"]).toLocaleString("en", dateOptions);

  var isMe = data.user === "{{ request.user }}";
  var source = isMe ? "me" : "other";
  var name = isMe ? "Me" : data.user;

  var $chat = $("#chat");

  const html_msg =
    '<div class="message ' +
    source +
    '">' +
    "<strong>" +
    name +
    "</strong> " +
    '<span class="date">' +
    datetime +
    "</span><br>" +
    message +
    "</div>";

  $chat.append(html_msg);
};

// Closing a socket connection
chatSocket.onclose = function (e) {
  console.error(" Chat socket closed unexpectedly");
};

//Send message to the socket as well
var $input = $("#chat-message-input");
var $submit = $("#chat-message-submit");

$submit.click(function () {
  var message = $input.val();
  if (message) {
    // Send message in JSON format
    chatSocket.send(JSON.stringify({ message: message }));

    // Clear input
    $input.val("");
    $input.focus();
  }
});

// Focus on input as soon as the page loads so the user can start typing right away!
$input.focus();

// Send chat if the Enter key is pressed
$input.keyup(function (e) {
  if (e.which == 13) {
    $submit.click();
  }
});
