from __future__ import annotations
import numpy as np
from pyscses.set_up_calculation import sites_data_from_file
from typing import Tuple, List
from pyscses.site_data import SiteData

class StructureData(object):
    """A `StructureData` object contains all the structural information
    necessary for a calculation, including the positions of all
    defect sites, and all defect segregation energies.

    Attributes:
        sites_data (list(SiteData)): List of `SiteData` objects for each site to be explicitly included in a calculation.
        adjacent_sites_data (tuple(SiteData, SiteData)): Pair of `SiteData` objects describing the sites immediately adjacent to the lower and upper x-bounds for the calculation.
            These `SiteData` objects are used to calculate the boundary terms for Poisson solver.
        x_limits (tuple(float, float)): x coordinates of the lower and upper bounds for the calculation.
        b (float): Length of the b dimension of the input structure (perpendicular to x).
        c (float): Length of the c dimension of the input structure (perpendicular to x).
        site_x_coords (np.array): Array of the unique x coordinates of the sites to be explicitly included in a calculation.
        system (str): ?? (TODO)

    """

    def __init__(self,
                 sites_data: List[SiteData],
                 x_limits: Tuple[float, float],
                 b: float,
                 c: float,
                 system: str) -> None:
        """Initialise a StructureData object.

        Args:
            sites_data (list(site_data)): List of `SiteData` objects.
            x_limits (tuple(float, float)):

        """
        (self.sites_data,
            self.adjacent_sites_data) = StructureData.split_sites_dat(
                sites_data=sites_data,
                x_limits=x_limits)
        self.x_limits = x_limits
        self.b = b
        self.c = c
        self.site_x_coords = np.unique([sd.x for sd in self.sites_data])
        self.system = system

    @staticmethod
    def split_sites_data(sites_data: List[SiteData],
                         x_limits: Tuple[float, float]) -> Tuple[List[SiteData], Tuple[SiteData, SiteData]]:
        """TODO"""
        x_coords = [sd.x for sd in sites_data]
        index_lower = int(np.searchsorted(x_coords, x_limits[0]))
        index_upper = int(np.searchsorted(x_coords, x_limits[1]))
        adjacent_sites_data = sites_data[index_lower-1], sites_data[index_upper]
        inner_sites_data = sites_data[index_lower:index_upper]
        return inner_sites_data, adjacent_sites_data


    @classmethod
    def from_file(cls,
                  filename: str,
                  x_limits: Tuple[float, float],
                  b: float,
                  c: float,
                  system: str,
                  clustering_threshold: float = 1e-10,
                  site_charge: bool = False) -> StructureData:
        """TODO"""
        sites_data = sites_data_from_file(filename=filename,
                                          clustering_threshold=clustering_threshold,
                                          site_charge=site_charge)
        return StructureData(sites_data=sites_data,
                             x_limits=x_limits,
                             b=b,
                             c=c,
                             system=system)

    @property
    def limits(self) -> Tuple[float, float]:
        """TODO"""
        min_offset = (self.site_x_coords[1] - self.adjacent_sites_data[0].x)/2.0
        max_offset = (self.adjacent_sites_data[1].x - self.site_x_coords[-2])/2.0
        if self.system == 'single':
            return (min_offset, max_offset)
        elif self.system == 'double':
            return (min_offset, min_offset)
        else:
            raise Exception("TODO")

    @property
    def limits_for_laplacian(self) -> Tuple[float, float]:
        """TODO"""
        min_offset = (self.site_x_coords[1] - self.adjacent_sites_data[0].x)/2.0
        max_offset = (self.adjacent_sites_data[1].x - self.site_x_coords[-2])/2.0
        if self.system == 'single':
            return (self.site_x_coords[0] - self.adjacent_sites_data[0].x,
                    self.adjacent_sites_data[1].x - self.site_x_coords[-1])
        elif self.system == 'double':
                return (self.site_x_coords[0] - self.adjacent_sites_data[0].x,
                        self.site_x_coords[0] - self.adjacent_sites_data[0].x)
        else:
            raise Exception("TODO")
