cat index.html | sed -e '0,/^cat / d' -e '/^EOF/,$ d' -e 's/&lt;/</g' -e 's/\\\\/\\/g' > site/wakey_inspector.py
