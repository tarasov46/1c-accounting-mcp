def main():
    print("Starting 1C Accounting MCP Server...")

    try:
        from server import main as server_main
        server_main()
    except ImportError as e:
        print(f"Import error: {e}")
        print("Install dependencies: pip install -r requirements.txt")
        exit(1)
    except Exception as e:
        print(f"Server startup error: {e}")
        exit(1)


if __name__ == "__main__":
    main()