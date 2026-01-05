// Tab switching functionality
function showTab(tabName) {
    // Hide all tabs
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => tab.classList.remove('active'));
    
    // Remove active class from all buttons
    const buttons = document.querySelectorAll('.tab-button');
    buttons.forEach(btn => btn.classList.remove('active'));
    
    // Show selected tab
    document.getElementById(tabName).classList.add('active');
    
    // Add active class to clicked button
    event.target.closest('.tab-button').classList.add('active');
}

// File input handlers
function setupFileInput(inputId, fileNameId, uploadAreaId) {
    const input = document.getElementById(inputId);
    const fileName = document.getElementById(fileNameId);
    const uploadArea = document.getElementById(uploadAreaId);
    
    input.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            fileName.textContent = `📎 ${this.files[0].name}`;
            fileName.classList.add('show');
        }
    });
    
    // Drag and drop functionality
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('drag-over');
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('drag-over');
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');
        
        if (e.dataTransfer.files.length) {
            input.files = e.dataTransfer.files;
            fileName.textContent = `📎 ${e.dataTransfer.files[0].name}`;
            fileName.classList.add('show');
        }
    });
    
    uploadArea.addEventListener('click', (e) => {
        if (!e.target.classList.contains('browse-btn')) {
            input.click();
        }
    });
}

// Setup all file inputs
setupFileInput('imageFile', 'convertFileName', 'convertUpload');
setupFileInput('pdfFile', 'splitFileName', 'splitUpload');
setupFileInput('pdf1File', 'merge1FileName', 'mergeUpload1');
setupFileInput('pdf2File', 'merge2FileName', 'mergeUpload2');

// Convert form handler
document.getElementById('convertForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    const submitBtn = this.querySelector('.submit-btn');
    const resultDiv = document.getElementById('convertResult');
    
    // Disable button and show loading
    submitBtn.disabled = true;
    submitBtn.innerHTML = 'Converting... <span class="loading"></span>';
    resultDiv.classList.remove('show', 'success', 'error');
    
    try {
        const response = await fetch('/convert', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            resultDiv.className = 'result show success';
            resultDiv.innerHTML = `
                <h3>✅ Success!</h3>
                <p>${data.message}</p>
                <a href="${data.download_url}" class="download-btn" download>⬇️ Download PDF</a>
            `;
        } else {
            throw new Error(data.error || 'Conversion failed');
        }
    } catch (error) {
        resultDiv.className = 'result show error';
        resultDiv.innerHTML = `
            <h3>❌ Error</h3>
            <p>${error.message}</p>
        `;
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Convert to PDF';
    }
});

// Split form handler
document.getElementById('splitForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    const submitBtn = this.querySelector('.submit-btn');
    const resultDiv = document.getElementById('splitResult');
    
    submitBtn.disabled = true;
    submitBtn.innerHTML = 'Splitting... <span class="loading"></span>';
    resultDiv.classList.remove('show', 'success', 'error');
    
    try {
        const response = await fetch('/split', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            resultDiv.className = 'result show success';
            resultDiv.innerHTML = `
                <h3>✅ Success!</h3>
                <p>${data.message}</p>
                <p>Total pages: ${data.pages}</p>
                <a href="${data.download_url}" class="download-btn" download>⬇️ Download ZIP (All Pages)</a>
            `;
        } else {
            throw new Error(data.error || 'Split failed');
        }
    } catch (error) {
        resultDiv.className = 'result show error';
        resultDiv.innerHTML = `
            <h3>❌ Error</h3>
            <p>${error.message}</p>
        `;
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Split PDF';
    }
});

// Merge form handler
document.getElementById('mergeForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    const submitBtn = this.querySelector('.submit-btn');
    const resultDiv = document.getElementById('mergeResult');
    
    submitBtn.disabled = true;
    submitBtn.innerHTML = 'Merging... <span class="loading"></span>';
    resultDiv.classList.remove('show', 'success', 'error');
    
    try {
        const response = await fetch('/merge', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            resultDiv.className = 'result show success';
            resultDiv.innerHTML = `
                <h3>✅ Success!</h3>
                <p>${data.message}</p>
                <a href="${data.download_url}" class="download-btn" download>⬇️ Download Merged PDF</a>
            `;
        } else {
            throw new Error(data.error || 'Merge failed');
        }
    } catch (error) {
        resultDiv.className = 'result show error';
        resultDiv.innerHTML = `
            <h3>❌ Error</h3>
            <p>${error.message}</p>
        `;
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Merge PDFs';
    }
});
