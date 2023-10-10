$('#submit').click(function() {


    const column = $('#column').val();
    const regex = $('#regex').val();
    const size = $('#size').val();
    const data = {
        column: column,
        regex: regex,
        size: size
    };

    $.ajax({
        type: 'POST',
        url: 'pandas/',
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: function(data) {
            let csvData = jsonToCsv(data["data"]); // Add .items.data
            // Create a CSV file and allow the user to download it
            let blob = new Blob([csvData], { type: 'text/csv' });
            let url = window.URL.createObjectURL(blob);
            let a = document.createElement('a');
            a.href = url;
            a.download = 'data.csv';
            document.body.appendChild(a);
            a.click();

        },
        error: function(error) {
            console.log(error);
        }
    });
});



function jsonToCsv(jsonData) {
    let csv = '';
    // Get the headers
    let headers = Object.keys(jsonData[0]);
    csv += headers.join(',') + '\n';
    // Add the data
    jsonData.forEach(function (row) {
        let data = headers.map(header => JSON.stringify(row[header])).join(','); // Add JSON.stringify statement
        csv += data + '\n';
    });
    return csv;
}