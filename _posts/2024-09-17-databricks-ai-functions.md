---
title: "Databricks AI Functions"
date: 2024-09-17T10:00:00-04:00
categories:
  - Data Engineering
tags:
  - Databricks
  - GenAI
  - SQL
---

{% raw %}<img src="/blog/assets/images/blog_images/databricks-ai-functions/blog_image.jpg" alt="">{% endraw %}

I recently had the opportunity to play around with [Databricks AI functions](https://learn.microsoft.com/en-us/azure/databricks/large-language-models/ai-functions) for a use case that involved categorizing data based on a free-text description field. I wanted to generalize my experience and share my thoughts in this blog to demonstrate the power and ease of leveraging these AI functions.

I hope you enjoy this blog.

## What Are Databricks AI Functions ❓

Databricks AI functions are built-in SQL functions that enable you to apply AI to your data. These functions use the Mixtral-8x7B Instruct model by default and support a variety of tasks. Some examples include:

- [ai_classify](https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/functions/ai_classify), which allows developers to classify input text according to a provided array of labels.

```sql
SELECT
    description,
    ai_classify(description, ARRAY('horror', 'thriller', 'scifi', 'comedy')) AS category
FROM
    movies
```

- [ai_gen](https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/functions/ai_gen), which enables you to input your own prompt or instructions to the LLM.

```sql
SELECT
    question,
    ai_gen(
      'Answer the following question: ' || question
    ) AS answer
FROM
    questions
```

- [ai_analyze_sentiment](https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/functions/ai_analyze_sentiment), which allows sentiment analysis based on the input provided in SQL.

```sql
SELECT ai_analyze_sentiment('I was not a fan of this pizza');
```

At the time of writing, this functionality is in [public preview](https://learn.microsoft.com/en-us/azure/databricks/release-notes/release-types#platform-releases).

From my experience, leveraging these functions is tightly integrated into the Databricks platform and SQL language. What I mean by this is that interacting with the Mixtral LLM through these AI functions requires no token storage or authentication tokens, unlike API calls to services like Azure OpenAI. In those cases, you'd need to generate and store an authentication token to make calls.

Databricks abstracts this complexity from the user, offering a seamless experience that is fully integrated with SQL, making it incredibly easy to use these AI functions.

The [price](https://www.databricks.com/product/pricing/foundation-model-serving) for using Databricks AI functions (with the default Mixtral model) is $0.50 USD per million input tokens and $1.00 USD per million output tokens. Keep in mind, these costs are in addition to any compute expenses associated with running your SQL queries.

In the Data & AI space, where we often work with large datasets, it's easy to overuse these functions given their tight integration with SQL. Be mindful of the number of tokens you're consuming when interacting with these functions.

## Databricks AI Functions in Practice ⛹️

I have generated some sample [CSV data](https://github.com/Schiiss/blog/tree/master/code/databricks-ai-functions/data.csv) using GPT to compliment a demonstration of Databricks AI Functions.

[![sample_csv](/blog/assets/images/blog_images/databricks-ai-functions/sample_csv.png)](/blog/assets/images/blog_images/databricks-ai-functions/sample_csv.png){:target="_blank"}

Let’s run a couple of functions against this sample data.

After loading the CSV data into my workspace catalog in the default schema, running a Spark SQL query reveals the sample data.

[![databricks_query_csv](/blog/assets/images/blog_images/databricks-ai-functions/databricks_query_csv.png)](/blog/assets/images/blog_images/databricks-ai-functions/databricks_query_csv.png){:target="_blank"}

Let’s start by applying the [ai_classify](https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/functions/ai_classify) function on the Text column to categorize the data based on the content. The following SQL query takes the 'Text' column as input, leverages the ai_classify function, and passes an array of categories to output a new column called 'Category'.

```sql
SELECT
    Text,
    ai_classify(Text, ARRAY('Business', 'Sports', 'Technology', 'Entertainment', 'Fashion', 'Education', 'Food', 'Economics')) AS Category
  FROM
    databricks_ai_functions.default.data
```

The output looks like this:

[![output_of_gen_function](/blog/assets/images/blog_images/databricks-ai-functions/output_of_classify_function.png)](/blog/assets/images/blog_images/databricks-ai-functions/output_of_classify_function.png){:target="_blank"}

As you can see, there is a new column called ‘Category’ with one of the eight categorizations provided in the SQL query.

Next, we can use the [ai_gen](https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/functions/ai_gen) function to generate a custom response. This function is useful when the other out-of-the-box functions (e.g., similarity, summarize) don't meet your needs. The following query takes the Text column as input and responds with a follow-up question.

```sql
SELECT
    Text,
    ai_gen(
      'Respond to the following text with a follow up question: ' || Text
    ) AS Question
  FROM
    databricks_ai_functions.default.data
```

[![output_of_gen_function](/blog/assets/images/blog_images/databricks-ai-functions/output_of_gen_function.png)](/blog/assets/images/blog_images/databricks-ai-functions/output_of_gen_function.png){:target="_blank"}

As shown, the results are cast to a new column. The ai_gen function offers flexibility by letting you customize your prompts, but this can also be its biggest drawback since managing prompts can be challenging. If possible, I recommend using functions that don’t require prompt management (e.g., ai_translate, ai_similarity, ai_extract, etc.).

## Wrapping Up 🏁

Databricks has created a seamless integration between SQL and generative AI APIs. Given SQL's widespread adoption, data professionals can easily incorporate AI capabilities into their daily workflows.

The pricing for input/output tokens is reasonable, but you should monitor usage closely, as it’s easy to run large amounts of data through these functions.

I have [open-sourced](https://github.com/Schiiss/blog/tree/master/code/databricks-ai-functions/ai_functions.sql) the SQL queries used in the screenshots above, along with sample data, if you’d like to try them yourself.

Thanks for reading!
