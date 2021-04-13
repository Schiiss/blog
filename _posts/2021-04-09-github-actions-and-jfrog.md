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

The last few weeks I have had the priviledge to work with a technology stack I am not overly farmilar with. I had gotten very comfortable with the "Azure Devops" suite of tools the last year or so, and I wanted to share my experience moving out of that realm and changing it up a little. The technologies I am referring to in this case are JFrog and Github actions. In this blog I want to take you through the process of integrating Github actions with a private JFrog Docker repository. 

## Understanding The Technologies

Before diving into the technical implementation, I want to go through the two technologies and what purporse they serve in a broader sense

### Github Actions

As software is being released at a faster and faster rate, developers need a method of ensuring code quality before pushing to production. The less manual processes you have between your feature branch and pushing your changes to master, the more efficent this process becomes. This is where CI/CD pipelines come into play and make this whole process much simpler. I personally have spent most of my time using Azure Pipelines for my CI/CD builds, but I found my knowledge from that platform translated very nicely over to Github actions. For now, look at Github actions as a way to orchestrate development workflows. As an example, lets say you want to automatically run your unit/integration tests when a push is made to any branch. You can declare such workflow in Github actions and have that workflow execute in an automated fashion. I will dig into Github actions more when I get into the implementation.

### JFrog Artifactory
 
After a CI/CD pipeline runs, you will often have an output of that particular workflow. That output if reffered to as an "artifact". In the Java world, perhaps your artifact is a jar file, or in .NET it is a nuget package etc. These artifacts help you version your code and allow you to roll back to a previous build very easily. JFrog comes in with providing a place to store your artifacts, which can then be leveraged downstream. As an example, lets say you run your CI/CD pipeline and as a part of that you build a docker image. You could push that docker image to a docker repository in JFrog. 

## Implementation

Now that I have got the boring pieces out of the way, I want to get into the implementation details. For this example, I will be building a Java application into a docker image, and storing that image in a private Docker JFrog repository.

### JFrog Setup

Login to Jfrog and generate an API key. This can be done by navigating to 'Edit Profile' > 'Authentication Settings' and generate a new API key. 

{% raw %}<img src="/blog/assets/images/blog_images/2021-04-09-github-actions-and-jfrog/jfrog_api_key.PNG" alt="">{% endraw %}

This API key will be used by GitHub actions to authenticate against JFrog.

### Github Setup

Inside GitHub you will need to create two secrets in the repo.

1. JFROG_USERNAME
2. JFROG_API_KEY

You can create secrets 'Settings' > 'Secrets' > 'New repository secret'

{% raw %}<img src="/blog/assets/images/blog_images/2021-04-09-github-actions-and-jfrog/github_secrets.PNG" alt="">{% endraw %}

The below YAML will build a java application before deploying a docker image to JFrog


```
name: Deploy_To_JFrog

on:
  push:
    branches:
    - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2
      - name: Set up JDK 11
        uses: actions/setup-java@v2
        with:
          java-version: '11'
          distribution: 'adopt'
      - name: Build with Maven
        run: mvn clean install
      - name: "Login to JFrog Registry"
        run: docker login <insert_your_endpoint_here>.jfrog.io -u ${{ secrets.JFROG_USERNAME }} -p ${{ secrets.JFROG_API_KEY }}
      - name: "Push Docker Image"
        run: |
          git_hash=$(git rev-parse --short "$GITHUB_SHA")
          docker build -t app . 
          docker tag app <insert_your_endpoint_here>.jfrog.io/app:$git_hash
          docker push <insert_your_endpoint_here>.jfrog.io/app:$git_hash
```



### Results