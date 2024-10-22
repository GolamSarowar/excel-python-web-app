document.getElementById("uploadForm").addEventListener("submit", function(e) {
    e.preventDefault();

    const fileInput = document.getElementById("fileInput");
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.sheet_names) {
            const sheetSelect = document.getElementById("sheetSelect");
            sheetSelect.innerHTML = ""; // Clear existing options
            // Add default option
            sheetSelect.appendChild(new Option("-- Select a Sheet --", ""));
            data.sheet_names.forEach(sheet => {
                const opt = document.createElement("option");
                opt.value = sheet;
                opt.innerHTML = sheet;
                sheetSelect.appendChild(opt);
            });
            document.getElementById("dropdowns").style.display = "block"; // Assuming this is the section for dropdowns
        }
    })
    .catch(error => console.error('Error uploading file:', error));
});

document.getElementById("sheetSelect").addEventListener("change", function() {
    const sheetName = this.value;
    if (sheetName) { // Only fetch options if a valid sheet is selected
        fetch('/get_options', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ sheet_name: sheetName })
        })
        .then(response => response.json())
        .then(data => {
            const dropdown = document.getElementById("dropdownSelect");
            dropdown.innerHTML = ""; // Clear existing options
            dropdown.appendChild(new Option("-- Select an Option --", "")); // Add default option
            data.options.forEach(option => {
                const opt = document.createElement("option");
                opt.value = option;
                opt.innerHTML = option;
                dropdown.appendChild(opt);
            });
        })
        .catch(error => console.error('Error fetching options:', error));
    }
});

document.getElementById("dropdownSelect").addEventListener("change", function() {
    const sheetName = document.getElementById("sheetSelect").value;
    const selectedValue = this.value;

    if (sheetName && selectedValue) { // Only proceed if both values are selected
        fetch('/update_table', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ sheet_name: sheetName, selected_value: selectedValue })
        })
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById("table-body");
            tableBody.innerHTML = ""; // Clear existing rows

            data.forEach(row => {
                const tr = document.createElement("tr");
                row.forEach(cellValue => {
                    const td = document.createElement("td");
                    td.innerText = cellValue;
                    tr.appendChild(td);
                });
                tableBody.appendChild(tr);
            });
        })
        .catch(error => console.error('Error updating table:', error));
    }
});
