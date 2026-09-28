\# Sunny Days Childcare Policy Bot



\## About



This project is a grounded policy chatbot for a fictional childcare center called Sunny Days Childcare. The bot answers parent questions using only information contained in its parent handbook knowledge base.



The project uses TF-IDF and cosine similarity to retrieve relevant information before sending a question to the language model. If no information passes the similarity threshold, the bot refuses to answer instead of guessing.



\## How to Run



1\. Install the required packages:



&#x20;  pip install -r requirements.txt



2\. Add a Groq API key to:



&#x20;  .streamlit/secrets.toml



3\. Run the bot:



&#x20;  streamlit run grounded\_bot.py



\## Retrieval and Threshold



I tested the retriever with questions that should match the handbook and questions that should not match.



The final similarity threshold is 0.23. I chose this threshold based on the test results instead of guessing. The lowest score for a question that should retrieve was about 0.239, while the highest score for a question that should be refused was about 0.220.



I also changed some of the knowledge base chunk wording to make it closer to the way a parent would naturally ask a question. For example, changing the meals chunk to "Are meals and snacks included?" helped prevent an unrelated transportation question from matching that chunk.



\## Hallucination Tests



I tested five questions that are related to childcare but are not covered by the Sunny Days Parent Handbook.



\### Test 1

Question: Do you offer weekend childcare?



Response: I don't have enough information in the Sunny Days Parent Handbook to answer that question.



Result: Correctly refused.



\### Test 2

Question: Are there cameras parents can watch online?



Response: I don't have enough information in the Sunny Days Parent Handbook to answer that question.



Result: Correctly refused.



\### Test 3

Question: Does the daycare provide transportation from school?



Response: I don't have enough information in the Sunny Days Parent Handbook to answer that question.



Result: Correctly refused.



\### Test 4

Question: What is the teacher to child ratio?



Response: I don't have enough information in the Sunny Days Parent Handbook to answer that question.



Result: Correctly refused.



\### Test 5

Question: Do you give sibling discounts?



Response: I don't have enough information in the Sunny Days Parent Handbook to answer that question.



Result: Correctly refused.



\## What I Changed



During testing, I adjusted the similarity threshold and improved the wording of some knowledge base chunks. I added stop words to reduce matches caused by common words and set the final threshold to 0.23 based on the scores from my retrieval tests.



The bot also has a short circuit. If retrieval finds no matching information, the refusal is returned directly from the program and the language model is not called.



\## Source Attribution



The bot displays the source of the retrieved information under each grounded answer. This helps identify where a problem happens. If the wrong source is retrieved, that indicates a retrieval problem. If the correct source is retrieved but the model gives an unsupported answer, that indicates a grounding or prompt problem.



\## If I Had More Time



With more time, I would expand the parent handbook with additional childcare policies and test the retriever with more variations of questions that parents might ask.

