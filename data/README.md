# Crawling Sacombank Data for Training a Chatbot

- Thêm **prompt** giải thích thuật ngữ ngân hàng và từ viết tắt cần tại `details_1.jsonl`
- Xóa prompt trùng lắp
- Phân rã một số **prompt** thành **prompt** nhỏ hơn
- Loại bỏ một số **prompt** có từ khóa, thông tin không có ý nghĩa ở Việt Nam ở file `details_5.jsonl`. (tên file cũ `vi_FAQs.jsonl`)
- xử lý thủ công một số prompt


## Version 2:
- transform a question to a complete question
- 

## Version 1
`jsonl` file will be used for training chatbot. And their structure is:
```jsonl
[{'prompt':'sample question', 'response':'sample response'}]

```

- `details.jsonl` was data crawling from [Sacombank website](https://www.sacombank.com.vn/)    
- `FAQ.jsonl` was file answers and question of bank
- `filter.jsonl` was file filtering (by keyword) from other data


