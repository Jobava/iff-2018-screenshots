import click
import re
import os
import shutil
import errno
import time


def normalize_path(path):
    if path.endswith("/"):
        return path
    else:
        return path + "/"


def poll(path, pattern, destination, polling_time):
    def to_path(x):
        return os.path.realpath(os.path.expanduser(x))
    def listdir(x):
        return os.listdir(to_path(x))

    regex_pattern = re.compile(pattern)
    normalized_path = normalize_path(path)
    destination_file = to_path(destination)
    prev_file = ""
    while True:
        files = sorted(to_path(os.path.join(normalized_path, f))
                       for f in listdir(normalized_path)
                       if regex_pattern.match(f))
        cur_file = files[-1]
        if cur_file != prev_file:
            try:
                shutil.copyfile(cur_file, destination_file)
                # os.symlink(cur_file, destination_file)
            except OSError as e:
                if e.errno == errno.EEXIST:
                    os.remove(destination_file)
                    shutil.copyfile(cur_file, destination_file)
                    # os.unlink(destination_file)
                    # os.symlink(cur_file, destination_file)
                else:
                    # an error we don't know about
                    raise
        prev_file = cur_file
        time.sleep(polling_time)


@click.command()
@click.option("-p", "--path", required=True, help="A folder path to look into")
@click.option("-r", "--pattern", default=".*", help="A regex pattern")
@click.option("-d", "--destination", help="A destination file to write to")
@click.option("-t", "--polling-time", default=1,
              help="Polling interval default is 1 second")
def cli(path, pattern, destination, polling_time):
    poll(path, pattern, destination, polling_time)


if __name__ == '__main__':
    cli()
