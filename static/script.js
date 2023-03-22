function onEventReceived(e) {
    addMessage(e.type, e.data);
}

function addMessage(type, content) {
    let template = document.querySelector("#message-template");
    let clone = template.content.cloneNode(true);
    let typeElement = clone.querySelector(".type")
    typeElement.innerText = type;
    typeElement.classList.add(type);
    clone.querySelector(".content").innerText = content;
    messagesDiv.appendChild(clone);
}

const messagesDiv = document.querySelector("div#messages");

const source = new EventSource("/events");
source.onerror = (err) => {
    console.log(err)
}



source.addEventListener("message", onEventReceived);
source.addEventListener("info", onEventReceived);
source.addEventListener("warning", onEventReceived);
source.addEventListener("error", onEventReceived);