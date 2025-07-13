# Backend

A FastAPI-based backend service for scraping and analyzing cloud architecture diagrams using Google's Gemini AI.

## Setup

### Prerequisites

- Python 3.11+
- MongoDB
- Google Cloud Platform account (for Gemini API)

### Environment Setup

1. Create a virtual environment:

```bash
python -m venv myenv
```

2. Activate the virtual environment:

- Windows:

```bash
myenv\Scripts\activate
```

- Linux/Mac:

```bash
source myenv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following variables:

```env
MONGO_URI=mongodb://your-mongodb-uri
DB_NAME=your-database-name
GEMINI_API_KEY=your-gemini-api-key
```

## Running the Server

Start the server using uvicorn:

```bash
uvicorn main:app --reload
```

The server will start at `http://localhost:8000`

## API Endpoints

### Scrape Architecture

- **POST** `/scrape`
  - Scrapes and analyzes architecture from a provided URL
  - Body:
    ```json
    {
      "url": "https://your-diagram-url"
    }
    ```
  - Returns: Architecture object with analysis results

### Get Architectures

- **GET** `/architectures`
  - Retrieves a list of stored architectures
  - Query Parameters:
    - `skip` (optional, default: 0): Number of records to skip
    - `limit` (optional, default: 100): Maximum number of records to return
  - Returns: List of architecture objects

## Supported Input Types

- Images (PNG, JPG)
- SVG diagrams
- HTML pages
- JSON files
- Plain text

## Features

- Automatic format detection
- AI-powered diagram analysis using Google Gemini
- OCR backup for image processing
- MongoDB storage for analysis results
- Pagination support for large datasets

## Error Handling

The API returns appropriate HTTP status codes:

- 200: Successful operation
- 400: Invalid request
- 404: Resource not found
- 500: Server error

## Environment Variables Details

### Required Variables:

- `MONGO_URI`: Your MongoDB connection string

  - Format: `mongodb://[username:password@]host[:port]/[database]`
  - Example: `mongodb://localhost:27017` or `mongodb+srv://user:pass@cluster.mongodb.net`

- `DB_NAME`: Name of your MongoDB database

  - Example: `Architectures`

- `GEMINI_API_KEY`: Your Google Gemini API key
  - Get it from: Google AI Studio
  - Format: A string of characters provided by Google

--

# Frontend

A React application that scrapes and visualizes AWS cloud architecture from various sources including images, JSON, and YAML files.

## Prerequisites

- Node.js (v16 or higher)
- npm (v8 or higher)

## Setup Instructions

1. Clone the repository

```bash
git clone <repository-url>
cd frontend
```

2. Install dependencies

```bash
npm install
```

3. Create environment file
   Create a new file named `.env` in the root following content:

```plaintext
REACT_APP_API_URL=
```

## Running the Application

1. Start the development server:

```bash
npm start
```

2. Open your browser and navigate to:

```
http://localhost:3000
```

## Features

- Scrape architecture from various sources:
  - AWS Architecture Diagrams (images)
  - CloudFormation Templates (YAML)
  - AWS Resource Templates (JSON)
- Interactive UI with example URLs
- Real-time architecture visualization
- Detailed view of scraped components

## Example URLs

The application comes with several example URLs that demonstrate different types of inputs:

1. AWS Architecture Diagrams (Image)
2. CloudFormation Templates (YAML)
3. AWS Resource Templates (JSON)

## Troubleshooting

If you encounter issues with environment variables:

1. Ensure the `.env` file is in the correct location (root directory)
2. Restart the development server after making changes to `.env`
3. Check the browser console for environment variable values
4. Make sure the backend server is running at the URL specified in REACT_APP_API_URL

## Project Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── ArchitectureItem.js
│   │   ├── ExampleUrls.js
│   │   └── Modal.js
│   ├── App.js
│   ├── App.css
│   └── index.js
├── .env
├── package.json
└── README.md
```

## Frontend Images

![frontend](assests/image1.png)
![frontend](assests/image2.png)
