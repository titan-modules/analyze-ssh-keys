Analyze SSH Keys
============

-----------
a [Titan][1] Module
## Name: 

Analyze SSH Keys

## Purpose: 
To provide public key fingerprints in the event a device is compromised. You can check remote systems for public keys and remove them effectively.

## Example:

Coming soon

## Schema:

| Column      |      Type      |  Default |  Description |
|-------------|:-------------:|------:|:-----------------|
| name        |  TEXT | NULL  | SSH key filname  |
| strength    |    TEXT   | NULL  | Bit strength of Key|
| fingerprint | TEXT | NULL  | Key fingerprint  |
| comment     | TEXT | NULL  | Comment attached to fingerprint
| date        | TEXT | NULL  | Date discovered
    
    
See `schema.json` for more details.

## Author:

This module was created by Mike Mackintosh [`splug`]. 

You can follow him below:

[![@mikemackintosh][twitter]][2]
[![mikemackintosh][github]][3]

[1]: https://github.com/mikemackintosh/titan
[2]: http://www.twitter.com/mikemackintosh
[3]: http://github.com/mikemackintosh
[twitter]: http://i.imgur.com/tXSoThF.png
[github]: http://i.imgur.com/0o48UoR.png

