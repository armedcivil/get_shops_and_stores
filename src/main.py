import MeCab
import os
import httpx
import json
import ipadic

apikey = os.environ.get('API_KEY')
api_url = 'https://places.googleapis.com/v1/places:searchText'
headers = {'X-Goog-Api-Key': apikey, 'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,places.priceLevel,nextPageToken,places.nationalPhoneNumber,places.regularOpeningHours.weekdayDescriptions,places.websiteUri,places.types'}
data = {
  "textQuery" : "埼玉県深谷市 レストラン",
  "languageCode": "ja"
}

def main():
  next_page_token = ''
  count = 0

  f = open('/root/opt/result.txt', mode='w')

  while next_page_token != None:
    response = httpx.post(api_url, headers=headers, data=data)
    response_dic = response.json()
    for place in response_dic['places']:
      count += 1
      pro = convert_kata_to_hira(extract_pronunciation(place['displayName']['text']))
      place['displayName']['pronunciation'] = pro
      print(place)
      json.dump(place, f, ensure_ascii=False)
      f.write('\n')
    try:
      next_page_token = response_dic['nextPageToken']
      data['pageToken'] = next_page_token
    except:
      break

  print(count)
  f.close()

def extract_pronunciation(text):
  CHASEN_ARGS = r' -F "%m\t%f[7]\t%f[6]\t%F-[0,1,2,3]\t%f[4]\t%f[5]\n"'
  CHASEN_ARGS += r' -U "%m\t%m\t%m\t%F-[0,1,2,3]\t\t\n"'
  tagger = MeCab.Tagger(ipadic.MECAB_ARGS + CHASEN_ARGS)
  tagger.parse('')
  node = tagger.parseToNode(text)
  result = ''
  while node:
    wclass = node.feature.split(',')
    if wclass[0] != u'BOS/EOS':
      if len(wclass) >= 8:
        result += wclass[7]
      else:
        result += node.surface
    node = node.next
  return result

def convert_kata_to_hira(katakana):
  hira_tupple = ('あ','い','う','え','お','か','き','く','け','こ','さ','し','す','せ','そ','た','ち','つ','て','と','な','に','ぬ','ね','の','は','ひ','ふ','へ','ほ','ま','み','む','め','も','や','ゆ','よ','ら','り','る','れ','ろ','わ','を','ん','っ','ぁ','ぃ','ぅ','ぇ','ぉ','ゃ','ゅ','ょ','ー','が','ぎ','ぐ','げ','ご','ざ','じ','ず','ぜ','ぞ','だ','ぢ','づ','で','ど','ば','び','ぶ','べ','ぼ','ぱ','ぴ','ぷ','ぺ','ぽ')
  kata_tupple = ('ア','イ','ウ','エ','オ','カ','キ','ク','ケ','コ','サ','シ','ス','セ','ソ','タ','チ','ツ','テ','ト','ナ','ニ','ヌ','ネ','ノ','ハ','ヒ','フ','ヘ','ホ','マ','ミ','ム','メ','モ','ヤ','ユ','ヨ','ラ','リ','ル','レ','ロ','ワ','ヲ','ン','ッ','ァ','ィ','ゥ','ェ','ォ','ャ','ュ','ョ','ー','ガ','ギ','グ','ゲ','ゴ','ザ','ジ','ズ','ゼ','ゾ','ダ','ヂ','ヅ','デ','ド','バ','ビ','ブ','ベ','ボ','パ','ピ','プ','ペ','ポ')
  k_to_h_dict = dict()
  for i in range(len(hira_tupple)):
    k_to_h_dict[kata_tupple[i]] = hira_tupple[i]
  hiragana = ""
  for i in range(len(katakana)):
    if katakana[i] in k_to_h_dict:
      hiragana += k_to_h_dict[katakana[i]]
    else:
      hiragana += katakana[i]
  return hiragana

if __name__ == '__main__':
  main()