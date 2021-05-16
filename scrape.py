import requests

for i in range(8168, 10000):
    response = requests.get('http://wordscapesanswers.net/wordscapes-level-'+str(i)+'-answers/')
    page = response.text

    words = [word.split("</")[0] for word in page.split("<div class=answer-text>")[1:]]
    print(i, words)
    with open("wordscape_words.txt", 'a') as file1:
        file1.write("\n".join(words))
        file1.write("\n")