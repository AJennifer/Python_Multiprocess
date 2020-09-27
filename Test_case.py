import io


def speech_to_text(content, hertz, append_list = [], max_alternative = 5):
    stt_result = list(content)
    return stt_result


def synonym(sentence, correct_file):
    synonyms = []
    new_sentence = sentence

    input_file = open(correct_file, 'r')
    for line in input_file:
        synonyms.append(line.split())

    for each in synonyms:
        # sentence是原始的transcript，数据类型是str，所以这类的correction是讲字符串的替代词进行替换
        new_sentence = new_sentence.replace(each[0], each[1])
    return new_sentence


def simple_auto_correct(sentence):
    new_sentence = sentence
    return new_sentence


class TestCase(object):
    def __init__(self, audio_path, sample_rate, key_word_verify_path, contexts):
        self.audio_path = audio_path
        self.sample_rate = sample_rate
        self.key_word_verify_path = key_word_verify_path
        self.key_words = []
        self._init_key_words(key_word_verify_path)
        self.contexts = contexts
        self.raw_result_transcript = ''
        self.corrected_transcript = ''
        self.passed_keywords = []
        self.failed_keywords = []

    def _init_key_words(self, keyword_file_path):
        # key_words 的内容是获取人工听取每个audio，记录的每个audio出现的关键字，相当于原始的配置
        with open(file=keyword_file_path, mode='r', encoding='utf-8-sig') as keyword_file:
            first_line = keyword_file.readline()
        self.key_words = first_line.strip().split(' ')

    @staticmethod
    def test_case_get_context(test_case):
        audio_file = io.open(test_case.audio_seg_path, 'rb')
        audio_content = audio_file.read()
        # text_case.contexts代表的内容是需要tune的boost_value_word的组合
        response = speech_to_text(audio_content, test_case.sample_rate, appended_context=test_case.contexts,
                                  max_alternative=1)
        audio_file.close()
        if len(response.results) == 0:
            return
        response_word = response.results[0].alernatives[0].words
        words_str = []
        for each_word in response_word:
            words_str.append(each_word)
        # 每次获得的raw_result_transcript是在完成stt后得到的raw文本
        test_case.raw_result_transcript = ''.join(words_str)
        # 这个调用的是一个方法
        test_case.correct_transcript()

    def correct_transcript(self):
        pre_processed_transcript = synonym(self.raw_result_transcript, 'Correction.txt')
        # self函数中的correct_transcript是调用了simple_auto_correct方法得到的，得到的是函数的返回值
        self.correct_transcript = simple_auto_correct(pre_processed_transcript)

    def verify_transcript(self):
        for key_word in self.key_words:
            if key_word in self.correct_transcript:
                self.passed_keywords.append(key_word)
            else:
                self.failed_keywords.append(key_word)