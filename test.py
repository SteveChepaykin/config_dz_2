from main import makeDependencyList, generateDot, visualizeGraph, findPacket2
import unittest
import os.path as p

class TestMethods(unittest.TestCase):
    def test_make_dependency_list(self):
        listt = makeDependencyList("testdeps.txt")
        self.assertCountEqual(listt, [{"name": "name1", "provides": ["namename"], "depends": ["name2", "name3"]}, {"name": "name2", "provides": ["namename2"], "depends": ["name3"]}, {"name": "name3", "provides": [], "depends": []}]);
    
    def test_find_packet_2(self):
        listt = makeDependencyList("testdeps.txt")
        res = {}
        findPacket2(listt, "name1", res)
        self.assertDictEqual(res, {"name1": ["name2", "name3"], "name2": ["name3"], "name3": []})

    def test_generate_dot(self):
        listt = makeDependencyList("testdeps.txt")
        res = {}
        findPacket2(listt, "name1", res)
        generateDot(res)
        self.assertTrue(p.isfile("graph.dot"))

    def test_vesualize_graph(self):
        visualizeGraph()
        self.assertTrue(p.isfile("res.png"))


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)