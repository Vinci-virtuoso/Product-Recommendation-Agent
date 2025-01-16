from pydantic import BaseModel,Field

class Query(BaseModel):
    question: str
    user_id: str

class GetCurrentUser(BaseModel):
    current_user: str = Field(
        description="The name of the current user based on the provided user ID."
    )

class CheckRelevance(BaseModel):
    relevance: str = Field(
        description="Indicates whether the question is related to the database schema. 'relevant' or 'not_relevant'."
    )
class ConvertToSQL(BaseModel):
    sql_query: str = Field(
        description="The SQL query corresponding to the user's natural language question."
    )
class RewrittenQuestion(BaseModel):
    question: str = Field(description="The rewritten question.")