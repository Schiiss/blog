---
title: "🎨🧑‍🎨 The Art of Keeping Things Simple: Automated Testing"
date: 2025-08-09T10:00:00-04:00
categories:
  - Data
  - Data Weaver
tags:
  - Data Engineering
  - Platform Engineering
---

{% raw %}<img src="/blog/assets/images/blog_images/the-art-of-keeping-things-simple-automated-testing/blog_image.PNG" alt="">{% endraw %}

We have a goal internally to keep PRs under 30 minutes, including the time waiting for a code review and while we appreciate this goal is ambitious and we want to talk about how we are leveraging automated testing to help us reach this goal.

In our recent blog, [The Art of Keeping Things Simple](https://www.linkedin.com/posts/conner-schiissler_dataengineering-platformengineering-databricks-activity-7312458737800069120-1YMf?utm_source=share&utm_medium=member_desktop&rcm=ACoAACXEibYBngZiCRvQiwlsg8p1A85--baPNfw), [Mark van der Linden](https://www.linkedin.com/in/mark-van-der-linden-30798811/) and I argued for the value of taking a **Python-based approach** and abiding by platform and software engineering practices.

This is a follow up post to demonstrate the value and how it makes your platform more *testable*.

Also, we have decided to brand our framework as **Data Weaver**. We hope to make the **Art of Keeping Things Simple** into a series to discuss the challenges and triumphs we have experienced along the way.

## 🚀 Introduction

Automated testing is **essential** for delivering reliable data and AI solutions, especially as your solution and platform evolve over time! Nothing is worse than getting pinged out during your evening after a recent release to production due to bugs being introduced into the code base.

As our development team has grown and the number of features being worked on at a given time has increased, automated testing has allowed us to continue moving fast while ensuring the dreaded 'ping' after hours on Teams is heavily mitigated.

Testing in the data and AI space is hard on it's own but testing is especially challenging in environments built on **low code/no code tools**. While these platforms promise rapid development and ease of use, they often introduce hidden complexity that makes testing, debugging, and maintaining workflows much harder. We have found it especially difficult to test low code tools like Azure Data Factory that basically generate a JSON artifact in the background.

While low code/no code tools have enabled citizen developers access to data engineering and automation, they introduce unique challenges for testing and quality assurance. Take Azure Data Factory (ADF) as a prime example. On the surface, ADF’s drag-and-drop interface makes it easy to build data pipelines quickly, but this visual abstraction hides a lot of the underlying logic. We’ve run into situations where a simple change to a pipeline like adding a new activity or tweaking a parameter had unexpected side effects buried several layers deep. Because the logic is obscured behind the UI, tracing data flow or debugging issues can become a time consuming process. We have spent a lot of time in the past tracing through parent and child pipelines to try to identify the issue.

Assuming you are leveraging the reference architecture from Microsoft called [metadata-driven pipelines](https://learn.microsoft.com/en-us/azure/data-factory/copy-data-tool-metadata-driven), nearly all of your ADF objects (ie: pipelines, triggers etc.) are stored inside a relational database which makes automated testing all the more difficult.

**How do we test this at scale?**

While low code/no code tools like ADF accelerate initial development and lower the barrier to entry, we have found them to make testing, debugging, and collaboration significantly harder. We’re not saying to avoid these kinds of tools, but there are definitely trade-offs, and it’s important to go in with your eyes open to the challenges.

We hope this post demonstrates how following a code first approach can make your platform more testable.

> ❗ **Important Note**: We’re learning as we go, and Data Weaver is very much a work in progress! This series is our way of documenting the journey and sharing what’s worked, what hasn’t, and the lessons along the way. We’re committed to continuous learning and improvement, and hope that by sharing our experiences, we encourage others to experiment, take risks, and grow alongside us.

**In this post, we'll explore:**

- Why automated testing is critical for building reliable data and AI solutions.
- The unique challenges of testing complex data pipelines and AI workflows.
- Practical strategies and patterns for making testing simpler and more effective in real-world projects.

---

## ⁉️ Why is Automated Testing Important?

Automated testing is the backbone of reliable software and data engineering. It ensures that changes to code, data pipelines, and AI workflows do not introduce unexpected errors or regressions. In fast moving environments, manual testing quickly becomes impractical and error-prone.

**Key reasons why automated testing is essential:**

- **Consistency and Reliability:** Automated tests run the same way every time, catching issues early and preventing bugs from reaching production.
- **Faster Development Cycles:** Developers can make changes with confidence, knowing that tests will validate their work automatically.
- **Reduced Maintenance Overhead:** Automated tests help identify breaking changes quickly, making it easier to maintain and refactor codebases.
- **Documentation of Expected Behavior:** Well-written tests serve as living documentation, clarifying how code and data flows are supposed to work.
- **Enabling CI/CD:** Automated testing is a prerequisite for continuous integration and deployment, allowing teams to deliver features and fixes rapidly.

Each time a developer opens a PR, our automated testing suite runs. We have found the team to be much more confident in shipping their code to production knowing our automated testing has passed all the checks.

---

## 🧑‍💻 Testing in Data & AI: Best Practices and Real-World Challenges

“Best Practices” are helpful, but sometimes they can be a bit distracting. It is so easy getting tangled up in doing things “the right way” that we forget the point is to ship code that works and is easy to fix when it breaks. There’s no one size fits all recipe. What works for a tiny ETL script might be total overkill for a big, messy AI pipeline.

In our **Data Weaver** journey, we’ve had tests that looked beautiful on paper but fell apart the first time a data source changed or a schema evolved. We’ve also had “ugly” tests that caught real bugs and saved us hours of debugging. Don’t worship best practices. Use them as a guide, but trust your gut and your team’s experience.

So here’s what’s actually helped us:

- **Keep tests fast and independent.** If a test takes more than a few seconds, we ask if it’s really a unit test or if it belongs somewhere else.
- **Mock external stuff.** Databases, APIs, file systems. If it’s not your code, mock it.
- **Use tiny, fake data.** Real data is messy and slow. Mock data keeps tests quick and predictable.
- **Focus on what matters.** We try to test behavior and outputs, not every line of code. If a test breaks every time we refactor, it’s probably not helping.
- **Make tests readable.** If someone can’t tell what a test is doing very quickly, it’s too complicated.
- **Automate in CI/CD.** We run a subset of tests on every commit and another subset on PR's, but also make sure devs can run them 'locally' without a DevOps skillset.
- **Expect the unexpected.** We write tests for weird data, missing fields, and edge cases. Those are what actually break things in production.

And honestly, sometimes we just write a quick test, see if it fails, and move on. Not every test needs to be a masterpiece. The goal is to catch real problems before users do, not to win a testing style contest.

> 💡 **Tip:** High code coverage is nice, but meaningful tests that catch real issues are what matter most.

---

## 🧪 Testing in Data Weaver

We have broken down our **Data Weaver** framework into two high-level components for the sake of testing:
  
1. Framework code
2. Product code

Since we have been following an object-oriented approach, we have tried to abstract certain components where it makes sense. In an [example](https://schiiss.github.io/blog/data/the-art-of-keeping-things-simple/#ingest-from-sql) from the previous blog, we showed how we abstracted the ability to read from a SQL server and write the tables coming out of there into parquet (bronze) and then to silver as SCD Type1.

The classes and methods for those items exist in our 'framework code' since many products in our data platform need to leverage these operations. We are in the process of packaging our shared framework as a wheel file so we can version it (i.e., v1.0.2), and developers on the product side can just install the wheel file on their compute of choice to leverage the shared components.

> **Note**: Working to get our framework code into a wheel file has been a challenge. It has required an entire restructuring of folder structures and converting Jupyter notebooks to .py files. We wish we had the foresight to think of this earlier. If anyone is going down this path and wants to chat about packaging their software, please reach out!

So, in our case, there are two high-level components to test: our framework code and our product code. Let's step through an example to understand how we test code in the shared components of **Data Weaver**.

### 🧩 Framework Code: SCD Type 2 Writer

One of the most critical shared components in our codebase is the SCD (Slowly Changing Dimension) Type 2 writer, which manages historical changes in dimensional tables. This class encapsulates the logic for handling inserts, updates, and deletes, ensuring that changes are tracked over time and audit columns are properly maintained.

#### ❓ Why Unit Test SCD Type 2 Logic?

SCD Type 2 logic can be complex, with edge cases around effective dates, current flags, and hash columns. Automated unit tests are essential to:

- Validate that new rows are correctly inserted.
- Ensure updates create new versions and close out old ones.
- Confirm deletes are properly flagged.
- Check audit columns and data types.

#### 😎 Example: Unit Testing the SCD Type 2 Writer in Databricks

We use a suite of unit tests to cover the main scenarios for SCD Type 2. Below is a mock of our tests to articulate the idea/concepts:

```python
import unittest

from dataweaver.framework import DeltaType2Writer

class TestDeltaType2Writer(unittest.TestCase):
    """
    Unit tests for SCD Type 2 logic using DeltaType2Writer utility.
    """

    def setUp(self):
        # Setup: create a mock empty table and a DeltaType2Writer instance
        self.writer = DeltaType2Writer()
        self.mock_table = []

    def test_write_to_empty_table(self):
        # Test: Write initial rows to an empty table
        source_data = [
            {"id": 1, "name": "Alice", "effective_date": "2024-01-01"},
            {"id": 2, "name": "Bob", "effective_date": "2024-01-01"},
        ]
        result = self.writer.write(self.mock_table, source_data)
        self.assertEqual(len(result), 2)
        self.assertTrue(all(row["current_flag"] for row in result))

    def test_update_row(self):
        # Test: Update an existing row and verify SCD2 versioning
        self.mock_table = [
            {"id": 1, "name": "Alice", "effective_date": "2024-01-01", "current_flag": True}
        ]
        source_data = [
            {"id": 1, "name": "Alice Smith", "effective_date": "2024-06-01"}
        ]
        result = self.writer.write(self.mock_table, source_data)
        # Old version should be closed, new version should be current
        self.assertEqual(len(result), 2)
        self.assertTrue(any(row["name"] == "Alice Smith" and row["current_flag"] for row in result))
        self.assertTrue(any(row["name"] == "Alice" and not row["current_flag"] for row in result))

    def test_delete_row(self):
        # Test: Delete a row and verify it is flagged as deleted
        self.mock_table = [
            {"id": 2, "name": "Bob", "effective_date": "2024-01-01", "current_flag": True}
        ]
        source_data = []  # Bob is missing from source, should be deleted
        result = self.writer.write(self.mock_table, source_data)
        self.assertTrue(any(row["id"] == 2 and row.get("deleted_flag", False) for row in result))

    def test_insert_new_row(self):
        # Test: Insert a new row to the source data
        self.mock_table = [
            {"id": 1, "name": "Alice", "effective_date": "2024-01-01", "current_flag": True}
        ]
        source_data = [
            {"id": 1, "name": "Alice", "effective_date": "2024-01-01"},
            {"id": 3, "name": "Charlie", "effective_date": "2024-07-01"}
        ]
        result = self.writer.write(self.mock_table, source_data)
        self.assertTrue(any(row["id"] == 3 and row["current_flag"] for row in result))

if __name__ == "__main__":
    unittest.main()
```

Each test case sets up the table, performs the operation, writes to the delta table, and reads the results back to assert correctness. This approach ensures that the SCD Type 2 writer behaves as expected across all scenarios, and any regression is caught early in development.

**How this example follows best practices:**

- Tests are fast and independent, using mock data to control input data.
- Each test is isolated and repeatable.
- Focuses on behavior (row data, audit columns) rather than implementation details.
- Uses small, representative sample data for each scenario.
- Tests are readable and self-documenting, with descriptive class and method names.
- Covers edge cases (insert, update, delete) relevant to data variability.

### 📦 Product Code: Structured Extraction

In the product zone, we focus on leveraging the shared framework to perform certain tasks. For example, extracting structured information from unstructured data sources, such as oil and gas contracts. Here, the main challenge is ensuring that our extraction logic remains robust and reliable as prompts, models, and requirements evolve. Automated tests in this layer help validate that key fields are consistently and accurately extracted, and that the product logic gracefully handles changes or unexpected input. This section outlines why and how we test our product code, building on the foundation provided by the framework.

#### ❓ Why Unit Test Structured Extraction Logic?

Extracting structured information from unstructured oil and gas contracts involves handling non-deterministic LLM outputs and evolving prompts. Automated unit tests are essential to:

- Validate that key contract fields are correctly extracted from OCR'd data.
- Ensure the extraction logic handles missing or unexpected fields gracefully.
- Confirm that changes to prompts or LLMs do not break expected outputs.
- Provide confidence as product logic evolves.

#### Example: Unit Testing Contract Field Extraction

In this example, we leverage components from the framework to extract structured information from unstructured oil and gas contracts. As product zone developers, we trust the framework is well-tested, so our focus is on testing the product specific extraction logic.

We pass a few inputs to the framework (such as the LLM of choice and the prompt) and use a suite of tests to ensure outputs remain consistent and reliable as prompts or models change.

Here is a simplified example of how we structure these tests in our product zone:

```python
import unittest

from dataweaver.framework import StructuredLLMExtractor

class TestContractFieldExtraction(unittest.TestCase):
    """
    Unit tests for structured contract field extraction using StructuredLLMExtractor utility.
    """

    def setUp(self):
        """
        Set up the StructuredLLMExtractor instance with a prompt and LLM for use in tests.
        """
        self.prompt = "Extract contract_number, effective_date, end_date from contract text."
        self.llm = "gpt-4o"  # Example LLM choice
        self.extractor = StructuredLLMExtractor(prompt=self.prompt, llm=self.llm)

    def test_contract_number_extraction(self):
        """
        Test extraction of contract_number from mock OCR data.
        """
        mock_ocr_data = {
            "text": "Contract Number: 1234-5678\nEffective Date: 2024-07-01\nEnd Date: 2025-06-30",
        }
        result = self.extractor.extract(mock_ocr_data)
        self.assertEqual(result["contract_number"], "1234-5678")

    def test_effective_date_extraction(self):
        """
        Test extraction of effective_date from mock OCR data.
        """
        mock_ocr_data = {
            "text": "Contract Number: 1234-5678\nEffective Date: 2024-07-01\nEnd Date: 2025-06-30",
        }
        result = self.extractor.extract(mock_ocr_data)
        self.assertEqual(result["effective_date"], "2024-07-01")

    def test_end_date_extraction(self):
        """
        Test extraction of end_date from mock OCR data.
        """
        mock_ocr_data = {
            "text": "Contract Number: 1234-5678\nEffective Date: 2024-07-01\nEnd Date: 2025-06-30",
        }
        result = self.extractor.extract(mock_ocr_data)
        self.assertEqual(result["end_date"], "2025-06-30")

    def test_missing_field_handling(self):
        """
        Test that extraction logic handles missing fields gracefully.
        """
        mock_ocr_data = {
            "text": "Contract Number: 1234-5678\nEnd Date: 2025-06-30",  # effective_date missing
        }
        result = self.extractor.extract(mock_ocr_data)
        self.assertIsNone(result.get("effective_date"))

if __name__ == "__main__":
    unittest.main()
```

**How this example follows best practices:**

- Tests are fast and independent, using mock data (minus an LLM call to structure the mock OCR data).
- Each test is isolated and repeatable.
- Focuses on expected outputs and behavior, not internal implementation.
- Uses small, representative sample data for each test.
- Test names and docstrings are clear and descriptive.

## 🎉 Conclusion

As we strive to keep pull request (PR) times under 30 minutes, we’re constantly balancing the need for rapid iteration with the realities of integration testing which can take several minutes per run. Our ongoing focus is on making tests faster and more accessible, so every developer can run the full suite 'locally' and get quick feedback, without waiting for CI or opening a PR. Improving the efficiency and usability of our testing process will make the developer experience better.

We are learning that the key is to keep tests fast, focused, and easy to understand. Prioritize clarity, isolation, and meaningful coverage over sheer quantity. Make testing a natural part of your workflow, not an afterthought. As your codebase matures, explore advanced practices like [Test-Driven Development (TDD)](https://microsoft.github.io/code-with-engineering-playbook/automated-testing/unit-testing/tdd-example/) to make writing tests a natural part of your software development.

Simplicity in testing is about building trust in your code and empowering your team to move quickly and safely. The more robust and approachable your tests are, the more confidently you can innovate and deliver value.

If you want to connect and talk shop, Mark and I are always up for a conversation!

Thanks for reading 😀!
