if __name__ == "__main__":
    import sys
    import os
    import os.path
    if len(sys.argv) > 0:
        arg = sys.argv[1]
        if arg == "app":
            appname = sys.argv[2]
            if os.path.exists(appname):
                print("{} is exists.".format(appname))
            else:
                os.system("cp -r apptemplate {}".format(appname))
    else:
        print("""
        app <name>: create app
        """)
