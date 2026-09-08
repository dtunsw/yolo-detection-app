const API_BASE = import.meta.env.VITE_API_BASE_URL

export async function getHealth(file) {
    const res = await fetch(`${API_BASE}/health`)
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

    const res = await fetch(`${API_BASE}/api/detect/image`, {
        method: 'POST',
        body: formData
    });

    if (!res.ok) {
        const errorText = await res.text();
        throw new Error(errorText || `Request failed with status ${res.status}`);
    }

    return res.json();
}

export async function detectVideo(fileOrFormData) {
    const formData = fileOrFormData instanceof FormData
        ? fileOrFormData
        : (() => {
            const data = new FormData();
            data.append('file', fileOrFormData);
            return data;
        })();

    const res = await fetch(`${API_BASE}/api/detect/video`, {
        method: 'POST',
        body: formData
    });

    if (!res.ok) {
        const errorText = await res.text();
        throw new Error(errorText || `Request failed with status ${res.status}`);
    }

    return res.json();
}

export async function getResults(filename){
    const res = await fetch(`${API_BASE}/api/results/${filename}`)
    return res.blob();
}