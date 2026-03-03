# Instructions

- You will need to increase the memory allocated to your podman machine this can be done on the command line with `podman machine set --memory 10240` or through the podman desktop application. After changing the memory allocation you will need to restart your podman machine for the changes to take effect.
  
- You may need to stop your podman machine before you can change the memory allocation. This can be done with `podman machine stop` and then `podman machine start` after you have made the changes.
  
- You can verify that the memory allocation has been updated by running `podman machine inspect` and looking for the Memory field under the Resources section. It should show the new memory allocation that you set.
  
- Once you have increased the memory allocation you can start the services with `podman compose up --build` from the week4 directory. This will start the OpenSearch RAG and Streamlit services as well as build the images. The first time you run this command it will take some time to build the images and start the containers, but subsequent runs will be faster as the images will be cached.
  
- You will need to ensure that ollama is running on your local machine and that you have the nomic-embed-text model available and llama3.2. If you've been following along they should already be installed from previous sessions.
  
- You can check if the model is available by running `ollama list` in your terminal. If the model is not available you can pull it with `ollama pull nomic-embed-text`. You can also pull the llama3.2 model with `ollama pull llama3.2`.
  
- FastAPI will be available at `http://localhost:8000` if you navigate to the /docs endpoint you will see the automatically generated API documentation where you can test the endpoints. Now you can either use the API documentation to test the endpoints or you can use a tool like Postman or curl to send requests to the API. For example, you can use the following curl command to test the /ingest endpoint:

```bash
curl -X 'POST' \
  'http://localhost:8000/ingest' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "urls": [
    "https://en.wikipedia.org/wiki/Yellow_warbler",
    "https://en.wikipedia.org/wiki/Natural_language_processing",
    "https://en.wikipedia.org/wiki/Bioluminescence",
    "https://en.wikipedia.org/wiki/Generation"

  ]
}'
```
or you can just paste the following JSON into the request body in the API documentation:

```json
{
  "urls": [
    "https://en.wikipedia.org/wiki/Yellow_warbler",
    "https://en.wikipedia.org/wiki/Natural_language_processing",
    "https://en.wikipedia.org/wiki/Bioluminescence",
    "https://en.wikipedia.org/wiki/Generation"
  ]
}
```

- After ingesting the documents, you can test querying using the streamlit application available at `http://localhost:8501`. The streamlit application provides a simple interface for querying the RAG service and displaying the results. You can enter a query in the input box and click the "Ask" button to see the retrieved documents and the generated answer from the language model.