import {getResults} from "../api/api";
import {useEffect, useState} from "react";
import {useParams} from "react-router-dom";

function Result() {
    const {filename} = useParams();
    const [result, setResult] = useState(null);
    const isVideo = filename.endsWith('.mp4') || filename.endsWith('.avi') || filename.endsWith('.mov');

    useEffect(() => {
        const fetchResults = async () => {
            let objectURL;
            try {
                const blob = await getResults(filename);
                objectURL = URL.createObjectURL(blob);
                setResult(objectURL);
            } catch (error) {
                console.error("Error fetching results:", error);
            }
        };
        fetchResults();
    }, [filename]);
    
     return (
            <div>
                {result &&(
                    isVideo ? (
                        <video controls>
                            <source src={result} type="video/mp4" style={{ maxWidth: '100%' }} />
                        </video>
                    ) : (
                        <img src={result} alt="Result" style={{ maxWidth: '100%' }} />
                    )
                )}
            </div>
        )
}
export default Result