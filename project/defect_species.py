class Defect_Species:
    """ The Defect_Species class includes the information about each defect species present in the system. 
        label refers to what the defect is call ie 'Vo' for an oxygen vacancy. The valence is the charge of the defect and the mole_fraction is the mole fraction of the defect present in the system. fixed refers to whether the system is following a Mott-Schottky (immobile dopant ions) or Gouy Chapman ( mobile dopant ions ) approximation."""
    def __init__( self, label, valence, mole_fraction, fixed = False, mobility = 0.0 ):
        assert( isinstance( label, str ) )
        assert( isinstance( valence, float ) )
        assert( isinstance( mole_fraction, float ) )
        self.label = label
        self.valence = valence
        self.mole_fraction = mole_fraction
        self.fixed = fixed
        self.mobility = mobility
