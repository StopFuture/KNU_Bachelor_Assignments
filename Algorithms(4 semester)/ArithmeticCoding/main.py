# Fedorych Andrii K25
from Elements.Coder import *


if __name__ == '__main__':
    alphabet = input("Enter a string that specifies the alphabet and clearly "
                     "identifies the probability of each character:")
    if "#" not in alphabet:
        alphabet += "#"
    cd = Coder(alphabet)

    sent = input("Enter a string to encoding:")
    if "#" not in sent:
        sent += "#"
    encoded_sent = cd.encode_sentence(sent)

    print(f"Encoded: {encoded_sent}\n")
    input_ = input("Enter a number to decoding or press enter to decode previous input:")
    to_decode = None
    if len(input_) == 0:
        to_decode = encoded_sent
    else:
        to_decode = input_.strip().replace(",", ".")

    decoded_sent = cd.decode_sentence(Decimal(to_decode))
    print("Decoded: ", decoded_sent)

    step_by_step = input("To get step by step solution of decoding/encoding process enter '1': ")
    if step_by_step.strip().replace("'", "") == "1":
        cd.display_log()
