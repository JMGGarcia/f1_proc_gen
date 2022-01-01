import os


def run_names():
    subdir, dirs, files = next(os.walk("./names"))
    print(subdir)
    print(dirs)
    print(files)

    for subdir, dirs, files in os.walk("./names"):
        print(subdir)
        print(dirs)
        print(files)


if __name__ == "__main__":
    run_names()
