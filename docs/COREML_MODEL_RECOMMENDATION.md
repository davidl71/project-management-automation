# Core ML Model Recommendation for Task Estimation

**Date:** 2025-12-28  
**Purpose:** Determine the most useful Core ML model for task duration estimation

---

## Task Requirements

### Input Features
- **Task name** (text): e.g., "Implement user authentication"
- **Task details** (text): e.g., "Add OAuth2 login with Google"
- **Tags** (categorical array): e.g., ["auth", "backend", "security"]
- **Priority** (categorical): "low", "medium", "high", "critical"

### Output
- **Estimate hours** (continuous): 0.5 - 100+ hours
- **Confidence** (optional): 0.0 - 1.0
- **Complexity** (optional): 1 - 10

### Model Type
**Regression** - Predicting a continuous numeric value (hours)

---

## Available Historical Data

- **19 completed tasks** with actual hours
- **100% have tags** and priority
- **Average duration:** 26.0 hours
- **Range:** 0.5h - 71.2h

**Data Quality:** Good for training a small model

---

## Model Options Comparison

### 🎯 Option 1: Custom Regression Model (RECOMMENDED)

**Approach:** Train a custom model on your historical task data

**Pros:**
- ✅ **Best fit** for your specific task patterns
- ✅ **Small model size** (< 10MB) - fast inference
- ✅ **Optimized for Neural Engine** - can use ANE operations
- ✅ **Uses your actual data** - learns your team's patterns
- ✅ **Fast training** - small dataset (19 tasks)

**Cons:**
- ⚠️ Requires training script
- ⚠️ Need feature engineering (text → numeric)

**Implementation:**
1. Feature engineering: Convert text to numeric features
2. Train regression model (scikit-learn or PyTorch)
3. Convert to Core ML format
4. Optimize for Neural Engine

**Best For:** Production use, optimal performance

---

### Option 2: CreateML Regression Model

**Approach:** Use Apple's CreateML tool to train from CSV/JSON

**Pros:**
- ✅ **Apple native** - designed for Core ML
- ✅ **GUI-based** - easy to use (Xcode)
- ✅ **Auto-optimization** - automatically optimized for Neural Engine
- ✅ **Good for tabular data** - structured features

**Cons:**
- ⚠️ Limited text processing (need feature engineering first)
- ⚠️ Requires Xcode/macOS GUI
- ⚠️ Less flexible than custom training

**Best For:** Quick prototyping, non-technical users

---

### Option 3: Scikit-learn → Core ML

**Approach:** Train with scikit-learn, convert to Core ML

**Pros:**
- ✅ **Familiar tools** - scikit-learn is well-known
- ✅ **Many algorithms** - Linear, Random Forest, Gradient Boosting
- ✅ **Easy conversion** - coremltools supports scikit-learn
- ✅ **Good performance** - proven algorithms

**Cons:**
- ⚠️ Need feature engineering (text → numeric)
- ⚠️ May not use Neural Engine optimally (depends on operations)

**Best For:** Data scientists, Python-first workflow

---

### Option 4: Pre-trained Text Model

**Approach:** Use existing Core ML text models

**Cons:**
- ❌ Not designed for regression
- ❌ Would need significant adaptation
- ❌ Larger model size
- ❌ Not optimized for this task

**Verdict:** Not recommended

---

## Recommendation: Custom Regression Model

### Why Custom Model?

1. **Perfect Fit:** Trained on your actual task data
2. **Small & Fast:** < 10MB, optimized for Neural Engine
3. **Accurate:** Learns your team's specific patterns
4. **Efficient:** Fast inference, low power consumption

### Model Architecture

**Recommended Approach:**

1. **Feature Engineering:**
   - Text features: Word count, keyword presence, complexity indicators
   - Categorical: One-hot encode tags and priority
   - Numeric: Tag count, priority score

2. **Model Type:**
   - **Linear Regression** (simple, fast, Neural Engine friendly)
   - **Random Forest** (better accuracy, may not use Neural Engine)
   - **Neural Network** (best for Neural Engine, more complex)

3. **Training:**
   - Use 19 historical tasks
   - Feature engineering pipeline
   - Train regression model
   - Convert to Core ML

4. **Optimization:**
   - Quantize to 8-bit (smaller, faster)
   - Optimize for Neural Engine operations
   - Test inference speed

---

## Implementation Plan

### Phase 1: Feature Engineering

```python
def extract_features(task):
    features = {
        # Text features
        'name_length': len(task['name']),
        'details_length': len(task.get('details', '')),
        'word_count': len(task['name'].split()) + len(task.get('details', '').split()),
        
        # Keyword features
        'has_auth': 'auth' in task['name'].lower() or 'auth' in task.get('details', '').lower(),
        'has_test': 'test' in task['name'].lower(),
        'has_refactor': 'refactor' in task['name'].lower(),
        
        # Categorical features (one-hot)
        'priority_low': 1 if task['priority'] == 'low' else 0,
        'priority_medium': 1 if task['priority'] == 'medium' else 0,
        'priority_high': 1 if task['priority'] == 'high' else 0,
        'priority_critical': 1 if task['priority'] == 'critical' else 0,
        
        # Tag features
        'tag_count': len(task.get('tags', [])),
        'has_security_tag': 'security' in [t.lower() for t in task.get('tags', [])],
        'has_testing_tag': 'test' in [t.lower() for t in task.get('tags', [])],
    }
    return features
```

### Phase 2: Model Training

```python
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import coremltools as ct

# Load historical data
data = load_historical_tasks()

# Extract features
X = [extract_features(task) for task in data]
y = [task['actual_hours'] for task in data]

# Train model
model = LinearRegression()  # or RandomForestRegressor
model.fit(X, y)

# Convert to Core ML
coreml_model = ct.converters.sklearn.convert(
    model,
    input_features=[ct.TensorType(name='features', shape=(len(X[0]),))],
    compute_units=ct.ComputeUnit.ALL,  # Enable Neural Engine
)

coreml_model.save('models/coreml/task_estimator.mlpackage')
```

### Phase 3: Integration

```python
# Use in estimation tool
estimation(
    action="estimate",
    name="Task name",
    use_coreml=True,
    coreml_model_path="models/coreml/task_estimator.mlpackage",
    compute_units="all",
)
```

---

## Quick Start: Simple Linear Model

For immediate use, a **simple linear regression model** is recommended:

1. **Fast to train** (seconds)
2. **Small model** (< 1MB)
3. **Neural Engine compatible** (linear operations)
4. **Good baseline** accuracy

Can be enhanced later with:
- More features
- Non-linear models (Random Forest, Neural Network)
- Better feature engineering

---

## Summary

**Most Useful Model:** Custom Regression Model

**Why:**
- ✅ Best fit for your data
- ✅ Small and fast
- ✅ Neural Engine optimized
- ✅ Learns your patterns

**Next Steps:**
1. Create feature engineering pipeline
2. Train linear regression model
3. Convert to Core ML
4. Test with estimation tool

**Expected Performance:**
- Model size: < 5MB
- Inference time: < 10ms (Neural Engine)
- Accuracy: Better than statistical-only (uses learned patterns)

