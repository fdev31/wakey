#!/bin/sh
(python -m http.server || python -m SimpleHTTPServer) &
xdg-open http://localhost:8000/
