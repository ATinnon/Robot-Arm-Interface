document.addEventListener("DOMContentLoaded", function () {
    const buttons = document.querySelectorAll(".tabs-button");
    const contentDiv = document.getElementById("tab-content");

    function attachFormEventListeners() {
        document.querySelectorAll(".control-form").forEach(form => {
            form.addEventListener("submit", function(event) {
                event.preventDefault(); // Prevent default form submission

                let motor_id = this.querySelector("[name='motor_id']").value;
                let stepsInput = this.querySelector("[name='steps']");
                let steps = parseInt(stepsInput.value, 10);

                if (isNaN(steps)) {
                    alert("Please enter a valid number.");
                    return;
                }

                let direction = steps >= 0 ? 1 : -1;
                let absoluteSteps = Math.abs(steps);

                let output = `${motor_id}, ${absoluteSteps}, ${direction}`;
                console.log("Sending Data:", output); // Debugging

                fetch("/control", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ motor_id: motor_id, steps: absoluteSteps, direction: direction })
                })
                .then(response => response.json())
                .then(data => {
                    console.log("Response:", data);
                    alert("Response: " + data.message);
                })
                .catch(error => console.error("Error:", error));
            });
        });
    }

    buttons.forEach(button => {
        button.addEventListener("click", function () {
            const tabTarget = this.getAttribute("data-target");

            fetch(tabTarget) // Make the request to the URL passed from Flask
                .then(response => response.text())
                .then(html => {
                    contentDiv.innerHTML = "";
                    const tempDiv = document.createElement("div");
                    tempDiv.innerHTML = html;

                    const newContent = tempDiv.querySelector("#tab-content");
                    if (newContent) {
                        contentDiv.innerHTML = newContent.innerHTML;
                    } else {
                        contentDiv.innerHTML = html;
                    }

                    attachFormEventListeners(); // Reattach event listeners
                })
                .catch(error => console.error("Error loading tab:", error));
        });
    });

    attachFormEventListeners(); // Initial call to attach listeners when the page loads
});