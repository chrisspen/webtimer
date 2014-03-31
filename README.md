=======================================================================
WebTimer - Measures download times of web page resources.
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

    webtimer.py <url>
    
An example output would look like:

    $ webtimer.py https://pypi.python.org/pypi/webtimer
    Measuring 12 of 12 100.00%: /static/images/python-logo.png
    --------------------------------------------------------------------------------
    Download times by URL:
    0.77 https://pypi.python.org/pypi/webtimer
    1.09 http://pypi.python.org/static/css/pypi-screen.css
    ...
    --------------------------------------------------------------------------------
    Download times by asset type:
     0.77   5.46% HTML
     2.33  16.43% Image
    11.07  78.12% CSS
    --------------------------------------------------------------------------------
    Total download seconds: 14.18

Note, to use it from the command line, you'll need to ensure it has execute
permission and is located in your PATH. On most platforms, this should
automatically be done by setup.py.
