import json
import os
import numpy as np
from dataclasses import dataclass
from abc import ABC
from typing import Any, Sequence, Tuple

def debugprint(data):
    pass
    # print

@dataclass
class ClusterParametersBase:
    thumb_style: str = 'NONE'
    package: str = 'cluster_abc'
    class_name: str = 'ClusterBase'

    thumb_offsets: Sequence[float] = (6, -3, 7)

    tr_rotation: Sequence[float] = (7.5, -18, 10)
    tr_position: Sequence[float] = (-32.5, -14.5, -2.5)

    tl_rotation: Sequence[float] = (10, -15, 10)
    tl_position: Sequence[float] = (-12, -16, 3)

    mr_rotation: Sequence[float] = (-6, -34, 48)
    mr_position: Sequence[float] = (-29, -40, -13)

    ml_rotation: Sequence[float] = (6, -34, 40)
    ml_position: Sequence[float] = (-51, -25, -12)

    br_rotation: Sequence[float] = (-16, -33, 54)
    br_position: Sequence[float] = (-37.8, -55.3, -25.3)

    bl_rotation: Sequence[float] = (-4, -35, 52)
    bl_position: Sequence[float] = (-56.3, -43.3, -23.5)

    thumb_plate_tr_rotation: float = 0
    thumb_plate_tl_rotation: float = 0
    thumb_plate_mr_rotation: float = 0
    thumb_plate_ml_rotation: float = 0
    thumb_plate_br_rotation: float = 0
    thumb_plate_bl_rotation: float = 0

    thumb_screw_xy_locations: Sequence[Sequence[float]] = ((-21, -58),)
    separable_thumb_screw_xy_locations: Sequence[Sequence[float]] = ((-21, -58),)


class ClusterBase(ABC):
    parameter_type = ClusterParametersBase
    num_keys = 6
    is_tb = False

    def __init__(self, parent, t_parameters=None):
        self.overrides = {}
        self.g = parent.g
        self.p = parent.p
        self.parent = parent
        self.sh = parent.sh

        if t_parameters is None:
            t_parameters = self.parameter_type()

        self.tp = t_parameters


    def get_overrides(self):
        return self.overrides


    @staticmethod
    def name():
        return "ABC"

    def thumborigin(self):
        origin = self.parent.key_position([self.p.mount_width / 2, -(self.p.mount_height / 2), 0], 1, self.p.cornerrow)

        for i in range(len(origin)):
            origin[i] = origin[i] + self.tp.thumb_offsets[i]

        return origin

    def thumb_1x_layout(self, shape, cap=False):
        return shape

    def thumb_15x_layout(self, shape, cap=False, plate=True):
        return shape

    def thumbcaps(self, side='right'):
        return self.sh.sa_cap(1)

    def thumb(self, side="right"):
        return self.sh.single_plate(side=side)

    def thumb_connectors(self, side="right"):
        return self.sh.web_post_tl()


    def walls(self, side="right", skeleton=False):
        return self.sh.web_post_tl()

    def connection(self, side='right', skeleton=False):
        return self.sh.web_post_tl()


    def screw_positions(self):
        position = [self.thumborigin()]
        return position

    def get_extras(self, shape, pos):
        return shape

    def thumb_pcb_plate_cutouts(self, side="right"):
        return self.sh.plate_pcb_cutout(side=side)