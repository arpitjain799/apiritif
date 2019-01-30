import csv
import copy
import logging
import os
import tempfile
import time
from unittest import TestCase
from itertools import islice, cycle

from apiritif.loadgen import Worker, Params, Supervisor

dummy_tests = [os.path.join(os.path.dirname(__file__), "test_dummy.py")]

logging.basicConfig(level=logging.DEBUG)


class TestLoadGen(TestCase):
    def test_threads_and_processes(self):
        log = "/tmp/apiritif.log"
        if os.path.exists(log):
            os.remove(log)
        script = os.path.dirname(os.path.realpath(__file__)) + "/resources/test_requests.py"
        outfile = tempfile.NamedTemporaryFile()
        report = outfile.name + "%s.csv"
        outfile.close()
        print(report)
        params = Params()
        params.concurrency = 3
        params.iterations = 4
        params.report = report
        params.tests = [script]
        params.worker_count = 2

        sup = Supervisor(params)
        sup.start()
        sup.join()
        with open(log) as f:
            content = f.readlines()
        a = 1 + 1

    def test_thread(self):
        outfile = tempfile.NamedTemporaryFile()
        print(outfile.name)
        params = Params()
        params.concurrency = 2
        params.iterations = 10
        params.report = outfile.name
        params.tests = dummy_tests

        worker = Worker(params)
        worker.run_nose(params)

    def test_worker(self):
        outfile = tempfile.NamedTemporaryFile()
        print(outfile.name)
        params = Params()
        params.concurrency = 2
        params.iterations = 10
        params.report = outfile.name
        params.tests = dummy_tests

        worker = Worker(params)
        worker.start()
        worker.join()

    def test_supervisor(self):
        outfile = tempfile.NamedTemporaryFile()
        params = Params()
        params.tests = dummy_tests
        params.report = outfile.name + "%s"
        params.concurrency = 9
        params.iterations = 5
        sup = Supervisor(params)
        sup.start()
        while sup.isAlive():
            time.sleep(1)
        pass

    def test_ramp_up1(self):
        outfile = tempfile.NamedTemporaryFile()
        print(outfile.name)

        params1 = Params()
        params1.concurrency = 50
        params1.report = outfile.name
        params1.tests = dummy_tests
        params1.ramp_up = 60
        params1.steps = 5

        params1.worker_count = 2
        params1.worker_index = 0

        worker1 = Worker(params1)
        res1 = [x.delay for x in worker1._get_thread_params()]
        print(res1)
        self.assertEquals(params1.concurrency, len(res1))

        params2 = copy.deepcopy(params1)
        params2.worker_index = 1
        worker2 = Worker(params2)
        res2 = [x.delay for x in worker2._get_thread_params()]
        print(res2)
        self.assertEquals(params2.concurrency, len(res2))

        print(sorted(res1 + res2))

    def test_ramp_up2(self):
        outfile = tempfile.NamedTemporaryFile()
        print(outfile.name)

        params1 = Params()
        params1.concurrency = 50
        params1.report = outfile.name
        params1.tests = dummy_tests
        params1.ramp_up = 60

        params1.worker_count = 1
        params1.worker_index = 0

        worker1 = Worker(params1)
        res1 = [x.delay for x in worker1._get_thread_params()]
        print(res1)
        self.assertEquals(params1.concurrency, len(res1))

    def test_unicode_ldjson(self):
        outfile = tempfile.NamedTemporaryFile(suffix=".ldjson")
        print(outfile.name)
        params = Params()
        params.concurrency = 2
        params.iterations = 1
        params.report = outfile.name
        params.tests = dummy_tests

        worker = Worker(params)
        worker.start()
        worker.join()

        with open(outfile.name) as fds:
            print(fds.read())
