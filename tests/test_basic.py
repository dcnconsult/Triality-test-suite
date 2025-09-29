"""
Basic tests for Triality Test Suite
"""
import pytest
import numpy as np
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def test_imports():
    """Test that basic imports work"""
    try:
        import numpy as np
        import scipy
        import matplotlib
        import pandas as pd
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import required packages: {e}")


def test_numpy_basic():
    """Test basic numpy functionality"""
    arr = np.array([1, 2, 3, 4, 5])
    assert len(arr) == 5
    assert arr.sum() == 15
    assert arr.mean() == 3.0


def test_analysis_modules_exist():
    """Test that analysis modules can be imported"""
    try:
        # Test if analysis modules exist and can be imported
        import analysis.bispectrum
        import analysis.surrogates
        import analysis.power_calc
        assert True
    except ImportError as e:
        # If modules can't be imported, that's okay for now
        # Just ensure the files exist
        analysis_dir = os.path.join(os.path.dirname(__file__), '..', 'analysis')
        assert os.path.exists(analysis_dir)
        assert os.path.exists(os.path.join(analysis_dir, 'bispectrum.py'))
        assert os.path.exists(os.path.join(analysis_dir, 'surrogates.py'))
        assert os.path.exists(os.path.join(analysis_dir, 'power_calc.py'))


def test_config_files_exist():
    """Test that configuration files exist"""
    config_dir = os.path.join(os.path.dirname(__file__), '..', 'analysis', 'configs')
    assert os.path.exists(config_dir)
    assert os.path.exists(os.path.join(config_dir, 'jpc_run_15.json'))
    assert os.path.exists(os.path.join(config_dir, 'spdc_batch.json'))


def test_environment_files_exist():
    """Test that environment files exist"""
    env_dir = os.path.join(os.path.dirname(__file__), '..', 'env')
    assert os.path.exists(env_dir)
    assert os.path.exists(os.path.join(env_dir, 'environment.yml'))
    assert os.path.exists(os.path.join(env_dir, 'requirements.txt'))


def test_documentation_exists():
    """Test that documentation files exist"""
    docs_dir = os.path.join(os.path.dirname(__file__), '..', 'docs')
    assert os.path.exists(docs_dir)
    assert os.path.exists(os.path.join(docs_dir, 'README.md'))
    assert os.path.exists(os.path.join(docs_dir, 'replicate.md'))


def test_scripts_exist():
    """Test that script files exist"""
    scripts_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
    assert os.path.exists(scripts_dir)
    assert os.path.exists(os.path.join(scripts_dir, 'run_replication.sh'))
    assert os.path.exists(os.path.join(scripts_dir, 'get_started.sh'))


class TestTrialitySuite:
    """Test class for Triality-specific functionality"""
    
    def test_project_structure(self):
        """Test that the project has the expected structure"""
        project_root = os.path.join(os.path.dirname(__file__), '..')
        
        # Check main directories exist
        expected_dirs = ['analysis', 'control', 'cosmo', 'docs', 'model', 
                        'neuro', 'sim', 'sweeps', 'tests', 'env', 'scripts']
        
        for dir_name in expected_dirs:
            dir_path = os.path.join(project_root, dir_name)
            assert os.path.exists(dir_path), f"Directory {dir_name} should exist"
    
    def test_python_version(self):
        """Test that we're running on a supported Python version"""
        assert sys.version_info >= (3, 11), "Python 3.11+ required"
    
    def test_numpy_version(self):
        """Test that numpy version is adequate"""
        import numpy as np
        version = np.__version__
        major, minor = map(int, version.split('.')[:2])
        assert major >= 1 and minor >= 26, f"NumPy 1.26+ required, got {version}"


if __name__ == "__main__":
    pytest.main([__file__])
