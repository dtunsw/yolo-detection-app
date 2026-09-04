import {useEffect, useState} from 'react'
import { detectVideo } from '../api/api.js'

function VideoUpload() {
    const [file, setFile] = useState(null)
    const [result, setResult] = useState(null)
    const handleSubmit = async (event) => {
        event.preventDefault()
        if (!file) return
        try {
            const data = await detectVideo(file)
            setResult(data)
        } catch (error) {
            console.error('Error detecting video:', error)
            }
        }

    const handleFileChange = (event) => {
        setFile(event.target.files[0])
    }
    
    return (
        <div>
            <form onSubmit={handleSubmit}>
                <input type = "file" onChange = {handleFileChange} />
                <button type = "submit">Upload Video</button>
            </form>
            {result && (
                <div>
                    <button onClick={() => window.location.href = `/results/${result.annotated_video}`}>
                        View Result
                    </button>
                    <h2>Upload Result:</h2>
                    <p>{JSON.stringify(result)}</p>
                </div>
            )}
        </div>
    )
}

function VideoResult({VideoResult}) {}

export default VideoUpload