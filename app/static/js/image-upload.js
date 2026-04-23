document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("image-input");
    if (!input) return;

    input.addEventListener("change", async function () {
        const file = this.files[0];
        if (!file) return;

        const uploadUrl = this.dataset.uploadUrl;
        const previewSelector = this.dataset.previewTarget;
        const hiddenSelector = this.dataset.hiddenInput;

        const formData = new FormData();
        formData.append("file", file);

        const response = await fetch(uploadUrl, {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            alert("Failed to upload image");
            return;
        }

        const data = await response.json();

        if (hiddenSelector) {
            document.querySelector(hiddenSelector).value = data.image_url;
        }

        if (previewSelector) {
            document.querySelector(previewSelector).src = data.image_url;
        }
    });
});