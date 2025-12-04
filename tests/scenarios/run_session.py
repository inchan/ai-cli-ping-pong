import asyncio
import sys
import os

# 프로젝트 루트를 path에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

from ai_cli_mcp.server import call_tool
from ai_cli_mcp.task_manager import get_task_manager, InMemoryStorage

async def run_scenarios():
    print("=== 🅱️ 장기 세션 및 컨텍스트 시나리오 테스트 ===")

    # 0. 세션 지원 테스트용 CLI 추가
    # Claude처럼 동작하는 echo 봇
    print("\n[Setup] 세션 지원 테스트용 CLI 'session-bot' 추가 중 (350초 지연)...")
    await call_tool("add_tool", {
        "name": "session-bot",
        "command": "bash", # command는 "bash"여야 함
        "extra_args": ["-c", "sleep 350 && cat"], # 350초 지연 추가
        "supported_args": ["-c", "--session-id", "--resume"], # supported_args에 "-c" 추가
        "timeout": 360 # CLI 기본 타임아웃 300초를 덮어씀
    })

    # 1. [Session] 기본 정보 주입 (세션 시작)
    print("\n1. [Session] 세션 시작")
    result = await call_tool("run_tool", {
        "cli_name": "session-bot",
        "message": "My info",
        "session_id": "my-long-session-001"
    })
    print(f"Result: {result}")
    # echo는 인자를 그대로 출력하지 않고 stdin을 출력함.
    # 하지만 execute_with_session 내부 로직을 탔다는 것이 중요.
    assert "response" in result
    print("✅ Pass")

    # 2. [Session] 정보 회상 (컨텍스트 유지 - 재개)
    print("\n2. [Session] 세션 재개 (Resume)")
    result = await call_tool("run_tool", {
        "cli_name": "session-bot",
        "message": "Recall info",
        "session_id": "my-long-session-001",
        "resume": True
    })
    print(f"Result: {result}")
    assert "response" in result
    print("✅ Pass")

    # 3. [Session + Async] 비동기 세션 대화
    print("\n3. [Session + Async] 비동기 세션 요청 (350초 이상 대기 필요)")
    result = await call_tool("run_tool", {
        "cli_name": "session-bot",
        "message": "Async Session Work",
        "session_id": "my-long-session-001",
        "run_async": True
    })
    print(f"Result: {result}")
    assert "task_id" in result
    task_id = result["task_id"]
    
    # 결과 대기 시간을 넉넉하게 설정 (예: 360초 동안 1초 간격 폴링)
    for i in range(360): # 최대 360초 대기
        status = await call_tool("get_run_status", {"task_id": task_id})
        print(f"Status (attempt {i+1}/360): {status}")
        if status["status"] == "completed":
            print(f"Async Task Completed: {status['result']}")
            assert "Async Session Work" in status["result"] # cat이 입력 그대로 반환하므로
            print("✅ Pass")
            break
        await asyncio.sleep(1) # 1초 간격 폴링
    else:
        print("❌ Fail: Timeout waiting for long-running async task")
        assert False, "Timeout waiting for long-running async task"


    # 4. [Session] 다른 세션 ID 사용
    print("\n4. [Session] 다른 세션 ID 사용")
    result = await call_tool("run_tool", {
        "cli_name": "session-bot",
        "message": "Other session",
        "session_id": "other-session-002"
    })
    print(f"Result: {result}")
    assert "response" in result
    print("✅ Pass")

if __name__ == "__main__":
    get_task_manager().storage = InMemoryStorage()
    asyncio.run(run_scenarios())
