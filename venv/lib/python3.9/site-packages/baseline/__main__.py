# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2020 Daniel Mark Gass
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from __future__ import absolute_import, division, print_function, unicode_literals

import difflib
import os
import sys
from argparse import ArgumentParser
from glob import glob

PY2 = sys.version_info.major < 3
if PY2:  # pragma: no cover
    input = raw_input


DESCRIPTION = """
Locate scripts with baseline updates within the paths specified and modify 
the scripts with the updates found. (The scripts to be modified will be 
summarized and you will be offered a chance to cancel before files are 
changed.)
""".strip()


def locate_updates(paths):
    """Find location of baseline update files.

    Recursively walk through `paths` and find baseline
    update files and return their locations.

    :param paths: paths to search
    :returns: relative paths (from CWD) of update files found
    :rtype: list of str

    """
    updates = []
    for dirpath in (p for p in paths if os.path.isdir(p)):
        for path, _dirs, files in os.walk(dirpath):
            for name in files:
                if name.endswith('.update'):
                    updates.append(
                        os.path.join(os.path.relpath(path, os.getcwd()), name))
    return updates


def perform_action(script_path, update_path, args):
    """Perform update/clean action for baseline update.

    :param str script_path: script with outdated baseline
    :param str update_path: copy of script with updates
    :param str args: command line arguments

    """
    if args.movepath:
        script_path = os.path.join(args.movepath, script_path)
        script_dirpath = os.path.dirname(script_path)
        if not os.path.isdir(script_dirpath):
            os.makedirs(script_dirpath)

    if not args.clean:
        with open(update_path) as update:
            new_content = update.read()

        if args.diff and os.path.exists(script_path):
            with open(script_path) as script:
                old_content = script.read()

            title = '=== {} ==='.format(script_path).center(71, '=')
            border = '=' * len(title)

            print(border)
            print(title)
            print(border)

            keepends = True
            diff_lines = difflib.context_diff(
                old_content.splitlines(keepends), new_content.splitlines(keepends))
            print(''.join(diff_lines).rstrip())

            print(title)
            print()
            while True:
                answer = input(
                    '[A]ccept [R]eject, [Ctrl-C] to quit -> ').upper()
                if answer == 'A':
                    break
                if answer == 'R':
                    return

        try:
            stat_info = os.stat(script_path)
        except OSError:
            stat_info = None

        with open(script_path, 'w') as script:
            script.write(new_content)

        if stat_info is not None:
            os.chmod(script_path, stat_info.st_mode)
            try:
                os.chown(script_path, stat_info.st_uid, stat_info.st_gid)
            except AttributeError:
                pass  # must be windows

    os.remove(update_path)


def main(args=None):
    """Command line interface.

    :param list args: command line options (defaults to sys.argv)
    :returns: exit code
    :rtype: int

    """
    parser = ArgumentParser(
        prog='baseline',
        description=DESCRIPTION)

    parser.add_argument(
        'path', nargs='*',
        help='directory path to search (default to CWD)')

    parser.add_argument(
        '-c', '--clean', action='store_true',
        help='remove baseline update files')

    parser.add_argument(
        '-d', '--diff', action='store_true',
        help='show contextual difference for each update')

    parser.add_argument(
        '--movepath', help='location to move script updates')

    parser.add_argument(
        '--force', action='store_true',
        help='do not prompt (does not apply to --diff')

    args = parser.parse_args(args)

    paths = args.path or ['.']

    # weed out incorrect names, expand wildcards
    paths = [path for pattern in paths for path in glob(pattern)]

    if args.movepath:
        rel_paths = [os.path.relpath(path, os.getcwd()) for path in paths]

        if any(path.startswith('..') for path in rel_paths):
            print(
                "ERROR: search paths outside of current working directory "
                "not allowed when using --movepath option"
            )
            return 1

    update_file_paths = locate_updates(paths)

    exitcode = 0

    if update_file_paths:
        script_paths = [
            os.path.splitext(pth)[0] for pth in update_file_paths]

        print('Found baseline updates for:')
        for path in script_paths:
            print('  ' + path)
        print()

        try:
            if not args.diff and not args.force:
                prompt = 'Hit [ENTER] to {}, [Ctrl-C] to cancel '.format(
                    'clean' if args.clean else
                    'move' if args.movepath else 'accept')
                input(prompt)

            for script_path, update_path in zip(script_paths, update_file_paths):
                perform_action(script_path, update_path, args)

        except KeyboardInterrupt:
            print()
            print('Canceled')
            exitcode = 1

    return exitcode


if __name__ == '__main__':

    sys.exit(main())
