export async function getHealth(file) {
    const res = await fetch("http://localhost:8888/health",)
    return res.json();
}

export async function detectImage(fileOrFormData) {
    const formData = fileOrFormData instanceof FormData
        ? fileOrFormData
        : (() => {
            const data = new FormData();
            data.append('file', fileOrFormData);
            return data;
        })();

    const res = await fetch("http://localhost:8888/api/detect/image", {
        method: 'POST',
        body: formData
    });

    if (!res.ok) {
        const errorText = await res.text();
        throw new Error(errorText || `Request failed with status ${res.status}`);
    }

    return res.json();
}