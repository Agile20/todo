document.addEventListener("DOMContentLoaded", function () {
    const addForm = document.querySelector("form");
    
    addForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const title = document.querySelector("input[name='title']").value;
        const description = document.querySelector("textarea[name='description']").value;

        fetch("/add_todo", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                title: title,
                description: description
            })
        })
        .then(response => response.json())
        .then(data => {
            alert("Task added!");
            window.location.reload();
        })
        .catch(error => console.error("Error:", error));
    });
});
