import jieba
import jieba.analyse
from DAL import ReviewsContentDAL, SplitWordDAL


def splitSentence():
    reviews_dal = ReviewsContentDAL()
    split_dal = SplitWordDAL()
    not_split_records = reviews_dal.query_all_not_split()
    for record in not_split_records:
        review_content = record["review_content"].strip()
        review_title = record["review_title"].strip()
        content_split_result = jieba.analyse.extract_tags(review_content)
        title_split_result = jieba.analyse.extract_tags(review_title)
        content_split_result.extend(title_split_result)
        content_id = record["id"]
        reviews_dal.update_split_status(content_id)
        word_app_id = record["review_app_id_id"]
        print(word_app_id, content_split_result)
        for word in content_split_result:
            data = {"word": word, "word_app_id_id": word_app_id}
            split_dal.insert_one_set(**data)


splitSentence()
print("finished")
