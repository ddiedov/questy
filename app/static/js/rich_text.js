// Запрещаем вложения
document.addEventListener("trix-file-accept", (event) => {
    event.preventDefault();
});

// Показываем toolbar только во время редактирования
document.querySelectorAll(".rich-text-container").forEach(container => {

    const editor = container.querySelector("trix-editor");
    const toolbar = document.getElementById(editor.getAttribute("toolbar"));

    if (!toolbar) return;

    container.addEventListener("focusin", () => {
        console.log("focusin");
        toolbar.classList.add("visible");
    });

    container.addEventListener("focusout", () => {
        console.log("focusout");

        setTimeout(() => {
            if (!container.contains(document.activeElement)) {
                toolbar.classList.remove("visible");
            }
        }, 0);
    });

});