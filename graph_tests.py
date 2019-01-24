import unittest
from graph import *

class TestList(unittest.TestCase):

    def test_01(self):
        g = Graph('test1.txt') 
        self.assertTrue(g.is_bipartite())
        self.assertEqual(g.conn_components(), [['v1', 'v2', 'v3', 'v4', 'v5'], ['v6', 'v7', 'v8', 'v9']])
        
        
    def test_02(self):
        g = Graph('test2.txt')
        self.assertEqual(g.conn_components(), [['v1', 'v2', 'v3'], ['v4', 'v6', 'v7', 'v8']])
        self.assertFalse(g.is_bipartite())

    def test_03(self):
        g = Graph('test3.txt')
        self.assertEqual(g.conn_components(), [['v1', 'v2', 'v3']])
        self.assertEqual(g.get_vertex('v2'), g.vertices['v2'])
        g.add_vertex('v4')
        g.add_edge('v2', 'v4')
        g.add_edge('v3', 'v4')
        g.add_edge('v1', 'v4')
        self.assertEqual(g.get_vertex('v5'), None)
        # self.assertEqual(g.conn_components(), [['v1', 'v2', 'v3', 'v4']])
        self.assertFalse(g.is_bipartite())

    # def test_04(self):
    #     g = Graph("test4.txt")
    #     g.vertices
    #     g.conn_components()
    #     g.is_bipartite()

        

if __name__ == '__main__':
   unittest.main()
