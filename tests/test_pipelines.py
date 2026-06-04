"""
Unit Tests for Data Pipelines & ML Models
Ensures data quality and model accuracy
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from src.utils.data_quality import DataQualityChecker, DataValidator
from src.models.ml_models import DemandForecaster, CustomerSegmenter

class TestDataQuality:
    """Test data quality validation functions"""
    
    @pytest.fixture
    def sample_orders_df(self):
        """Sample orders dataframe"""
        return pd.DataFrame({
            'NAME_ON_ORDER': ['Alice', 'Bob', 'Charlie'],
            'INGREDIENTS': ['Apple, Banana', 'Mango, Orange', 'Berries, Kiwi'],
            'ORDER_TS': [datetime.now(), datetime.now(), datetime.now()],
            'ORDER_FILLED': [True, False, True]
        })
    
    def test_validate_orders_no_nulls(self, sample_orders_df):
        """Test that null validation works"""
        checker = DataQualityChecker()
        results = checker.validate_orders(sample_orders_df)
        
        assert results['no_null_names'] == True
        assert results['no_null_ingredients'] == True
    
    def test_check_duplicates(self):
        """Test duplicate detection"""
        df = pd.DataFrame({
            'ORDER_ID': [1, 1, 2],
            'NAME': ['A', 'A', 'B']
        })
        
        checker = DataQualityChecker()
        duplicates = checker.check_duplicates(df, ['ORDER_ID'])
        
        assert duplicates == 1
    
    def test_check_missing_values(self):
        """Test missing value detection"""
        df = pd.DataFrame({
            'COL1': [1, 2, None],
            'COL2': ['A', 'B', 'C']
        })
        
        checker = DataQualityChecker()
        missing = checker.check_missing_values(df)
        
        assert 'COL1' in missing
        assert missing['COL1'] == 1

class TestDataValidator:
    """Test input validation functions"""
    
    def test_validate_email(self):
        """Test email validation"""
        assert DataValidator.validate_email("test@example.com") == True
        assert DataValidator.validate_email("invalid-email") == False
    
    def test_validate_phone(self):
        """Test phone validation"""
        assert DataValidator.validate_phone("1234567890") == True
        assert DataValidator.validate_phone("abc") == False
    
    def test_validate_currency(self):
        """Test currency validation"""
        assert DataValidator.validate_currency(12.99) == True
        assert DataValidator.validate_currency(-5.0) == False
    
    def test_sanitize_string(self):
        """Test string sanitization"""
        result = DataValidator.sanitize_string("test'string")
        assert "test''string" in result

class TestMLModels:
    """Test machine learning models"""
    
    @pytest.fixture
    def sample_time_series(self):
        """Sample time series data"""
        dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
        orders = np.random.randint(10, 50, 100)
        return pd.DataFrame({
            'SUMMARY_DATE': dates,
            'TOTAL_ORDERS': orders,
            'UNIQUE_CUSTOMERS': np.random.randint(5, 30, 100)
        })
    
    def test_demand_forecaster_initialization(self):
        """Test forecaster initialization"""
        forecaster = DemandForecaster()
        assert forecaster is not None
        assert forecaster.model is None
    
    def test_prepare_time_series(self, sample_time_series):
        """Test time series preparation"""
        forecaster = DemandForecaster()
        prepared = forecaster.prepare_time_series_data(sample_time_series)
        
        assert 'ORDERS_LAG_1' in prepared.columns
        assert 'ORDERS_LAG_7' in prepared.columns
        assert len(prepared) < len(sample_time_series)  # Due to NaN drops
    
    def test_customer_segmenter(self):
        """Test customer segmentation"""
        segmenter = CustomerSegmenter(n_clusters=3)
        
        df = pd.DataFrame({
            'CUSTOMER_ID': [1, 2, 3, 4],
            'CUSTOMER_NAME': ['A', 'B', 'C', 'D'],
            'LAST_ORDER_DATE': [
                datetime.now() - timedelta(days=10),
                datetime.now() - timedelta(days=50),
                datetime.now() - timedelta(days=100),
                datetime.now() - timedelta(days=5)
            ],
            'TOTAL_ORDERS': [10, 5, 2, 20]
        })
        
        rfm = segmenter.prepare_rfm_features(df)
        assert 'RECENCY' in rfm.columns
        assert 'FREQUENCY' in rfm.columns
        assert 'MONETARY' in rfm.columns

class TestIntegration:
    """Integration tests"""
    
    def test_end_to_end_pipeline(self):
        """Test complete pipeline flow"""
        # Create sample data
        orders_df = pd.DataFrame({
            'NAME_ON_ORDER': ['Test User'] * 5,
            'INGREDIENTS': ['Apple, Banana'] * 5,
            'ORDER_TS': pd.date_range(start='2024-01-01', periods=5, freq='D'),
            'ORDER_FILLED': [True] * 5
        })
        
        # Validate
        checker = DataQualityChecker()
        results = checker.validate_orders(orders_df)
        
        assert all(results.values())

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
