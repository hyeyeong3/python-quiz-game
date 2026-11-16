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
        try:
            print_menu()
            choice = input("번호를 선택하세요: ").strip()

            if choice == "":
                print("⚠️ 값을 입력해주세요.")
                continue

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
                print("⚠️ 1~5 사이의 번호를 입력하세요.")

        except KeyboardInterrupt:
            # Ctrl+C 입력 시
            print("\n\n⚠️ 강제 종료가 감지되었습니다. 저장 후 종료합니다.")
            game.save_state()
            break

        except EOFError:
            # 입력 스트림 종료 시
            print("\n\n⚠️ 입력이 종료되었습니다. 저장 후 종료합니다.")
            game.save_state()
            break

if __name__ == "__main__":
    main()