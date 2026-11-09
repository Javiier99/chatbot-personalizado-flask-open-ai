

const formulario = document.querySelector(".main-div2-form");



formulario.addEventListener("submit", async (e)=>{
    e.preventDefault();

    const textoAI = document.querySelector(".main-div1");
    const textoH1 = document.querySelector(".main-div2--h1");
    const main =  document.querySelector(".main");

    main.classList.add("main-section-end");
    main.classList.remove("main-section-center");


    if(textoAI.classList.contains("hidden")){
        textoAI.classList.remove("hidden");
    }

    if(!textoH1.classList.contains("hidden")){
        textoH1.classList.add("hidden");
    }
    const textPromt = document.querySelector(".main-div2-form--textarea")
    const iaEscogida = document.querySelector(".main-div2-form--select");
    const filesEscogido =  document.getElementById("imagePdfInput");
    const formData = new FormData();
    formData.append('prompt', textPromt.value);
    formData.append('ia-escogida', iaEscogida.value);
    formData.append('files', filesEscogido.value);
    try{

        const response = await fetch('/', {
            method: 'POST',
            body: formData
        });
        textPromt.value = ""; 
        textPromt.textContent = "";
        filesEscogido.value = "";

        if(!response.ok){
            throw new Error("Error al comunicarse con la IA");
        }

        const data = await response.json();
        const textoIAHTNL = document.querySelector(".main-div1--p");
        textoIAHTNL.innerHTML = DOMPurify.sanitize(marked.parse(data['respuesta_ia']));

    }catch(error){
        console.error(`Hubo error ${error}`);
    }
    


})



const efectHoverP = document.querySelector(".main-div2-form-label");
const efectoHoverPSelect = document.querySelector(".main-div2-div--p");



efectHoverP.addEventListener("mouseenter", ()=>{
    efectoHoverPSelect.textContent = "Sube una imagen, PDF o Audio";
})



efectHoverP.addEventListener("mouseleave", ()=>{
    efectoHoverPSelect.textContent = "";
})
