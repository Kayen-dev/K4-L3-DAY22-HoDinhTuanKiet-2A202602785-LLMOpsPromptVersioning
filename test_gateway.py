"""Smoke test vlearn: python test_gateway.py [--model ID] [--embeddings]."""
import argparse

from openai import APIConnectionError, APIStatusError, OpenAI

from src import config


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default=config.OPENAI_MODEL)
    parser.add_argument("--embeddings", action="store_true", help="Kiểm tra thêm embeddings cho RAG")
    args = parser.parse_args()
    if not config.OPENAI_API_KEY:
        print("Thiếu OPENAI_API_KEY trong .env (gateway key được cấp).")
        return 1

    try:
        with OpenAI(
            api_key=config.OPENAI_API_KEY,
            base_url=config.OPENAI_BASE_URL or None,
            timeout=60,
            max_retries=0,
        ) as client:
            response = client.chat.completions.create(
                model=args.model,
                messages=[{"role": "user", "content": "Reply with exactly: PONG"}],
                max_tokens=256,
            )
            content = response.choices[0].message.content if response.choices else None
            print("model:", args.model)
            print("response:", content)
            if not content or content.strip() != "PONG":
                print("FAIL: model chưa trả về đúng PONG; kiểm tra model hoặc giới hạn output token.")
                return 1
            if args.embeddings:
                result = client.embeddings.create(
                    model=config.OPENAI_EMBEDDING_MODEL,
                    input=["Gateway embedding smoke test"],
                )
                if not result.data or not result.data[0].embedding:
                    print("FAIL: embeddings rỗng.")
                    return 1
                print("embedding model:", config.OPENAI_EMBEDDING_MODEL)
                print("embedding dimensions:", len(result.data[0].embedding))
    except APIStatusError as exc:
        # Không in response body vì gateway có thể chứa thông tin nhạy cảm.
        print(f"FAIL: HTTP {exc.status_code}. Kiểm tra key, quyền truy cập và model trên gateway.")
        return 1
    except APIConnectionError:
        print("FAIL: không kết nối được gateway; kiểm tra OPENAI_BASE_URL và mạng.")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
