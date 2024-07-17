## Backend

The backend, which is responsible for the identification based of a picture and streaming that information to the
frontend is build in Python 3.12 using poetry as its dependency manager. The backend is a flask application that
utilizes the Google Lens features by utilizing Selenium to access the Google Lens website and GPT-4o to generate
a description of the picture. The backend is containerized using Docker and can be run using the following command:

### Usage

The usage of the backend in production requires Docker to be installed on the system. The backend can be run
using the following command, replacing `sk-your-key-here` with the OpenAI API key:

```bash
cd lens-gpt-backend
docker build -t lens-gpt-backend .
docker run \
    --rm \                      
  -e DISPLAY=:99 \
  -e OPENAI_API_KEY=sk-your-key-here \ 
  -p 3002:5000  \
  lens-gpt-backend \
  /bin/bash -c "Xvfb :99 -screen 0 1280x1024x24 & poetry run python -m lens_gpt_backend.main"
```

The application can then be accessed at `http://localhost:3002` via curl or a web browser. The backend comes with a
demo frontend which allows the user to upload a picture and display the raw information that are streamed back
from the backend. The classification can be accessed via the `/classify` endpoint and the frontend can be
accessed via the `/` endpoint. If the backend should be used just over the API, the following curl command
can be used, if the current directory contains an ``img.png``

```bash 
curl --no-buffer -X POST -F "file=@img.png" http://localhost:3002
```

#### 4. Set Up the Project

Navigate to the `lens-gpt-backend` directory and install the project dependencies:

```bash
cd path/to/lens-gpt-backend
poetry install
```

#### 5. Run the Server

Once all the requirements are met, run the server using the command:

```bash
poetry run python -m lens_gpt_backend.main
```

This command starts the server, allowing you to begin development.

## Endpoints

Upon requesting the classification at the ``/classify`` endpoint, the server will stream the response back as
soon as partial results become available. As this is a POST request, the caller should not buffer the response,
as it will wait until all classifications are done. The different response are marked by a ``data_type`` and
``data_description`` field which help to identify the data on the client side. As of now the server streams the
following responses:

- ``model-producer``: The producer and the model, e.g. 'Patagonia', 'Nano Puff Jacket'. The ``data`` field
  contains the producer and the model as a directory with the respective keys. The ``data_description`` field
  contains the string 'model-producer' and the ``data_type`` field contains the string 'dict\[str, str]'.
- ``producer-url``: The website where the item was originally offered. The ``data`` field contains a directory
  with the key 'link' and the respective url as a string as well as the websites titles under 'title'.
  The ``data_description`` field contains the string
  'producer-url' and the ``data_type`` field contains the string 'dict\[str, str]'.
- ``retail-price-details``: The retail information about the item which are given on the website. The ``data``
  field contains a directory with the keys 'producer_url', 'price', 'original_name', 'description', 'material' and '
  specs'. The ``data_description`` field contains the string
  'retail-price-details' and the ``data_type`` field contains the string 'dict\[str, str]'.
- ``second-hand-offers``: The second hand offers for the item. The ``data`` field contains a list of directories
  with the keys 'price', 'link', 'title' and 'wear'. The ``data_description`` field contains the string
  'second-hand-offers' and the ``data_type`` field contains the string 'list\[dict\[str, str]]'.
- ``estimated-price``: The estimated price of the item. The ``data`` field contains a directory with the keys
  'price', 'min_range', 'max_range' and 'certainty'. The ``data_description`` field contains the string '
  estimated-price' and the ``data_type`` field contains the string 'dict\[str, str]'.

## Architecture

The backend is build in a modular way and extensible way that allows to add further classification and
scraping to be integrated with ease.

### Producer-Consumer Architecture

The backend is designed around a robust producer-consumer architecture, where producers are responsible for extracting
information and passing it downstream to consumers. These consumers can also act as producers for subsequent processing
stages, creating a flexible and extensible pipeline. This design pattern facilitates the easy integration of new
processing stages (consumers) that can handle information in novel ways, thereby enhancing the system's capabilities
without significant restructuring.

To integrate a new processing stage, developers simply extend the `Producer` class and implement its `produce` method.
This method encapsulates the logic for extracting or processing information. The architecture is organized as a
hierarchical tree of producers, where each node in the tree can register one or more child producers. Information flows
from parent producers to their children, enabling complex processing pipelines to be constructed from simple, reusable
components.

#### Defining the Pipeline

The pipeline is defined in a root-level file named `processing`. Here, the relationships between producers are
established, forming a tree structure. Each producer is responsible for a specific task, such as extracting data from a
webpage, processing text, or generating metadata. By registering child producers with their parents, the pipeline can
dynamically adapt to the data being processed, allowing for highly customizable and scalable data processing workflows.

#### Extending the Pipeline

To extend the pipeline, developers create new classes that inherit from the `Producer` class and implement the `produce`
method. This method should contain the logic specific to the new stage of processing or data extraction. Once
implemented, the new producer is registered with a parent producer, inserting it into the existing pipeline.

##### Example: Adding an Image Extraction Producer

For instance, to add a new producer that extracts images from webpages, one would create a class named `ImageProducer`.
This class extends the `Producer` class and implements the `produce` method to perform image extraction.
The `ImageProducer` is then registered with a parent producer, such as `ProducerWebsite`, which is responsible for
initial webpage data extraction. This registration is accomplished using the `register_producer` method on the parent
producer.

```python
class ImageProducer(Producer):
    def produce(self, data):
        # Logic to extract images from the input data
        extracted_images = ...
        return extracted_images


# Example of registering the new producer
parent_producer = ProducerWebsite(...)
parent_producer.register_producer(ImageProducer())
```

By following this pattern, each producer can autonomously stream its output to the frontend or pass it to another
producer for further processing. This modular approach ensures that the backend remains adaptable and scalable, capable
of accommodating new types of data extraction and processing as the project evolves.

### ResultQueue Documentation

#### Overview

The `ResultQueue` class is a crucial component designed to manage a queue of results for multiple concurrent requests in
the `lens_gpt_backend` project. It facilitates efficient communication between threads, allowing for the dynamic
addition of results and ensuring thread safety through synchronization mechanisms. This class plays a vital role in
streaming and buffering responses for the frontend, ensuring that data is delivered in a timely and organized manner.

#### Key Features

- **Thread Safety**: Utilizes locks and condition variables to ensure that operations on the queue are safe across
  multiple threads.
- **Dynamic Result Addition**: Supports the addition of results to the queue until it is explicitly closed, catering to
  the asynchronous nature of data processing and retrieval.
- **Efficient Communication**: Implements a condition variable to block consumers when no new data is available,
  reducing CPU usage and improving efficiency.
- **Concurrent Request Handling**: Manages separate queues for different file hashes, allowing multiple requests to be
  processed concurrently without interference.

#### Usage in the Project

1. **Initialization**: A `ResultQueue` instance is created or retrieved using the `factory` method, keyed by a unique
   file hash. This ensures that each file being processed has its own dedicated result queue.

2. **Adding Results**: As the backend processes data (e.g., classifying information from websites), results are added to
   the queue using the `put` method. This method notifies any waiting threads that new data is available, allowing for
   immediate processing or streaming.

3. **Retrieving Results**: The frontend or any consumer retrieves results using the `get_next` method, which blocks if
   no data is available. This ensures that consumers only process data as it becomes available, facilitating a
   streaming-like behavior.

4. **Streaming to Frontend**: The `str_generator` method acts as a generator, yielding results as they become available.
   This is particularly useful for streaming responses to the frontend, as it allows for partial responses to be sent
   without waiting for all data to be processed. This method is used in the `classify` endpoint to stream results to the
   frontend.

5. **Closing the Queue**: Once data processing is complete, the queue is closed using the `close` method. This notifies
   any waiting consumers that no more data will be added, allowing them to gracefully handle the end of the stream.

#### Example Scenario

Consider a scenario where the backend is tasked with extracting and classifying information from multiple websites
concurrently. Each website's data is processed in a separate thread, with results being added to a `ResultQueue`
instance specific to that website's file hash. As the backend processes each piece of information, results are streamed
to the frontend in real-time, allowing for a responsive and dynamic user experience. Once all data from a website has
been processed, the corresponding `ResultQueue` is closed, signaling to the frontend that the stream of data is
complete.

This architecture not only enhances the efficiency and responsiveness of the backend but also optimizes the flow of
information to the frontend, ensuring that data is delivered in a coherent and timely manner.

### API Documentation

#### Overview

The API for the `lens_gpt_backend` project is designed to handle image classification requests. It provides an interface
for clients to upload images, which are then processed asynchronously. The results of the classification are streamed
back to the client in real-time, utilizing a `ResultQueue` to manage the flow of data.

#### Endpoints

- **GET /**: Serves the static index.html file, acting as the entry point for the frontend application.
- **POST /classify**: Accepts image files for classification. It only supports `.png` files and streams the
  classification results back to the client.

#### Request Handling Process

1. **Pre-Request Setup**:
    - Each request is assigned a unique `request_id` using a UUID, which is stored in the Flask `g` context for the
      duration of the request. This ID can be used for logging, tracing, and associating requests with their processing
      threads and results.

2. **File Upload and Validation** (`/classify` endpoint):
    - The request is checked for the presence of a file part. If missing, it responds with an error.
    - Validates the file name and ensures it ends with `.png`. If not, it responds with an unsupported file type error.
    - If the file is valid, it proceeds to process the image.

3. **Image Processing**:
    - The uploaded file is hashed using SHA-256 to generate a unique identifier (`file_hash`) for the image. This hash
      is used to manage caching and to ensure that each image is processed once.
    - The image is saved to a temporary directory (`tmp`) using its hash as the file name. This allows the image to be
      accessed by the processing functions and that no unauthorized actors can access the image directly.
    - A `ResultQueue` instance is created or retrieved for the `file_hash`. If the queue is fresh (indicating that the
      image has not been processed before), the image is sent for asynchronous processing.
    - The processing function (`process_async`) is called with a lambda function that specifies how the image should be
      processed. This typically involves extracting features or classifying the image content.
    - The `ResultQueue`'s `str_generator` method is used to stream results back to the client. This method yields
      results as they become available, i.e. when the respective producers push them into the result queue, allowing for
      real-time data streaming.

4. **Streaming Results**:
    - The results of the image processing are streamed back to the client , providing a
      continuous flow of data as the classification results are produced.

#### Error Handling

- The API is designed to gracefully handle errors, such as invalid file uploads or unsupported file types, by responding
  with appropriate HTTP status codes and error messages.
- Exceptions during image processing are caught and logged, ensuring that the server remains stable even in the face of
  unexpected errors.

#### Security Considerations

- File validation is performed to ensure that only supported file types are processed. This helps mitigate risks
  associated with handling arbitrary file uploads.
- Unique identifiers (`request_id` and `file_hash`) are used extensively for tracing and to prevent collisions in
  processing, enhancing the overall security and reliability of the system.

