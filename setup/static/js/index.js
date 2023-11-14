const BASE_URL = 'http://127.0.0.1:8000'
let clearHistory = document.querySelector('#clear-history')
let chat = document.querySelector('#chat')
let inputPrompt = document.querySelector('#input-prompt')
let formPrompt = document.querySelector('form')


formPrompt.addEventListener('submit', (event) => {
    event.preventDefault()
    sendMessage()
})


clearHistory.addEventListener('click', (event) => {
    event.preventDefault()
    clearMessages()
})


async function sendMessage() {
    if (inputPrompt.value == '' || inputPrompt.value == null) return
    const formData = new FormData(formPrompt)
    let message = inputPrompt.value
    inputPrompt.value = ''

    let newBubble = createUserBubble()
    newBubble.innerHTML = message
    chat.appendChild(newBubble)

    let newBubbleBot = createBotBubble()
    chat.appendChild(newBubbleBot)
    goToChatEnd()

    const response = await fetch(`${ BASE_URL }/chat`, {
        method: 'POST',
        body: formData
    })

    const decoder = new TextDecoder()
    const respReader = response.body.getReader()
    let partialResponse = ''
    while (true) {
        // Aguarda e recebe o próximo pedaço da response da API
        const { done, value: responsePiece } = await respReader.read()
        if (done) break

        // Concatena o novo pedaço da response com a response parcial e atualiza na tela
        partialResponse += decoder.decode(responsePiece).replace(/\n/g, '<br>')
        newBubbleBot.innerHTML = partialResponse
        goToChatEnd()
    }
}


function createUserBubble() {
    let bubble = document.createElement('p')
    bubble.classList = 'chat__bubble chat__bubble--user'
    return bubble
}


function createBotBubble() {
    let bubble = document.createElement('p')
    bubble.classList = 'chat__bubble chat__bubble--bot'
    bubble.innerHTML = `<img src="/static/img/loader.svg" alt="Loader" height="20" />`
    return bubble
}


function goToChatEnd() {
    chat.scrollTop = chat.scrollHeight
}


function clearMessages(){
    fetch(`${ BASE_URL }/clear_history`, {method: 'GET'})
    chat.innerHTML = `
        <p class="chat__bubble chat__bubble--bot">
            Olá! Eu sou o assistente virtual da <b>EcoMart</b>.
            <br/>
            <br/>
            Como posso te ajudar?
        </p>
    `
}