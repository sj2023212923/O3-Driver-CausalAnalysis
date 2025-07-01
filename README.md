# O3-Driver-CausalAnalysis
Integrating AutoML, SHAP, and causal inference to identify O₃ drivers
# O3-Driver-CausalAnalysis

This repository contains the code and data processing workflow for the manuscript:  
**"Integrating causal inference and interpretable automated machine learning to identify surface O₃ drivers in East China"**, submitted to *Environmental Modelling & Software*.

## 1. Overview

We develop an integrated framework that combines AutoML, SHAP (Shapley Additive Explanations), and causal inference algorithms (Causal Forest and Double Machine Learning) to identify the key environmental drivers of surface-level ozone (O₃) across East China during March 2022 to February 2023. The framework supports transparent, scalable, and causally robust environmental modeling.

## 2. Requirements

### Python Environment
- Python ≥ 3.10  
- Required packages:
  - pycaret
  - shap
  - scikit-learn
  - pandas
  - econml

You can install dependencies using:

```bash
pip install -r requirements.txt
