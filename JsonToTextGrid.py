import json
import os 
import re 
# whisper 输出的json 文件转为 textGrid
def whisperJsonToTextGrid(jsonfile,newTextGrid):
	data = ""
	with open(jsonfile,encoding="utf-8") as f:
		data = json.load(f)

	word_seements = data["segments"]

	data_text_heand = "File type = \"ooTextFile\"\n"
	data_text_heand += "Object class = \"TextGrid\"\n\n"
	data_text_heand +="xmin = 0\n"
	data_text_heand +="xmax = %s\n" % word_seements[-1]['end']

	data_text_heand += "tiers? <exists>\n"
	data_text_heand += "size = 2\n"
	data_text_heand += "item []:\n"

	data_text_segment = "    item [1]:\n"
	data_text_segment +="        class = \"IntervalTier\"\n        name = \"segments\""
	data_text_segment +="\n"
	data_text_segment +="        xmin = 0\n"
	data_text_segment +="        xmax = %s\n" % word_seements[-1]['end']
	data_text_segment +="        intervals: size = %s\n" % len(word_seements)
	wordscount = 0 
	segments = []

	for i in range(len(word_seements)):
		lineStr = "        intervals [%s]:\n            xmin = %s\n            xman = %s\n            text = \"%s\"\n" % ((i+1),word_seements[i]['start'],word_seements[i]['end'],word_seements[i]['text'])
		data_text_segment += lineStr
		wordscount += len(word_seements[i]['words'])
		segments.extend(word_seements[i]['words'])

	data_text = "    item [2]:\n"
	data_text +="        class = \"IntervalTier\"\n        name = \"word\""
	data_text +="\n"
	data_text +="        xmin = 0\n"
	data_text +="        xmax = %s\n" % word_seements[-1]['end']
	data_text +="        intervals: size = %s\n" % len(segments)

	for i in range(len(segments)):
		lineStr = "        intervals [%s]:\n            xmin = %s\n            xman = %s\n            text = \"%s\"\n" % ((i+1),segments[i]['start'],segments[i]['end'],segments[i]['word'])
		data_text += lineStr

	with open(newTextGrid, 'w',encoding="utf-8") as f:
		f.write(data_text_heand)
		f.write(data_text_segment)
		f.write(data_text) 

# whisperX 输出的json 文件转为 textGrid
def whisperXJsonToTextGrid(jsonfile,newTextGrid):
	data = ""
	with open(jsonfile,encoding="utf-8") as f:
		data = json.load(f)

	word_seements = data["word_segments"]
	segments = data['segments']

	data_text_heand = "File type = \"ooTextFile\"\n"
	data_text_heand += "Object class = \"TextGrid\"\n\n"
	data_text_heand +="xmin = 0\n"
	data_text_heand +="xmax = %s\n" % word_seements[-1]['end']

	data_text_heand += "tiers? <exists>\n"
	data_text_heand += "size = 2\n"
	data_text_heand += "item []:\n"

	data_text_segment = "    item [1]:\n"
	data_text_segment +="        class = \"IntervalTier\"\n        name = \"segments\""
	data_text_segment +="\n"
	data_text_segment +="        xmin = 0\n"
	data_text_segment +="        xmax = %s\n" % word_seements[-1]['end']
	data_text_segment +="        intervals: size = %s\n" % len(segments)
	for i in range(len(segments)):
		lineStr = "        intervals [%s]:\n            xmin = %s\n            xman = %s\n            text = \"%s\"\n" % ((i+1),segments[i]['start'],segments[i]['end'],segments[i]['text'])
		data_text_segment += lineStr

	data_text = "    item [2]:\n"
	data_text +="        class = \"IntervalTier\"\n        name = \"word\""
	data_text +="\n"
	data_text +="        xmin = 0\n"
	data_text +="        xmax = %s\n" % word_seements[-1]['end']
	data_text +="        intervals: size = %s\n" % len(word_seements)

	for i in range(len(word_seements)):
		lineStr = "        intervals [%s]:\n            xmin = %s\n            xman = %s\n            text = \"%s\"\n" % ((i+1),word_seements[i]['start'],word_seements[i]['end'],word_seements[i]['word'])
		data_text += lineStr

	with open(newTextGrid, 'w',encoding="utf-8") as f:
		f.write(data_text_heand)
		f.write(data_text_segment)
		f.write(data_text)


if __name__ == '__main__':
	
	root_dir = r"D:\Anaconda\envs\OpenAIWhisper\Scripts"
	
	jsonpattern = re.compile(r"(.*)\.json$")
	for path_root,dir_name,files in os.walk(root_dir):
		for file_name in files:
			output = jsonpattern.match(file_name)
			if output is not None:
				json_file = path_root +"\\"+ file_name
				text_grid = path_root + "\\" + output.group(1) + ".TextGrid"
				if not os.path.exists(text_grid):
					print(json_file)
					whisperJsonToTextGrid(json_file,text_grid)

#jsonfile = r"D:\Anaconda\envs\OpenAIWhisper\Scripts\03_split_0__Au.json"
#textgrid = r"D:\Anaconda\envs\OpenAIWhisper\Scripts\03_split_0__Au.TextGrid"
#whisperJsonToTextGrid(jsonfile,textgrid)
