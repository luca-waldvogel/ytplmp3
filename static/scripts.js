document.getElementById('downloadForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    const formData = new FormData(this);

    // Show the loading spinner
    document.getElementById('loading-spinner').style.display = 'flex';

    fetch('/download', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => { throw new Error(data.error); });
        }

        // Get the content disposition header to determine the filename
        const contentDisposition = response.headers.get('Content-Disposition');
        let filename;

        if (contentDisposition) {
            const match = contentDisposition.match(/filename="(.+)"/);
            if (match) {
                filename = match[1];
            }
        }

        // Fallback, falls kein Dateiname gefunden wurde
        if (!filename) {
            // Bestimme den Dateinamen basierend auf der erwarteten Dateiendung
            const isZip = response.headers.get('Content-Type') === 'application/zip';
            filename = isZip ? 'download.zip' : 'download.mp3';
        }

        // Überprüfe, ob es sich um eine ZIP-Datei handelt, um den MIME-Typ richtig zu setzen
        const isZip = filename.endsWith('.zip');
        const mimeType = isZip ? 'application/zip' : 'audio/mpeg';

        return response.blob().then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            a.type = mimeType;
            document.body.appendChild(a);
            a.click();
            a.remove();

            // Hide the spinner after the file is downloaded
            document.getElementById('loading-spinner').style.display = 'none';
            document.querySelector('button[type="submit"]').disabled = false;

            // Reset the input field and placeholder after the download
            const inputField = document.getElementById('playlist_url');
            inputField.value = '';
            inputField.placeholder = 'Enter YouTube Video or Playlist URL';
        });
    })
    .catch(error => {
        console.error('Error:', error);
        alert(error.message);
        document.getElementById('loading-spinner').style.display = 'none';
        document.querySelector('button[type="submit"]').disabled = false;
    });

    // Disable the submit button to prevent multiple submissions
    document.querySelector('button[type="submit"]').disabled = true;
});