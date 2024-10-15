# Thai G2P API

This project provides a REST API for converting Thai text into a grapheme-to-phoneme (G2P) representation using Flask. It uses a custom dictionary for word tokenization and romanization to handle words not present in the dictionary.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python 3.7+**: Download Python from [python.org](https://www.python.org/downloads/).
- **Git**: For version control and cloning the repository.
- **pip**: Python's package manager, which comes bundled with Python.

## Setup

Follow these steps to set up the project:

### 1. Clone the Repository

```bash
git clone <REPO_URL>
cd <REPO_NAME>
```

### 2. Create a virtual environment
It's recommended to create a virtual environment to keep the dependencies isolated:

```bash
python3 -m venv venv
```

Activate the virtual environment:

- On Windows:
```bash
venv\Scripts\activate
```
- On MacOS/Linux:
```bash
source venv/bin/activate
```

### 3. Install dependencies
Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

### 4. Run the API Server
Start the Flask server:

```bash
python thai_g2p_api.py
```
By default, the server will run on http://localhost:5000.

## Usage
You can test the API using `curl` or Postman. Here’s an example using `curl`:
```bash
curl -X POST http://localhost:5000/api/g2p -H "Content-Type: application/json" -d '{"text": "สวัสดี"}'
```

The API will respond with:
```json
{
    "result": "sa-wàt-dii"
}
```

### API Endpoints
### API Endpoints

- **`POST /api/g2p`**: Converts Thai text into its G2P representation.

| Parameter | Type   | Description                     |
|-----------|--------|---------------------------------|
| `text`    | string | Thai text to be converted      |

**Response:**

| Field   | Type   | Description                                       |
|---------|--------|---------------------------------------------------|
| `result`| string | representation of the converted Thai text     |


## License

This project is licensed under the MIT License. See the LICENSE file for details.