# ml-deployment-on-gcloud

## Initial description
In this project I'll create a pipeline to Continuous Integration (CI) and Continuous Development (CD) to deploy a machine learning (ML) model on Google Cloud Platform (GCP).

This ML model will be developed in Python as a containerized application using Flask as a web framework to expose the code. 

The pipeline will start with this GitHub repository, that will contain the needed files for my application. The GCP's Cloud Build API will automatically build our code each time we push a new commit and store my container image on GCP's Container Registry API.The building and store/registration steps will be coded in a YAML file, `cloudbuild.yaml`, that Cloud Build reads as default. In this YAML file I'll write the code to deploy my application/model on GCP's Cloud Run API.

I know that the first deploy will take some minutes, but I want to do some updates and re-deploy my aplication as fast as possible. First, I will understand how to use Docker's building cache to re-build my image fast and, second, I will try to rollout without downtime for my possible new updates.
