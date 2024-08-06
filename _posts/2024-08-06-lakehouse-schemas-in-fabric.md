---
title: "Lakehouse Schemas in Fabric"
date: 2024-08-06T6:00:00-04:00
categories:
  - Fabric
tags:
  - Data Engineering
  - Lakehouse
---

{% raw %}<img src="/blog/assets/images/blog_images/lakehouse-schemas-in-fabric/blog_image.png" alt="">{% endraw %}

In this post I wanted to spend some time reviewing the preview feature [lakehouse schemas](https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-schemas) in Microsoft Fabric. This is an important feature in Fabric since the only way to query across lakehouses prior to this was to select the relevant folders and tables and [shortcut](https://learn.microsoft.com/en-us/fabric/onelake/onelake-shortcuts#internal-onelake-shortcuts) between them. Lakehouse schemas enable you to logically group tables under schemas and through what is called a [‘schema shortcut’](https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-schemas#bring-multiple-tables-with-schema-shortcut), bring in data from other lakehouses and external storage like ADLS Gen2. The [POSIX permissions](https://www.byteworks.com/resources/blog/understanding-osx-permissions/#:~:text=POSIX%20Permissions,-Unix%2FLinux%20systems&text=Each%203%2Dbit%20section%20has,%2C%20and%20execute%20(X).) are very limiting when it comes to securing data in your lake but lakehouse schemas seem to be setting up lakehouses in Fabric to support more complex security requirements in the future.

> **_NOTE:_**  Please note, this feature is in preview as of writing this post.

## Life Prior to Lakehouse Schemas

To understand the value this feature provides, we first need to understand what life was like before schema shortcuts. From my experience leveraging Fabric Notebooks, there have been a few instances where I wanted to query delta tables across lakehouses. If you open a notebook in Fabric you have the option to [attach to a lakehouse]( https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-notebook-explore#open-a-lakehouse-from-a-new-notebook) and set one as a default. In the example below, I have a lakehouse called ‘lakehouse1’ and I have loaded it with the sample public holidays table. If I query that table in the lakehouse it works just fine since I have set it as my default lakehouse.

[![query_lakehouse1](/blog/assets/images/blog_images/lakehouse-schemas-in-fabric/query_lakehouse1.png)](/blog/assets/images/blog_images/lakehouse-schemas-in-fabric/query_lakehouse1.png){:target="_blank"}

I have also created another lakehouse in seperate workspace called ‘lakehouse2’ however, it is not set as my default lakehouse. If I attempt to query it in the same way, we get an error back.

[![error_querying_lakehouse2](/blog/assets/images/blog_images/lakehouse-schemas-in-fabric/error_querying_lakehouse2.png)](/blog/assets/images/blog_images/lakehouse-schemas-in-fabric/error_querying_lakehouse2.png){:target="_blank"}

As mentioned earlier, you can work around this by [shortcutting](https://learn.microsoft.com/en-us/fabric/onelake/onelake-shortcuts#internal-onelake-shortcuts) to the lakehouse where the tables that you want to query against exist.

Since lakehouse schemas did not exist prior to July 2024, shortcutting was done directly against folders or tables and we did not have the added benefit of leveraging schemas.

I have a been a big fan of Unity Catalog and how it exposes [schemas](https://learn.microsoft.com/en-us/azure/databricks/schemas/) in it's interface. I like how the tool enables you to logically group and categorize data as well as manage access to those schemas and with lakehouse schemas coming to Fabric I imagine this is the direction Microsoft is taking as well.

I have found the [POSIX type](https://www.byteworks.com/resources/blog/understanding-osx-permissions/#:~:text=POSIX%20Permissions,-Unix%2FLinux%20systems&text=Each%203%2Dbit%20section%20has,%2C%20and%20execute%20(X).) permissions (ie: RWX) to be very limiting and when Unity Catalog came out, it was a game changer for securing and accessing your data. My hope is Microsoft will eventually support a similar model.

## Schema Shortcuts

Now that we have lakehouse schemas, we can take advantage of logically organizing our data and combine it with the power of shortcuts. This is a neat feature to have in the fabric lakehouse experience and I imagine Microsoft will continue to add features that will be very similar to what [Databricks Unity Catalog]( https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/) provides. Only time will tell if it will be as good or as featured as what databricks offers 😉.

To enable lakehouse schemas you must explicitly enable the option upon creation.

[![enable_lakehouse_schemas](/blog/assets/images/blog_images/lakehouse-schemas-in-fabric/enable_lakehouse_schemas.png)](/blog/assets/images/blog_images/lakehouse-schemas-in-fabric/enable_lakehouse_schemas.png){:target="_blank"}

You cannot enable this on existing lakehouses currently, only on news ones.

There are a few [public preview]( https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-schemas#public-preview-limitations) limitations to be aware of and I would advise giving those a read before enabling this. A few noteworthy limitations right now:

- The SQL Analytics Endpoint is disabled until a 'fix' is deployed

- 'Migration of existing non-schema Lakehouses to schema-based Lakehouses isn't supported’

While it does not seem possible to opt in for [OneLake data access roles](https://learn.microsoft.com/en-us/fabric/onelake/security/get-started-data-access-roles) on a schema enabled lakehouse, I imagine you will be able to start securing your schemas via these roles in the future.

My hope is technology like OneLake data access roles will start to support more complex data access and security requirements such as [row filters and column masks](https://learn.microsoft.com/en-us/azure/databricks/tables/row-and-column-filters) in Unity Catalog and move past the existing POSIX type permissions.

[![onelake_data_access_roles](/blog/assets/images/blog_images/lakehouse-schemas-in-fabric/onelake_data_access_roles.png)](/blog/assets/images/blog_images/lakehouse-schemas-in-fabric/onelake_data_access_roles.png){:target="_blank"}

## Conclusion 🏁

Fabric is making good progress in terms of features on the lakehouse. Lakehouse schemas is a great addition to the platform however, if I contrast what Fabric currently has with what Databricks offers today with technology like Unity Catalog, it has a lot of catching up to do.

I am still unclear how use cases such as row and column level masking (for example) can be applied on data that exists in a lakehouse in Fabric. I imagine things like this are on the ‘road map’ and are coming soon to a Fabric near you.

Thanks for reading!
