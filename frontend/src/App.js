import { useState, useEffect } from "react";
import axios from "axios";
import ArchitectureItem from "./components/ArchitectureItem";
import ExampleUrls from "./components/ExampleUrls";
import "./App.css";

const API_URL = process.env.REACT_APP_API_URL;

function App() {
  const [architectures, setArchitectures] = useState([]);
  const [isVisible, setIsVisible] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [url, setUrl] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Debug useEffect
  useEffect(() => {
    console.log("Environment Variables:", {
      REACT_APP_API_URL: process.env.REACT_APP_API_URL,
      API_URL: API_URL,
      NODE_ENV: process.env.NODE_ENV,
    });
  }, []);

  const fetchArchitectures = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const { data } = await axios.get(`${API_URL}/architectures`);
      setArchitectures(data);
      setIsVisible(true);
    } catch (err) {
      setError(err.response?.data?.message || "Failed to fetch architectures");
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmitUrl = async () => {
    if (!url.trim()) {
      setError("Please enter a URL");
      return;
    }

    try {
      setIsSubmitting(true);
      setError(null);
      await axios.post(`${API_URL}/scrape?url=${url}`);
      setUrl("");
      await fetchArchitectures();
    } catch (err) {
      setError(err.response?.data?.message || "Failed to submit URL");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleExampleUrlClick = (exampleUrl) => {
    setUrl(exampleUrl);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>AWS Cloud Architecture Scraper</h1>

        <ExampleUrls onUrlClick={handleExampleUrlClick} />

        <div className="url-input-container">
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="Enter any Image Html Json or text file url"
            className="url-input"
            disabled={isSubmitting}
          />
          <button
            className="fetch-button"
            onClick={handleSubmitUrl}
            disabled={isSubmitting}
          >
            {isSubmitting ? "Scraping..." : "Scrape Architecture"}
          </button>
        </div>

        <button
          className="fetch-button"
          onClick={fetchArchitectures}
          disabled={isLoading}
        >
          {isLoading ? "Loading..." : "Show Architectures"}
        </button>

        {error && <div className="error-message">{error}</div>}

        {isVisible && architectures.length > 0 && (
          <div className="architectures-container">
            <div className="controls">
              <button
                className="fetch-button"
                onClick={() => setIsVisible(false)}
              >
                Hide Data
              </button>
            </div>
            <div className="architectures-list">
              {architectures.map((architecture, index) => (
                <ArchitectureItem key={index} architecture={architecture} />
              ))}
            </div>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
