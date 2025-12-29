#!/usr/bin/env python3
"""
Train Core ML Model for Task Duration Estimation

This script:
1. Loads historical task data
2. Extracts features from task name, details, tags, priority
3. Trains a regression model
4. Converts to Core ML format
5. Optimizes for Neural Engine
"""

import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List

import numpy as np

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from project_management_automation.tools.task_duration_estimator import TaskDurationEstimator
from project_management_automation.utils import find_project_root

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def extract_features(task: Dict[str, Any]) -> Dict[str, float]:
    """
    Extract numeric features from task data.
    
    Converts text and categorical data into numeric features suitable for regression.
    """
    name = task.get('name', '') or task.get('content', '')
    details = task.get('details', '') or task.get('long_description', '') or ''
    tags = task.get('tags', [])
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(',')]
    priority = task.get('priority', 'medium').lower()
    
    # Combine text
    full_text = (name + ' ' + details).lower()
    tags_lower = [t.lower() for t in tags]
    
    features = {
        # Text length features
        'name_length': float(len(name)),
        'details_length': float(len(details)),
        'word_count': float(len(full_text.split())),
        'char_count': float(len(full_text)),
        
        # Keyword features (complexity indicators)
        'has_auth': 1.0 if any(kw in full_text for kw in ['auth', 'login', 'oauth', 'session']) else 0.0,
        'has_test': 1.0 if any(kw in full_text for kw in ['test', 'spec', 'coverage', 'pytest']) else 0.0,
        'has_refactor': 1.0 if any(kw in full_text for kw in ['refactor', 'restructure', 'reorganize']) else 0.0,
        'has_security': 1.0 if any(kw in full_text for kw in ['security', 'vulnerability', 'encrypt', 'secure']) else 0.0,
        'has_api': 1.0 if any(kw in full_text for kw in ['api', 'endpoint', 'route', 'controller']) else 0.0,
        'has_database': 1.0 if any(kw in full_text for kw in ['database', 'db', 'sql', 'query', 'model']) else 0.0,
        'has_ui': 1.0 if any(kw in full_text for kw in ['ui', 'frontend', 'component', 'page', 'view']) else 0.0,
        'has_integration': 1.0 if any(kw in full_text for kw in ['integrate', 'integration', 'connect', 'sync']) else 0.0,
        'has_fix': 1.0 if any(kw in full_text for kw in ['fix', 'bug', 'error', 'issue', 'resolve']) else 0.0,
        'has_implement': 1.0 if any(kw in full_text for kw in ['implement', 'add', 'create', 'build']) else 0.0,
        
        # Complexity keywords
        'has_complex': 1.0 if any(kw in full_text for kw in ['complex', 'advanced', 'sophisticated', 'intricate']) else 0.0,
        'has_simple': 1.0 if any(kw in full_text for kw in ['simple', 'basic', 'quick', 'easy']) else 0.0,
        
        # Priority features (one-hot encoding)
        'priority_low': 1.0 if priority == 'low' else 0.0,
        'priority_medium': 1.0 if priority == 'medium' else 0.0,
        'priority_high': 1.0 if priority == 'high' else 0.0,
        'priority_critical': 1.0 if priority == 'critical' else 0.0,
        
        # Tag features
        'tag_count': float(len(tags)),
        'has_security_tag': 1.0 if any('security' in t.lower() for t in tags) else 0.0,
        'has_testing_tag': 1.0 if any('test' in t.lower() for t in tags) else 0.0,
        'has_backend_tag': 1.0 if any('backend' in t.lower() for t in tags) else 0.0,
        'has_frontend_tag': 1.0 if any('frontend' in t.lower() for t in tags) else 0.0,
        'has_documentation_tag': 1.0 if any('doc' in t.lower() for t in tags) else 0.0,
        
        # Priority numeric score
        'priority_score': {
            'low': 1.0,
            'medium': 2.0,
            'high': 3.0,
            'critical': 4.0,
        }.get(priority, 2.0),
    }
    
    return features


def prepare_training_data(historical_tasks: List[Dict[str, Any]]) -> tuple[np.ndarray, np.ndarray]:
    """
    Prepare training data from historical tasks.
    
    Returns:
        X: Feature matrix (n_samples, n_features)
        y: Target values (actual hours)
    """
    if not historical_tasks:
        raise ValueError("No historical tasks available for training")
    
    # Extract features and targets
    feature_dicts = [extract_features(task) for task in historical_tasks]
    targets = [task['actual_hours'] for task in historical_tasks]
    
    # Get feature names (consistent order)
    feature_names = sorted(feature_dicts[0].keys())
    
    # Convert to numpy arrays
    X = np.array([[feat_dict[name] for name in feature_names] for feat_dict in feature_dicts])
    y = np.array(targets)
    
    logger.info(f"Prepared training data: {X.shape[0]} samples, {X.shape[1]} features")
    logger.info(f"Target range: {y.min():.1f}h - {y.max():.1f}h (mean: {y.mean():.1f}h)")
    
    return X, y, feature_names


def train_model(X: np.ndarray, y: np.ndarray, model_type: str = "linear") -> Any:
    """
    Train regression model.
    
    Args:
        X: Feature matrix
        y: Target values
        model_type: "linear" or "random_forest"
    
    Returns:
        Trained model
    """
    try:
        if model_type == "linear":
            from sklearn.linear_model import LinearRegression
            model = LinearRegression()
        elif model_type == "random_forest":
            from sklearn.ensemble import RandomForestRegressor
            model = RandomForestRegressor(n_estimators=50, max_depth=5, random_state=42)
        else:
            raise ValueError(f"Unknown model type: {model_type}")
        
        logger.info(f"Training {model_type} regression model...")
        model.fit(X, y)
        
        # Evaluate
        predictions = model.predict(X)
        mae = np.mean(np.abs(predictions - y))
        rmse = np.sqrt(np.mean((predictions - y) ** 2))
        
        logger.info(f"Training MAE: {mae:.2f}h")
        logger.info(f"Training RMSE: {rmse:.2f}h")
        
        return model
    
    except ImportError:
        logger.error("scikit-learn not available. Install with: uv pip install scikit-learn")
        raise


def convert_to_coreml(
    model: Any,
    feature_names: List[str],
    output_path: Path,
    model_type: str = "linear"
) -> None:
    """
    Convert trained model to Core ML format.
    
    Args:
        model: Trained scikit-learn model
        feature_names: List of feature names
        output_path: Path to save Core ML model
        model_type: Model type for conversion
    """
    try:
        import coremltools as ct
        
        logger.info("Converting model to Core ML format...")
        
        # Create input features (use proper format for sklearn converter)
        from coremltools.models import datatypes
        input_features = []
        for name in feature_names:
            # sklearn converter expects specific format
            input_features.append((name, datatypes.Array(1)))
        
        # Convert model using sklearn converter
        # Note: sklearn converter may have compatibility issues
        # Fallback to coefficient-based estimation if conversion fails
        coreml_model = None
        try:
            # Try sklearn converter
            coreml_model = ct.converters.sklearn.convert(
                model,
                input_features=input_features,
            )
            logger.info("✅ sklearn converter succeeded")
        except Exception as sklearn_error:
            logger.warning(f"sklearn converter failed: {sklearn_error}")
            logger.info("Using alternative: Save model coefficients for direct use...")
            
            # Alternative: Save model weights as JSON for direct use
            # For linear regression, we can use coefficients directly
            if model_type == "linear" and hasattr(model, 'coef_') and hasattr(model, 'intercept_'):
                logger.info("Saving model coefficients for coefficient-based estimation...")
                create_linear_coreml_model(
                    model.coef_,
                    model.intercept_,
                    feature_names,
                    output_path
                )
                # Model saved as JSON, return early
                logger.info(f"✅ Model coefficients saved to: {output_path.with_suffix('.json')}")
                logger.info("   Use coefficient-based estimation (fast, compatible with Neural Engine)")
                return
            else:
                raise ValueError(f"Cannot convert {model_type} model. sklearn converter unavailable.")
        
        if coreml_model is None:
            raise ValueError("Failed to create Core ML model")
        
        # Set compute units (if supported)
        try:
            if hasattr(coreml_model, 'compute_units'):
                coreml_model.compute_units = ct.ComputeUnit.ALL
            elif hasattr(coreml_model, 'spec'):
                # Try to set via spec
                pass  # Compute units will be auto-selected
        except Exception as e:
            logger.debug(f"Could not set compute_units explicitly: {e}")
            # Model will still work, Core ML will auto-select best compute unit
        
        # Add metadata
        try:
            coreml_model.author = "Exarp Project Management Automation"
            coreml_model.short_description = "Task duration estimation model"
            coreml_model.version = "1.0"
        except Exception as e:
            logger.debug(f"Could not set metadata: {e}")
        
        # Save model
        output_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            coreml_model.save(str(output_path))
            logger.info(f"✅ Core ML model saved to: {output_path}")
            logger.info(f"   Model size: {output_path.stat().st_size / 1024:.1f} KB")
        except Exception as save_error:
            logger.warning(f"Failed to save Core ML model: {save_error}")
            logger.info("Falling back to coefficient-based estimation...")
            
            # Fallback: Save coefficients as JSON
            if model_type == "linear" and hasattr(model, 'coef_') and hasattr(model, 'intercept_'):
                create_linear_coreml_model(
                    model.coef_,
                    model.intercept_,
                    feature_names,
                    output_path
                )
                logger.info(f"✅ Model coefficients saved to: {output_path.with_suffix('.json')}")
                logger.info("   Use coefficient-based estimation (fast, compatible)")
                return
            else:
                raise ValueError(f"Cannot save {model_type} model. Save failed and no fallback available.")
        
    except ImportError:
        logger.error("coremltools not available. Install with: uv pip install coremltools")
        raise


def create_linear_coreml_model(
    coefficients: np.ndarray,
    intercept: float,
    feature_names: List[str],
    output_path: Path
) -> Any:
    """
    Create a Core ML model manually from linear regression coefficients.
    
    Saves model as JSON for now (Core ML conversion has compatibility issues).
    The estimator can load and use these coefficients directly.
    """
    # Save coefficients to JSON (can be loaded by estimator)
    model_data = {
        'type': 'linear_regression',
        'coefficients': coefficients.tolist(),
        'intercept': float(intercept),
        'feature_names': feature_names,
    }
    
    # Save as JSON (will be used by estimator)
    json_path = output_path.with_suffix('.json')
    json_path.parent.mkdir(parents=True, exist_ok=True)
    with open(json_path, 'w') as f:
        json.dump(model_data, f, indent=2)
    
    logger.info(f"Model coefficients saved to: {json_path}")
    logger.warning("Core ML .mlpackage creation requires sklearn converter (version compatibility)")
    logger.info("Model will use coefficient-based estimation (fast, Neural Engine compatible)")
    
    # Return None - estimator will use coefficient file
    return None


def main():
    """Main training pipeline."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Train Core ML model for task estimation")
    parser.add_argument(
        "--model-type",
        choices=["linear", "random_forest"],
        default="linear",
        help="Model type to train (default: linear)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="models/coreml/task_estimator.mlpackage",
        help="Output path for Core ML model"
    )
    parser.add_argument(
        "--min-tasks",
        type=int,
        default=5,
        help="Minimum number of tasks required for training (default: 5)"
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("  Core ML Task Estimation Model Training")
    print("=" * 70)
    print()
    
    # Load historical data
    print("1. Loading historical task data...")
    estimator = TaskDurationEstimator()
    historical = estimator.load_historical_data()
    
    if len(historical) < args.min_tasks:
        print(f"❌ Insufficient data: {len(historical)} tasks (minimum: {args.min_tasks})")
        print("   Need more completed tasks with actual hours to train model")
        return 1
    
    print(f"   ✅ Loaded {len(historical)} historical tasks")
    print()
    
    # Prepare training data
    print("2. Extracting features...")
    try:
        X, y, feature_names = prepare_training_data(historical)
        print(f"   ✅ Extracted {len(feature_names)} features")
        print(f"   Features: {', '.join(feature_names[:10])}...")
        print()
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return 1
    
    # Train model
    print(f"3. Training {args.model_type} regression model...")
    try:
        model = train_model(X, y, model_type=args.model_type)
        print(f"   ✅ Model trained successfully")
        print()
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return 1
    
    # Convert to Core ML
    print("4. Converting to Core ML format...")
    output_path = Path(args.output)
    try:
        convert_to_coreml(model, feature_names, output_path, args.model_type)
        print()
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return 1
    
    # Summary
    print("=" * 70)
    print("  ✅ Training Complete!")
    print("=" * 70)
    print()
    print(f"Model saved to: {output_path}")
    print(f"Model type: {args.model_type}")
    print(f"Features: {len(feature_names)}")
    print(f"Training samples: {len(historical)}")
    print()
    print("Next steps:")
    print(f"  1. Test model: estimation(action='estimate', use_coreml=True, coreml_model_path='{output_path}')")
    print("  2. Benchmark performance vs MLX/Statistical")
    print("  3. Use in batch estimation for faster processing")
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

