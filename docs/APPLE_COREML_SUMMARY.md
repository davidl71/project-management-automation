# Apple Core ML Models - Quick Summary

**Date:** 2025-12-28

## Available Models

Apple provides **10 pre-trained Core ML models** on their official website:

### ✅ Available Categories:
- **Image Classification**: FastViT, MobileNetV2, Resnet50, MNIST
- **Depth Estimation**: Depth Anything V2
- **Object Detection**: DETR, DeeplabV3, YOLOv3
- **Question Answering**: BERT-SQuAD
- **Custom Learning**: UpdatableDrawingClassifier

### ❌ NOT Available:
- **Text Generation Models** (like GPT, CodeLlama)
- **Code Generation Models**
- **Language Models for Test Generation**

## Key Finding

**Apple's Core ML gallery focuses on computer vision and Q&A tasks, not text/code generation.**

## For Test Generation

Since Apple doesn't provide text generation models:

1. ✅ **MLX (Current Solution)** - Working well with GPU acceleration
2. 🔄 **Convert PyTorch CodeLlama** - Use coremltools
3. 🔍 **Hugging Face** - Search for pre-converted Core ML models
4. 👥 **Community Models** - Check GitHub for converted models

## Access

Visit: https://developer.apple.com/machine-learning/models/

---

**Conclusion:** Continue using MLX for test generation, or convert PyTorch models to Core ML format.
