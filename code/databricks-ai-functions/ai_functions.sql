SELECT * FROM databricks_ai_functions.default.data

SELECT
    Text,
    ai_classify(Text, ARRAY('Business', 'Sports', 'Technology', 'Entertainment', 'Fashion', 'Education', 'Food', 'Economics')) AS Category
  FROM
    databricks_ai_functions.default.data


SELECT
    Text,
    ai_gen(
      'Respond to the following text with a follow up question: ' || Text
    ) AS Question
  FROM
    databricks_ai_functions.default.data