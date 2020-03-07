import numpy as np
import unittest

from cpprb import (ReplayBuffer,PrioritizedReplayBuffer)
from cpprb import create_buffer


class TestIssue39(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.rb = ReplayBuffer(10,
                              {"obs": {"shape": 3},
                               "act": {"shape": 3},
                               "rew": {},
                               "next_obs": {"shape": 3},
                               "done": {}})
        for i in range(10):
            obs_act = np.array([i for _ in range(3)], dtype=np.float64)
            cls.rb.add(obs=obs_act,
                       act=obs_act,
                       next_obs=obs_act,
                       rew=float(i),
                       done=False)
        cls.s = cls.rb._encode_sample(range(10))

    def test_obs(self):
        self.assertTrue((self.s['obs'] == np.array(((0,0,0),
                                                    (1,1,1),
                                                    (2,2,2),
                                                    (3,3,3),
                                                    (4,4,4),
                                                    (5,5,5),
                                                    (6,6,6),
                                                    (7,7,7),
                                                    (8,8,8),
                                                    (9,9,9)))).all())

    def test_act(self):
        self.assertTrue((self.s['act'] == np.array(((0,0,0),
                                                    (1,1,1),
                                                    (2,2,2),
                                                    (3,3,3),
                                                    (4,4,4),
                                                    (5,5,5),
                                                    (6,6,6),
                                                    (7,7,7),
                                                    (8,8,8),
                                                    (9,9,9)))).all())
    def test_next_obs(self):
        self.assertTrue((self.s['next_obs'] == np.array(((0,0,0),
                                                         (1,1,1),
                                                         (2,2,2),
                                                         (3,3,3),
                                                         (4,4,4),
                                                         (5,5,5),
                                                         (6,6,6),
                                                         (7,7,7),
                                                         (8,8,8),
                                                         (9,9,9)))).all())
    def test_rew(self):
        self.assertTrue((self.s['rew'] == np.array((0,1,2,3,4,
                                                    5,6,7,8,9)).reshape(-1,1)).all())

    def test_done(self):
        self.assertTrue((self.s['done'] == np.zeros(shape=(10))).all())

class TestIssue40(unittest.TestCase):
    def test(self):
        buffer_size = 256
        obs_dim = 3
        act_dim = 1
        rb = ReplayBuffer(buffer_size,{"obs": {"shape": obs_dim}, "act": {"shape": act_dim}, "rew": {}, "next_obs": {"shape": obs_dim}, "done": {}})

        obs = np.ones(shape=(obs_dim))
        act = np.ones(shape=(act_dim))
        rew = 0
        next_obs = np.ones(shape=(obs_dim))
        done = 0

        for i in range(500):
            rb.add(obs=obs,act=act,rew=rew,next_obs=next_obs,done=done)


        batch_size = 32
        sample = rb.sample(batch_size)

class TestIssue43(unittest.TestCase):
    def test_buffer_size(self):
        buffer_size = 1000
        obs_dim = 3
        act_dim = 1

        rb = ReplayBuffer(buffer_size,
                          {"obs": {"shape": obs_dim},
                           "act": {"shape": act_dim},
                           "rew": {},
                           "next_obs": {"shape": obs_dim},
                           "done": {}})
        prb = PrioritizedReplayBuffer(buffer_size,
                                      {"obs": {"shape": obs_dim},
                                       "act": {"shape": act_dim},
                                       "rew": {},
                                       "next_obs": {"shape": obs_dim},
                                       "done": {}})

        self.assertEqual(1000,rb.get_buffer_size())
        self.assertEqual(1000,prb.get_buffer_size())

        rb._encode_sample([i for i in range(1000)])

class TestIssue44(unittest.TestCase):
    def test_cpdef_super(self):
        buffer_size = 256
        obs_dim = 15
        act_dim = 3

        prb = PrioritizedReplayBuffer(buffer_size,
                                      {"obs": {"shape": obs_dim},
                                       "act": {"shape": act_dim},
                                       "rew": {},
                                       "next_obs": {"shape": obs_dim},
                                       "done": {}})

        prb.clear()

class TestIssue45(unittest.TestCase):
    def test_large_size(self):
        buffer_size = 256
        obs_shape = (210, 160, 3)
        act_dim = 4

        rb = create_buffer(buffer_size,obs_shape=obs_shape,act_dim=act_dim,
                           is_discrete_action = True,
                           prioritized = True)

class TestIssue46(unittest.TestCase):
    def test_large_size(self):
        buffer_size = 256
        obs_shape = np.array((210, 160, 3))
        act_dim = 4

        rb = create_buffer(buffer_size,obs_shape=obs_shape,act_dim=act_dim,
                           is_discrete_action = True,
                           prioritized = True)
        rb._encode_sample((0))

class TestIssue90(unittest.TestCase):
    def test_with_empty(self):
        buffer_size = 32
        obs_shape = 3
        act_shape = 4

        rb = ReplayBuffer(buffer_size,{"obs": {"shape": obs_shape},
                                       "act": {"shape": act_shape},
                                       "done": {}})

        tx = rb.get_all_transitions()

        for key in ["obs","act","done"]:
            with self.subTest(key=key):
                np.testing.assert_allclose(tx[key],np.array([]))

    def test_with_one(self):
        buffer_size = 32
        obs_shape = 3
        act_shape = 4

        rb = ReplayBuffer(buffer_size,{"obs": {"shape": obs_shape},
                                       "act": {"shape": act_shape},
                                       "done": {}})

        v = {"obs": np.ones(shape=obs_shape),
             "act": np.zeros(shape=act_shape),
             "done": 0}

        rb.add(**v)

        tx = rb.get_all_transitions()

        for key in ["obs","act","done"]:
            with self.subTest(key=key):
                np.testing.assert_allclose(tx[key],v[key].reshape((1,-1)))

if __name__ == '__main__':
    unittest.main()
