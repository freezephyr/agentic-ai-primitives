''' This code demonstrates usage for evals/tests for RAG pipelines
'''

from pathlib import Path
import sys
import json
MODULE_DIR = Path(__file__).resolve().parent
if str(MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(MODULE_DIR))

from RAG_functions import (
    answer_question,
    build_collection,
    chunk_text,
    load_pdf,
    logger,
    run_inference,
)

RAG_TESTS=[
    {
        "Test_id":1,
        "Question": "who owns Wonderkid wonderland",
        "Expected":"not clear from document"
     },
    {
        "Test_id":2,
        "Question": "what was 2025 revenue?",
        "Expected":"USD 178 Million"
    },   
    {
        "Test_id":3,
        "Question": "Who founded wonderkid wonderland?",
        "Expected":"Kid Wonders"
    },
    {
        "Test_id":4,
        "Question": "Who used most wish credits?",
        "Expected":"not clear from document"
    }
    ]



def judge_prompt_generator(test_id: str, test_question:str ,expected_answer:str, actual_answer:str )->str:
    
    judge_prompt= (

        "RESPOND ONLY WITH JSON: {\"test_id\": N, \"score\": N}. NO OTHER TEXT.\n"
        "Score 1-5 how well the actual answer matches the expected answer.\n"
        f"Test ID: {test_id}\n"
        f"Question: {test_question}\n"
        f"Expected: {expected_answer}\n"
        f"Actual: {actual_answer}"
        )
    return judge_prompt


def run_rag_query_tests(collection, tests, n_results):
    print(f"starting Rag tests: {tests}")
    '''this function runs inference on test questions and responds with inference results'''
    test_results=[]
    for test in tests:
        question = test["Question"]
        result=answer_question(collection, question, n_results)
        print(f"collection:{collection}\n\n question: {question} \n\n result:{result}")
        test_results.append(result)

    return test_results


def judge_test_results(tests, answers):
    
    response=[]
    i=0
    for test in tests:
        print(f"Judge test:{test["Question"]}")
        test_id=test["Test_id"]
        question=test["Question"]
        expected=test["Expected"]
        answer=answers[i]
        prompt=judge_prompt_generator(test_id, question, expected, answer)
        messages=[{"role":"user", "content":prompt}]
        response.append(run_inference(messages, "tool", tools=None))
        i=i+1
    return response


pdf="C:\\Users\\malho\\OneDrive\\Documents\\Wonderkid_Wonderland_Annual_Earnings_Report.pdf"
collection="rag_tutorial"
chunk_size=512
overlap=64
n_results=3

'''
logging.basicConfig(
    level=logging.INFO if args.verbose else logging.WARNING,
    format="%(levelname)s %(message)s",
)
'''
doc = load_pdf(pdf)
logger.info("Loaded %d pages from %s", len(doc.pages), doc.name)

chunks = chunk_text(doc.text, chunk_size, overlap)
logger.info("Created %d chunks", len(chunks))
if not chunks:
    raise SystemExit("No text extracted from PDF; nothing to index.")

collection = build_collection(collection, chunks, source=doc.name)

test_results=run_rag_query_tests(collection,RAG_TESTS,3  )
answer=judge_test_results(RAG_TESTS, test_results)

print(answer)


scores = [json.loads(r[0])['score'] for r in x]
avg = sum(scores) / len(scores)
failed = [s for s in scores if s < 3]

print(f"Average score: {avg:.1f}/5")
print(f"Failed tests: {len(failed)}")



