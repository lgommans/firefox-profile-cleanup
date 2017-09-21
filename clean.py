#!/usr/bin/env python3

import sys, os

if len(sys.argv) != 2 or '-h' in sys.argv or '--help' in sys.argv:
    print("Usage: {} configfile".format(sys.argv[0]))
    print("Use --genconfig to show a configuration example")
    print("Note: you need the sqlite3 binary in your $PATH.")
    sys.exit(1)

if '--genconfig' in sys.argv:
    print("""
# A comment is a line starting with a #

# The profile name, identical to the folder name
profile=abcdef01.default

# Path to said profile
# Optional. It defaults to ~/.mozilla/firefox
#mozpath=/home/USERNAME/.mozilla/firefox

# The whitelist: domains of which information should be kept (such as cookies)
# This can be specified multiple times, as shown in the example.
# Will include subdomains, e.g. example.com includes www.example.com
# and students.example.com includes joe.students.example.com
keep=example.com
keep=wikipedia.org
""".strip())
    sys.exit(0)

conffile = sys.argv[1]

if not os.path.isfile(conffile):
    sys.stderr.write('Error: config file "{}" not found.\n'.format(conffile))
    sys.exit(2)

mozpath = os.path.expanduser('~') + '/.mozilla/firefox'
profile = None
keep = []

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
        keep.append(val)
    elif key == 'mozpath':
        mozpath = val
    else:
        sys.stderr.write('Error: unrecognized config key "{}" on line {}\n'.format(key, lineN))
        sys.exit(1)

if profile is None:
    print('Error: no profile specified in the config file.')
    sys.exit(2)

if len(keep) == 0:
    print('Error: no keep= lines found in config file. Please use --genconfig to generate an example config.')
    print('If you understand what keep= is for and you wish not to use it, then this is probably the wrong tool for you.')
    print('If not, feel free to edit out this if statement :)')
    sys.exit(2)

profilep = '{}/{}'.format(mozpath, profile) # profile-path

# Cleanup cookies
where = ''
nd = ''
for domain in keep:
    where += '{}host NOT LIKE "%{}"'.format(nd, domain)
    nd = ' AND '

if len(where) > 3900:
    sys.stderr.write('Warning: you got a lot of keeps. Just know that this has not been tested.\n')

s = "echo 'DELETE FROM moz_cookies WHERE {};' | sqlite3 {}/cookies.sqlite".format(where, profilep)
print('Running: {}'.format(s))
os.system(s)

# Cleanup localstorage
where = ''
nd = ''
for domain in keep:
    where += '{}originKey NOT LIKE "{}%"'.format(nd, domain[::-1]) # reverse domain, str[from:to:step]
    nd = ' AND '

s = "echo 'DELETE FROM webappsstore2 WHERE {};' | sqlite3 {}/webappsstore.sqlite".format(where, profilep)
print('Running: {}'.format(s))
os.system(s)

# Cleanup ... other stuff? Idk even what this is, but more site-specific storage
d = os.scandir('{}/storage/default'.format(profilep))
for f in d:
    f = f.name
    if 'moz-extension+++' in f:
        continue

    keepdir = False
    for domain in keep:
        if domain in f:
            keepdir = True
            break
    if not keepdir:
        s = 'rm -r "{}/storage/default/{}"'.format(profilep, f)
        print('Running: {}'.format(s))
        os.system(s)

d = os.scandir('{}/storage/temporary'.format(profilep))
for f in d:
    f = f.name
    if 'moz-extension+++' in f:
        continue

    keepdir = False
    for domain in keep:
        if domain in f:
            keepdir = True
            break
    if not keepdir:
        s = 'rm -r "{}/storage/temporary/{}"'.format(profilep, f)
        print('Running: {}'.format(s))
        os.system(s)

# TODO:
# Thwart advanced profiling techniques by cleaning up:
#  - favicons.sqlite
#  - SiteSecurityServiceState.txt (HSTS, HPKP)
#  - kinto.sqlite
#  - permissions.sqlite
#
# maybe cert_override.txt
# and wtf is serviceworker.txt?
