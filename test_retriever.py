# Michelle Salgado, 09/28/26, Assignment 6 Retriever Tests
# Tests the Sunny Days Childcare Policy Bot retrieval system.

from retriever import Retriever


retriever = Retriever()


# Questions that SHOULD find information in the knowledge base.
SHOULD_RETRIEVE = [
    "What time can I drop off my child?",
    "What time do I need to pick up my child?",
    "Can my child come to daycare with a fever?",
    "Can the staff give my child medication?",
    "Does the daycare provide meals and snacks?",
    "Do the children have nap time?",
    "When is tuition due?",
    "Do I still pay if my child is absent?"
]


# Questions that SHOULD NOT find an answer in the knowledge base.
SHOULD_REFUSE = [
    "Does the daycare provide transportation from school?",
    "Are there cameras parents can watch online?",
    "Do you offer weekend childcare?",
    "What is the teacher to child ratio?",
    "Do you give sibling discounts?"
]


def print_results(title, questions):
    print("\n" + title)
    print("-" * 60)

    for question in questions:
        hits = retriever.search(question)

        print("\nQuestion:", question)

        if hits:
            for document, score in hits:
                print(
                    "  ",
                    document["id"],
                    "- score:",
                    round(score, 3)
                )
        else:
            print("   No match")


print_results("QUESTIONS THAT SHOULD RETRIEVE", SHOULD_RETRIEVE)
print_results("QUESTIONS THAT SHOULD BE REFUSED", SHOULD_REFUSE)