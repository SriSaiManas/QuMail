## Missing Test Files

### `tests/__init__.py`
"""python
Test package for QuMail application
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))