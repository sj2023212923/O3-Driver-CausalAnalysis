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
R Environment (optional for visualization)
R ≥ 4.2

Packages: ggplot2, mgcv

Other Tools
ArcGIS Pro 3.x (for spatial data processing and mapping)

Origin 2021 (for figure refinement and plotting)
├── data/                 # Example test data (see Zenodo DOI)
├── src/                  # Python scripts: model training, SHAP, causal estimation
├── results/              # Output files, SHAP plots, and ATE maps
├── requirements.txt      # Python dependencies
└── README.md             # This file
git clone https://github.com/sj2023212923/O3-Driver-CausalAnalysis.git
cd O3-Driver-CausalAnalysis
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cd src
python run_pipeline.py
SHAP values and causal estimates will be stored in /results.

5. Data Availability
All preprocessed input data and test samples are available at Zenodo:
https://doi.org/10.5281/zenodo.15780809
Including:

Surface-level O₃ concentrations (CNEMC)

ERA5 meteorological data (ECMWF)

Sentinel-5P TROPOMI tropospheric O₃ columns

Gridded socio-economic and emissions data

6. License
This project is licensed under the MIT License.

7. Contact
If you have questions or suggestions, please contact:
📧 Jing Shi — 13399424359@163.com
🏫 College of Geography and Environmental Science, Northwest Normal University
