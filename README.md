# Voices AI Music API

This is an the official Voices AI Music API based on Python and FastAPI. It currently supports generating songs, lyrics, etc.  

### Features

- Automatic token maintenance and keep-alive
- Fully asynchronous, fast, suitable for later expansion
- Simple code, easy to maintain, convenient for secondary development


### Usage

#### Configuration

Edit the `.env.example` file, rename to `.env` and fill in the session_id and cookie.

These are initially obtained from the browser, and will be automatically kept alive later.

![cookie](./images/cover.png)


#### Run

Install dependencies 

```bash
pip3 install -r requirements.txt
```

For this part, refer to the FastAPI documentation on your own.
```bash
uvicorn main:app 
```

#### Docker

```bash
docker compose build && docker compose up
```

#### Documentation

After setting up the service, visit /docs

![docs](./images/docs.png)
