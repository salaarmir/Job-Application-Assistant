    let cvPdfUrl = null;
    let coverLetterPdfUrl = null;

    async function createDocuments() {
      const companyName = document.getElementById("companyName").value;
      const jobDescription = document.getElementById("jobDescription").value;
      const userPrompts = document.getElementById("userPrompts").value;
      const status = document.getElementById("status");

      status.textContent = "Generating documents...";

      const formData = new FormData();
      formData.append("company_name", companyName);
      formData.append("job_description", jobDescription);
      formData.append("user_prompts", userPrompts);

      const response = await fetch("http://127.0.0.1:8000/create_documents", {
        method: "POST",
        body: formData
      });

      if (!response.ok) {
        status.textContent = "Something went wrong.";
        return;
      }

      const data = await response.json();
      document.getElementById("outputLatexCV").value = data.latex_cv;
      document.getElementById("outputLatexCoverLetter").value = data.latex_cover_letter;

      status.textContent = "Documents generated successfully!";
    }

    async function uploadDocuments() {
      const fileInput = document.getElementById("academicFile");
      const status = document.getElementById("status");

      if (!fileInput.files.length) {
        status.textContent = "Please select a file to upload.";
        return;
      }

      const formData = new FormData();
      formData.append("academic_file", fileInput.files[0]);

      status.textContent = "Uploading and ingesting document...";

      const response = await fetch("/upload_documents", {
        method: "POST",
        body: formData
      });

      if (!response.ok) {
        status.textContent = "Something went wrong.";
        return;
      }

      status.textContent = "Document uploaded and ingested successfully!";
      fileInput.value = ""; // Clear the file input

      await loadDocuments(); // Refresh the documents list
    }

    async function loadDocuments() {
      const response = await fetch("/documents");
      const data = await response.json();

      const container = document.getElementById("documentsList");
      container.innerHTML = ""; // Clear previous content

      if (!data.filenames || data.filenames.length === 0) {
        container.innerHTML = "<p>No documents uploaded yet.</p>";
        return;
      }

      data.filenames.forEach(filename => {
        const div = document.createElement("div");
        div.style.border = "1px solid #000000";
        div.style.padding = "12px";
        div.style.marginBottom = "12px";
        div.style.borderRadius = "8px";

        div.textContent = filename;
        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Delete";
        deleteButton.style.marginLeft = "12px";
        deleteButton.addEventListener("click", async () => {
          await fetch(`/delete_document/${filename}`, { method: "DELETE" });
          await loadDocuments(); // Refresh the list after deletion
        });

        div.appendChild(deleteButton);

        container.appendChild(div);
      });
    }

    async function convertToPDF(filetype) {

      const companyName = document.getElementById("companyName").value;
      const latexCV = document.getElementById("outputLatexCV").value;
      const latexCoverLetter = document.getElementById("outputLatexCoverLetter").value
      const status = document.getElementById("status");
      
      status.textContent = "Converting to PDF...";

      const formData = new FormData();
      formData.append("company_name", companyName);
      formData.append("filetype", filetype);

      if (filetype === "cv"){
        formData.append("latex_content", latexCV);
      } else {
        formData.append("latex_content", latexCoverLetter);
      }

      const response = await fetch("http://127.0.0.1:8000/convert_to_pdf", {
        method: "POST",
        body: formData
      });

      if (!response.ok) {
        status.textContent = "Something went wrong.";
        return;
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);

      if (filetype === "cv"){
        cvPdfUrl = url;
        document.getElementById("pdfPreviewCV").src = url;
      } else {
        coverLetterPdfUrl = url;
        document.getElementById("pdfPreviewCoverLetter").src = url;
      }

      status.textContent = "PDF generated successfully!";
    
    }

    function downloadPDF(filetype) {
      const companyName = document.getElementById("companyName").value;
      const status = document.getElementById("status");
      const url = filetype === "cv" ? cvPdfUrl : coverLetterPdfUrl;
      const a = document.createElement("a");
      a.href = url;
      a.download = filetype === "cv" ? `Salaar_Mir_CV_${companyName}.pdf` : `Salaar_Mir_CoverLetter_${companyName}.pdf`;
      a.click();
      URL.revokeObjectURL(url);

      status.textContent = "PDF downloaded!";
    }

    function openMenu() {
    document.getElementById("sidebar").classList.add("open");
    document.getElementById("overlay").classList.add("open");
    document.getElementById("menuButton").classList.add("hidden");
    }

    function closeMenu() {
        document.getElementById("sidebar").classList.remove("open");
        document.getElementById("overlay").classList.remove("open");
        document.getElementById("menuButton").classList.remove("hidden");
    }

    function toggleMenu() {
        document.getElementById("sidebar").classList.toggle("open");
        document.getElementById("overlay").classList.toggle("open");
        document.getElementById("menuButton").classList.toggle("menuOpen");
    }   

    document.addEventListener("DOMContentLoaded", () => {

        if (document.getElementById("documentsList")) {
          loadDocuments();
        }
      });