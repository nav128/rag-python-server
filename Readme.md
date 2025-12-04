### Setup
- `git clone git@github.com:nav128/rag-python-server.git`
- `cd rag`
- `source venv/bin/activate`
- `pip install .`
- Run qdrant docker 
`docker run -p 6333:6333 -v {PROJECT-PATH}/vector_db_data:/qdrant/storage:Z qdrant/qdrant`
- create `.env` file and populate the fields as in the `env_example` file
- `uvicorn src.app:app --host 0.0.0.0 --port 8000`

### Usage
- Upload your files via `api/files/upload`. using in the headers the same `x_api_key` you have defined in the `.env` file
- Ask questions via `api/chat/simple` Or use a web-client with `api/chat/stream` for sse experience and sesson continuity.

A React client is available [here](https://github.com/nav128/rag-react-client)
