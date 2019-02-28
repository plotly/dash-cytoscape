from __future__ import absolute_import

import logging
import os
import multiprocessing
import sys
import time
import unittest
import percy
import threading
import platform
import flask
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class IntegrationTests(unittest.TestCase):
    def percy_snapshot(self, name=''):
        if os.environ.get('PERCY_ENABLED', False):
            snapshot_name = '{} - {}'.format(name, sys.version_info)

            self.percy_runner.snapshot(
                name=snapshot_name
            )

    @classmethod
    def setUpClass(cls):
        super(IntegrationTests, cls).setUpClass()

        options = Options()
        if 'DASH_TEST_CHROMEPATH' in os.environ:
            options.binary_location = os.environ['DASH_TEST_CHROMEPATH']

        cls.driver = webdriver.Chrome(options=options)
        cls.driver.set_window_size(1280, 1000)

        if os.environ.get('PERCY_ENABLED', False):
            loader = percy.ResourceLoader(webdriver=cls.driver)
            percy_config = percy.Config(default_widths=[1280])
            cls.percy_runner = percy.Runner(loader=loader, config=percy_config)
            cls.percy_runner.initialize_build()

    @classmethod
    def tearDownClass(cls):
        super(IntegrationTests, cls).tearDownClass()

        cls.driver.quit()
        if os.environ.get('PERCY_ENABLED', False):
            cls.percy_runner.finalize_build()

    def setUp(self):
        pass

    def tearDown(self):
        time.sleep(3)
        if platform.system() == 'Windows':
            requests.get('http://localhost:8050/stop')
            sys.exit()
        else:
            self.server_process.terminate()
        time.sleep(3)

    def startServer(self, app, port=8050):
        if 'DASH_TEST_PROCESSES' in os.environ:
            processes = int(os.environ['DASH_TEST_PROCESSES'])
        else:
            processes = 1

        def run():
            app.scripts.config.serve_locally = True
            app.css.config.serve_locally = True
            app.run_server(
                port=port,
                debug=False,
                processes=processes
            )

        def run_windows():
            app.scripts.config.serve_locally = True
            app.css.config.serve_locally = True

            @app.server.route('/stop')
            def _stop_server_windows():
                stopper = flask.request.environ['werkzeug.server.shutdown']
                stopper()
                return 'stop'

            app.run_server(
                port=port,
                debug=False,
                threaded=False
            )

        # Run on a separate process so that it doesn't block

        system = platform.system()
        if system == 'Windows':
            self.server_thread = threading.Thread(target=run_windows)
            self.server_thread.start()
        else:
            self.server_process = multiprocessing.Process(target=run)
            self.server_process.start()
        logging.getLogger('werkzeug').setLevel(logging.ERROR)
        time.sleep(5)

        # Visit the dash page
        self.driver.get('http://localhost:{}'.format(port))
        time.sleep(0.5)
