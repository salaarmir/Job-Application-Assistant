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