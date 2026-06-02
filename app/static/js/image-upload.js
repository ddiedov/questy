document.addEventListener("DOMContentLoaded", () => {

    const inputs = document.querySelectorAll(
        'input[type="file"][data-preview-target]'
    );

    inputs.forEach(input => {

        input.addEventListener("change", async function () {

            const file = this.files[0];

            if (!file) {
                return;
            }

            const uploadUrl = this.dataset.uploadUrl;
            const previewSelector = this.dataset.previewTarget;
            const hiddenSelector = this.dataset.hiddenInput;

            // Local preview if upload is not available.
            if (!uploadUrl) {

                if (previewSelector) {
                    const preview = document.querySelector(previewSelector);

                    if (preview) {
                        preview.src = URL.createObjectURL(file);
                    }
                }

                return;
            }

            const formData = new FormData();
            formData.append("file", file);

            try {

                const response = await fetch(uploadUrl, {
                    method: "POST",
                    body: formData
                });

                if (!response.ok) {
                    throw new Error("Upload failed");
                }

                const data = await response.json();

                if (hiddenSelector) {
                    const hiddenInput = document.querySelector(hiddenSelector);

                    if (hiddenInput) {
                        hiddenInput.value = data.image_url;
                    }
                }

                if (previewSelector) {
                    const preview = document.querySelector(previewSelector);

                    if (preview) {
                        preview.src = data.image_url;
                    }
                }

            } catch (error) {

                console.error(error);

                alert("Failed to upload image");
            }
        });

    });

});
