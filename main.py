# main.py
from common.result import Failure, Success
from user.use_case import process_new_user, retrieve_user_profile, process_existing_user

TRACING = False
USE_CASES = {
    "process_new_user": (
        {"id": "b5591e6a-7feb-4c93-aeff-596c14e8f3bb",  "name": "Alice", "scenario": "normal" },
        {"id": "bb5db7f3-107a-46f7-a148-14a43f28e7c2",  "name": "Hi", "scenario": "normal" },
        {"name": "Alan", "scenario": "timeout" },
    ),
    "retrieve_user_profile": ("b5591e6a-7feb-4c93-aeff-596c14e8f3bb", "nonexistent-id"),
    "process_existing_user": (
        ("b5591e6a-7feb-4c93-aeff-596c14e8f3bb", {"name": "Alice Wilson", "scenario": "normal"}),
    )
}

if __name__ == "__main__":
    # Example raw data

    for key in USE_CASES:
        print(f"\n=== USE CASE: {key} ===")
        for data in USE_CASES[key]:
            match key:
                case "process_new_user":
                    final_result = process_new_user(data)
                case "retrieve_user_profile":
                    final_result = retrieve_user_profile(data)
                case "process_existing_user":
                    final_result = process_existing_user(*data)
                case _:
                    final_result = Failure(error=Exception("Unknown use case"))

            match(final_result):
                case Success(message):
                    print(f"🎉 Final Result: SUCCESS! -> {message}")
                case Failure(error, traceback_info):
                    print(f"🔥 Final Result: FAILED! -> {type(error).__name__}: {error}")
                    if TRACING and traceback_info:
                        print("📟 Traceback info:")
                        print(traceback_info)
            print("-" * 40)