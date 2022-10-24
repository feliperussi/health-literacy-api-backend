const resultSection = document.getElementById("result-section")
const resultText = document.getElementById("result-text")
const resultSubtext = document.getElementById("result-subtext")

const textarea = document.getElementById("text")
const form = document.getElementById("entry-form")

const BASE_URL = form.action

const textValues = {
    "default": {
        "result-text": "",
        "result-subtext": "Por favor ingresar y enviar el mensaje que se desea corregir."
    },
    "error": {
        "result-text": "ERROR",
        "result-subtext": "Se presento un error en el modelo o en el servidor. Por favor leer la consola."
    },
}

async function submit(e){
    e.preventDefault()
    resultSection.classList.remove("change")
    resultSection.classList.add("loading")
    resultText.innerText = "Cargando..."

    const textContent = textarea.value.trim()
    let result = null
    /*"response": "[x1, x2, x3, x4, x5]]",
      "original_input": data*/
    try {
        result = (await axios.post(`${BASE_URL}comment/predict`, {text: textContent})).data
        console.log(result)
        resultSection.classList.remove("change", "loading")
        resultSection.classList.add("change")
        applyText(result["response"], result["original_input"])

    } catch (error) {
        applyText("error")
        console.error(error)
    }


}
function applyText(response, original_input){
    var colours = response;
    const contents = original_input.split(" ");
    let text = "";
    for (i = 0; i < contents.length; i++){
        if (colours[i] == 1){
            text = text + "<font color='red'>" + " " + contents[i] + "</font>"
        }
        else if (colours[i] == 2){
            text = text + "<font color='yellow'>" + " " + contents[i] + "</font>"
        }
        else if (colours[i] == 3){
            text = text + "<font color='blue'>" + " " + contents[i] + "</font>"
        }
        else{
            text = text + " " + contents[i]
        }
    }
    console.log(text)
    resultText.innerHTML =  text
}

function onTextSelection(){
    resultSection.classList.remove("change", "loading")
    applyText("default")
}

textarea.addEventListener("input", onTextSelection)
form.addEventListener("submit", submit)