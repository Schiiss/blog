import uvicorn


def main():
    uvicorn.run(
        "databricks_app.app:app",  # import path to your `app`
        host="0.0.0.0",
        port=8000,
        reload=True,  # optional
    )
