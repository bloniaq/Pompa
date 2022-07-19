# -*- coding: utf-8 -*-

import application

def start_app():
    return application.Application()

if __name__ == '__main__':
        app = start_app()
        app.run_gui()
