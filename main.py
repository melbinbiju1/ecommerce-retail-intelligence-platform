"""
Project entry point.

The FastAPI application is defined in:

    src/api/main.py

Run the API locally with:

    uvicorn src.api.main:app --reload

This root-level file is kept as a lightweight pointer so the repository
has a clear Python entry point without duplicating application logic.
"""


def main() -> None:
    print("E-Commerce Retail Intelligence Platform")
    print("FastAPI app location: src/api/main.py")
    print("Run locally with: uvicorn src.api.main:app --reload")


if __name__ == "__main__":
    main()