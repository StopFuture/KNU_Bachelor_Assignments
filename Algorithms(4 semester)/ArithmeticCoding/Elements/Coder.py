import collections
from decimal import *
getcontext().prec = 100


class Coder:
    def __init__(self, alphabet):
        self.alphabet = alphabet
        self.frequency_dict = self.alphabet_to_freq_dict(self.alphabet)
        self.probability_table = self.freq_dict_to_prob_table(self.frequency_dict)
        self.order = "".join([char for char in self.probability_table])
        self.log_ = list()

    @staticmethod
    def alphabet_to_freq_dict(alphabet):
        dct = collections.defaultdict(int)
        for char in alphabet:
            dct[char] += 1
        return dct

    @staticmethod
    def freq_dict_to_prob_table(freq_dict):
        a_len = sum(freq_dict.values())

        # "sorting" dict in decreasing order order
        sorted_ = sorted(freq_dict.items(), key=lambda x: -x[1])
        res = collections.defaultdict()
        left = Decimal(0.0)
        for element in sorted_:
            res[element[0]] = [left, left + Decimal(element[1] / a_len)]
            left += Decimal(element[1] / a_len)

        return res

    def encode_current_char(self, left, right, prob_table):
        current_prob = collections.defaultdict()
        interval_len = right - left
        prob_keys = [el for el in prob_table.keys()]
        for i in range(len(prob_table)):
            char = prob_keys[i]
            prev_prob = self.probability_table[char][1] - self.probability_table[char][0]
            new_prob = prev_prob * interval_len + left
            current_prob[char] = [left, new_prob]
            left = new_prob

        return current_prob

    def encode_sentence(self, sent):
        self.log_.append(f"\nEncoding {sent}: \n")
        prob_table = self.probability_table

        left = Decimal(0.0)
        right = Decimal(1.0)

        for i, char in enumerate(sent):
            prob_table = self.encode_current_char(left, right, prob_table)
            # print(prob_table)
            left = prob_table[char][0]
            right = prob_table[char][1]

            self.log_.append(f"Iteration {i}:\n char = {char},\n left = {left},\n "
                             f"right = {right}\n")
        encoded_sent = self.get_answer(left, right)
        self.log_.append(f"Encoded: {encoded_sent}")
        return encoded_sent

    def decode_sentence(self, number):
        self.log_.append(f"\nDecoding {number}: \n")
        prob_table = self.probability_table
        res = []
        left = Decimal(0.0)
        right = Decimal(1.0)
        char = None
        i = 0
        while True:
            prob_table = self.encode_current_char(left, right, prob_table)
            for char, interval in prob_table.items():
                if interval[0] <= number <= interval[1]:
                    res.append(char)
                    break

            left = prob_table[char][0]
            right = prob_table[char][1]

            self.log_.append(f"Iteration {i}:\n char = {char},\n left = {left},\n "
                             f"right = {right}\n")
            i += 1
            if char == "#":
                break

        decoded_sent = "".join(res)
        self.log_.append(f"Decoded: {decoded_sent}")
        return decoded_sent

    @staticmethod
    def get_answer(left, right):
        prec = -1
        n = right
        rt = str(right)
        e_view = rt.find("-")
        if e_view > -1:
            prec += int(rt[e_view + 1:]) + 2
        for char1, char2 in zip(str(right), str(left)):
            if char1 == char2:
                prec += 1
            else:
                break
        # print(prec)
        n = n if isinstance(n, Decimal) else Decimal(str(n))
        fmt = ".{}1".format("0" * (prec - 1))
        return n.quantize(Decimal(fmt), rounding=ROUND_DOWN)

    def set_alphabet(self, alphabet):  # init_coder_2.0
        self.alphabet = alphabet
        self.frequency_dict = self.alphabet_to_freq_dict(self.alphabet)
        self.probability_table = self.freq_dict_to_prob_table(self.frequency_dict)
        self.order = "".join([char for char in self.probability_table])
        self.log_ = None

    def display_log(self):
        for element in self.log_:
            print(element)
