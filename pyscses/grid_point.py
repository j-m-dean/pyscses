from __future__ import annotations
from typing import Optional, List
import numpy as np
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pyscses.site import Site

class GridPoint:
    """ The GridPoint class contains the information and calculations for each grid point individually """

    def __init__(self,
                 x: float,
                 volume: float) -> None:
        """Initialise a GridPoint object.

        Args:
            x (float): x coordinate of grid point.
            volume (float): volume of site at grid point.
        """
        self.x = x
        self.volume = volume
        self.sites: List[Site] = []

    def average_site_energy(self,
                            method: str = 'mean') -> Optional[np.ndarray]:
        """Returns the average segregation energy for all sites based on a specified method

        Args:
			method (str): The method in which the average segregation energies will be calculated.
						  'mean' - Returns the sum of all values at that site divided by the number of values at that site.
						  'min' - Returns the minimum segregation energy value for that site (appropriate for low temperature calculations).

		Returns:
            np.ndarray: Average segregation energies on a 1D grid.

		"""
        if self.sites:
            return avg(np.array([s.energies() for s in self.sites]), method)
        else:
            return None

def avg(energies,
	    method: str = 'mean') -> np.ndarray:
	"""Returns the average segregation energy for a site based on a specified method

	Args:
		energies (np.array): Segregation energies on 1D grid.
		method (str): The method in which the average segregation energies will be calculated.
					  'mean' - Returns the sum of all values at that site divided by the number of values at that site.
					  'min' - Returns the minimum segregation energy value for that site (appropriate for low temperature calculations).

	Returns:
		np.array: Average segregation energies on a 1D grid.

	"""
	if method == 'mean':
		return np.array([np.mean(row) for row in energies.T])
	elif method == 'min':
		return np.array([np.min(row) for row in energies.T])
	else:
		raise ValueError("method: {}".format(method))
