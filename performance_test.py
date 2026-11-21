
import json
import random
import time
import tracemalloc

from quiz import Quiz


def create_test_quizzes(count):
    """측정용 퀴즈 데이터를 생성한다."""
    return [
        Quiz(
            f"테스트 문제 {i}",
            [f"보기 {j}" for j in range(1, 5)],
            random.randint(1, 4)
        )
        for i in range(count)
    ]


def measure_performance(count):
    print(f"\n===== 퀴즈 {count:,}개 성능 측정 =====")

    # 메모리 사용량 측정
    tracemalloc.start()
    quizzes = create_test_quizzes(count)
    current_memory, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # 무작위 출제 준비 시간 측정
    start = time.perf_counter()
    random.sample(quizzes, len(quizzes))
    sample_time = time.perf_counter() - start

    # JSON 변환 시간 측정
    start = time.perf_counter()
    json_data = json.dumps(
        [quiz.to_dict() for quiz in quizzes],
        ensure_ascii=False
    )
    save_time = time.perf_counter() - start

    # JSON 데이터 읽기 및 객체 복원 시간 측정
    start = time.perf_counter()
    loaded_data = json.loads(json_data)
    restored_quizzes = [
        Quiz.from_dict(data) for data in loaded_data
    ]
    load_time = time.perf_counter() - start

    print(f"현재 메모리 사용량: {current_memory / 1024:.2f} KB")
    print(f"최대 메모리 사용량: {peak_memory / 1024:.2f} KB")
    print(f"무작위 출제 준비 시간: {sample_time * 1000:.2f} ms")
    print(f"JSON 변환 시간: {save_time * 1000:.2f} ms")
    print(f"JSON 읽기 및 객체 복원 시간: {load_time * 1000:.2f} ms")
    print(f"복원된 퀴즈 수: {len(restored_quizzes):,}개")


if __name__ == "__main__":
    for quiz_count in (1000, 5000, 10000):
        measure_performance(quiz_count)
