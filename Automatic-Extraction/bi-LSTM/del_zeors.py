import os

input_file_path = r'E:\python_\Emotional-Action-Visualization-and-Automatic-Extraction-master\corpus\xie0-4_19-23\all_sentences\x'
output_file_path = r'E:\python_\Emotional-Action-Visualization-and-Automatic-Extraction-master\corpus\xie0-4_19-23\all_sentences\y'
inputPath_list = os.listdir(input_file_path) #列出文件夹下所有的目录与文件
real_input = []
real_output = []
for i in range(len(inputPath_list)):
    input_file = str(i) + r'.txt'
    with open(input_file_path + '\\' + input_file, "r", encoding="utf-8") as fh:
        inputs = eval(fh.read())
    with open(output_file_path + '\\' + input_file, "r", encoding="utf-8") as fh:
        outputs = eval(fh.read())
    for line_num in range(len(outputs)):
        if 1 in outputs[line_num]:
            real_input.append(inputs[line_num])
            real_output.append(outputs[line_num])
print(len(real_input), len(real_output))
with open(r'xie_data\xie_x.txt', "w", encoding="utf-8") as fh:
    fh.write(str(real_input))
with open(r'xie_data\xie_y.txt', "w", encoding="utf-8") as fh:
    fh.write(str(real_output))