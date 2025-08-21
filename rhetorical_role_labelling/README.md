# Rhetorical Role Labelling

This folder is for preparing and processing inputs to the **pretrained rhetorical role classifier** provided in the [Law-AI Semantic Segmentation repository](https://github.com/Law-AI/semantic-segmentation).

---
## Usage

1. **Prepare sentences**  
   Run the helper script to split judgments into sentences:

   ```bash
   python prepare_sentences.py
   ```
This generates sentences.txt with one sentence per line.

2. Run rhetorical role labelling
Follow the instructions in the [semantic-segmentation repo](https://github.com/Law-AI/semantic-segmentation) to perform inference with the pretrained variant of the Hier-BiLSTM-CRF model, using sentences.txt as input.

3. Postprocess output (optional)
After inference, you can convert the raw output into a CSV.
