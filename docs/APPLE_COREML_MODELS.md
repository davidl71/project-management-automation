# Apple's Core ML Model Gallery

**Date:** 2025-12-28  
**Source:** [Apple Developer - Machine Learning Models](https://developer.apple.com/machine-learning/models/)

---

## Available Models on Apple's Website

Apple provides a curated collection of pre-trained Core ML models optimized for Apple Silicon and Neural Engine acceleration.

### Image Classification Models

1. **FastViT**
   - Fast Hybrid Vision Transformer architecture
   - Classifies the main object in images
   - Optimized for Neural Engine

2. **MobileNetV2**
   - MobileNetv2 architecture
   - Classifies the main object in images
   - Lightweight, mobile-optimized

3. **Resnet50**
   - Residual neural network
   - Image classification tasks
   - High accuracy

4. **MNIST**
   - Classifies handwritten digits (0-9)
   - Simple, educational model

### Depth Estimation

5. **Depth Anything V2**
   - Monocular depth estimation
   - Predicts depth from a single image
   - No stereo vision required

### Object Detection & Segmentation

6. **DETR Resnet50 Semantic Segmentation**
   - Detection Transformer (DETR) architecture
   - Object detection and panoptic segmentation
   - Returns semantic segmentation masks

7. **DeeplabV3**
   - Image segmentation model
   - Segments pixels into predefined classes
   - High-quality segmentation

8. **YOLOv3**
   - Detects and classifies 80 object types
   - Real-time object detection
   - Optimized for mobile

### Text/NLP Models

9. **BERT-SQuAD**
   - Question-answering model
   - Finds answers in text passages
   - Based on BERT architecture
   - **Note:** Not for text generation, only Q&A

### Custom Learning

10. **UpdatableDrawingClassifier**
    - K-nearest neighbors (KNN) model
    - Learns to recognize new drawings
    - On-device training capability

---

## ❌ Text Generation Models

**Unfortunately, Apple does not provide text generation models (like CodeLlama) in their official Core ML gallery.**

The available models focus on:
- ✅ Computer vision (images, depth, segmentation)
- ✅ Question answering (BERT-SQuAD)
- ❌ **No text generation models**
- ❌ **No code generation models**
- ❌ **No language models for test generation**

---

## Alternative Sources for Text Generation Core ML Models

### 1. Hugging Face Core ML Models

Search for Core ML models on Hugging Face:
- Filter by "coreml" tag
- Look for community-converted models
- Check model compatibility

### 2. Community Conversions

- **Apple's Core ML Tools**: Convert PyTorch/Transformers models
- **Hugging Face Optimum**: Some models have Core ML exports
- **Community repositories**: GitHub projects with converted models

### 3. Direct Conversion

Use `coremltools` to convert:
- PyTorch models
- Transformers models
- ONNX models (via conversion)

---

## Recommendations for Test Generation

Since Apple doesn't provide text generation models:

1. **Use MLX (Current Solution)** ✅
   - MLX CodeLlama works well
   - Metal GPU acceleration
   - No conversion needed

2. **Convert PyTorch CodeLlama**
   - Download PyTorch model from Hugging Face
   - Use `coremltools` to convert
   - Optimize for Neural Engine

3. **Find Pre-converted Models**
   - Search Hugging Face for Core ML CodeLlama
   - Check community repositories
   - Verify Neural Engine compatibility

4. **Use BERT-SQuAD for Q&A Tasks**
   - If test generation can be framed as Q&A
   - Apple's BERT-SQuAD is optimized
   - Limited to question-answering format

---

## Accessing Apple's Models

1. Visit: https://developer.apple.com/machine-learning/models/
2. Browse available models
3. Download `.mlpackage` or `.mlmodel` files
4. Integrate into your project

---

## Summary

**Apple's Core ML Gallery:**
- ✅ Great for computer vision tasks
- ✅ Optimized for Neural Engine
- ✅ Easy to integrate
- ❌ **No text/code generation models**

**For Test Generation:**
- Continue using MLX (GPU acceleration) ✅
- Or convert PyTorch CodeLlama to Core ML
- Or find community-converted models

