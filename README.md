# Firefox Profile Cleaner

**Removes cookies, localStorage, etc. from non-whitelisted domains to prevent tracking**

This program is a replacement for self-destructing cookies, since that add-on is
(1) no longer maintained and (2) the WebExtension hell makes it currently
impossible to make such an add-on work in Firefox 57+. This program is not an add-on.

Close Firefox (saving tabs is fine) and run `clean.py` whenever you want cookies to be destructed.

Tested in Firefox 56. Fully compatible with self-destructing cookies, uBlock, Privacy Badger,
container tabs, etc., since it works externally and just removes data from Firefox'
`cookies.sqlite` and other such files.

## Getting Started

1. Always have backups. This is beta software tested by only one person!
2. Run `./clean.py --genconfig` to generate a config file and store it in, for example, `config.txt`.
3. Modify the config file to include (at least):  
3.1. the Firefox profile you wish to clean  
3.2. the whitelist of sites to not remove
4. Run `./clean.py config.txt`.
