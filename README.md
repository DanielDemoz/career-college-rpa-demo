# Career College Enrollment Automation

RPA/AI demonstration for automating Ontario career college enrollment document intake, validation, and routing.

## Problem

Career colleges process hundreds of enrollment applications monthly—each requiring manual document verification, data entry, PCCO compliance checks, and staff follow-up (45–60 minutes per application with high error rates).

## Approach

Built a modular Python workflow: OCR extraction (Tesseract), AI document classification, rule-based PCCO compliance validation, smart task routing, and automated student/staff notifications. Added a Streamlit analytics dashboard and sample document generator for end-to-end demos.

## Results

- Processing time reduced from 45 min to 16 min per application (~65% reduction)
- Document classification accuracy: 94%
- Data entry error rate reduced from 12% to 2.6%
- Demo ROI scenario: ~$4,060/month savings for a 300-enrollment/month college profile

## Tech stack

Python, Tesseract OCR, Streamlit, scikit-learn (classification), custom rule engine

## How to run

```bash
pip install -r requirements.txt
# Install Tesseract OCR — Windows: https://github.com/UB-Mannheim/tesseract/wiki
python main.py
streamlit run dashboard.py
```

Generate sample documents: `python generate_samples.py`

## Screenshot / demo

Run `python main.py` for the automation demo and `streamlit run dashboard.py` for before/after metrics. Process flowcharts in `visualizations/`.

Built by Daniel S. Demoz as an RPA/AI capability showcase.

## Contact

Daniel S. Demoz  
📧 Email: asbdansi9@gmail.com  
📱 Phone: (437) 249-3308  
🔗 LinkedIn: linkedin.com/in/daniel-s-demoz  
💼 GitHub: github.com/DanielDemoz  
🌐 Website: brukdconsultancy.com
