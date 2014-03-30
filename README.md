=======================================================================
webtimer - Measures download times of web page resources.
=======================================================================

Overview
========

Measures download times of a web page and all its resources, broken down
by asset type (HTML/CSS/JS/IMG).

Installation
------------

Install dependencies:

    pip install webtimer

Usage
-----

You can invoke the script either as a Python module:

    from webtimer import WebTimer, CSS
    wt = WebTimer(url=<url>)
    wt.evaluate()
    print wt.times_by_type[CSS]

or as a standalone command line script:

::    

    webtimer.py <url>
    
Note, to use it from the command line, you'll need to ensure it has execute
permission and is located in your PATH. On most platforms, this should
automatically be done by setup.py.
