---
title: "AI Safety in RAG 🛟🤖"
date: 2024-11-18T10:00:00-04:00
categories:
  - GenAI
tags:
  - RAG
  - Cyber Security
  - LLM
---

{% raw %}<img src="/blog/assets/images/blog_images/ai-safety-in-rag/blog_image.png" alt="">{% endraw %}

## Introduction

AI Safety is a topic often discussed in the context of large language models, or LLMs. In that context, it often refers to a field of study focused on ensuring that artificial intelligence systems are safe and beneficial to humanity.

What does AI Safety actually mean?

Essentially, it means ensuring AI systems are aligned with human goals and avoiding negative or unintended consequences from AI systems. This might result in unfair hiring practices such as those reported in Amazon’s AI-based recruiting software that was later [discontinued](https://www.technologyreview.com/2018/10/10/139858/amazon-ditched-ai-recruitment-software-because-it-was-biased-against-women/) due to its bias against women, AI based chatbots dispensing bad or dangerous advise, to worst-case scenarios such as that depicted by the famous [Skynet](https://en.wikipedia.org/wiki/Skynet_(Terminator)) scenario from the movie Terminator, where an autonomous system pursues goals misaligned with human interests.

In practice, AI Safety comes down to a design focus by AI practitioners to maximize the benefit of AI systems while minimizing any potential downsides and ensuring AI remains under responsible human control.

In 2024, Anthropic [published](https://www.anthropic.com/research) multiple research papers covering three of the top concepts in AI safety: explainability, alignment and societal impact. OpenAI published its [safety practices](https://openai.com/index/openai-safety-update/) and Google released its own [guidelines](https://ai.google/responsibility/responsible-ai-practices/) about responsible AI practices.

There is an active discussion in the LLM community about whether making LLMs open source (publishing their weights and/or their training sets) makes them safer. On the one hand, scientific transparency and reproducibility can allow independent researchers to audit and validate the safety of such models. Furthermore, it accelerates the detection and remediation of any safety issues. However, such openness presents some risks, allowing bad actors to exploit vulnerabilities and known safety risks, or create unsafe derivatives.

Thankfully, both commercial research labs and academic research labs are working hard to understand and improve AI safety in foundation models.

Retrieval-Augmented Generation (or RAG) is the most common approach for building enterprise grade AI Assistants and Agents, due to being grounded in trusted enterprise data or knowledge. It is therefore not a surprise that the discussion is now increasing in focus on how RAG can help amplify AI Safety for enterprise applications.

But what does AI Safety mean for RAG?

Let’s dive in.

## AI Safety Challenges with Generative Models

Although we are quite far from immediate concerns about a Skynet worst-case scenario, the power of large language models like OpenAI’s GPT-4o, Anthropic Claude, Google’s Gemini, Meta’s Llama-3, and others triggered industry-wide work to think about AI Safety in the context of generative AI.

What are some of the challenges for developing Safe generative models?

### LLM Hallucinations

LLM hallucinations (also known as confabulations) present significant challenges in AI safety as they undermine the reliability and trustworthiness of AI systems, particularly in critical applications like healthcare, law, and education.

When users depend on AI for accurate and actionable insights, hallucinations can lead to misinformation, poor decision-making, or even harm.

The challenge is compounded by the difficulty of detecting and mitigating hallucinations, as they often appear plausible and are seamlessly woven into otherwise coherent outputs.

### Lack of Explainability

A critical limitation of current LLMs is their lack of transparency and explainability. This "black box" nature manifests in several ways:

1. Output Generation: Users receive responses without insight into the reasoning process or decision-making criteria that produced them.

2. Fact vs. Fiction: Without clear explanation of sources or reasoning chains, distinguishing between accurate and inaccurate information becomes extremely difficult.

3. Trust and Accountability: The inability to audit or understand model decisions hampers trust and makes it challenging to implement meaningful accountability measures.  

The lack of explainability is even more critical in applications within certain domains, where regulations and policies explicitly require explainability and auditability.

In spite of ongoing research to introduce explainability for LLMs (such as [Anthropic’s work](https://transformer-circuits.pub/2024/scaling-monosemanticity/index.html) in this area), there is still no good solution. As we’ll see later, this is one of the areas for which RAG provides a natural solution, increasing trust and explainability.

### Output Control and Alignment

A fundamental challenge in AI safety is ensuring output control and alignment. Modern LLMs must generate content that aligns with human values and ethical principles while avoiding harmful or discriminatory content, deliberate misinformation, hate speech or inappropriate material.

Output control goes beyond content filtering. We must prevent LLMs from being weaponized for things like misinformation campaigns, terrorist activities or radicalization.

An additional threat is that of criminal activity such as financial fraud or scam, social engineering and cyber-attacks (malicious code generation).

### Prompt Injection

As LLMs become more sophisticated, they face increasingly complex safety challenges, particularly through [prompt injection attacks](https://arxiv.org/html/2403.04957v1), which attempt to elicit an unintended response from an LLM.

These types of attacks may be used to override built-in safety measures to extract unauthorized information (as [demonstrated](https://www.wired.com/story/microsoft-copilot-phishing-data-extraction/) for example in BlackHat 2024), or to manipulate the model’s behavior in order to bypass ethical guidelines.

While model designers continuously strengthen defenses through advanced training methodologies and robust guardrails, this creates an ongoing arms race between security researchers and potential attackers, not unlike traditional cybersecurity challenges.

## What is Retrieval-Augmented Generation?

LLMs, while powerful, can sometimes provide outdated, inaccurate or incomplete information since their knowledge (generally speaking) is static and cut off at the point at which they were last trained. RAG helps by fetching up-to-date facts from external sources, ensuring the content generated is relevant and accurate.

It’s like giving the LLM an assistant to quickly pull in the latest information needed from a large dataset to help the LLM answer the question. RAG helps extend LLMs to specific domains or an internal corpus of information. There are quite a few technical considerations when implementing a RAG architecture.

Below is a diagram demonstrating the RAG architecture and its complexities.

[![rag_architecture](/blog/assets/images/blog_images/ai-safety-in-rag/rag_architecture.png)](/blog/assets/images/blog_images/ai-safety-in-rag/rag_architecture.png){:target="_blank"}

There are a few key concepts and steps required to understand RAG

1. The first step is to curate an external dataset outside of the LLM’s original training data. This data could be from multiple sources in various formats. We will take this data and leverage an sentence embedding model to convert that data into a vector of floats (aka “vector representation”) and add that information into a special database called a vector store.

2. Once the vector store is updated, we can start retrieving information from it based on a user query. Here again we leverage an embeddings model to convert the user’s query into a vector representation so a similarity search can be performed. This search is done against the vector store, and is the “R” in RAG. The results are returned from the vector store and optionally passed through a reranker to help improve accuracy of the retrieved information.

3. This information is passed to a prompt to enable the LLM to generate an accurate response based on the user’s query. This is the “G” step in RAG. Before returning the LLM’s response to the user, it can be run through a ‘hallucination’ detection model (such as HHEM) to determine if the response is grounded in the facts provided or is hallucinated.

4. Finally, the response is returned to a hopefully happy user.

[![rag_meme](/blog/assets/images/blog_images/ai-safety-in-rag/rag_meme.png)](/blog/assets/images/blog_images/ai-safety-in-rag/rag_meme.png){:target="_blank"}

There are a lot of considerations to make all this work. To name just a few:

- Chunking: are the documents you are loading into your vector store optimized for RAG? LLM’s have limited input limits and large/complex documents need to be broken down into smaller chunks

- State of the art retrieval: the retrieval step in RAG is of utmost importance to achieve the highest quality results. It’s like the old saying “garbage-in-garbage-out": if you can’t provide the LLM with the most relevant facts or data to answer the query, it will ground on the wrong facts and provide low quality responses. Improving retrieval with techniques like Hybrid Search and reranking helps to significantly improve the accuracy of RAG.

- LLM choice: what LLM will you select to output your response? Some LLM’s perform better for certain use cases. In addition, different LLMs have different AI Safety characteristics, and some LLMs may hallucinate more than others, as is shown in the [HHEM leaderboard](https://huggingface.co/spaces/vectara/leaderboard).

## How RAG Enhances AI Safety

RAG provides several key benefits to AI Safety by reducing hallucinations, enhancing transparency, and offering greater control over information sources. 
Let's explore these aspects in more detail.

### Reducing Hallucination and Misinformation

One of the most significant challenges with LLMs is "hallucinations" — the phenomenon where models produce incorrect or fabricated information. Since traditional LLMs rely solely on their internal training data, they can often "make up" information when they lack the facts.

How RAG Helps:

By incorporating a retrieval step, RAG enables the model to pull real, contextual information from vetted data sources or a reliable API. This access to contextually relevant information can prevent the model from speculating, and instead ground responses in verified data, substantially reducing the risk of hallucination. For instance, in a medical application, a RAG system could access a trusted database of health guidelines, ensuring that users receive accurate, up-to-date advice rather than potentially harmful misinformation.

### Enhancing Transparency and Explainability

A key aspect of safe AI systems is the users’ ability to understand and trust the origin of a model’s responses. Standard LLMs can be opaque, as it is often unclear where information comes from or why certain responses are generated.

How RAG Helps:

Because RAG models rely on information retrieved from the source documents, they can provide citations or evidence with their responses, making it possible to trace back the information to its source. This transparency improves user trust and accountability, as users can verify the response’s origin. In fields where accuracy is critical, such as law or finance, this traceability is essential to ensure AI systems remain accountable and compliant with regulatory standards.

### Reducing Bias by Controlling Information Sources

Bias in AI models remains a persistent challenge, often introduced unintentionally through training data. LLMs are susceptible to inheriting biases present in the data they are trained on, which can lead to skewed or insensitive responses.

How RAG Helps:

RAG enables developers to control the sources from which information is retrieved. By carefully curating and diversifying this knowledge base, RAG allows for a higher degree of control over bias in responses. Additionally, updates to the knowledge base can be made without needing to retrain the entire language model, allowing developers to keep the system aligned with evolving ethical standards and societal values.

### Providing Real-Time Updates and Safe Adaptability

Language models traditionally struggle to keep up with rapidly changing knowledge, since training and fine-tuning them is both time-consuming and computationally expensive. This can create safety risks when information goes out of date, especially in fields requiring immediate accuracy, like news, health, and public safety.

How RAG Helps:

With RAG, the retrieval component can pull in real-time information from trusted sources, ensuring that responses are based on the latest data. This capability allows RAG-powered systems to adapt safely to new knowledge and minimizes the risk of outdated responses that could lead to user harm. For example, in the context of natural disaster alerts, a RAG model could provide users with the most recent updates sourced directly from official feeds, helping to keep people informed and safe.

Furthermore, this ability to quickly update the data used for answering questions enables important regulatory compliance, such as with GDPR’s right-to-be-forgotten, which are otherwise difficult to achieve.

### Supporting Robustness in Adversarial Situations

As AI systems become more widely adopted, they face increasing risks of adversarial attacks. Attackers can exploit vulnerabilities in LLMs to produce unsafe or misleading responses, which could have serious consequences.

How RAG Helps:

RAG adds a layer of robustness by incorporating an external retrieval mechanism that can verify or contradict potential manipulative prompts. For instance, when faced with an adversarial prompt, a RAG system could check the prompt against reliable sources, reducing the likelihood of generating a harmful response. Additionally, RAG’s structured approach to incorporating external information makes it easier to monitor for security risks and establish filters against suspicious inputs.

## RAG Safety Best Practices

We’ve seen how RAG helps address some of the key risks in using LLMs and reduce the risk. Now let’s talk about some additional measures that you might consider when implementing your RAG solution, to further enhance AI safety.

### Role-based access control

Your RAG system often includes information that has role-based access permissions. For example, some documents might be accessible to anyone in your company, whereas a subset of the documents are accessible only to the CEO.

You can implement RBAC as part of your RAG to restrict access to sensitive data based on user roles, ensuring that responses generated by your RAG assistant adhere to roles and permissions of your organization, and are only grounded in data the user has access to.

### Data Anonymization

Before ingesting data into your RAG pipeline, you should consider anonymizing sensitive information within documents and databases to protect individual privacy and comply with data protection regulations such as GDPR.

This often includes personally identifiable information (PII) such as name, address, phone number, email or social security number. But it may also include other types of sensitive information like credit card numbers or personal health information (PHI).

For RAG to work properly it is important to properly anonymize sensitive data in a way that allows the LLM to connect information across entities such as people or locations. For example, imagine a simple anonymization scheme replacing people’s names with “*****”; while this certainly removes the identifiable information from the text, it results in the LLM missing the distinction between different people.

One common approach is tokenization, where any piece of sensitive information is replaced by a unique random token, allowing the LLM to identify the same token as the same entity, while allowing the application builder to control if and how de-identification is performed after the response has been generated by the LLM.

### Prompt Engineering and Guardrails

In many RAG systems you can modify the default prompt to your needs. Make sure to develop RAG prompts that enforce security measures against common threats like prompt injection, prompt leaking, and jailbreaking.

In some cases, you might implement a mechanism to tag and filter inappropriate user input as an additional safeguard against malicious prompts.

These prompts should work consistently across different LLMs in case your system uses multiple LLMs.

### Mitigating AI Hallucinations

RAG by itself already largely already mitigates hallucinations, but even that is not 100% foolproof. Using a post-response model like [HHEM](https://huggingface.co/vectara/hallucination_evaluation_model) in your user-interface to identify RAG hallucinations and inform the user improves the user experience. You might also consider just removing responses if their hallucination detection score is below a certain threshold as “too hallucinated”.

Furthermore, ensuring your user interface includes citations that are easy to understand and use increases user trust in the RAG response and allows them to dig deeper into the facts from which the response was derived.

### Human Feedback

Incorporating human feedback (such as thumbs up or down) can help you collect data about which responses are good and which are bad, as perceived by the end user. Acting on this data is essential in understanding the overall quality of responses from your RAG system and in making continuous improvements.

## Conclusions

In summary, Retrieval Augmented Generation (RAG) represents a significant advancement in building safer and more reliable AI systems. By integrating retrieval mechanisms with generative models, RAG helps address many of the safety and reliability challenges that traditional LLMs face. This is especially useful to reduce hallucinations and enhance transparency within AI systems, ensuring they are better aligned with human values and result in safer real-world applications.

Looking ahead, implementing best practices such as role-based access control, data anonymization, robust prompt engineering, and continuous human feedback will further improve RAG’s effectiveness in safety critical settings. While RAG cannot eliminate risks, it offers a strong foundation to maximize the benefits of generative AI, making it a practical choice for applications where accuracy, trust and security are paramount.

In an era where AI is increasingly embedded in decision-making and public-facing roles, embracing RAG's safety enhancements can support a future where AI tools remain not only useful but aligned with the highest ethical and safety standards.
