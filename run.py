"""
启动 Web 服务器
运行方式: python run.py
"""
import uvicorn

if __name__ == "__main__":
    print("=" * 50)
    print("AI 短视频生成器 - Web 服务")
    print("=" * 50)
    print("服务器启动后，请在浏览器打开:")
    print("  http://localhost:8000")
    print("按 Ctrl+C 可停止服务")
    print("=" * 50)

    uvicorn.run(
        "src.api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )
