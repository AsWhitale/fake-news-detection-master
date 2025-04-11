def platform_tokenizer(x):
    """将整个 platform 字段视为单个 token"""
    return [str(x)]  # 确保转换为字符串


def hashtag_tokenizer(x):
    """按逗号分割话题标签"""
    return str(x).split(',')  # 确保处理字符串输入
