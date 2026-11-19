---
title: Credit Risk Prediction
emoji: 📊
colorFrom: blue
colorTo: green
sdk: static
app_file: index.html
---

# Module 10: browser-based model deployment

This Static Space runs the unchanged Module 8 Trial 4 neural network in the browser. The exported model contains its trained weights, fitted numerical means/scales, and fitted one-hot category order. EDUCATION 5 and 6 are mapped to 0. Unseen valid categories produce all-zero one-hot blocks, matching the Python preprocessor. No retraining is performed.

Trial 4 was selected using validation default F1 among eight configurations. Test accuracy was 82.05%, recall 38.43%, and F1 0.4864; tuning did not improve the baseline test results. The fixed classification threshold is 0.5.

The initial Docker design was replaced because the account's Space creation page required a paid plan for Docker/Gradio. Static hosting serves the HTML, JavaScript and model weights, while inference runs on the visitor's device. It is not a Python server or a hosted prediction API. Model weights are public. Form values are not sent to a prediction server.

The deployed files are index.html, inference.js, model.json, and this README. The original Python artifacts can remain in GitHub for provenance. CI/CD setup is a separate step; creating this Space alone does not complete CI/CD.

Limitations: historical dataset, low default recall, uncalibrated probability estimates, no authentication or drift monitoring, browser-dependent performance, and no automated retraining. This is a course demonstration, not a lending decision system.

Sources: https://huggingface.co/docs/hub/spaces-overview and https://huggingface.co/docs/hub/spaces-sdks-static
