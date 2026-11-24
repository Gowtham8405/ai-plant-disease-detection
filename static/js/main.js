/**
 * AI Plant Disease Detection - Client-side JavaScript
 * Handles interactive file drag & drop, client-side image preview,
 * form interactions, and real-time inference loading progress indication.
 */

document.addEventListener('DOMContentLoaded', () => {
    const uploadForm = document.getElementById('leaf-upload-form');
    const fileInput = document.getElementById('leaf-image-input');
    const dropZone = document.getElementById('drop-zone');
    const dropPrompt = document.getElementById('drop-zone-prompt');
    const previewContainer = document.getElementById('preview-container');
    const imagePreview = document.getElementById('image-preview');
    const fileNameBadge = document.getElementById('file-name');
    const removeBtn = document.getElementById('remove-image-btn');
    const predictBtn = document.getElementById('predict-btn');
    const loadingState = document.getElementById('loading-state');

    if (!fileInput || !dropZone) return;

    let isSubmitting = false;

    // Handle file selection from input
    fileInput.addEventListener('change', (e) => {
        handleFiles(e.target.files);
    });

    // Drag and Drop Event Listeners
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.add('dragover');
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.remove('dragover');
        }, false);
    });

    dropZone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files && files.length > 0) {
            fileInput.files = files;
            handleFiles(files);
        }
    });

    // Remove / Reset Image Selection
    if (removeBtn) {
        removeBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            e.preventDefault();
            resetFileInput();
        });
    }

    // Form Submission & Loading State
    if (uploadForm) {
        uploadForm.addEventListener('submit', (e) => {
            if (isSubmitting) {
                e.preventDefault();
                return;
            }

            if (!fileInput.files || fileInput.files.length === 0) {
                e.preventDefault();
                alert('Please select a plant leaf image before predicting.');
                return;
            }

            // Flag submission to prevent duplicate clicks
            isSubmitting = true;
            showLoadingState();
        });
    }

    /**
     * Display the frontend loading state during model inference
     */
    function showLoadingState() {
        if (predictBtn) {
            predictBtn.classList.add('is-loading');
            predictBtn.style.pointerEvents = 'none';
            predictBtn.innerHTML = `
                <span class="btn-spinner" aria-hidden="true"></span>
                <span class="btn-text">Analyzing...</span>
            `;
        }

        if (loadingState) {
            loadingState.style.display = 'flex';
        }
    }

    /**
     * Reset loading state back to default
     */
    function resetLoadingState() {
        isSubmitting = false;

        if (predictBtn) {
            predictBtn.classList.remove('is-loading');
            predictBtn.style.pointerEvents = '';
            predictBtn.innerHTML = `
                <span class="btn-icon" id="predict-btn-icon">⚡</span>
                <span class="btn-text" id="predict-btn-text">Predict Disease</span>
            `;
            predictBtn.disabled = !(fileInput.files && fileInput.files.length > 0);
        }

        if (loadingState) {
            loadingState.style.display = 'none';
        }
    }

    /**
     * Process selected files and show client-side preview
     */
    function handleFiles(files) {
        if (!files || files.length === 0) return;

        const file = files[0];

        // Check if uploaded file is an image
        if (!file.type.startsWith('image/')) {
            alert('Please select a valid image file (PNG, JPG, JPEG, WEBP).');
            resetFileInput();
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            fileNameBadge.textContent = file.name;
            
            // Toggle preview visibility
            dropPrompt.style.display = 'none';
            previewContainer.style.display = 'flex';
            
            // Enable predict button and reset loading state
            resetLoadingState();
            if (predictBtn) {
                predictBtn.disabled = false;
            }
        };
        reader.readAsDataURL(file);
    }

    /**
     * Reset file input and preview display
     */
    function resetFileInput() {
        fileInput.value = '';
        imagePreview.src = '';
        fileNameBadge.textContent = '';
        previewContainer.style.display = 'none';
        dropPrompt.style.display = 'block';
        resetLoadingState();
        if (predictBtn) {
            predictBtn.disabled = true;
        }
    }

    // Reset loading state on browser back/forward navigation
    window.addEventListener('pageshow', () => {
        resetLoadingState();
    });
});
