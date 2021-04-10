---
title: "Integrating Github Actions With Jfrog Artifactory"
date: 2021-04-09T16:34:30-04:00
categories:
  - CI/CD
tags:
  - JFrog
  - Github Actions
---

{% raw %}<img src="/blog/assets/images/blog_images/2021-04-09-github-actions-and-jfrog/jfrog.jpg" alt="">{% endraw %}

The last few weeks I have had the priviledge to work with a technology stack I am not overly farmilar with. I had gotten very comfortable with the "Azure Devops" suite of tools the last year or so, and I wanted to share my experience moving out of that realm and changing it up a little. The technologies I am referring to in this case are JFrog and Github actions. In this blog I want to take you through the process to integrate Github actions with a private JFrog Docker repository. 

## Understanding The Technologies

Before diving into the technical implementation, I want to go through the two technologies and what purporse they serve in a broader sense

### Github Actions

As software is being released at a faster and faster rate, developers need a method of ensuring code quality before pushing to production. The less manual processes you have between your feature branch and pushing your changes to master, the more efficent this process becomes. This is where CI/CD pipelines come into play and make this whole process much simpler. I personally have spent most of my time using Azure Pipelines for my CI/CD builds, but I found my knowledge from that platform translated very nicely over to Github actions. For now, look at Github actions as a way to orchestrate development workflows. As an example, lets say you want to automatically run your unit/integration tests when a push is made to any branch. You can declare such workflow in Github actions and have that workflow execute in an automated fashion. I will dig into Github actions more when I get into the implementation.

### JFrog Artifactory
 
After a CI/CD pipeline runs, you will often have an output of that particular workflow. That output if reffered to as an "artifact". In the Java world, perhaps your artifact is a jar file, or in .NET it is a nuget package etc. These artifacts help you version your code and allow you to roll back to a previous build very easily. JFrog comes in with providing a place to store your artifacts, which can then be leveraged downstream. As an example, lets say you run your CI/CD pipeline and as a part of that you build a docker image. You could push that docker image to a docker repository in JFrog. 

## Implementation

Now that I have got the boring pieces out of the way, I want to get into the implementation details. For this example, I will be building a Java application into a docker image, and storing that image in a private Docker JFrog repository.

### Github Setup

Create secrets
Create YAML

### Jfrog Setup

Create Repo

### Results