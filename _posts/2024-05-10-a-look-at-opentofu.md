---
title: "A Look at OpenTofu 👁️ (with a GenAI Twist 🤖)"
date: 2024-05-10T10:00:00-04:00
categories:
  - IaC
tags:
  - Azure
  - GenAI
  - DevOps
  - OpenAI
  - OpenTofu
  - Terraform
---

{% raw %}<img src="/blog/assets/images/blog_images/a-look-at-opentofu/blog_image.jpg" alt="">{% endraw %}

In this blog I wanted to take a look at [OpenTofu](https://opentofu.org/), an open-source infrastructure as code tool, in response to some recent drama with HashiCorp and Terraform. For those who do not know, Terraform was open-sourced in 2014 and it has built up quite the community ever since. On August 10th, 2023, HashiCorp decided to change the licensing to a non-open source license, causing an uproar in the community.

This decision seems to have shaken the confidence in the Terraform community, and as a result, OpenTofu was created. OpenTofu has a [manifesto](https://opentofu.org/manifesto/) detailing their motives and goals that I recommend everyone read.

The long story short of all this is the Linux Foundation created a fork of Terraform and plan to maintain it going forward. On April 3rd, 2024, OpenTofu received a Cease and Desist letter from HashiCorp, claiming copyright infringement. OpenTofu [responded](https://opentofu.org/blog/our-response-to-hashicorps-cease-and-desist/) and the OpenTofu team 'vehemently disagrees with any suggestion that it misappropriated, mis-sourced, or otherwise misused HashiCorp’s BSL code'. On top of all this, IBM is purchasing HashiCorp for [$6.4B](https://www.crn.com/news/cloud/2024/ibm-confirms-6-4b-hashicorp-purchase-by-year-s-end). While this is all very interesting, the point of this article is not to cover the legality and the drama behind all of this.

What I wanted to cover was OpenTofu from a technical standpoint and pit it against Terraform to see how it works. I will also put a 'GenAI Twist' on this blog and generate the OpenTofu code using [GPT Vision](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/gpt-with-vision).

Let's dive in!

> **_NOTE:_**  In this blog, I will be deploying an Azure VM via OpenTofu. I will be creating a VM that leverages a username and password for authentication to demonstrate OpenTofu's state encryption feature. In an actual environment, it is not advisable to use username and password authentication for a VM. Instead, SSH keys are generally a more secure option. Additionally, credentials should not be checked into source control.

## OpenTofu Setup ⚙️

If you have set up Terraform before, you will be right at home with OpenTofu. For those who haven't set up tools like Terraform before, allow me to step you through how to set it up

The easiest way to get the OpenTofu binary is to navigate to the [OpenTofu releases page](https://github.com/opentofu/opentofu/releases) and download the latest stable version.

[![OpenTofu_Releases](/blog/assets/images/blog_images/a-look-at-opentofu/opentofu_releases.png)](/blog/assets/images/blog_images/a-look-at-opentofu/opentofu_releases.png){:target="_blank"}

Note the highlighted assets section above. You will need to download the binary for your distribution. In my case, I am running windows so I will download the tofu_1.7.1_windows_amd64.zip file. Once you have downloaded the zip file, you will notice a few items inside. The file that is important in this case is the tofu.exe file:

[![Tofu_Binary](/blog/assets/images/blog_images/a-look-at-opentofu/tofu_binary.png)](/blog/assets/images/blog_images/a-look-at-opentofu/tofu_binary.png){:target="_blank"}

Move that tofu.exe to a location you can remember and copy the file path to the exe and create a new PATH environment variable.

[![Tofu_Env_Var](/blog/assets/images/blog_images/a-look-at-opentofu/add_path_env_var.png)](/blog/assets/images/blog_images/a-look-at-opentofu/add_path_env_var.png){:target="_blank"}

Open up a PowerShell terminal and type tofu.

[![Type_Tofu](/blog/assets/images/blog_images/a-look-at-opentofu/type_tofu.png)](/blog/assets/images/blog_images/a-look-at-opentofu/type_tofu.png){:target="_blank"}

You will notice right away, it looks almost identical to Terraform.

## Leveraging GPT Vision to Generate the Code 🤖

Let's ask GPT Vision to generate OpenTofu code for the below architecture:

[![Azure_Architecture](/blog/assets/images/blog_images/a-look-at-opentofu/azure_architecture.png)](/blog/assets/images/blog_images/a-look-at-opentofu/azure_architecture.png){:target="_blank"}

Please keep in mind that we need to ask for Terraform code generation because GPT isn't familiar with OpenTofu yet, as it's a relatively new tool. However, this isn't a big issue currently, as the feature sets of the two tools haven't differed much. Below, you'll find a snippet of the code we used to prompt GPT to generate the code for us:

```python
response = client.chat.completions.create(
    model=deployment_name,
    messages=[
        { "role": "system", "content": "You are a helpful assistant that analyzes azure architectures" },
        { "role": "user", "content": [  
            { 
                "type": "text", 
                "text": "Describe this architecture and generate terraform code to deploy it:" 
            },
            { 
                "type": "image_url",
                "image_url": {
                    "url": data_url
                }
            }
        ] } 
    ],
    extra_body={
        "dataSources": [
            {
                "type": "AzureComputerVision",
                "parameters": {
                    "endpoint": os.environ.get("COMPUTER_VISION_ENDPOINT"),
                    "key": os.environ.get("COMPUTER_VISION_KEY")
                }
            }],
        "enhancements": {
            "ocr": {
                "enabled": True
            },
            "grounding": {
                "enabled": True
            }
        }
    },
    max_tokens=2000
)
print(response)
```

The code for this can be found [here](https://github.com/Schiiss/blog/tree/master/code/a-look-at-opentofu/gpt_vision.py) if you want to try using GPT vision to generate the code yourself. Having a look at the output and parsing out just the code, we get the following:

```terraform
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "example" {
  name     = "example-resources"
  location = "East US"
}

resource "azurerm_virtual_network" "example" {
  name                = "example-network"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
}

resource "azurerm_subnet" "example" {
  name                 = "example-subnet"
  resource_group_name  = azurerm_resource_group.example.name
  virtual_network_name = azurerm_virtual_network.example.name
  address_prefixes     = ["10.0.2.0/24"]
}

resource "azurerm_network_interface" "example" {
  name                = "example-nic"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.example.id
    private_ip_address_allocation = "Dynamic"
  }
}

resource "azurerm_linux_virtual_machine" "example" {
  name                            = "example-vm"
  resource_group_name             = azurerm_resource_group.example.name
  location                        = azurerm_resource_group.example.location
  size                            = "Standard_F2"
  admin_username                  = "adminuser"
  admin_password                  = "P@ssword1234"
  disable_password_authentication = false
  network_interface_ids = [
    azurerm_network_interface.example.id,
  ]

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }
}
```

Looks pretty good. Let's run this code in the next section.

## Running OpenTofu 🏃‍♂️

Let's bring that code into a [terraform file](https://github.com/Schiiss/blog/tree/master/code/a-look-at-opentofu/main.tf) so we can execute it. The steps to do this are exactly the same as Terraform. Open up a PowerShell terminal and run tofu init:

[![Tofu_Init](/blog/assets/images/blog_images/a-look-at-opentofu/tofu_init.png)](/blog/assets/images/blog_images/a-look-at-opentofu/tofu_init.png){:target="_blank"}

And then, tofu plan:

[![tofu_plan](/blog/assets/images/blog_images/a-look-at-opentofu/tofu_plan.png)](/blog/assets/images/blog_images/a-look-at-opentofu/tofu_plan.png){:target="_blank"}

Notice the plan file looks the same to what Terraform does. Let's run a tofu apply and deploy those resources to Azure.

[![azure_resources](/blog/assets/images/blog_images/a-look-at-opentofu/azure_resources.png)](/blog/assets/images/blog_images/a-look-at-opentofu/azure_resources.png){:target="_blank"}

Awesome! Our resources are deployed. With OpenTofu being a fork of Terraform, we can also run Terraform commands on the code for the time being. For example, terraform init, plan, and apply all work the same.

terraform init:

[![terraform_init](/blog/assets/images/blog_images/a-look-at-opentofu/terraform_init.png)](/blog/assets/images/blog_images/a-look-at-opentofu/terraform_init.png){:target="_blank"}

terraform plan:

[![terraform_plan](/blog/assets/images/blog_images/a-look-at-opentofu/terraform_plan.png)](/blog/assets/images/blog_images/a-look-at-opentofu/terraform_plan.png){:target="_blank"}

And a terraform apply creates the resources exactly the same. With this all being said, while Terraform and OpenTofu are very similar now, I expect them to diverge over time, and as we will see in the next section, already have to an extent. We are already seeing this with OpenTofu releasing features like [state encryption](https://opentofu.org/docs/language/state/encryption/) which encrypts the state files at rest.

To demonstrate state encryption, you will notice I have deployed a VM with a username and password. This password is sensitive and since OpenTofu leverages an external state file to manage the infrastructure, this password is stored in plain text my default:

[![tofu_state_file](/blog/assets/images/blog_images/a-look-at-opentofu/tofu_state_file.png)](/blog/assets/images/blog_images/a-look-at-opentofu/tofu_state_file.png){:target="_blank"}

Let's have a look at how we can encrypt that state file.

## State Encryption 🔒

Following the OpenTofu [example](https://opentofu.org/docs/language/state/encryption/#configuration) we can see we have to add a few lines of code to our main.tf file that will enable us to encrypt the state file at rest.

```terraform
terraform {
encryption {
    key_provider "pbkdf2" "my_passphrase" {
      passphrase = "RnndN6kcHf7fgQca"
    }
    method "aes_gcm" "my_method" {
      keys = key_provider.pbkdf2.my_passphrase
    }
    state {
      method = method.aes_gcm.my_method
      fallback {}
    }
  }
}
```

Rerunning our Tofu Apply, we can now see the state file is now encrypted and we can no longer see the VM password.

[![tofu_state_file_encrypted](/blog/assets/images/blog_images/a-look-at-opentofu/tofu_state_file_encrypted.png)](/blog/assets/images/blog_images/a-look-at-opentofu/tofu_state_file_encrypted.png){:target="_blank"}

OpenTofu also provides a mechanism to [decrypt the state file](https://opentofu.org/docs/language/state/encryption/#rolling-back-encryption).

To demonstrate how OpenTofu and Terraform have started to diverge, trying to run this same code in Terraform gives us an error:

[![terraform_state_encryption_error](/blog/assets/images/blog_images/a-look-at-opentofu/terraform_init_encryption.png)](/blog/assets/images/blog_images/a-look-at-opentofu/terraform_init_encryption.png)
{:target="_blank"}

This is to be expected since Terraform does not have the same functionality around encrypting state files at rest.

In a production environment, the encryption key needs to be stored somewhere securely and passed through to the code when executed. One method I have leveraged in the past is [GitHub Secrets](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions) and passing through the encryption key to your CI/CD pipeline.

## Conclusion

In conclusion, OpenTofu emerges as a promising technology for deploying infrastructure through code. With its innovative features like state encryption, OpenTofu is already differentiating itself in the market. While it shares similarities with Terraform, its unique capabilities and potential for future development make it an exciting prospect for DevOps teams and infrastructure engineers. As the landscape of infrastructure as code continues to evolve, OpenTofu's trajectory warrants close attention, offering the potential to streamline and enhance the process of managing infrastructure.