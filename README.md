---
title: Credit Risk Prediction
emoji: 📊
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
---

# Module 10 deployment draft

This application serves Module 8 Trial 4, selected by validation default F1 among eight configurations. It uses the original fitted Module 5 preprocessor (23 original features to 89 model inputs) and unchanged model weights. EDUCATION codes 5 and 6 map to 0 before transformation.

Architecture: 89 → 64 ReLU → 32 ReLU → 1 sigmoid. Training learning rate 0.0005, batch size 32, selected epoch 6. Fixed classification threshold 0.5. Test accuracy 0.8205, default F1 0.486409. Tuning did not improve on the baseline test results. This course demonstration is not validated for lending decisions.

## Local use

Use Python 3.11. Install `requirements.txt`, run `python -m unittest test_prediction.py`, then `python app.py`. Open http://localhost:7860. The application does not retrain the model.

## Deployment setup (not yet executed)

1. Create a GitHub repository and upload the contents of this directory at its root, including `.github/workflows/deploy.yml`.
2. Create a Docker Space on Hugging Face with free CPU basic hardware; confirm pricing at creation.
3. Set GitHub repository variable `HF_SPACE_ID` to `username/space-name`.
4. Set GitHub Actions secret `HF_TOKEN` to a Hugging Face token permitted to write to that Space. Never put the token in source code or chat.
5. Push to `main`. Tests must pass before synchronization. Check both the GitHub Actions result and the Space build/runtime logs; synchronization success alone does not prove the application is healthy.
6. Test a fictional profile in the hosted interface and retain screenshots, URLs and commit ID for the report.

The included workflow performs CI checks and deployment synchronization. It does not implement retraining, drift monitoring, automated rollback or a hosted prediction health check. Gradio has a bounded version range and should be pinned to the verified version after a clean build. Linux container and hosted behavior still require verification.

Only the fitted preprocessor is exported from the original joblib bundle; customer IDs and training/test records are excluded.

References: https://huggingface.co/docs/hub/spaces-github-actions and https://huggingface.co/docs/hub/spaces-sdks-docker
