import os
import sys

from openspeechlib.transcriptions.common import extract_phones_from_word, apply_filters


def generate_mlf_files(transcription_folder, output_file):
    files = os.listdir(transcription_folder)
    output_file = open(output_file, 'w+')
    output_file.write("#!MLF!#\n")
    for file_name in files:
        if len(file_name) > 8:
            output_file.write(f'"*/{file_name.replace("txt", "wav")}.lab"\n')
            with open(os.path.join(transcription_folder, file_name), encoding='latin1') as current_file:
                output_file.write("sil\n")
                lines = current_file.readlines()
                for line in lines:
                    for word in line.split():
                        word = apply_filters(word.lower())
                        output_file.write(f"{word}\n")
            output_file.write("sil\n")
            output_file.write(".\n")

    output_file.close()


def generate_copy_scp_files(source_folder, destination_folder, output_file, include_source=True):
    files = os.listdir(source_folder)
    output_file = open(output_file, 'w+')
    for file_name in files:
        if include_source:
            output_file.write(f"{os.path.abspath(os.path.join(source_folder, file_name))} {os.path.abspath(destination_folder)}/{file_name}.mfc\n")
        else:
            output_file.write(
                f"{os.path.abspath(destination_folder)}/{file_name}.mfc\n")
    output_file.close()


def generate_dict(transcription_folder, output_file):
    files = os.listdir(transcription_folder)
    different_words = set()
    word_transcription = list()
    for file_name in files:
        if len(file_name) > 8:
            with open(os.path.join(transcription_folder, file_name), encoding='latin1') as current_file:
                lines = current_file.readlines()
                for line in lines:
                    for word in line.split():
                        word = apply_filters(word.lower())
                        word = word.replace("x", "cs")
                        if word not in different_words:
                            different_words.add(word)
                            word_transcription.append(f"{word}  {extract_phones_from_word(word)}")
    output_file = open(output_file, 'w+')
    word_list = '\n'.join(sorted(word_transcription)).encode("UTF-8").decode("UTF-8")
    output_file.write(word_list)
    output_file.close()


if __name__ == '__main__':
    print(sys.argv)
    generate_mlf_files(sys.argv[1], sys.argv[2])
    # generate_copy_scp_files(sys.argv[1], sys.argv[2], sys.argv[3], False)
    # generate_dict(sys.argv[1], sys.argv[2])


# HVite -T 1  -l '*'  -b sil -C config.deltas -H ../../01_open_speech_corpus/htk_experiments/words1/hmm1/macros -H ../../01_open_speech_corpus/htk_experiments/words1/hmm1/hmmdefs -i aligned.mlf -m -t 250.0 -y lab -I words.mlf -S test.scp -a s001.dict ../../01_open_speech_corpus/htk_experiments/words1/isolated_words.phonemes_sorted.list
