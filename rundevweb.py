#!/usr/bin/env python3

""" Runs the PIoT Development Web Server. The Development Web Server supports
    auto-reloading when web-related files are changed. This server MUST NOT
    be used in production.
"""

from piot.web import app

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
