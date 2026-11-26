

const formulario = document.querySelector(".main-div2-form");
const inputArchivo = document.querySelector(".main-div2-form-label-input");
const textoArchivoSubido = document.querySelector(".main-div2-div-archivoSubido");
const borrarArchivoSubido = document.querySelector(".main-div2-div-borrar");

formulario.addEventListener("submit", async (e)=>{
    e.preventDefault();

    const textoAI = document.querySelector(".main-div1");
    const textoH1 = document.querySelector(".main-div2--h1");
    const main =  document.querySelector(".main");
    const textoIAHTNL = document.querySelector(".main-div1--p");
    main.classList.add("main-section-end");
    main.classList.remove("main-section-center");

    textoIAHTNL.textContent = "Pensando...";
    textoArchivoSubido.textContent = "";
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
    borrarArchivoSubido.textContent = "";
    formData.append('prompt', textPromt.value);
    formData.append('ia-escogida', iaEscogida.value);
    for (const archivo of filesEscogido.files) {
        formData.append('files', archivo);
    }
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
        textoArchivoSubido.textContent = "";
        
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





inputArchivo.addEventListener("change", ()=>{
    console.log()
    console.log(inputArchivo.files)
    console.log(inputArchivo.files.length)
    if(inputArchivo.files.length > 0){
        textoArchivoSubido.textContent = `Se ha subido este archivo: ${inputArchivo.files[0]['name']}`;
        borrarArchivoSubido.textContent = "Borrar Arhivo";
    }else{
        textoArchivoSubido.textContent = "";

    }
})


borrarArchivoSubido.addEventListener("click", ()=>{
    console.log()
    console.log(inputArchivo.files)
    console.log(inputArchivo.files.length)
    inputArchivo.value = "";
    borrarArchivoSubido.textContent = "";
    textoArchivoSubido.textContent = "";
})


