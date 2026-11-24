from langgraph.constants import START, END
from langgraph.graph import StateGraph
from typedict import TypeDict


class MyState(TypeDict):
    query:str
    rag_result:str
    web_search_result:str
    final_answer:str

class InputSchema(TypeDict):
    query: str

class OutputSchema(TypeDict):
    final_answer: str

graph = StateGraph(
    state_schema=MyState,
    input_schema=InputSchema,
    output_schema=OutputSchema
)





