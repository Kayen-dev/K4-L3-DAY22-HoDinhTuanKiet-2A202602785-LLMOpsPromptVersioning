# Evidence và phân tích prompt

Đánh giá RAGAS dùng 50 cặp câu hỏi cho mỗi prompt, với `openai/gpt-4o-mini` qua vlearn Gateway. Bốn chỉ số trong `03_ragas_report.json` là điểm trung bình của các mẫu hợp lệ.

| Chỉ số | V1 | V2 |
| --- | ---: | ---: |
| Faithfulness | 0.9840 | 0.7958 |
| Answer relevancy | 0.9140 | 0.8851 |
| Context recall | 1.0000 | 1.0000 |
| Context precision | 0.9450 | 0.9450 |

V1 đạt ngưỡng faithfulness 0.8 và cao hơn V2 ở faithfulness lẫn answer relevancy. Hai prompt dùng cùng retriever và knowledge base, nên context recall và context precision gần như bằng nhau. V1 yêu cầu câu trả lời ngắn; V2 yêu cầu giải thích cơ chế và hệ quả. Có thể yêu cầu dài hơn của V2 làm tăng khả năng đưa vào ý chưa được context hỗ trợ. Đây là giả thuyết từ điểm trung bình; cần xem các mẫu điểm thấp để xác định nguyên nhân.

`03_ragas_run_log.txt` ghi cả những lần thử gặp lỗi gateway/timeout và lần chấm lại thành công. Bảng `FINAL VERIFIED COMPARISON` ở cuối log cùng `03_ragas_report.json` là kết quả cuối.
