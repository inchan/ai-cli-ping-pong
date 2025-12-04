import asyncio
import sys
import os

# 프로젝트 루트를 path에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

from ai_cli_mcp.server import call_tool, list_available_tools
from ai_cli_mcp.task_manager import get_task_manager, InMemoryStorage

async def run_scenarios():
    print("=== 🅰️ 동기 vs 비동기 처리 시나리오 테스트 ===")

    # 0. 테스트용 CLI 추가 (echo 기반)
    print("\n[Setup] 테스트용 CLI 'test-bot' 추가 중...")
    await call_tool("add_tool", {
        "name": "test-bot",
        "command": "cat"
    })
    
    # 1. [Sync] 기본 단답형 질문
    print("\n1. [Sync] 기본 단답형 질문 (즉시 응답)")
    result = await call_tool("run_tool", {
        "cli_name": "test-bot",
        "message": "Hello Sync",
        "run_async": False
    })
    print(f"Result: {result}")
    assert "response" in result
    assert "Hello Sync" in result["response"]
    print("✅ Pass")

    # 2. [Async] 긴 작문 요청 (비동기 시작)
    print("\n2. [Async] 비동기 작업 시작")
    result = await call_tool("run_tool", {
        "cli_name": "test-bot",
        "message": "Hello Async",
        "run_async": True
    })
    print(f"Result: {result}")
    assert "task_id" in result
    assert result["status"] == "running"
    task_id = result["task_id"]
    print("✅ Pass")

    # 3. [Async] 작업 상태 조회 (Polling)
    print("\n3. [Async] 작업 상태 조회")
    for _ in range(5):
        status = await call_tool("get_run_status", {"task_id": task_id})
        print(f"Status: {status}")
        if status["status"] == "completed":
            assert "Hello Async" in status["result"]
            print("✅ Pass")
            break
        await asyncio.sleep(0.5)
    else:
        print("❌ Fail: Timeout waiting for task")

    # 4. [Async] 병렬 작업 요청
    print("\n4. [Async] 병렬 작업 요청")
    tasks = []
    for i in range(3):
        tasks.append(call_tool("run_tool", {
            "cli_name": "test-bot",
            "message": f"Parallel {i}",
            "run_async": True
        }))
    
    results = await asyncio.gather(*tasks)
    print(f"Launched {len(results)} tasks")
    for r in results:
        assert "task_id" in r
    print("✅ Pass")

    # 5. [Sync/Async] 존재하지 않는 명령어 에러 처리
    print("\n5. [Async] 존재하지 않는 CLI 에러 처리")
    result = await call_tool("run_tool", {
        "cli_name": "unknown_bot",
        "message": "test",
        "run_async": True
    })
    task_id = result["task_id"]
    
    await asyncio.sleep(0.5)
    status = await call_tool("get_run_status", {"task_id": task_id})
    print(f"Status: {status}")
    assert status["status"] == "failed"
    assert "CLINotFoundError" in status["error"] or "알 수 없는 CLI" in status["error"]
    print("✅ Pass")

if __name__ == "__main__":
    # TaskManager 초기화
    get_task_manager().storage = InMemoryStorage()
    asyncio.run(run_scenarios())
