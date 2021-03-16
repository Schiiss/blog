---
title: "An Introduction To Kubernetes"
date: 2021-03-16T16:34:30-04:00
categories:
  - Containers
tags:
  - Kubernetes
---

{% raw %}<img src="/schiiss_blog/assets/images/blog_images/2021-03-16-an-introduction-to-kubernetes/containers.jpeg" alt="">{% endraw %}


Big Data, Artificial Intelligence, Kubernetes, BlockChain, 5G. These are just some of the buzzwords I have been seeing in articles discussing what "trendy" technologies to look out for this year. One of those buzzwords I find people are getting excited about (even before 2021) is Kubernetes. I was a bit unsure as to what problem Kubernetes sets out to solve so I wanted to do some research and share my findings with you. Join me on an introduction to Kubernetes!


## What Problem Does It Solve?


To understand what problem Kubernetes sets out to solve we need to look at two popular way’s software is developed. Software practices have evolved significantly in the last decade and as companies adopt a more DevOps-centric culture, tools like Kubernetes are only going to increase in popularity. The two popular software methodologies I am referring to are called monolithic and microservice architecture.


“Monolithic architecture” is when an app is built as a single unit, packaged up, and typically deployed onto one server. As an example, you could have a piece of software that has a client-side app, a server-side API, and a database and all of this would be packaged into a deployable format to run on a server. Developing software in such a way can lead to apps becoming too large and complex to efficiently make changes. This causes a domino effect where new features are released less often, and changes to the code base are much higher risk as the full effect of the change may not be fully understood. Further to this, the entirety of the app must be deployed on each release, and depending on the size, it could take a long time for the app to start which leads to extended downtime. 


On the flip side of this, we have what is called “microservice architecture” and it sets out to alleviate many of the drawbacks that come with developing your software in a monolithic fashion. If we were to take the same three components above (client app, server API, and database) and maintain/deploy each separately, we would have a much more maintainable application. The app becomes less complex as each component is now broken down into smaller more manageable pieces making them independent from each other. Each component can now have different release cycles, scaling requirements, and making changes to the code base is much simpler.


My first question when learning about microservices was “how can we deploy, scale and monitor all these different microservices?”. As your company scales, deploying to a VM to run your various components becomes a tedious and time-consuming process. This is where the concept of containerization and Kubernetes comes into play.
Kubernetes can take your microservices (running on containers) and alleviate a lot of the administrative headache that comes with them. Kubernetes provides features such as self-healing containers, efficient resource usage (CPU, RAM, etc.), simplified deployment, etc. Now that I have given a high-level overview as to what problem Kubernetes attempts to solve, let us have a look at the architecture supporting Kubernetes and learn a bit more about the underlying components.


## Architecture
Kubernetes can be very complex, but the technology does a good job of obfuscating a lot of the nitty-gritty into easy-to-understand components. I have done up a diagram illustrating some of the key components (‘master’ and ‘worker’ nodes) that make up the base of the Kubernetes cluster. 

{% raw %}<img src="/schiiss_blog/assets/images/blog_images/2021-03-16-an-introduction-to-kubernetes/architecture.PNG" alt="">{% endraw %}


### Master Node
The master node is the component that will make global decisions about the cluster and respond to certain events. Some key components make up the master node:  

- API Service:

The API service is the doorway to interact with the various Kubernetes objects. This is the only way into the Kubernetes cluster. You can interact with it via a dashboard, directly via the API, or a command-line tool like kubectl. You must be authenticated to interact with the API. As an example, if we wanted to view all the pods we have running, this initial request would first need to go through the API server before allowing us to view this information. 


- Controller:


The controller is used to maintain the state of the various Kubernetes objects. Objects in Kubernetes are declared via YAML files and the controller will use these to ensure they meet spec. The controller will act typically via the API service. So, if we define that 5 pods should be always running in our YAML configuration, the controller will work to ensure this is the case.


- Scheduler:


The scheduler will assign a newly created pod to a node based on a two-step operation:
1. Filtering
2. Scoring 


Pods can be defined with certain resource requirements (CPU, Memory, etc.) which the scheduler will take into consideration when selecting a node to run the pod on. This is the filtering stage, and if the scheduler cannot find a suitable node, it will remain unscheduled and will sit in a type of queue until it can be. The second operation is what is called ‘scoring’. If a node makes it past the filtering stage, it will be scored based on certain priorities. An example of this would be the ‘LeastRequestedPriority’ policy which favors nodes with fewer requested resources. There is an excellent article [here](https://kubernetes.io/docs/reference/scheduling/policies/) that details the various policies the scheduler will consider. 


- Etcd:


This is a datastore that contains the state of the Kubernetes cluster. An example of when etcd is used would be when using the command line tool ‘kubectl’. If we were to use ‘kubectl’ to gather the pods running on Kubernetes, that command would query the etcd database for that information. Further to this, a component like the Controller would not work properly without this data store. The controller will also query this database to ensure the desired state is upheld on the various Kubernetes objects. Etcd uses something called the ‘raft algorithm’ and I found this excellent [animation](http://thesecretlivesofdata.com/raft/) showing how this works. 


### Worker Node


Certain components run on each of the worker nodes apart of the Kubernetes cluster. These are the components that make up each worker node:


- Kube-proxy:


Networking in Kubernetes is not trivial to setup. Kube-proxy’s job to maintain the network inside a Kubernetes cluster. This service is what helps facilitate networking for pods, containers, nodes, and helps expose services externally. As an example, pod IP addresses constantly change, and it is the job of the kube-proxy to keep all these routes up to date to ensure efficient network communication.
- Kubelet:


This Kubelet will ensure that each node is registered with the API server and all pods running on that node are running and healthy. 


- Container runtime:


This is simply the software used for running the containers on a node. This could be “containerd” or “CRI-O”. 


- Pods: 


As defined in the documentation, Pods are the “smallest deployable units of computing that you can create and manage in Kubernetes.” Effectively, a pod is a grouping of one or more containers that share the same specified resources (CPU, Memory, etc.), network, and storage. 


## Ending things off

The idea of this blog was to give you an overview of what problems kubernetes attempts to solve. Containers are a very poplular way to deploy applications and Kubernetes provides an orchestration framework that makes scaling your containerized apps much simpler. 