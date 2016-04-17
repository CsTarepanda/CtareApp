import sys

if __name__ == "__main__":
    app = __import__(sys.argv[1] + ".main")
    app.main.exe(sys.argv[2:])
