---
title: "An exploration of managed identities on Azure Virtual Machines"
date: 2021-03-11T15:34:30-04:00
categories:
  - Blog
tags:
  - Azure
  - Virtual Machines
  - Azure AD
---

{% raw %}<img src="{{ site.url }}{{ site.baseurl }}/assets/images/blog_images/2021-03-11-an-exploration-of-managed-identities-on-azure-virtual-machines/identity.jpeg" alt="">{% endraw %}

I find Managed Service Identities (MSI’s) in Azure to be rather curious. They address a familiar question application developers and DevOps engineers alike will have, “How do we manage and secure keys and secrets?” Traditionally, a Service Principal could authorize communication between Azure resources, but this approach comes with the overhead of managing an API key. Managed Identities set out to eliminate this overhead and turn that responsibility to Microsoft, who will manage the key for you. Maybe it is a VM, an App service, or even Kubernetes (god forbid). Many different services support managed service identities (link to azure services which support MSI). In this post, I will focus on system-assigned MSI’s in the VM realm. MSI’s for VMs seem like a great alternative to Service Principals, but after utilizing them on virtual machines, I am not so sure. I also explore recent findings with MSI’s on virtual machines and some of their security implications. I will be your guide as we dig a bit deeper into the concepts of MSI’s.

## Understanding MSI’s

As briefly described above, one of MSI’s benefits is that it removes the overhead of managing credentials that an application may rely on to authenticate to various Azure resources. There are two different kinds of MSI’s:

1. System-assigned
2. User-assigned

There are some critical differences between the two. A system-assigned MSI is directly tied to a particular resource’s life cycle and has a one-to-one relationship with it. A user-assigned MSI is a standalone resource and has a one-to-many relationship as it’s identity can be associated with multiple resources. For example, a VM with a system-assigned MSI enabled will have a corresponding identity created in AAD. Once this identity is created, you can assign it permissions (RBAC, POSIX, etc.) to interact with other resources. VM deletion will also clean up the corresponding identity in AAD automatically.

Now that we understand the system-assigned MSI concept, how do we utilize it to authenticate against an Azure resource? From a Linux VM standpoint, we will need to retrieve a JSON Web Token (JWT) from an internal endpoint exposed by Azure. Once we have the JWT, we will pass it through in our subsequent request when interacting with Azure resources. Here is an example of a CURL command I used to request the JWT:

- curl “http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/” -H Metadata:true

This command gets executed directly on the Linux VM. Notice the ‘resource’ parameter at the end of the URL? Depending on what the Azure target is (storage, management, etc.), this will need to be modified to the target’s correct resource audience. As an example, if we were targeting the storage audience, the CURL command would look something like this:

- curl “http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://storage.azure.com/” -H Metadata:true

Once you receive the token in the HTTP response, it can be passed through on your subsequent requests to authenticate the desired Azure resource. Only the Azure resource where the system-assigned MSI is enabled can request a token associated with the identity.

It was at this point when I discovered our potential security risk.

## Setting the Stage

To speak to what scenarios this potential problem would be evident in, allow me to describe a use case in which files move from an on-premise environment to Azure and vice versa. In this use-case, I utilize the following services and utilities in Azure:

A Linux Virtual Machine
Azure Data Lake Storage (ADLS) Gen2
AzCopy Utility
The VM acts as a gateway between the on-premise environment and the cloud. The storage product that is housing the files leaving and entering the cloud is ADLS Gen2.

I focused on files entering the cloud (files written from the VM to the ADLS Gen2 account). When files land on the VM, I required a way to get them passed over to ADLS Gen2. AzCopy is an excellent tool for this. It is orchestrated via the command line, offering the ability to automate copy operations in the future through a custom script. There are two methods that AzCopy can use to authenticate to Azure resources. The first is with SAS tokens and the second is with AAD. Since our system-assigned MSI exists in AAD I went with the second option. The MSI is assigned POSIX controls on the ADLS Gen2 account, which will have ‘write’ access due to the use-case requirement to write files to Gen2.

## Reviewing the Findings

As I tested out the above use-case, I decided to utilize Postman to make API calls against the ADLS Gen2 Rest API as the MSI. Requiring me to log onto the VM, request a JWT, and copy the token to my laptop. Having configured Postman with the JWT, my initial thought was, ‘I should not be able to use this token to authenticate against ADLS.’ The token, being on my laptop, is no longer in the VM boundary. I assumed Azure validates the origin of this token and would deny it should it come from outside. Right?

Wrong!

After taking the token off the VM and generating a PUT request against a folder in the data lake, I discovered that I could write a text file to the ADLS location. Effectively, I was able to impersonate the MSI from a different machine and another network. Additionally, anyone who can access this virtual machine can execute this CURL command to retrieve this token.

We raised this with Microsoft, and they had mentioned that this is expected behavior. I want to break down some security risks if this honestly is expected behavior.

## Assessing the Risk

From a security perspective, this breaks the fundamental principle of MSI’s.

### Misleading Documentation

In the MSI documentation, they talk about [security boundaries](https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/known-issues#what-is-the-security-boundary-of-managed-identities-for-azure-resources) of the MSI and even use a VM as an example. It states: “the security boundary for a Virtual Machine with managed identities for Azure resources enabled, is the Virtual Machine.” To me, this statement means you cannot make any API calls on the MSI’s behalf outside of the VM. When clarifying this with Microsoft, their answer makes the documentation seem misleading. Microsoft stated, “The documentation is around token acquisition and not token use.” When reading the documentation before speaking with Microsoft, I interpreted it as the acquisition and use of the JWT. I advised Microsoft to consider having the documentation updated to reflect that the security boundary covers only the acquisition of tokens.

### Different Attack Surface

A big selling point of MSI’s is Microsoft handles key management for you. Compared to Service Principals, where the key management is in the hands of the customer. Part of the attack surface for Service Principals is around key management, as the customer is now responsible for rotating, securing, and reacting if their key is exposed. This responsibility also comes with greater control over how you store and secure keys. For example, you could keep a key in an Azure Key Vault and define an array of access policies to restrict only specific identities to have access to read said key. But what about the attack surface for MSI’s based on the findings in this blog?

Since anyone who has access to the VM (or any process) can request a JWT associated with the MSI, it becomes increasingly difficult to control who can make requests on the MSI’s behalf. The system-assigned MSI has ‘write’ access to many folders in the ADLS Gen2 account in the use-case detailed earlier. It’s easy to visualize a scenario where you have users who need access to the VM but do not need to have ‘write’ access on the ADLS Gen2 account. Since users can request a token, take it off the VM and use it anywhere, this changes the attack surface compared to Service Principals. Users that are unauthorized to write data into the ADLS can now do so, either knowingly or unknowingly. An example user may be support personnel required to monitor file transfers on the VM but shouldn’t see file contents. On the VM itself, you could lock down files and directories using ACL’s, but the concern still exists where that user can request a token and use it outside the VM, where you have no control.

## Recommendation

Considering the above, you should ask yourself, “Where am I willing to take on the risk?”.

MSI’s dramatically reduce the management overhead that would otherwise come with a Service Principal, but the attack surfaces between the two have changed. Now, I could say the choice between MSI’s and Service Principals “depends.” But I prefer to break down a couple of use-cases and let you know where I would choose one over the other.

Generally speaking, I think MSI’s are a good choice. Managing keys can be a massive headache without proper automation and alerting in place. Using MSI’s will alleviate that pain. An excellent example of where I think using an MSI makes sense would be if you are reading keys from a key vault. Can’t users with access to that VM still request a JWT and read those keys? Yes, they can, and depending on what kind of keys you have stored in your vault, this may not be a good option. For example, if the keys just read data from an API endpoint, this is a much lower risk than if the API could make changes to a database. In this particular use-case, I think this is a risk worth taking compared to what could happen if you mismanaged a key (i.e., Service Principal). You can also further mitigate the risk by adding firewall rules to the key vault to ensure requests are restricted to come only from that VM.

On the flip side, let’s go back to our initial use-case where you have sensitive data stored (PII, PCI, etc.) in your ADLS Gen 2 account with strict data protection policies. In this case, data integrity is critical, and having “unauthorized” users with the ability to impersonate the MSI and potentially make changes to that data is likely unacceptable. In this case, I would say the overhead of managing keys yourself is a risk I would take on.

## Conclusion

Making the right choice between MSI’s and Service Principals is about understanding how the risk between your authorization options work. My hope is this post will further guide you in your decision as to which one you choose. Thanks for reading!