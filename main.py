# main.py
from quiz import QuizGame

def print_menu():
    """메인 메뉴 출력"""
    print("\n" + "="*40)
    print("       🎮 게임 퀴즈 게임 🎮")
    print("="*40)
    print("  1. 퀴즈 풀기")
    print("  2. 퀴즈 추가")
    print("  3. 퀴즈 목록")
    print("  4. 점수 확인")
    print("  5. 종료")
    print("="*40)

def main():
    game = QuizGame()

    while True:
        print_menu()

        choice = input("번호를 선택하세요: ").strip()

        if choice == "1":
            game.play_quiz()
        elif choice == "2":
            game.add_quiz()
        elif choice == "3":
            game.show_quiz_list()
        elif choice == "4":
            game.show_high_score()
        elif choice == "5":
            print("\n게임을 종료합니다. 안녕히 가세요! 👋")
            break
        else:
            print("\n⚠️ 1~5 사이의 번호를 입력하세요.")

if __name__ == "__main__":
    main()