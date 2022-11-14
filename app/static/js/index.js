const resultSection = document.getElementById("result-section");
const resultText = document.getElementById("result-text");
const resultSubtext = document.getElementById("result-subtext");

const textarea = document.getElementById("text");
const form = document.getElementById("entry-form");
const file = document.getElementById("file");

const BASE_URL = form.action;

const textValues = {
    default: {
        "result-text": "",
        "result-subtext":
            "Por favor ingresar y enviar el mensaje que se desea corregir.",
    },
    error: {
        "result-text": "ERROR",
        "result-subtext":
            "Se presento un error en el modelo o en el servidor. Por favor leer la consola.",
    },
};

async function submit(e) {
    e.preventDefault();
    resultSection.classList.remove("change");
    resultSection.classList.add("loading");
    resultText.innerText = "Cargando...";

    const textContent = textarea.value.trim();
    let result = null;

    // Print file.txt content
    if (file.files.length > 0) {
        const fileContent = await file.files[0].text();
        console.log(fileContent);
    }

    /*"response": "[x1, x2, x3, x4, x5]]",
        "original_input": data*/
    try {
        result = (
            await axios.post(`${BASE_URL}comment/predict`, { text: textContent })
        ).data;
        resultSection.classList.remove("change", "loading");
        resultSection.classList.add("change");
        applyText(result["response"], result["original_input"]);
    } catch (error) {
        applyText("error");
        console.error(error);
    }
}

async function onFileSelection() {
    const fileContent = await file.files[0].text();
    textarea.value = fileContent;
    submit(new Event("submit"));
}

function applyText(response, original_input) {
    var colours = response;
    const contents = original_input.split(" ");
    let text = "";
    for (i = 0; i < contents.length; i++) {
        if (colours[i] == 1) {
            text = text + "<font color='red'>" + " " + contents[i] + "</font>";
        } else if (colours[i] == 2) {
            text = text + "<font color='yellow'>" + " " + contents[i] + "</font>";
        } else if (colours[i] == 3) {
            text = text + "<font color='blue'>" + " " + contents[i] + "</font>";
        } else {
            text = text + " " + contents[i];
        }
    }
    resultText.innerHTML = text;
}

function onTextSelection() {
    resultSection.classList.remove("change", "loading");
    applyText("default");
}

textarea.addEventListener("input", onTextSelection);
form.addEventListener("submit", submit);
file.addEventListener("change", onFileSelection);
