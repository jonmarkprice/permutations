import unittest
from unittest.case import skip
from main import compose, make_map, Permutation, identity, predecessor, successor

class TestCase(unittest.TestCase):

    
    def test_str(self):
        p1 = make_map([[1], [2], [3]])
        self.assertEqual(str(p1), 'id')

    def test_make_map(self):
        p1 = make_map([[1, 2], [3]])
        self.assertEqual(p1.cardinality, 3)
        self.assertDictEqual(p1.mapping, {1: 2, 2: 1, 3: 3})

        p1_abbrev = make_map([[1, 2]], n=3)
        self.assertEqual(p1, p1_abbrev)

        p2 = make_map([[1, 3], [2], [4]])
        p2_abbrev = make_map([[1, 3]], n=4)
        self.assertEqual(p2, p2_abbrev)

        
    def test_str_make_map(self):
        p1 = make_map([[1, 2], [3]])
        self.assertEqual(str(p1), '(1 2)')


    # TODO: More tests

    # @unittest.skip('')
    def test_compose(self):
        s = Permutation(3, {1: 2, 2: 3, 3: 1}, name='s')
        t = Permutation(3, {1: 2, 2: 1, 3: 3}, name='t')
        
        self.assertEqual(str(s), '(1 2 3)')
        self.assertEqual(str(t), '(1 2)')

        st = Permutation(3, {1: 3, 2: 2, 3: 1})
        self.assertDictEqual(st.mapping, compose(s, t).mapping)
        self.assertEqual(str(compose(s, t)), '(1 3)')
        self.assertEqual(str(compose(t, s)), '(2 3)')

    
    def test_compose_different_cardinalities(self):
        t = make_map([[1, 2]])
        s = successor(3)
        self.assertEqual(str(compose(s, t)), '(1 3)')
        self.assertEqual(str(compose(t, s)), '(2 3)')


    def test_power(self):
        tr = make_map([[1, 2]])
        self.assertEqual(tr.pow(1), tr)
        self.assertEqual(tr.pow(2), identity(2))

        succ = make_map([[1, 2, 3]])
        pred = make_map([[1, 3, 2]])
        self.assertEqual(succ.pow(1), succ)
        self.assertEqual(succ.pow(2), pred)
        self.assertEqual(succ.pow(3), identity(3))
        self.assertEqual(pred.pow(2), succ)


    def test_negative_power(self):
        p1 = make_map([[1, 3], [2, 4, 5]])
        self.assertEqual(compose(p1.pow(-3), p1.pow(3)), identity(5))


    # @unittest.skip('')
    def test_inverse(self):
        p1 = make_map([[1, 3, 2]])
        self.assertEqual(p1.inverse(), make_map([[1, 2, 3]]))
        self.assertEqual(compose(p1, p1.inverse()), identity(3))
        self.assertEqual(compose(p1.inverse(), p1), identity(3))

        self.assertEqual(identity(4), identity(4).inverse())

        p2 = make_map([[1, 2]])
        self.assertEqual(p2, p2.inverse())


    def test_ext(self):
        p1 = make_map([[1, 2]])
        # p1_ext = p1.ext(4)make_map([[1, 2], [3], [4]])
        self.assertEqual(p1.ext(4), make_map([[1, 2], [3], [4]]))
        # self.assertDictEqual(p1.ext(4).mapping, make_map([[1, 2], [3], [4]]).mapping)


    def test_composition(self):
        # TODO: can we define compose as * as an operator
        # what about inverse?

        # TODO: write test to show that extending a pair
        # compose(p, tr(i, j).ext(len(p))) = compose(p, tr(i, j))
        # for any permutation p, and integer i, j <= n
        # In other words, extending is unnecessary when composing.

        # TODO: test [1, 1] = id
        # Do similar thing with .ext and id

        t = make_map([[1, 2]]) # TODO: 
        tr = lambda i, j: make_map([[i, j]])
        sigma = lambda n: compose(t, successor(n))
        
        for n in range(1, 5):
            self.assertEqual(sigma(n).inverse(), compose(predecessor(n), t))
            for k in range(2, n):
                self.assertEqual(sigma(n).pow(-k), sigma(n).pow(k).inverse())
                self.assertEqual(sigma(n).pow(-k), sigma(n).inverse().pow(k))
                self.assertEqual(sigma(n).pow(-k) * sigma(n).pow(k), identity(n))

                # This works!
                # but it's the wrong equation
                self.assertEqual(compose(sigma(n).pow(-k), t, sigma(n).pow(k)), tr(1, n - k + 1).ext(n))
                
                # TODO: try this one
                # self.assertEqual(compose(sigma(n).pow(k), t, sigma(n).pow(-k)), tr(1, k + 1).ext(n))



if __name__ == '__main__':
    unittest.main()