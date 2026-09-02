import { useState } from 'react'
import { useEffect } from 'react'
import { getHealth } from '../api/api.js'

function Health() {
  const [status, setStatus] = useState(0)
  useEffect(() => {
    getHealth()
    .then((data) => setStatus(data.status))
    .catch((error) => console.log(error))
  },[])
  return (
    <>
      <div>
        <h1>Backend Health Status: {status}</h1>
      </div>
    </>
  )
}

export default Health
