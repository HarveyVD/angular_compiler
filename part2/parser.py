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

class AST(object):
    pass

class Attribute(AST):
    def __init__(self, token):
        self.token = token
        self.name = token.value[0]
        self.value = token.value[1]
    def __str__(self):
        """String representation of the class instance.
        Examples:
            Token(TAG_OPEN, 'h1')
            Token(ATTR, '+')
            Token(MUL, '*')
        """
        return 'Attribute( name = {name}, value = {value} )'.format(
            name=self.name,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

class Element(AST):
    def __init__(self, token, attrs, children):
        self.token = token
        self.name = token.value
        self.attrs = attrs
        self.children = children
    def __str__(self):
        """String representation of the class instance.
        Examples:
            Token(TAG_OPEN, 'h1')
            Token(ATTR, '+')
            Token(MUL, '*')
        """
        return """Element( 
                    name = {name}, 
                    attrs = {attrs}, 
                    children = {children} )""".format(
            name=self.name,
            attrs=self.attrs,
            children=self.children,
        )

    def __repr__(self):
        return self.__str__()

class Text(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __str__(self):
        """String representation of the class instance.
        Examples:
            Token(TAG_OPEN, 'h1')
            Token(ATTR, '+')
            Token(MUL, '*')
        """
        return """Text( 
                    value = {value} )""".format(
            value=self.value
        )

    def __repr__(self):
        return self.__str__()

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = lexer.tokens
        self.index = -1
        self.root_nodes = []
        self.current_token = None
        self.element_stack = []
        self.advance()

    def parse(self):
        while self.current_token.type is not None and self.current_token.type in (TEXT, TAG_OPEN):
            if self.current_token.type == TEXT:
                self.consumeText()
            elif self.current_token.type == TAG_OPEN:
                self.consumeTag()

    def consumeText(self):
        text_node = Text(self.current_token)
        self.addToParent(text_node)
        self.eat(TEXT)

    def eat(self, type_token):
        if self.current_token.type != type_token:
            raise Exception("Invalid token")
        else:
            self.advance()
    def addToParent(self, node):
        parent = self.getParentElement()
        if parent is not None:
            parent.children.append(node)
        else:
            self.root_nodes.append(node)

    def getParentElement(self):
        if len(self.element_stack) > 0:
            return self.element_stack[len(self.element_stack) - 1]
        else:
            return None

    def consumeTag(self):
        token = self.current_token
        attrs = []
        self.eat(TAG_OPEN)
        while self.current_token.type == ATTR:
            attrs.append(self.consumeAttr())
        element_node = Element(token, attrs, [])
        self.pushElement(element_node)
        self.consumeContent()
        self.consumeTagEnd()

    def consumeAttr(self):
        node = Attribute(self.current_token)
        self.eat(ATTR)
        return node

    def consumeTagEnd(self):
        name = self.current_token.value
        if self.popElement(name) == False:
            raise Exception("Unexpected closing tag")
        self.eat(TAG_CLOSE)

    def consumeContent(self):
        self.parse()
    def pushElement(self, node):
        self.addToParent(node)
        self.element_stack.append(node)

    def popElement(self, name):
        if len(self.element_stack) == 1:
            el = self.element_stack[0]
            if el.name == name:
                self.element_stack = []
                return True
            else:
                return False
        else:
            for index in range(len(self.element_stack) - 1, 0, -1):
                el = self.element_stack[index]
                if el.name == name:
                    self.element_stack = self.element_stack[0:index]
                    return True
        return False


    def peek(self):
        peek_index = self.index + 1
        if peek_index > len(self.tokens) - 1:
            return None
        else:
            return self.tokens[peek_index]

    def advance(self):
        self.index += 1
        if self.index > len(self.tokens) - 1:
            self.current_token = None # Indicate end of input
        else:
            self.current_token = self.tokens[self.index]

xx = Lexer().read('<p>My mother has <span style="color:blue">blue</span> eyes.</p>')
parser = Parser(xx)
parser.parse()
print(parser.root_nodes)