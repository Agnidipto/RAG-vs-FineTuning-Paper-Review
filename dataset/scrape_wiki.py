import json
import wikipediaapi
import os
from google import genai
import glob

wiki_wiki = wikipediaapi.Wikipedia(user_agent='CS421PaperReview (agnidipto12.25@gmail.com)', language='en')

def create_json(path, output) :
  data = {}
  with open(path, 'r') as file :
    for line in file.readlines() :
      chunks = line.split(' - ')
      topic, link = chunks[0], chunks[1].rstrip()
      data[topic] = link
  with open(output, 'w') as file:
    json.dump(data, file, indent=4)
 
def get_wiki_page_name(url: str) :
  # print('at f', url)
  return url.split('/')[-1]
      
def scrape_wiki(path) :
  text_data = {}
  with open(path, 'r') as file :
    data: dict = json.load(file)
    for topic in list(data.keys()) :
      page_name = get_wiki_page_name(data[topic])
      page_py = wiki_wiki.page(page_name)
      text = topic, page_py.text
      text_data[topic] = text
      print(topic, 'done')
      
  with open(f'wikipedia_text.json', 'w') as file:
    json.dump(text_data, file, indent=4)
    
def text_count() :
  with open('wikipedia_text.json', 'r') as file :
    text = file.read()
    print(len(text.split(' ')))
    
def get_questions(path) :
  api_key = os.environ.get('GEMINI_API_KEY')
  client = genai.Client(api_key=api_key)
  
  with open('wikipedia_text.json', 'r') as file :
    article_data: dict = json.load(file)
    for topic in list(article_data.keys()) :
      print(topic, 'start')
      total_content = '\n\n'.join(article_data[topic])
  
      response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"Can you create five multiple choice questions from each of the subtopics in this wikipedia article? Please give the multiple choice questions in a json format with keys question (string), choices (list[str]), and answer (index integer starting from zero). Content: {total_content}"
      )
      
      print(topic, 'got response')
      
      with open(f'wikipedia_content/{topic}.txt', 'w', encoding='UTF-8') as output_file :
        output_file.write(response.text)
      
      print(topic, 'done writing')
      
def combine_json_files(folder_path, output_file):
  all_data = []
  
  # Get all JSON files in the folder
  json_files = glob.glob(os.path.join(folder_path, "*.json"))
  
  # Read each file and append its content to all_data
  for file_path in json_files:
    with open(file_path, 'r', encoding='UTF-8') as file:
      data = json.load(file)
      if isinstance(data, list):
        all_data.extend(data)
      else:
        print(f"Warning: {file_path} does not contain a list. Skipping.")
  
  # Write the combined data to the output file
  with open(output_file, 'w') as outfile:
    json.dump(all_data, outfile, indent=4)
  
  print(f"Combined {len(json_files)} files into {output_file} with {len(all_data)} total items.")

combine_json_files('wikipedia_content', 'training_data.json')
      