from faker import Faker
import pandas as pd
import numpy as np

def generate_social_media_data(num_posts=200):
    """生成社交媒体舆情数据"""
    fake = Faker('zh_CN')
    np.random.seed(42)

    # 情感标签和关键词
    sentiments = ['正面', '负面', '中性']
    brands = ['苹果', '华为', '小米', 'OPPO', 'vivo', '三星']
    topics = ['电池续航', '拍照效果', '系统流畅度', '售后服务', '性价比']

    data = pd.DataFrame({
        '发布时间': pd.date_range('2023-06-01', periods=num_posts, freq='B'),
        '用户名': [fake.name() for _ in range(num_posts)],
        '品牌': np.random.choice(brands, num_posts),
        '讨论主题': np.random.choice(topics, num_posts),
        '情感倾向': np.random.choice(sentiments, num_posts, p=[0.6, 0.2, 0.2]),
        '点赞数': np.random.poisson(25, num_posts),
        '评论数': np.random.poisson(8, num_posts),
        '内容': [fake.sentence(nb_words=19) for _ in range(num_posts)]
    })
    return data

# 生成并保存数据
social_data = generate_social_media_data()
social_data.to_csv('social_media.csv', index=False, encoding='utf-8-sig')