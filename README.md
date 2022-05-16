# ProductivityTools.TechBricks.Api

![Class](./Images/ClassCategory.png)




```
@{name='VS';owners=@('pwujczyk@gmail.com','gopara@gmail.com');Data=@(@{shortuct="zrt";Explanation="fda"},@{shortuct="zrt";Explanation="fda"})}|ConvertTo-Json

Invoke-WebRequest -Uri http://127.0.0.1:8080/Card -Method Post -Body (@{name='VS';owners=@('pwujczyk@gmail.com','gopara@gmail.com');data=@(@{shortcut="zrt1";explanation="fda"},@{shortcut="zrt2";explanation="fda"})}|ConvertTo-Json) -ContentType application/json
```


Env variable for firebase:
$env:GOOGLE_APPLICATION_CREDENTIALS="D:\Bitbucket\all.configuration\pttechbricksapi-adminsdk.json"