import unittest
from pyscses.set_of_sites import SetOfSites
from pyscses.defect_species import DefectSpecies
from pyscses.defect_at_site import DefectAtSite
from pyscses.site import Site, LabelError
from unittest.mock import Mock, patch
import numpy as np

def create_mock_defect_species(n):
    labels = ['a', 'b', 'c', 'd', 'e']
    valence = [-2.0, -1.0, 0.0, 1.0, 2.0]
    mole_fraction = [0.15, 0.25, 0.35, 0.45, 0.55]
    mobility = [0.1, 0.2, 0.3, 0.4, 0.5]
    mock_defect_species = []
    for i in range(n):
        m = Mock(spec=DefectSpecies)
        m.label = labels.pop()
        m.mole_fraction = mole_fraction.pop()
        m.valence = valence.pop()
        m.mobility = mobility.pop()
        m.fixed = False
        mock_defect_species.append(m)
    return mock_defect_species

class TestSiteInit(unittest.TestCase):

    def test_site_is_initialised(self):
        mock_defect_species = create_mock_defect_species(2)
        with patch('pyscses.site.DefectAtSite', autospec=True) as mock_DefectAtSite:
            site = Site(label='A',
                        x=1.5,
                        defect_species=mock_defect_species,
                        defect_energies=[-0.2, +0.2])
        self.assertEqual(site.label, 'A')
        self.assertEqual(site.x, 1.5)
        self.assertEqual(site.defect_species, mock_defect_species)
        self.assertEqual(site.defect_energies, [-0.2, +0.2])
        np.testing.assert_equal(site.scaling, np.array([1.0, 1.0]))
        self.assertEqual(site.valence, 0.0)

    def test_site_is_initialised_with_optional_args(self):
        mock_defect_species = create_mock_defect_species(2)
        with patch('pyscses.site.DefectAtSite', autospec=True) as mock_DefectAtSite:
            site = Site(label='B',
                        x=1.5,
                        defect_species=mock_defect_species,
                        defect_energies=[-0.2, +0.2],
                        scaling=[0.5, 0.4],
                        valence=-2.0)
        self.assertEqual(site.label, 'B')
        self.assertEqual(site.x, 1.5)
        self.assertEqual(site.defect_species, mock_defect_species)
        self.assertEqual(site.defect_energies, [-0.2, +0.2])
        np.testing.assert_equal(site.scaling, np.array([0.5, 0.4]))
        self.assertEqual(site.valence, -2.0)

    def test_site_init_data_check_1(self):
        """Checks that initialising a Site object raises a ValueError if n(defect_species) != n(defect_energies)"""
        mock_defect_species = create_mock_defect_species(1)
        with patch('pyscses.site.DefectAtSite', autospec=True) as mock_DefectAtSite:
            with self.assertRaises(ValueError):
                site = Site(label='A',
                            x=1.5,
                            defect_species=mock_defect_species,
                            defect_energies=[-0.2, +0.2])

    def test_site_init_data_check_2(self):
        """Checks that initialising a Site object raises a ValueError if n(defect_species) != n(scaling) (if passed)"""
        mock_defect_species = create_mock_defect_species(2)
        with patch('pyscses.site.DefectAtSite', autospec=True) as mock_DefectAtSite:
            with self.assertRaises(ValueError):
                site = Site(label='A',
                            x=1.5,
                            defect_species=mock_defect_species,
                            defect_energies=[-0.2, +0.2],
                            scaling=[0.5])

class TestSite(unittest.TestCase):

    def setUp(self):
        mock_defect_species = create_mock_defect_species(2)
        with patch('pyscses.site.DefectAtSite', autospec=True) as mock_DefectAtSite:
            self.site = Site(label='A',
                        x=1.5,
                        defect_species=mock_defect_species,
                        defect_energies=[-0.2, +0.2])
        self.site.defects = [Mock(spec=DefectAtSite), Mock(spec=DefectAtSite)]


    def test_defect_with_label(self):
        self.site.defects[0].label = 'foo'
        self.site.defects[1].label = 'bar'
        self.assertEqual(self.site.defect_with_label('foo'), self.site.defects[0])
        self.assertEqual(self.site.defect_with_label('bar'), self.site.defects[1])

    def test_defect_with_label_2(self):
        """Checks that defect_with_label() raises a LabelError if the argument does not match any of the defect labels for this site."""
        self.site.defects[0].label = 'foo'
        self.site.defects[1].label = 'bar'
        with self.assertRaises(LabelError):
            self.site.defect_with_label('banana')

    def test_energies(self):
        self.site.defects[0].energy = -0.2
        self.site.defects[1].energy = +0.2
        self.assertEqual(self.site.energies(), [-0.2, +0.2])


if __name__ == '__main__':
    unittest.main()