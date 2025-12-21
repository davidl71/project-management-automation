# Ollama Model Performance Comparison (Intel Mac - CPU Only)

## Test Results Summary

Performance test results on Intel Mac with 4 CPU cores (no GPU acceleration).

### Model Comparison

| Model | Size | Duration | Throughput | Speedup |
|-------|------|----------|------------|---------|
| **llama3.2:1b** | 1.3 GB | 22.56s | **22.7 chars/sec** | **1.65x faster** ⚡ |
| llama3.2 | 2.0 GB | 37.23s | 10.9 chars/sec | Baseline |

### Key Findings

✅ **Smaller model = Much Faster!**
- `llama3.2:1b` (1.3GB) is **1.65x faster** than `llama3.2` (2.0GB)
- Throughput improved from 10.9 to 22.7 chars/sec
- Response time reduced from 37s to 23s

### Hardware Configuration Used

- **Platform**: Intel Mac
- **GPU**: None (CPU-only inference)
- **CPU Cores**: 4
- **Threads**: 3 (auto-optimized)
- **Context Size**: 2048 (auto-optimized for CPU)

### Recommendations for Intel Mac Users

Since GPU acceleration isn't available on Intel Macs, focus on:

1. **Use Smaller Models**: 
   - ✅ `llama3.2:1b` (1.3GB) - **Recommended** - Fast and efficient
   - `phi3` (2.3GB) - Good alternative
   - `llama3.2` (2.0GB) - Baseline, acceptable performance

2. **Optimize CPU Settings** (auto-applied):
   - Context size: 2048 (reduced for faster inference)
   - CPU threads: Match your core count - 1
   - Enable streaming for better perceived performance

3. **For Best Performance**:
   ```python
   from project_management_automation.tools.ollama_integration import generate_with_ollama
   
   result = generate_with_ollama(
       prompt="Your prompt",
       model="llama3.2:1b",  # Smallest, fastest
       stream=True,           # Better UX
       # Hardware optimizations auto-applied!
   )
   ```

## Expected Performance Improvements

When moving to smaller models on Intel Mac (CPU-only):

- **llama3.2:1b vs llama3.2**: ~1.65x faster ✅ (tested)
- **phi3 vs llama3.2**: ~1.3-1.5x faster (estimated)
- **Combined with optimizations**: Up to 2x total improvement

## Notes

- These results are for CPU-only inference on Intel Mac
- Apple Silicon Macs with Metal GPU would see 5-20x faster performance
- Smaller models trade some quality for significant speed improvements
- For most tasks, `llama3.2:1b` provides good quality with much better speed
