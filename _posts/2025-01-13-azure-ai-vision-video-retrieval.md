---
title: "Azure AI Vision Video Retrieval 🤖📽️"
date: 2025-01-13T10:00:00-04:00
categories:
  - GenAI
tags:
  - RAG
  - Azure
  - AI Vision
---

{% raw %}<img src="/blog/assets/images/blog_images/azure-ai-vision-video-retrieval/blog_image.png" alt="">{% endraw %}

I recently had an interesting use case for [Azure AI Vision](https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/) where the end users wanted to leverage the power of semantic search to help guide them what timestamp/segment in a teams recording to watch based on a natural language query.

In this blog I wanted to capture and genericize the use case and integration with Azure AI Vision.

Join me as we dig into the Azure AI Vision API and how we can leverage it to enable retrieval over videos.

## Use Case Overview

To maintain tribal knowledge, folks often record key business processes in Microsoft Teams and store them on SharePoint. However, efficiently indexing and searching these recordings remains a challenge, especially as team members transition roles. There is lots of tribal knowledge that exists within teams, and it is always a challenge to maintain this knowledge as folks move on to new roles. I think capturing recordings is a great way to archive this knowledge so long as you are doing them regularly and provide a mechanism to efficiently index/search them.

This is where Azure AI Vision comes into play. Azure AI Vision provides a mechanism to perform [retrieval over videos](https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/reference-video-search) and I think is a good technology candidate to help make the videos searchable and more accessible.

Similar to how we can use [Azure Search](https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview) to store embeddings (ie: vectors) for our documents to support RAG type flows, we can leverage Azure AI Vision to create a sort of vector database for videos to provide indexing for both speech and vision.

Let’s check out how this works.

## Multimodal Embeddings

Like other types embeddings, multimodal embeddings are stored in a [vector database](https://schiiss.github.io/blog/data%20engineering/databricks-vector-search/#what-is-a-vector-database-%EF%B8%8F). In this context, multimodal means an LLM being able to process information from different modalities, including videos, images, audio, and text. Video involves images, audio, and text and is a neat multimodal format to throw at an LLM to see how it can handle it.

In my last blog on [Databricks Vector Search](https://schiiss.github.io/blog/data%20engineering/databricks-vector-search/), we only embedded information from one modality, which was text. The concept however, remains the same for videos.

Let's take a look at what Azure resources are required to make this possible.

## Azure Components

To get this all working in Azure requires a few resources:

1. Blob Storage Account

2. Azure AI Vision Account (must be in one of the following regions: Australia East, Switzerland North, Sweden Central, or East US)

The end-to-end solution will look something like this once we have everything deployed and the API wrapper is built.

[![end-to-end-solution](/blog/assets/images/blog_images/azure-ai-vision-video-retrieval/end-to-end-solution.png)](/blog/assets/images/blog_images/azure-ai-vision-video-retrieval/end-to-end-solution.png){:target="_blank"}

1. Upload the video(s) to blob storage. This is required by the [CreateIngestion](https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/reference-video-search#createingestion) endpoint to bring the videos into a state where they can be searchable. You will notice in the [IngestionDocumentRequestModel](https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/reference-video-search#ingestiondocumentrequestmodel) there is a property called documentUrl that 'Gets or sets the document URL. Shared access signature (SAS), if any, will be removed from the URL.' This is why the videos must be stored in blob for processing.

2. Create an ingestion in Azure AI Vision to bring the videos into an index. An index in AI Vision seems very similar to an [index in Azure Search](https://learn.microsoft.com/en-us/azure/search/search-what-is-an-index) in the sense that you can create an index with a [schema](https://learn.microsoft.com/en-us/azure/search/search-what-is-an-index#schema-of-a-search-index) and define metadata that is searchable, filterable, sortable, etc.

3. The user can now query the index using natural language on top of their videos.

Let's see how we can leverage the [Video Retrieval API](https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/reference-video-search) to orchestrate all of this.

## Understanding the Video Retrieval API

Microsoft has published some [documentation](https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/how-to/video-retrieval) on how to setup the index on the Azure AI Vision service. It effectively boils down into 3 steps:

1. Create an Index

2. Add video to the index

3. Wait for ingestion to complete

Once those 3 steps are completed, we can then use natural language to search over our video.

## Testing the Retrieval

I have built a [sample notebook](https://github.com/Schiiss/blog/tree/master/code/azure-ai-vision-video-retrieval/main.ipynb) to take a video and run it through the above-mentioned steps as well as some convenience functions to help display the results returned from the index.

Here are some examples of queries I sent to the Azure AI Vision index.

In the first example, I send the query "horses running":

[![query_1](/blog/assets/images/blog_images/azure-ai-vision-video-retrieval/query_1.png)](/blog/assets/images/blog_images/azure-ai-vision-video-retrieval/query_1.png){:target="_blank"}

In the second example, I send the query "birds flying":

[![query_2](/blog/assets/images/blog_images/azure-ai-vision-video-retrieval/query_2.png)](/blog/assets/images/blog_images/azure-ai-vision-video-retrieval/query_2.png){:target="_blank"}

I wanted to pass through a more obscure query as well to see how it performs. At the 0:00:21 second mark is a very sleepy koala, hence the big yawn the little fella makes. Passing through the query "very sleepy" reveals that the search feature was able to find that sleepy koala 😀

[![query_3](/blog/assets/images/blog_images/azure-ai-vision-video-retrieval/query_3.png)](/blog/assets/images/blog_images/azure-ai-vision-video-retrieval/query_3.png){:target="_blank"}

## Closing Thoughts

Azure AI Vision was neat once I got it working, however, there were a few annoying hurdles I need to workaround to get this all working. I had a few cases were my video ingestion into the index kept failing with the following message:

Response Body: {'value': [{'name': 'my-ingestion', 'state': 'Failed', 'batchName': 'a19f78a8-6c4d-4e4b-b530-33059dc38800', 'createdDateTime': '2025-01-06T20:19:02.5983467Z', 'lastModifiedDateTime': '2025-01-06T20:19:28.2081137Z'}]}

Besides the state being marked as 'failed' I could not find anyway to enable more verbose logging via the [GetIngestion](https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/reference-video-search#getingestion) API endpoint, making it very difficult to troubleshoot what the problem was.

I also realized midway through writing this blog post that there is a new service to do retrieval over videos (as well as other document types) called [Content Understanding](https://learn.microsoft.com/en-us/azure/ai-services/content-understanding/). Azure AI Content Understanding is available in preview and I have a blog queued up to talk about it in a bit more detail.

If you have similar use cases or want to experiment with video retrieval, I’d love to hear your thoughts and feedback. Feel free to try out the notebook and share your results!

Thanks for reading!
