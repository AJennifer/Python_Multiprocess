import csv
from pathlib import Path


class AnnualReport(object):
    def __init__(self, contexts, test_cases):
        self.contexts = contexts
        self.test_cases = test_cases
        self.key_words = set()
        self.key_word_accuracy = dict()
        self.key_word_total =dict()
        self.key_word_passed = dict()
        self.overall_passed = 0

    def _init_key_words_and_dict(self):
        for test_case in self.test_cases:
            # 在report的key_words跟前面test_case得到的key_words是一样的
            self.key_words |= set(test_case.key_words)

        for key_word in self.key_words:
            # 初始化这几个字典的key是each key_word，value是0
            self.key_word_accuracy[key_word] = 0
            self.key_word_passed[key_word] = 0
            self.key_word_total[key_word] = 0

    def compute_general_accuracy(self):
        self._init_key_words_and_dict()
        for test_case in self.test_cases:
            for key_word in test_case.key_words:
                # 只要配置文件里面出现任何一个关键字，则key_word_total的计算就应该增加一个
                # 所以每个关键字的总数是加总每个关键字出现在文件中的数
                self.key_word_total[key_word] += 1
            if len(test_case.key_words) == len(test_case.passed_keywords):
                self.overall_passed += 1
                for key_word in test_case.keywords:
                    self.key_word_passed[key_word] += 1
            else:
                for key_word in test_case.passed_keywords:
                    # 这里统计的是将each key_word有出现在前面pass_keywords列表进行加总
                    # 得到的就是每个key_word出现的次数
                    self.key_word_passed[key_word] += 1
        for key_word in self.key_words:
            self.key_word_accuracy[key_word] = "{}/{}".format(self.key_word_passed[key_word],
                                                              self.key_word_total[key_word])

    def export_to_csv(self, general_report_path, detail_report_path):
        general_report_file = open(general_report_path, 'a', newline='', encoding='UTF-8')
        spamwriter = csv.writer(general_report_file)
        spamwriter.writerow(
            [
                self.contexts,
                self.key_word_accuracy
            ]
        )
        general_report_file.close()

        detail_report_file = open(detail_report_path, 'a', newline='', encoding='UTF-8')
        spamwriter = csv.writer(detail_report_file)
        for test_case in self.test_cases:
            spamwriter.writerow(
                [
                    Path(test_case.file_path).stem,
                    test_case.contexts,
                    ' '.join(test_case.passed_keywords),
                    ' '.join(test_case.failed_keywords),
                    test_case.raw_result_transcript,
                    test_case.corrected_transcript
                ]
            )
        detail_report_file.close()