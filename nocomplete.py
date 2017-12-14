#!/usr/bin/env python3

import sys, os

if len(sys.argv) < 3 or '-h' in sys.argv or '--help' in sys.argv:
    print('Usage: nocomplete.py configfile domain')
    print('Where <domain> is the domain you want Firefox to stop autocompleting.')
    print('For the config file format, see clean.py.')
    exit(1)

conffile = sys.argv[1]

if not os.path.isfile(conffile):
    sys.stderr.write('Error: config file "{}" not found.\n'.format(conffile))
    sys.exit(2)

mozpath = os.path.expanduser('~') + '/.mozilla/firefox'
profile = None

configlines = open(conffile).read().replace('\r', '').split('\n')
lineN = 0
for line in configlines:
    lineN += 1
    if len(line.strip()) == 0:
        continue

    if line[0] == '#':
        continue

    if '=' not in line:
        sys.stderr.write('Error in config file on line {} (=-sign not found)\n'.format(lineN))
        sys.exit(2)

    key, val = line.split('=', 1)

    if key == 'profile':
        profile = val
    elif key == 'keep':
        pass
    elif key == 'mozpath':
        mozpath = val
    else:
        sys.stderr.write('Error: unrecognized config key "{}" on line {}\n'.format(key, lineN))
        sys.exit(1)

if profile is None:
    print('Error: no profile specified in the config file.')
    sys.exit(2)

profilep = '{}/{}'.format(mozpath, profile) # profile-path

print("Confirm that you want to delete the following from your browser history:")
s = "echo 'SELECT url FROM moz_places WHERE url LIKE \"%{}%\";' | sqlite3 {}/places.sqlite".format(sys.argv[2], profilep);
os.system(s)

yes = input("Type yes to confirm deletion: ")
if yes == 'yes':
    s = "echo 'DELETE FROM moz_places WHERE url LIKE \"%{}%\";' | sqlite3 {}/places.sqlite".format(sys.argv[2], profilep);
    os.system(s)
else:
    print("That was not a yes, so I will not delete it.")

