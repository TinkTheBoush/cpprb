import sys
import unittest

import jax.numpy as jnp

from cpprb import ReplayBuffer

@unittest.skipIf(sys.platform.startswith("win"), "JAX doesn't support Windows")
class TestJAX(unittest.TestCase):
    def test_add(self):
        rb = ReplayBuffer({"done": {}})

        done = jnp.asarray(1)

        rb.add(done=done)

    def test_nstep(self):
        rb = ReplayBuffer({"obs": {}, "rew": {}, "done": {}, "next_obs":{}},
                          Nstep={"size": 4, "rew": "rew", "next": "next_obs"})

        obs = jnp.asarray(1)
        rew = jnp.asarray(1)
        done = jnp.asarray(1)
        next_obs = jnp.asarray(1)

        rb.add(obs=obs, rew=rew, done=done, next_obs=next_obs)
        rb.add(obs=obs, rew=rew, done=done, next_obs=next_obs)
        rb.add(obs=obs, rew=rew, done=done, next_obs=next_obs)
        rb.add(obs=obs, rew=rew, done=done, next_obs=next_obs)


if __name__ == "__main__":
    unittest.main()
