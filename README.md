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

```
Invoke-WebRequest -Uri http://127.0.0.1:8080/Card -Method Post -Body (@{name='VS';owners=@('pwujczyk@gmail.com','gopara@gmail.com');data=@(@{shortcut="zrt1";explanation="fda"},@{shortcut="zrt2";explanation="fda"})}|ConvertTo-Json) -ContentType application/json
```

in requrements maybe firestore shuld be added

API which needs to be enabled
- Cloud Run API
- Artifact Repository API