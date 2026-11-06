# Diabetes Prediction MLOps Architecture

The project uses the Churn Prediction repository as an architectural reference, with diabetes-specific data contracts.

```text
Raw diabetes CSV
   |
   v
Load -> Validate -> Split -> Preprocess -> Train
   |                                  |
   v                                  v
Data reports                     Evaluation
                                      |
                                      v
                              Quality gate / lifecycle
                                      |
                                      v
                              Inference predictions
                                      |
                                      v
                         Deployment bundle (Lab 11)
                                      |
                         +------------+------------+
                         |                         |
                       FastAPI                   Docker
                         |                         |
                    JSONL events               Kubernetes
                         |
                         v
             Lab 13 monitoring and drift reports
                         |
                         v
              Reviewed labelled data required
                         |
                         v
                 Candidate retraining
```

The Labs 1–6 Pima-style experiment remains separate from the Labs 7–13 eight-feature diabetes workflow. This avoids silently changing feature meanings or target labels.
