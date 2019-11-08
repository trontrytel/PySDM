"""
Created at 06.11.2019

@author: Piotr Bartman
@author: Michael Olesik
@author: Sylwester Arabas
"""

import numpy as np


class MoistAir:
    def __init__(self, grid, backend, thd_xzt_lambda, qv_xzt_lambda, rhod_z_lambda):
        self.backend = backend
        self.thd_lambda = thd_xzt_lambda
        self.qv_lambda = qv_xzt_lambda

        n_cell = int(np.prod(grid)) # TODO state.n_cell...
        self.qv = backend.array((n_cell,), float)
        self.thd = backend.array((n_cell,), float)

        self.RH = backend.array((n_cell,), float)
        self.p = backend.array((n_cell,), float)
        self.T = backend.array((n_cell,), float)

        rhod = np.repeat(rhod_z_lambda((np.arange(grid[1]) + 1/2)/grid[1]).reshape((1, grid[1])), grid[0], axis=0)
        self.rhod = backend.from_ndarray(rhod.ravel())

        self.sync()

    def sync(self):
        self.backend.upload(self.qv_lambda().ravel(), self.qv)
        self.backend.upload(self.thd_lambda().ravel(), self.thd)

        self.backend.apply(
            function=self.backend.temperature_pressure_RH,
            args=(self.rhod, self.thd, self.qv),
            output=(self.T, self.p, self.RH)
        )

