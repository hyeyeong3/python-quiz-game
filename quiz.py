# quiz.py
import json
import os
import random

class Quiz:
    def __init__(self, question, options, answer):
        self.question = question    # 문제
        self.options = options      # 보기 리스트
        self.answer = answer        # 정답 번호 (1~4)

    def to_dict(self):
        """Quiz 객체를 딕셔너리로 변환 (JSON 저장용)"""
        return {
            "question": self.question,
            "options": self.options,
            "answer": self.answer
        }

    @staticmethod
    def from_dict(data):
        """딕셔너리를 Quiz 객체로 변환 (JSON 불러오기용)"""
        return Quiz(data["question"], data["options"], data["answer"])


class QuizGame:
    STATE_FILE = "state.json"

    def __init__(self):
        self.quizzes = []
        self.high_score = 0
        self.load_state()

    # ────────────────────────────────
    # 파일 저장 / 불러오기
    # ────────────────────────────────
    def load_state(self):
        """state.json에서 퀴즈 목록과 최고 점수를 불러온다."""
        if not os.path.exists(self.STATE_FILE):
            # 파일 없음 → 기본 데이터 사용
            self._init_default_quizzes()
            self.save_state()
            return

        try:
            with open(self.STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.quizzes = [Quiz.from_dict(q) for q in data.get("quizzes", [])]
            self.high_score = data.get("high_score", 0)
        except (json.JSONDecodeError, KeyError):
            # 파일 손상 → 기본 데이터로 복구
            print("⚠️ 저장 파일이 손상되었습니다. 기본 데이터로 초기화합니다.")
            self._init_default_quizzes()
            self.high_score = 0
            self.save_state()

    def save_state(self):
        """퀴즈 목록과 최고 점수를 state.json에 저장한다."""
        try:
            data = {
                "quizzes": [q.to_dict() for q in self.quizzes],
                "high_score": self.high_score
            }
            with open(self.STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError as e:
            print(f"⚠️ 파일 저장 중 오류가 발생했습니다: {e}")

    def _init_default_quizzes(self):
        """기본 퀴즈 5개를 초기 데이터로 등록한다."""
        default = [
            Quiz(
                "닌텐도에서 2026년 11월 5일에 발매한, 젤다의 전설 40주년 기념 리메이크 작은?",
                ["브레스 오브 더 와일드", "몽환의 모래시계", "시간의 오카리나", "무쥬라의 가면"],
                3
            ),
            Quiz(
                "'드레스 메이커'는 기존에 액션 게임을 만들던 개발사에서 출시한 드레스 만들기 게임입니다. "
                "다음 중 제작자가 드레스 메이커라는 게임을 만들고자 한 동기는?",
                ["예쁜 드레스를 만들고 싶어서.", "많은 돈을 벌기 위해서.",
                 "예쁜 드레스를 입고 싶어서.", "질병으로 인해 의상 디자이너 일을 못하는 아내를 위해서."],
                4
            ),
            Quiz(
                "농장 시뮬레이션 게임 '스타듀밸리'의 개발 인원 수는?",
                ["1명", "2명", "10명", "100명"],
                1
            ),
            Quiz(
                "국내 게임 제작사 '에피드게임즈'는 한 때 개발비에 허덕여, 개발비를 충원하기 위해 "
                "회사의 대표가 큰 선택을 했습니다... 다음 중 대표가 담보로 건 것은?",
                ["콩팥", "집문서", "새끼손가락", "1억원 수표"],
                2
            ),
            Quiz(
                "게임 제작자가 게임의 무료 체험판을 배포하는 일은 아주 흔합니다. 하지만 최근에 들어선 "
                "아예 예정되어있던 체험판도 철회하는 일이 잦습니다. "
                "다음 중 게임 제작자가 무료 체험판의 배포를 철회하는 이유는 무엇일까요.",
                ["별도 버전 제작 및 유지보수 부담으로 인해서.", "많은 돈을 벌기 위해서.",
                 "AI로 게임 내 코드를 복제한 모방작을 우려하여.", "게임 개발 자체가 철회되어서."],
                3
            ),
        ]
        self.quizzes = default

    # ────────────────────────────────
    # 공통 입력 처리 헬퍼
    # ────────────────────────────────
    def _input_number(self, prompt, min_val, max_val):
        """
        숫자 입력을 받는 공통 메서드.
        - 빈 입력, 공백, 숫자 변환 실패, 범위 밖 모두 처리
        - KeyboardInterrupt / EOFError 는 호출부(main.py)에서 처리
        """
        while True:
            raw = input(prompt)
            stripped = raw.strip()

            if stripped == "":
                print("⚠️ 값을 입력해주세요.")
                continue

            try:
                num = int(stripped)
            except ValueError:
                print(f"⚠️ 숫자를 입력해주세요. (예: {min_val})")
                continue

            if not (min_val <= num <= max_val):
                print(f"⚠️ {min_val}~{max_val} 사이의 번호를 입력하세요.")
                continue

            return num

    def _input_text(self, prompt):
        """
        텍스트 입력을 받는 공통 메서드.
        - 빈 입력 방지
        """
        while True:
            raw = input(prompt).strip()
            if raw == "":
                print("⚠️ 내용을 입력해주세요.")
                continue
            return raw

    # ────────────────────────────────
    # 기능별 메서드
    # ────────────────────────────────
    def play_quiz(self):
        """퀴즈 풀기"""
        if not self.quizzes:
            print("\n등록된 퀴즈가 없습니다.")
            return

        questions = random.sample(self.quizzes, len(self.quizzes))
        score = 0

        print("\n" + "="*40)
        print("        퀴즈 시작!")
        print("="*40)

        for i, quiz in enumerate(questions, 1):
            print(f"\nQ{i}. {quiz.question}")
            for j, option in enumerate(quiz.options, 1):
                print(f"  {j}) {option}")

            ans = self._input_number("정답 번호를 입력하세요: ", 1, 4)

            if ans == quiz.answer:
                print("✅ 정답입니다!")
                score += 1
            else:
                print(f"❌ 오답입니다! 정답은 {quiz.answer}번이에요.")

        print("\n" + "="*40)
        print(f"최종 점수: {score} / {len(questions)}")

        if score > self.high_score:
            self.high_score = score
            print("🏆 새로운 최고 점수입니다!")
            self.save_state()

        print("="*40)

    def add_quiz(self):
        """퀴즈 추가"""
        print("\n" + "="*40)
        print("        퀴즈 추가")
        print("="*40)

        question = self._input_text("문제를 입력하세요: ")
        options = []
        for i in range(1, 5):
            opt = self._input_text(f"{i}번 보기를 입력하세요: ")
            options.append(opt)

        answer = self._input_number("정답 번호 (1~4): ", 1, 4)

        self.quizzes.append(Quiz(question, options, answer))
        self.save_state()
        print("✅ 퀴즈가 추가되었습니다!")

    def show_quiz_list(self):
        """퀴즈 목록 출력"""
        print("\n" + "="*40)
        print("        퀴즈 목록")
        print("="*40)

        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        for i, quiz in enumerate(self.quizzes, 1):
            print(f"\nQ{i}. {quiz.question}")
            for j, option in enumerate(quiz.options, 1):
                print(f"  {j}) {option}")
            print(f"  정답: {quiz.answer}번")

    def show_high_score(self):
        """최고 점수 출력"""
        print("\n" + "="*40)
        if self.high_score == 0:
            print("  아직 퀴즈를 풀지 않았습니다.")
        else:
            print(f"  🏆 최고 점수: {self.high_score} / {len(self.quizzes)}")
        print("="*40)