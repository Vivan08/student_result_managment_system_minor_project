document.addEventListener('DOMContentLoaded', () => {
    const tableBody = document.querySelector('#marksTable tbody');
    const addBtn = document.getElementById('addStudentBtn');

    // --- ACTION 1: ADD NEW STUDENT ---
    if (addBtn) {
    addBtn.addEventListener('click', () => {
        const name = prompt("Enter Student Name:");
        const roll = prompt("Enter Roll Number:");

        if (name && roll) {
            const newId = tableBody.rows.length + 1;

            const newRow = document.createElement('tr');

            newRow.innerHTML = `
                <td>${newId}</td>
                <td><b>${name}</b></td>
                <td>${roll}</td>
                <td><input type="number" class="marks-input" value="0"></td>
                <td class="actions">
                    <button class="edit-btn">Edit</button>
                    <button class="delete-btn">Delete</button>
                </td>
            `;

            tableBody.appendChild(newRow);
        }
    });
}

    // --- ACTION 2: EDIT & DELETE (Event Delegation) ---
    // We attach the listener to the table body so it works for new rows too
    tableBody.addEventListener('click', (e) => {
        const row = e.target.closest('tr');
        
        // Handle Delete
        if (e.target.classList.contains('delete-btn')) {
            if (confirm("Are you sure you want to remove this student?")) {
                row.style.opacity = '0';
                row.style.transform = 'translateX(20px)';
                setTimeout(() => row.remove(), 300);
            }
        }

        // Handle Edit
        if (e.target.classList.contains('edit-btn')) {
            const input = row.querySelector('.marks-input');
            input.focus();
            input.select();
            // Visual feedback that we are in "edit mode"
            input.style.boxShadow = "0 0 0 3px rgba(59, 130, 246, 0.3)";
            
            // Remove highlight when user clicks away
            input.addEventListener('blur', () => {
                input.style.boxShadow = "none";
            }, { once: true });
        }
    });

    // --- ACTION 3: SEARCH LOGIC ---
    const searchInput = document.querySelector('.search-box input');
    searchInput.addEventListener('input', (e) => {
        const term = e.target.value.toLowerCase();
        const rows = tableBody.querySelectorAll('tr');

        rows.forEach(row => {
            const text = row.innerText.toLowerCase();
            row.style.display = text.includes(term) ? "" : "none";
        });
    });
});