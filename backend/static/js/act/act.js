document.addEventListener("DOMContentLoaded", () => {
    const textArea = document.getElementById("text-area");
    const tagsContainer = document.getElementById("tags-container");
    const newTagInput = document.getElementById("new-tag");
    const addTagButton = document.getElementById("add-tag-button");
    const saveButton = document.getElementById("save-button");

    const tags = ["Prawo", "Ekonomia"]; // TODO: wyswietlac pobrane tagi z serwera z jinja variable
    const pdfUrl = "/static/pdf/sample.pdf"; // TODO: scieżka do odpowiedniego PDF z serwera 

    const pdfjsLib = window['pdfjs-dist/build/pdf'];
    pdfjsLib.GlobalWorkerOptions.workerSrc = `https://cdn.jsdelivr.net/npm/pdfjs-dist@3.1.81/build/pdf.worker.min.js`;

    const loadPdf = async (url) => {
        const pdfViewer = document.getElementById("pdf-viewer");
        const pdfDoc = await pdfjsLib.getDocument(url).promise;

        for (let i = 1; i <= pdfDoc.numPages; i++) {
            const page = await pdfDoc.getPage(i);
            const viewport = page.getViewport({ scale: 1 });
            const canvas = document.createElement("canvas");
            const context = canvas.getContext("2d");
            canvas.height = viewport.height;
            canvas.width = viewport.width;

            await page.render({ canvasContext: context, viewport }).promise;
            pdfViewer.appendChild(canvas);
        }
    };

    loadPdf(pdfUrl);

    const renderTags = () => {
        tagsContainer.innerHTML = "";
        tags.forEach((tag, index) => {
            const tagElement = document.createElement("div");
            tagElement.className = "tag";
            tagElement.innerHTML = `${tag} <button class="remove-tag" data-index="${index}">&times;</button>`;
            tagsContainer.appendChild(tagElement);
        });
    };

    tagsContainer.addEventListener("click", (event) => {
        if (event.target.classList.contains("remove-tag")) {
            const index = event.target.getAttribute("data-index");
            tags.splice(index, 1);
            renderTags();
        }
    });

    addTagButton.addEventListener("click", () => {
        const newTag = newTagInput.value.trim();
        if (newTag && !tags.includes(newTag)) {
            tags.push(newTag);
            newTagInput.value = "";
            renderTags();
        }
    });

    saveButton.addEventListener("click", () => {
        const updatedText = textArea.value;
        console.log("Zapisano zmiany:");
        console.log("Tekst:", updatedText);
        console.log("Tagi:", tags);

        fetch('/act/save', { // TODO: dodac parametr z id aktu
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: textArea.value, tags })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                window.location.reload();
            } else {
                alert("Wystąpił błąd podczas zapisu.");
            }
        });
    });

    renderTags();
});
