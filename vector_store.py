import chromadb


client = chromadb.PersistentClient(
    path="data/chroma_db"
)

collection = client.get_or_create_collection(
    name="store_policy"
)


def add_policy():
    with open(
        "docs/return_shipping_policy.txt",
        "r",
        encoding="utf-8"
    ) as file:
        policy = file.read()

    collection.upsert(
        ids=["policy"],
        documents=[policy]
    )

    print("Policy added to ChromaDB! ✅")


def search_policy(question):
    result = collection.query(
        query_texts=[question],
        n_results=1
    )

    return result["documents"][0][0]


if __name__ == "__main__":

    add_policy()

    answer = search_policy(
        "How many days can I return clothing?"
    )

    print()
    print("Search result:")
    print(answer)