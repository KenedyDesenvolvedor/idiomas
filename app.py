from flask import Flask, render_template, send_from_directory, abort
from gtts import gTTS
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_FOLDER = os.path.join(BASE_DIR, 'static', 'audio')

def gerar_audios():
    os.makedirs(AUDIO_FOLDER, exist_ok=True)

    idiomas = {
        'japones': {
            'lang_code': 'ja',
            'palavras': [
                {"texto": "こんにちは", "romaji": "konnichiwa", "pt": "olá"},
                {"texto": "ありがとう", "romaji": "arigatou", "pt": "obrigado"},
                {"texto": "さようなら", "romaji": "sayounara", "pt": "tchau"},
                {"texto": "はい", "romaji": "hai", "pt": "sim"},
                {"texto": "いいえ", "romaji": "iie", "pt": "não"},
                {"texto": "おはよう", "romaji": "ohayou", "pt": "bom dia"},
                {"texto": "こんばんは", "romaji": "konbanwa", "pt": "boa noite"},
                {"texto": "すみません", "romaji": "sumimasen", "pt": "com licença"},
                {"texto": "お願いします", "romaji": "onegai shimasu", "pt": "por favor"},
                {"texto": "元気ですか", "romaji": "genki desu ka", "pt": "tudo bem?"},
            ],
            'frases': [
                {"texto": "お元気ですか？", "romaji": "ogenki desu ka", "pt": "Você está bem?"},
                {"texto": "私は日本語を勉強しています", "romaji": "watashi wa nihongo o benkyou shiteimasu", "pt": "Estou estudando japonês."},
                {"texto": "名前は何ですか？", "romaji": "namae wa nan desu ka", "pt": "Qual é o seu nome?"},
                {"texto": "私は学生です", "romaji": "watashi wa gakusei desu", "pt": "Sou estudante."},
                {"texto": "これは何ですか？", "romaji": "kore wa nan desu ka", "pt": "O que é isso?"},
                {"texto": "英語を話せますか？", "romaji": "eigo o hanasemasu ka", "pt": "Você fala inglês?"},
                {"texto": "助けてください", "romaji": "tasukete kudasai", "pt": "Por favor, ajude-me."},
                {"texto": "わかりません", "romaji": "wakarimasen", "pt": "Não entendo."},
                {"texto": "大丈夫です", "romaji": "daijoubu desu", "pt": "Está tudo bem."},
                {"texto": "行きましょう", "romaji": "ikimashou", "pt": "Vamos!"},
            ]
        },
        'russo': {
            'lang_code': 'ru',
            'palavras': [
                {"texto": "привет", "romaji": "privet", "pt": "olá"},
                {"texto": "спасибо", "romaji": "spasibo", "pt": "obrigado"},
                {"texto": "пока", "romaji": "poka", "pt": "tchau"},
                {"texto": "да", "romaji": "da", "pt": "sim"},
                {"texto": "нет", "romaji": "nyet", "pt": "não"},
                {"texto": "доброе утро", "romaji": "dobroye utro", "pt": "bom dia"},
                {"texto": "добрый вечер", "romaji": "dobryy vecher", "pt": "boa noite"},
                {"texto": "извините", "romaji": "izvinite", "pt": "desculpe"},
                {"texto": "пожалуйста", "romaji": "pozhaluysta", "pt": "por favor"},
                {"texto": "как дела?", "romaji": "kak dela", "pt": "como vai?"},
            ],
            'frases': [
                {"texto": "Как тебя зовут?", "romaji": "kak tebya zovut", "pt": "Como você se chama?"},
                {"texto": "Меня зовут Анна.", "romaji": "menya zovut Anna", "pt": "Meu nome é Anna."},
                {"texto": "Я учу русский язык.", "romaji": "ya uchu russkiy yazyk", "pt": "Estou estudando russo."},
                {"texto": "Где находится туалет?", "romaji": "gde nakhoditsya tualet", "pt": "Onde fica o banheiro?"},
                {"texto": "Я не понимаю.", "romaji": "ya ne ponimayu", "pt": "Eu não entendo."},
                {"texto": "Вы говорите по-английски?", "romaji": "vy govorite po-angliyski", "pt": "Você fala inglês?"},
                {"texto": "Сколько это стоит?", "romaji": "skolko eto stoit", "pt": "Quanto custa isso?"},
                {"texto": "Помогите!", "romaji": "pomogite!", "pt": "Ajuda!"},
                {"texto": "Я из Бразилии.", "romaji": "ya iz Brazilii", "pt": "Sou do Brasil."},
                {"texto": "Пойдём!", "romaji": "poydyom!", "pt": "Vamos!"},
            ]
        },

        'frances': {
            'lang_code': 'fr',
            'palavras': [
                {"texto": "bonjour", "romaji": "bonjour", "pt": "bom dia"},
                {"texto": "merci", "romaji": "merci", "pt": "obrigado"},
                {"texto": "au revoir", "romaji": "au revoir", "pt": "tchau"},
                {"texto": "oui", "romaji": "oui", "pt": "sim"},
                {"texto": "non", "romaji": "non", "pt": "não"},
                {"texto": "bonsoir", "romaji": "bonsoir", "pt": "boa noite"},
                {"texto": "s'il vous plaît", "romaji": "s'il vous plaît", "pt": "por favor"},
                {"texto": "excusez-moi", "romaji": "excusez-moi", "pt": "com licença"},
                {"texto": "ça va?", "romaji": "ça va", "pt": "tudo bem?"},
                {"texto": "bien", "romaji": "bien", "pt": "bem"},
            ],
            'frases': [
                {"texto": "Comment tu t'appelles ?", "romaji": "comment tu t'appelles", "pt": "Como você se chama?"},
                {"texto": "Je m'appelle Marie.", "romaji": "je m'appelle Marie", "pt": "Meu nome é Marie."},
                {"texto": "Je parle un peu français.", "romaji": "je parle un peu français", "pt": "Eu falo um pouco de francês."},
                {"texto": "Où sont les toilettes ?", "romaji": "où sont les toilettes", "pt": "Onde fica o banheiro?"},
                {"texto": "Je ne comprends pas.", "romaji": "je ne comprends pas", "pt": "Não entendo."},
                {"texto": "Vous parlez anglais ?", "romaji": "vous parlez anglais", "pt": "Você fala inglês?"},
                {"texto": "Combien ça coûte ?", "romaji": "combien ça coûte", "pt": "Quanto custa?"},
                {"texto": "Aidez-moi !", "romaji": "aidez-moi!", "pt": "Ajude-me!"},
                {"texto": "Je viens du Brésil.", "romaji": "je viens du Brésil", "pt": "Sou do Brasil."},
                {"texto": "Allons-y !", "romaji": "allons-y!", "pt": "Vamos!"},
            ]
        },

        'italiano': {
            'lang_code': 'it',
            'palavras': [
                {"texto": "ciao", "romaji": "ciao", "pt": "olá/tchau"},
                {"texto": "grazie", "romaji": "grazie", "pt": "obrigado"},
                {"texto": "buongiorno", "romaji": "buongiorno", "pt": "bom dia"},
                {"texto": "buonasera", "romaji": "buonasera", "pt": "boa noite"},
                {"texto": "sì", "romaji": "sì", "pt": "sim"},
                {"texto": "no", "romaji": "no", "pt": "não"},
                {"texto": "per favore", "romaji": "per favore", "pt": "por favor"},
                {"texto": "scusa", "romaji": "scusa", "pt": "desculpe"},
                {"texto": "come va?", "romaji": "come va", "pt": "como vai?"},
                {"texto": "bene", "romaji": "bene", "pt": "bem"},
            ],
            'frases': [
                {"texto": "Come ti chiami?", "romaji": "come ti chiami", "pt": "Como você se chama?"},
                {"texto": "Mi chiamo Luca.", "romaji": "mi chiamo Luca", "pt": "Meu nome é Luca."},
                {"texto": "Parlo un po’ di italiano.", "romaji": "parlo un po’ di italiano", "pt": "Eu falo um pouco de italiano."},
                {"texto": "Dove sono i bagni?", "romaji": "dove sono i bagni", "pt": "Onde fica o banheiro?"},
                {"texto": "Non capisco.", "romaji": "non capisco", "pt": "Não entendo."},
                {"texto": "Parli inglese?", "romaji": "parli inglese", "pt": "Você fala inglês?"},
                {"texto": "Quanto costa?", "romaji": "quanto costa", "pt": "Quanto custa?"},
                {"texto": "Aiuto!", "romaji": "aiuto!", "pt": "Ajuda!"},
                {"texto": "Vengo dal Brasile.", "romaji": "vengo dal Brasile", "pt": "Sou do Brasil."},
                {"texto": "Andiamo!", "romaji": "andiamo!", "pt": "Vamos!"},
            ]
        },

        'ingles': {
            'lang_code': 'en',
            'palavras': [
                {"texto": "hello", "romaji": "hello", "pt": "olá"},
                {"texto": "thank you", "romaji": "thank you", "pt": "obrigado"},
                {"texto": "goodbye", "romaji": "goodbye", "pt": "tchau"},
                {"texto": "yes", "romaji": "yes", "pt": "sim"},
                {"texto": "no", "romaji": "no", "pt": "não"},
                {"texto": "good morning", "romaji": "good morning", "pt": "bom dia"},
                {"texto": "good night", "romaji": "good night", "pt": "boa noite"},
                {"texto": "please", "romaji": "please", "pt": "por favor"},
                {"texto": "excuse me", "romaji": "excuse me", "pt": "com licença"},
                {"texto": "how are you?", "romaji": "how are you", "pt": "como vai?"},
            ],
            'frases': [
                {"texto": "What is your name?", "romaji": "what is your name", "pt": "Qual é o seu nome?"},
                {"texto": "My name is John.", "romaji": "my name is John", "pt": "Meu nome é John."},
                {"texto": "I speak a little English.", "romaji": "i speak a little English", "pt": "Eu falo um pouco de inglês."},
                {"texto": "Where is the bathroom?", "romaji": "where is the bathroom", "pt": "Onde fica o banheiro?"},
                {"texto": "I don't understand.", "romaji": "i don't understand", "pt": "Eu não entendo."},
                {"texto": "Do you speak Portuguese?", "romaji": "do you speak Portuguese", "pt": "Você fala português?"},
                {"texto": "How much is this?", "romaji": "how much is this", "pt": "Quanto custa isso?"},
                {"texto": "Help me!", "romaji": "help me!", "pt": "Ajuda!"},
                {"texto": "I’m from Brazil.", "romaji": "i’m from Brazil", "pt": "Sou do Brasil."},
                {"texto": "Let’s go!", "romaji": "let’s go!", "pt": "Vamos!"},
            
            ]
        },
    }

    # Gerar áudios para palavras e frases
    for idioma, dados in idiomas.items():
        lang_code = dados['lang_code']
        for item in dados.get('palavras', []) + dados.get('frases', []):
            filename = f"{idioma}_{item['romaji'].replace(' ', '_')}.mp3"
            audio_path = os.path.join(AUDIO_FOLDER, filename)
            if not os.path.exists(audio_path):
                print(f"Gerando áudio {filename}")
                tts = gTTS(text=item['texto'], lang=lang_code)
                tts.save(audio_path)

    return idiomas

idiomas = gerar_audios()

@app.route('/')
def index():
    return render_template('index.html', idiomas=idiomas)

@app.route('/<idioma>')
def idioma_page(idioma):
    if idioma not in idiomas:
        abort(404)
    dados = idiomas[idioma]
    return render_template('idioma.html', idioma=idioma, dados=dados)

@app.route('/audio/<filename>')
def get_audio(filename):
    return send_from_directory(AUDIO_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
