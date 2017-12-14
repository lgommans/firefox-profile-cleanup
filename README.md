# Firefox Profile Cleaner

**Removes cookies, localStorage, etc. from non-whitelisted domains to prevent tracking**

This program is a replacement for self-destructing cookies, since that add-on is
(1) no longer maintained and (2) the WebExtension hell makes it currently
impossible to make such an add-on work in Firefox 57+. This program is not an add-on.

Run `clean.py` whenever you want cookies to be destructed.

Tested in Firefox 55 and 56. Fully compatible with any add-on that I know of,
since it works externally and just removes data from Firefox' `cookies.sqlite`
and other such files.

## First time setup

0. Always have backups. This is beta software, currently used by only one person!
1. Run `./clean.py --genconfig` to generate a config file and store it in, for example, `config.txt`.
2. In `config.txt`, configure the Firefox profile you wish to clean, and the whitelist of sites to keep.
3. Run `./clean.py config.txt`.

## Usage

`./clean.py config.txt`

---

## New: nocomplete.py

Beta stage. Attempts to make Firefox no longer autocomplete things, since it
seems to have moved from choosing the best option to always offering the one
you want the *least*.

