document.addEventListener('DOMContentLoaded', () => {
    const submitBtn = document.getElementById('submitBtn');
    const statusMsg = document.getElementById('statusMessage');
    const semesterSelect = document.getElementById('semester');

    submitBtn.addEventListener('click', () => {
        // Simple Validation
        if (semesterSelect.value === "") {
            alert("Please select a semester first!");
            return;
        }

        // Add a "Loading" effect to button
        submitBtn.innerText = "Checking...";
        submitBtn.style.opacity = "0.7";
        submitBtn.disabled = true;

        // Simulate API delay
        setTimeout(() => {
            submitBtn.innerText = "SUBMIT";
            submitBtn.style.opacity = "1";
            submitBtn.disabled = false;
            
            // Show the error message with a smooth fade
            statusMsg.classList.remove('hidden');
            statusMsg.style.animation = 'fadeIn 0.5s forwards';
        }, 800);
    });

    // Navigation Item Interaction
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', function() {
            navItems.forEach(i => i.classList.remove('active'));
            this.classList.add('active');
        });
    });
});