# Firefox Profile Cleaner

**Removes cookies, localStorage, etc. from non-whitelisted domains to prevent tracking**

This program is a replacement for self-destructing cookies. Since Firefox is
moving to WebExtensions before they even implemented half the necessary APIs to
port add-ons (let alone give developers time to do so), this is no longer
possible within Firefox itself.

This program does it externally. You need to close Firefox (saving tabs is
fine) and then run it when you want cookies to be destructed.

