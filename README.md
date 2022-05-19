# ProductivityTools.TechBricks.Api

![Class](./Images/ClassCategory.png)


## Configuration
For local run I have Environment Variable set which points out to the ServiceAccont json file
![PycharmEnvVariable](Images/PycharmEnvVariable.png)

For GCP I setup the ``GOOGLE_CLOUD_PROJECT`` environment variable in the ``cloudbuild.yaml`` file
GCP is on it is own make an validation with this setup
```
- name: google/cloud-sdk
  args: [ 'gcloud', 'run', 'deploy', 'techbricksapi',
          '--image=us-central1-docker.pkg.dev/${PROJECT_ID}/apiimage/image:${SHORT_SHA}',
          '--region', 'us-central1', '--platform', 'managed',
          '--allow-unauthenticated' ,'--update-env-vars', 'GOOGLE_CLOUD_PROJECT=${PROJECT_ID}']
```