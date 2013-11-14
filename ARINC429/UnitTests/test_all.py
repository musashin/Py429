'''
Created on 2013-11-13

@author: nicolas
'''
import unittest

if __name__ == "__main__":
    
    '''
    Test all the modules of the ARINC 429 Package
    '''
    suite = unittest.TestLoader().discover('.', pattern = "*Test.py")
    unittest.TextTestRunner(verbosity=1).run(suite)
    
