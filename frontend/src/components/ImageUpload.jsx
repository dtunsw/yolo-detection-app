import {useEffect, useState} from 'react'
import { detectImage } from '../api/api.js'

function ImageUpload() {
  const [file, setFile] = useState(null)
  const [result, setResult] = useState(null)
  
  const handleFileChange = (event) => {
    setFile(event.target.files[0])
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    if (!file) return

    try {
      const data = await detectImage(file)
      setResult(data)
    } catch (error) {
      console.error('Error detecting image:', error)
    }
  }

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} />
        <button type="submit">Upload Image</button>
      </form>
      {result && (
        <div>
          <h2>Upload Result:</h2>
          <p>{JSON.stringify(result)}</p>
        </div>
      )}
    </div>
  )
}

function ImageResult ({ImageResult}) {}


export default ImageUpload
