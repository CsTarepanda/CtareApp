import sys
import optparse

if __name__ == "__main__":
    app = __import__(sys.argv[1] + ".main")
    parser = optparse.OptionParser()
    app.main.options(parser)
    (options, args) = parser.parse_args(sys.argv[2:])
    app.main.exe(options, args)
