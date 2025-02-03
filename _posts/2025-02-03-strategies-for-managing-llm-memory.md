---
title: "Strategies for Managing LLM Memory 🤖🧠"
date: 2025-02-03T10:00:00-04:00
categories:
  - GenAI
tags:
  - LLMs
---

{% raw %}<img src="/blog/assets/images/blog_images/strategies-for-managing-llm-memory/blog_image.png" alt="">{% endraw %}

Building production chatbots requires more than just a wrapper on top of an LLMs API. Due to the popularity of ChatGPT, users have come to expect a robust chat experience that considers conversation history and the users intent. In this blog I wanted to step through a few strategies I have employed in the past for managing chat history, what worked well, and what didn’t.

LLMs, by default, do not have memory. Each API call is stateless, meaning the model does not retain any knowledge of past interactions. This poses a challenge when building chat applications, as users expect the AI to remember previous messages, maintain context, and provide coherent responses across turns.

To bridge this gap, developers must implement their own memory management strategies. These strategies vary in complexity from simple in-memory storage to persistent databases each with its own trade-offs in terms of scalability, performance, and cost.

There is no one size fits all strategy and the intent of this blog is to step you through various approaches and you can decide which will work best for your use case.

This will be a conceptual guide but if you would like me to build out one of these strategies in a dedicated blog, please let me know!

## Considerations

When designing a chatbot with memory, there are several factors to consider, including how much context to retain, where to store past conversations, and how to retrieve relevant history efficiently. Below are some key considerations when implementing LLM memory.

### Using LLMs with Larger Context Windows

LLMs process each interaction based on the provided context at runtime. Most models have a fixed context window, ranging from 128K tokens (about 96,000 words) to 1 million tokens (about 750,000 words). GPT-4o currently supports 128K tokens, while models like Gemini 1.5 Pro comes with 1 million tokens.

A larger context window allows more chat history to be included in a single request, improving coherence in conversations. However, using large context windows comes with trade-offs:

✅ Maintains full conversation history (as long as it fits in the window)

✅ No need for external storage or retrieval mechanisms

❌ Higher costs as longer inputs increase token usage

❌ Higher latency due to increased processing time

❌ Limited by the model’s maximum token length

To optimize memory usage, developers should carefully curate which messages are included in the prompt and summarize past exchanges or truncating older, less relevant messages can help balance cost and efficiency.

### Storing Chat History in a Database

For longer conversations or applications that require persistent memory, a database is often necessary. Document databases like MongoDB are well-suited for storing structured chat history.

✅ Enables long-term memory across sessions

✅ Supports multiple users and concurrent conversations

✅ Scalable as chat history grows

❌ Requires additional infrastructure and storage management

❌ Increased retrieval latency

A common approach is to fetch recent messages from the database before sending a request to the LLM, ensuring relevant context is maintained while avoiding excessive data retrieval.

### Using Vector Databases for Semantic Memory

For applications requiring deep memory retention and contextual understanding, vector databases like Pinecone allow storing past conversations as embeddings. This enables retrieving semantically relevant messages rather than just recent messages.

✅ Efficiently retrieves relevant past conversations using similarity search

✅ Scales better than traditional databases for large datasets

✅ Can filter and rank stored interactions based on metadata

❌ More complex to implement and tune for optimal retrieval

❌ Higher infrastructure costs compared to basic document storage

Vector databases are particularly useful for assistants that need to recall specific details from past interactions without storing the entire conversation history in the LLM’s prompt.

Let's jump into a few practical strategies for memory management with LLMs.

## Strategy 1: Leveraging Arrays

Let’s start with the simplest way to manage chat history, which might be a good fit for testing or single-user scenarios.

This first strategy involves using an in-memory data structure (an array) to manage the chat history. I would say this is a very naïve and simple approach but allows you to mock basic chat history functionality very quickly. It is naïve because this does not scale for multiple users and is difficult to persist the data accross sessions. Below is a diagram that shows off the approach at a high-level:

[![strategy_1_diagram](/blog/assets/images/blog_images/strategies-for-managing-llm-memory/strategy_1_diagram.png)](/blog/assets/images/blog_images/strategies-for-managing-llm-memory/strategy_1_diagram.png){:target="_blank"}

1. User will send input to our application. This input will be appended to an array.

2. The latest input will be passed to a carefully crafted prompt along with the chat history.

3. The prompt is sent to an LLM.

4. The LLM responds and the users message as well as the AI message is appended to the array.

I have leveraged this strategy to quickly mock LLM memory locally, but this does scale very well. Here are a few things to consider when leveraging this approach.

Advantages:

✅ Quick to implement

✅ Sufficient for prototyping or single-user applications

Considerations:

❌ Does not scale well for multiple users

❌ Chat history is lost when the application restarts

❌ Cannot persist conversations across sessions

## Strategy 2: Leveraging Document Databases

As your chatbot moves beyond simple prototypes and starts serving multiple users, storing chat history in a document database becomes a logical next step. This strategy allows you to persist chat data and support multiple users without losing track of conversations. Document databases, such as MongoDB, DynamoDB, or Couchbase, are particularly well-suited for this task due to their flexible, schema-less nature.

Here’s an overview of how this strategy works:

[![strategy_2_diagram](/blog/assets/images/blog_images/strategies-for-managing-llm-memory/strategy_2_diagram.png)](/blog/assets/images/blog_images/strategies-for-managing-llm-memory/strategy_2_diagram.png){:target="_blank"}

1. The user sends input to the chatbot application.

2. The application fetches the relevant chat history from the document database using a unique identifier (e.g., a user_id or session_id).

3. The retrieved chat history is combined with the latest user input to craft a prompt.

4. Once the LLM responds, both the user input and the AI response are appended to the chat history, and the updated conversation is stored back in the document database.

5. Send to LLM: The prompt is forwarded to the LLM for a response.

Here’s a simple example of how you might structure chat history in a document database like MongoDB:

```json
{
  "session_id": "12345",
  "user_id": "67890",
  "messages": [
    {
      "role": "user",
      "timestamp": "2025-01-01T12:00:00Z",
      "content": "Hello, can you help me with my order?"
    },
    {
      "role": "ai",
      "timestamp": "2025-01-01T12:00:05Z",
      "content": "Of course! Could you provide me with your order number?"
    }
  ],
  "last_updated": "2025-01-01T12:00:05Z"
}
```

This approach scales much better and is a strategy I have used in a few production scenarios. Here are some key takeaways,

Advantages:

✅ Supports multiple users and sessions.

✅ Data is persistent, enabling conversations to resume at any time.

✅ Flexible schema for storing complex or evolving message data.

Considerations:

❌ Increased latency compared to in-memory solutions.

❌ Requires additional infrastructure and may incur higher costs.

❌ Potential for complexity when scaling to distributed systems.

This strategy strikes a good balance between simplicity and scalability, making it ideal for most production chatbot applications. However, as the volume of chat history grows or you require more advanced features (e.g., searchability or analytics), you might need to explore additional strategies like vector databases.

## Strategy 3: Leveraging Vector Databases

Unlike strategy 2, which retrieves a fixed number of previous messages (e.g., the last 10 interactions), vector databases enable a more semantic approach to memory. Instead of relying on strict chronological order, this method retrieves the most relevant past messages based on their meaning.

This effectively looks the same as strategy 2, but this time we are swapping a document database for a vector database and instead of retrieving recent messages, we retrieve semantically similar ones.

[![strategy_3_diagram](/blog/assets/images/blog_images/strategies-for-managing-llm-memory/strategy_3_diagram.png)](/blog/assets/images/blog_images/strategies-for-managing-llm-memory/strategy_3_diagram.png){:target="_blank"}

1. The user sends a message to the application.

2. The app queries the vector database, searching for past interactions that are semantically similar to the current message. This ensures the model retrieves contextually relevant information instead of just the last few messages.

3. The retrieved context is formatted into a prompt and sent to the LLM alongside the user's latest message.

4. The LLM processes the prompt + user input and generates a response.

5. The app sends the response back to the user, completing the interaction. The latest conversation is embedded and stored in the vector database for future reference.

Here are some takeaways from this strategy,

Advantages:

✅ Scalability: Works well even with a large number of past interactions.

✅ More relevant responses: Instead of just retrieving the last few messages, the system retrieves information that is most contextually similar to the current query.

✅ Handles long-term memory: Even if a conversation spans multiple sessions, relevant details can still be recalled.

Considerations:

❌ Requires efficient retrieval mechanisms to avoid high latency.

❌ Embedding quality and vector search parameters impact the accuracy of retrieved results.

❌ May need metadata filtering to ensure the retrieval is scoped to the right topic, user, or session.

This approach significantly improves chatbot memory by making past interactions searchable based on meaning, rather than just time-based proximity.

## Conclusion

Choosing the right strategy for managing chat history depends on your specific use case and long-term goals. Each approach—whether it's using an in-memory array, a document database, or a vector database—offers unique advantages and trade-offs. Simple solutions work well for lightweight applications or prototypes, while more advanced architectures enable features like personalization, semantic search, and scalability.

As your user volume grows, evolving towards more sophisticated techniques such as vector databases—can enhance efficiency and retrieval without unnecessary complexity upfront. Balancing performance, cost, and maintainability is key to selecting the right approach.

I hope this blog has provided a clear overview of different strategies and how they can be applied. With a solid understanding of these options, you can make informed decisions to optimize your chatbot's performance and user experience.
