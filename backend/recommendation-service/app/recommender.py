from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


def calculate_match_score(
    resume_text,
    job_description
):
    resume_embedding = model.encode(
        [resume_text]
    )

    job_embedding = model.encode(
        [job_description]
    )

    similarity = cosine_similarity(
        resume_embedding,
        job_embedding
    )

    return round(
        float(similarity[0][0]) * 100,
        2
    )