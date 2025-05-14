import unittest
import time
from random import randrange
from faker import Faker

from dummydb.db_utils import DummyDB

class Benchmark(unittest.TestCase):
    def setUp(self):
        self.startTime = time.time()
        self.record_ids: list = []

    def tearDown(self):
        t = time.time() - self.startTime
        print('%s: %.3f' % (self.id(), t))

    def test_write_speed(self):
        db = DummyDB('file4.log')
        fake = Faker()
        total_records = 10 * 1000

        write_start_time = time.time()
        for i in range(total_records):
            print(f"Writing {i} out of {total_records}", end="\r")
            record_id = randrange(10**10, 10**11)
            self.record_ids.append(record_id)
            record_value = fake.name()
            db.set(record_id, record_value)

        total_write_time = time.time() - write_start_time
        print('%s: %.3f' % ('Write Time', total_write_time))

        read_start_time = time.time()
        for i, record_id in enumerate(self.record_ids):
            print(f"Reading {i} out of {total_records}", end="\r")
            db.get_2(record_id)

        total_read_time = time.time() - read_start_time
        print('%s: %.3f' % ('Read Time', total_read_time))

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)  # add assertion here

    def test_adding_and_getting_a_record(self):
        db = DummyDB('file1.log')
        db.set(12, "Peter")
        self.assertEqual("Peter", db.get(12))

    def test_adding_multiple_records_and_check_size(self):
        db = DummyDB('file1.log')
        db.set(12, "Yolo")
        db.set(123, "Raju")
        db.set(11, "Foo")
        self.assertEqual("Yolo", db.get_2(12))
        self.assertEqual("Raju", db.get_2(123))
        self.assertEqual("Foo", db.get_2(11))

    def test_adding_multiple_records_and_check_size_2(self):
        db = DummyDB('file1.log')
        fake = Faker()
        data = {}
        for _ in range(1000):
            record_id = randrange(10**10, 10**11)
            record_value = fake.name()
            data[record_id] = record_value
            db.set(record_id, record_value)

        for record in data:
            self.assertEqual(db.get(record), data.get(record))


if __name__ == '__main__':
    unittest.main()
