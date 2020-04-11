#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment:

@author: GanAH  2020/3/10.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""

from flask import Flask

app = Flask(__name__)


@app.route('/v2')
def hello_word():
    return '<html><body>' \
           '<h><title>python Flask Web开发</title/></h><h1>Hello Word!</h1>' \
           '</body></html>'


if __name__ == '__main__':
    app.run(debug=True)