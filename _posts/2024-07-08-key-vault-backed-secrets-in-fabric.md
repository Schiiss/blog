---
title: "Key Vault Backed Secrets in Fabric 🔐"
date: 2024-07-08T10:00:00-04:00
categories:
  - Fabric
tags:
  - Data Engineering
  - Key Vault
  - Security
---

{% raw %}<img src="/blog/assets/images/blog_images/key-vault-backed-secrets-in-fabric/blog_image.jpg" alt="">{% endraw %}

In this post I wanted to share how to enable key vault backed secrets in Microsoft Fabric. I personally had a difficult time finding documentation on how to do this but after meeting with Microsoft they were able to point me to a guide on how to enable this. I wanted to step through something called [MSSparkUtils](https://learn.microsoft.com/en-us/fabric/data-engineering/microsoft-spark-utilities) which is a tool we can leverage to secure our notebook secrets.

## Spark Utilities ⚙️

[MSSparkUtils](https://learn.microsoft.com/en-us/fabric/data-engineering/microsoft-spark-utilities) is a built-in package to help you easily perform common tasks. You can use MSSparkUtils to work with file systems, to get environment variables, to chain notebooks together, and to work with secrets. The MSSparkUtils package is available in PySpark (Python) Scala, SparkR notebooks, and Fabric pipelines. For those familiar with databricks, this seems very similar to [dbutils]( https://learn.microsoft.com/en-us/azure/databricks/dev-tools/databricks-utils) from databricks.

One of the utilities MSSparkUtils offers is the [credentials utilities]( https://learn.microsoft.com/en-us/fabric/data-engineering/microsoft-spark-utilities#credentials-utilities), more specifically, they have a method/function called .getSecret that takes in two arguments:

1. The FQDN of the key vault

2. The name of the secret you want to reference

```python
mssparkutils.credentials.getSecret('https://<name>.vault.azure.net/', 'secret name')
```

The [documentation]( https://learn.microsoft.com/en-us/fabric/data-engineering/microsoft-spark-utilities#get-secret-using-user-credentials) mentions that the utility leverages ‘user credentials’ to get the secret.

## Spark Utilities in a Synapse Engineering Notebook 🧑‍💻

Running this credential utility in a data engineering notebook nets the following results. First let’s run the help command:

```python
mssparkutils.credentials.help()
```

The following results are displayed which mentions the two methods/functions mentioned in the documentation:

1. getToken(audience): returns AAD token for a given audience

2. getSecret(akvName, secret): returns AKV secret for a given akvName, secret key

[![credential_utility_help](/blog/assets/images/blog_images/key-vault-backed-secrets-in-fabric/credential_utility_help.png)](/blog/assets/images/blog_images/key-vault-backed-secrets-in-fabric/credential_utility_help.png){:target="_blank"}

Let’s run the getSecret method to retrieve a secret from one of our key vaults:

```python
print(mssparkutils.credentials.getSecret('https://your_fqdn.vault.azure.net/', 'your_secret'))
```

I have redacted my key vault FQDN and secret name but you can see I wrapped the mssparkutils.credentials.getSecret in a print statement and the secret comes back as [REDACTED]. This is to be expected, you should not be able to print the secret to the screen.

[![credential_utility_getsecret](/blog/assets/images/blog_images/key-vault-backed-secrets-in-fabric/credential_utility_getsecret.png)](/blog/assets/images/blog_images/key-vault-backed-secrets-in-fabric/credential_utility_getsecret.png){:target="_blank"}

## Key Vault Logs 🪵

As mentioned earlier, the documentation mentions that the utility leverages the ‘user credentials’ to get the secret. Let’s see how this works in practice my monitoring the logs of the key vault in a few scenarios.

I will leverage the below log analytics query to retrieve the key vault logs:

```sql
AzureDiagnostics
| where ResourceProvider =="MICROSOFT.KEYVAULT" and Resource =="AKV_RESOURCE_NAME"
```

If I run the notebook directly in the Fabric Data Engineering experience, I expect the logs to indicate it was my user account that ran the query against the key vault secrets. Investigating the logs shows the following results which are expected:

[![running_notebook_directly_as_conner](/blog/assets/images/blog_images/key-vault-backed-secrets-in-fabric/running_notebook_directly_as_conner.png)](/blog/assets/images/blog_images/key-vault-backed-secrets-in-fabric/running_notebook_directly_as_conner.png){:target="_blank"}

Next if we run this notebook in a schedule, we can also see in the logs, the key vault is accessed via my user account:

[![running_notebook_directly_as_conner_via_schedule](/blog/assets/images/blog_images/key-vault-backed-secrets-in-fabric/running_notebook_directly_as_conner_via_schedule.png)](/blog/assets/images/blog_images/key-vault-backed-secrets-in-fabric/running_notebook_directly_as_conner_via_schedule.png){:target="_blank"}

And finally executing the notebook as a user that does not have access to the key vault results in the following error:

Py4JJavaError: An error occurred while calling z:mssparkutils.credentials.getSecret.
: java.io.IOException: 403 {"error":{"code":"Forbidden","message":"Caller is not authorized to perform action on resource.\r\nIf role assignments, deny assignments or role definitions were changed recently, please observe propagation time.}

This all works just as the documentation mentioned. So why did we test all this? Was it because I did not trust the documentation? No. I was considering the implications of the utility leveraging the ‘user credentials’ in a production environment.

For example, what happens if my current company decides they have had enough of me and lets me go? How will the jobs stay running in production now that my account no longer exists?

Generally, I have run jobs in production using a generic service account which is not tied to a particular individual. Meaning the chance of interruptions due to account changes is less likely. I have not found a way to leverage a service account or SPN in to pull secrets from Key Vault in Fabric.

## Conclusion 🏁

In summary, enabling Key Vault-backed secrets in Microsoft Fabric using MSSparkUtils can streamline and secure secret management within your data engineering workflows. MSSparkUtils offers versatile utilities, akin to dbutils from Databricks, facilitating tasks like fetching secrets through user credentials. While this approach works well for individual accounts, it raises concerns for production environments dependent on user-specific credentials. A potential solution involves leveraging service accounts to avoid disruptions from personnel changes, although this remains an area needing further exploration within Fabric. By understanding and testing these utilities, you can better secure and manage secrets in your data engineering projects.