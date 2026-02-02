"""测试 edge-tts"""
import asyncio
import threading

def test_tts_sync():
    """与主应用相同的方式测试"""
    import edge_tts
    
    text = "你好，这是一个测试"
    voice = "zh-CN-YunxiNeural"
    
    print(f"测试文本: {text}")
    print(f"使用声音: {voice}")
    
    result = [None]
    error = [None]
    
    def run_in_thread():
        async def _synthesize():
            try:
                communicate = edge_tts.Communicate(text, voice)
                audio_data = b""
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        audio_data += chunk["data"]
                print(f"stream完成: {len(audio_data)} bytes")
                return audio_data
            except Exception as e:
                print(f"异常: {e}")
                return b""
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result[0] = loop.run_until_complete(_synthesize())
        except Exception as e:
            error[0] = e
            print(f"线程异常: {e}")
        finally:
            loop.close()
    
    thread = threading.Thread(target=run_in_thread)
    thread.start()
    thread.join(timeout=60)
    
    if error[0]:
        print(f"TTS失败: {error[0]}")
        return
    
    mp3_bytes = result[0]
    
    if not mp3_bytes or len(mp3_bytes) < 1024:
        print(f"失败: MP3数据无效 ({len(mp3_bytes) if mp3_bytes else 0} bytes)")
        return
    
    print(f"✓ 成功! MP3大小: {len(mp3_bytes)} bytes")
    
    with open("test_output.mp3", "wb") as f:
        f.write(mp3_bytes)
    print("✓ 已保存到 test_output.mp3")

if __name__ == "__main__":
    print("=" * 40)
    print("测试 edge-tts (与主应用相同方式)")
    print("=" * 40)
    test_tts_sync()
    print("\n测试完成")
