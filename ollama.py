import subprocess
import datetime

def ask_ollama(question, model_name='llama3.1'):
    try:
        # Ollama 모델을 실행하여 질문을 보내고 결과를 받음
        result = subprocess.run(
            ['ollama', 'run', model_name],
            input=question,  # 질문을 입력으로 전달
            text=True,       # 결과를 텍스트로 처리
            check=True,      # 오류 발생 시 예외를 발생시킴
            stdout=subprocess.PIPE,  # 표준 출력으로 결과를 받음
            stderr=subprocess.PIPE   # 오류 출력을 받음
        )
        
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"오류 발생: {e.stderr.strip()}"
    except Exception as e:
        return f"실행 중 오류가 발생했습니다: {str(e)}"

def save_to_markdown(question, answer, filename="conversation.md"):
    # 현재 시간 추가
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Markdown 형식으로 저장
    with open(filename, 'a') as file:
        file.write(f"## 질문 ({current_time})\n")
        file.write(f"{question}\n\n")
        file.write(f"### 대답\n")
        file.write(f"{answer}\n\n")
        file.write("---\n\n")

if __name__ == "__main__":
    while True:
        question = input("Ollama에 질문하세요 (종료하려면 'exit' 입력): ")
        if question.lower() == 'exit':
            break
        
        # Ollama에 질문하고 대답 받기
        answer = ask_ollama(question)
        
        # 터미널에 출력
        print(f"대답: {answer}")
        
        # 결과를 Markdown 파일에 저장
        save_to_markdown(question, answer)
