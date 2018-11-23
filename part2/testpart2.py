import html.parser

(TAG_OPEN, ATTR, TAG_CLOSE, TEXT, EOF) = ('TAG_OPEN', 'ATTR', 'TAG_CLOSE', 'TEXT', 'EOF')

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        """String representation of the class instance.
        Examples:
            Token(TAG_OPEN, 'h1')
            Token(ATTR, '+')
            Token(MUL, '*')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()
class Lexer(html.parser.HTMLParser):
    def __init__(self):
        # initialize the base class
        html.parser.HTMLParser.__init__(self)
        self.tokens = []

    def handle_starttag(self, tag, attrs):
        print("Start tag:", tag)
        self.tokens.append(Token(TAG_OPEN, tag))
        for attr in attrs:
            print("     attr:", attr)
            self.tokens.append(Token(ATTR, attr))

    def handle_endtag(self, tag):
        self.tokens.append(Token(TAG_CLOSE, tag))
        print("End tag  :", tag)

    def handle_data(self, data):
        print("Data     :", data)
        self.tokens.append(Token(TEXT, data))
    def read(self, data):

        self.feed(data)
        self.tokens.append(Token(EOF, None))
        print(self.tokens)
        return self

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.index = 0
        self.current_token = self.lexer.tokens[self.index]
        self.test_tokens_passed = []
    def body(self):
        while self.current_token.type in (TAG_OPEN, TEXT):
            token = self.current_token
            if token.type == TAG_OPEN:
                self.tag()
            elif token.type == TEXT:
                self.test_tokens_passed.append(token)
                self.eat(TEXT)

    def tag(self):
        self.test_tokens_passed.append(self.current_token)
        self.eat(TAG_OPEN)
        while self.current_token.type == ATTR:
            self.test_tokens_passed.append(self.current_token)
            self.eat(ATTR)
        if self.current_token.type in (TAG_OPEN, TEXT):
            self.body()
        self.test_tokens_passed.append(self.current_token)
        self.eat(TAG_CLOSE)

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.index += 1
            self.current_token = self.lexer.tokens[self.index]
        else:
            raise Exception("Invalid syntax")

xx = Lexer().read('<p>My mother has <span style="color:blue">blue</span> eyes.</p>')
parser = Parser(xx)
parser.body()
print(parser.test_tokens_passed)
