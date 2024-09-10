import subprocess

def run_node():
    try:
       result =  subprocess.run(["node", "--version"],
            text=True,
            check=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
       
       return result.stdout.strip()
    except Exception as e:
        print(f"Error: {e}")

def check_str(text: str):
    if "노드" in text:
        result = run_node()
        print(result)

x = input("입력하세요")
check_str(x)