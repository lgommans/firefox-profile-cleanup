# Firefox Profile Cleaner

**Removes cookies, localStorage, etc. from non-whitelisted domains to prevent tracking**

Note: this program is not an add-on but a Python script.

Tested in Firefox 55 and 56. Fully compatible with any add-on that I know of,
since it works externally and just removes data from Firefox' `cookies.sqlite`
and other such files.

## First time setup

0. Always have backups (just copy your .mozilla folder). The code is stable, but currently used/tested by only one person.
1. Run `./clean.py --genconfig` to generate a config file and store it in, for example, `config.txt`.
2. Edit `config.txt` to select the Firefox profile you wish to clean, and the whitelist of sites to keep.
3. Run `./clean.py config.txt`.

## Usage

`./clean.py config.txt`

---

## nocomplete.py

This is a separate script, which attempts to make Firefox no longer
autocomplete things. Firefox sometimes bugs and autocompletes the worst option
rather than the best.

For example, when I type 'osm' I want to go to osm.org. Instead, it
autocompletes to osmhv.openstreetmap.de which is something I visited like once
a long time ago.

This script tries to remove the incorrect completion from the autocomplete
list.

