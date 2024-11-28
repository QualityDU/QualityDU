document.addEventListener("DOMContentLoaded", () => {
    const textArea = document.getElementById("text-area");
    const tagsContainer = document.getElementById("tags-container");
    const newTagInput = document.getElementById("new-tag");
    const addTagButton = document.getElementById("add-tag-button");
    const saveButton = document.getElementById("save-button");
    console.log(addTagButton)
    const tags = actTags; 
    const pdfUrl = `https://dziennikustaw.gov.pl/${actDuCode}.pdf`;
    console.log(pdfUrl);
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

    // loadPdf(pdfUrl);

    const renderTags = () => {
        tagsContainer.innerHTML = "";
        tags.forEach((tag, index) => {
            const tagElement = document.createElement("div");
            tagElement.className = "tag";
            if (userRole === "admin" || userRole === "expert") {
                tagElement.innerHTML = `${tag} <button class="remove-tag" data-index="${index}">&times;</button>`;
            } else {
                tagElement.innerHTML = tag;
            }
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

    if (addTagButton) {
        addTagButton.addEventListener("click", () => {
            const newTag = newTagInput.value.trim();
            if (newTag && !tags.includes(newTag)) {
                tags.push(newTag);
                newTagInput.value = "";
                renderTags();
            }
        });
    }
    
    if (saveButton) {
        saveButton.addEventListener("click", () => {
            const updatedText = textArea.value;
            console.log(actId);
            fetch('/act/save', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ act_id: actId, text: textArea.value, tags })
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
    }
    renderTags();

    function isMobile() { // https://medium.com/geekculture/detecting-mobile-vs-desktop-browsers-in-javascript-ad46e8d23ce5
        const regex = /Mobi|Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i;
        return regex.test(navigator.userAgent);
      }
  
      function createPDFViewer() {
        let actPdfViewerContainer = document.getElementById('act-pdf-viewer-container');
        let actPdfViewer;
        if (isMobile()) {
          actPdfViewer = document.createElement('iframe');
          actPdfViewer.setAttribute('id', 'act-pdf-viewer');
          actPdfViewer.setAttribute('class', 'pdf');
          actPdfViewer.setAttribute('src', `https://docs.google.com/gview?url=https://qualitydu.jpwo.v2024.pl/acts-pdf/${actDuCode}.pdf&embedded=true`);
        } else {
          actPdfViewer = document.createElement('object');
          actPdfViewer.setAttribute('id', 'act-pdf-viewer');
          actPdfViewer.setAttribute('class', 'pdf');
          actPdfViewer.setAttribute('type', 'application/pdf');
          actPdfViewer.setAttribute('data', `https://qualitydu.jpwo.v2024.pl/acts-pdf/${actDuCode}.pdf`);
        }
        actPdfViewerContainer.appendChild(actPdfViewer);
        console.log(actPdfViewer);
      }
  
      window.onload = function () {
        createPDFViewer();
      }
});
