"""
Created at 05.02.2020
"""

from PySDM.environments import Parcel
from PySDM.products.product import Product


class ParcelDisplacement(Product):

    def __init__(self):
        super().__init__(
            description="Parcel displacement",
            name="z",
            unit="m"
        )
        self.environment = None

    def register(self, builder):
        super().register(builder)
        assert isinstance(builder.core.env, Parcel)
        self.environment = builder.core.env

    def get(self):
        self.download_to_buffer(self.environment['z'])
        return self.buffer[0]
